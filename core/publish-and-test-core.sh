#!/usr/bin/env bash
#
# publish-and-test-core.sh
# ----------------------------------------------------------------------------
# Publish + smoke-test every core BYOSnap example, one language at a time.
#
# For each language this script:
#   1. Publishes the example as `byosnap-core` (Docker build + push + version
#      publish) at a monotonically increasing version.
#   2. Brings it up in ONE reusable Snapend and verifies the Snapend reaches the
#      LIVE state. The first successful language CREATEs the Snapend; every
#      subsequent language UPDATEs that same Snapend to the new byosnap-core
#      version (snapctl has no `snapend delete`, so we reuse a single Snapend).
#
# Why one shared `byosnap-core` id: it must match the URL prefix baked into the
# example code (`/v1/byosnap-core/...`). `snapctl byosnap publish` upserts the
# byosnap and requires each new version to be strictly greater than the last —
# hence the auto-incrementing version across the whole run.
#
# Prerequisites:
#   - snapctl installed and logged in   (verify: `snapctl validate`)
#   - Docker running
#   - Run from anywhere; paths resolve relative to this script.
#
# Usage (once core/.publish-and-test-core.env has your APP_ID + COMPANY_ID):
#   ./core/publish-and-test-core.sh                 # full 7-language sweep
#   LANGS="byosnap-rust-api" ./core/publish-and-test-core.sh   # just one
#
# Put APP_ID / COMPANY_ID (and any overrides) in core/.publish-and-test-core.env
# (gitignored) so a plain run just works. Any of these can also be set inline:
#   START_VERSION      first byosnap-core version   (default: auto — server latest + 1)
#   SNAPEND_NAME       name of the test Snapend      (default core-test)
#   SNAPEND_ENV        development | staging         (default development)
#   PLATFORM_OVERRIDE  e.g. linux/amd64              (default: profile's)
#   STOP_ON_FAIL       stop at first failure         (default true)
#   SNAPEND_ID         reuse/continue an existing Snapend id (default: create new)
#   LANGS              subset of language folders to run
#   MANIFEST_TEMPLATE  path to the create manifest template
#
# The Snapend is created from snapser-core-test-manifest.template.json (auth +
# byosnap-core + eventbus). The auth/eventbus platform-snap versions live in
# that template — edit it if your environment differs. Per-language resources
# (cpu/memory/readiness) come from each example's snapser-byosnap-profile.json.
# ----------------------------------------------------------------------------
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Optional local config (gitignored) so a plain run needs no env vars.
[ -f "$SCRIPT_DIR/.publish-and-test-core.env" ] && . "$SCRIPT_DIR/.publish-and-test-core.env"

# ---- Config ----------------------------------------------------------------
APP_ID="${APP_ID:?Set APP_ID (in core/.publish-and-test-core.env or inline)}"
COMPANY_ID="${COMPANY_ID:?Set COMPANY_ID (in core/.publish-and-test-core.env or inline)}"
START_VERSION="${START_VERSION:-}"   # empty => auto-detect (server's latest byosnap-core + 1)
SNAPEND_NAME="${SNAPEND_NAME:-core-test}"
SNAPEND_ENV="${SNAPEND_ENV:-development}"
PLATFORM_OVERRIDE="${PLATFORM_OVERRIDE:-}"
STOP_ON_FAIL="${STOP_ON_FAIL:-true}"
SNAPEND_ID="${SNAPEND_ID:-}"
BYOSNAP_ID="byosnap-core"
# Known-good manifest template (auth + byosnap-core + eventbus, incl. the
# byosnap deployment_profile and platform-snap versions). Edit it if your
# environment's auth/eventbus versions differ.
MANIFEST_TEMPLATE="${MANIFEST_TEMPLATE:-$SCRIPT_DIR/snapser-core-test-manifest.template.json}"

# Order matters only for version assignment. Folders are relative to this script.
# Override with LANGS="byosnap-java byosnap-kotlin byosnap-rust-api" to run a subset
# (handy for resuming after a failure against an existing SNAPEND_ID).
if [ -n "${LANGS:-}" ]; then
  read -ra LANG_DIRS <<< "$LANGS"
else
  LANG_DIRS=(
    "byosnap-python"
    "byosnap-go"
    "byosnap-node-ts"
    "ByoSnapCSharp"
    "byosnap-java"
    "byosnap-kotlin"
    "byosnap-rust-api"
  )
fi

# ---- Helpers ---------------------------------------------------------------
bump_patch() { # $1=vX.Y.Z $2=increment -> vX.Y.(Z+increment)
  local v="${1#v}"; IFS=. read -r a b c <<<"$v"; echo "v${a}.${b}.$((c + $2))"
}

compute_start_version() { # echo server's latest byosnap-core version + 1 (patch); timestamp fallback
  local f latest a b c
  f="$(mktemp -t snaps-XXXXXX).json"
  if snapctl snaps enumerate --out-path-filename "$f" >/dev/null 2>&1; then
    latest="$(python3 - "$f" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
    for s in d.get("services", []):
        if s.get("id") == "byosnap-core":
            print(s.get("latest_version") or "")
            break
except Exception:
    pass
PY
)"
  fi
  rm -f "$f"
  if [ -n "${latest:-}" ]; then
    latest="${latest#v}"; IFS=. read -r a b c <<<"$latest"
    echo "v${a:-1}.${b:-0}.$(( ${c:-0} + 1 ))"
  else
    echo "v1.0.$(date +%s)"   # never published (or lookup failed): guarantees a fresh, increasing version
  fi
}

profile_language() { # $1=folder -> language field from the byosnap profile
  python3 - "$1" <<'PY'
import json, sys, glob, os
c = glob.glob(os.path.join(sys.argv[1], '**', 'snapser-byosnap-profile.json'), recursive=True)
print(json.load(open(c[0]))['language'] if c else 'unknown')
PY
}

profile_path_for() { # $1=folder -> path to its snapser-byosnap-profile.json
  python3 - "$1" <<'PY'
import sys, glob, os
c = glob.glob(os.path.join(sys.argv[1], '**', 'snapser-byosnap-profile.json'), recursive=True)
print(c[0] if c else '')
PY
}

gen_manifest() { # $1=folder $2=language $3=version -> prints temp manifest path
  # Built by patching a known-good manifest template (auth + byosnap-core +
  # eventbus). We patch byosnap-core's language/version/author, snapend name,
  # and derive its `deployment_profile` (cpu/memory/replicas) from THIS
  # language's byosnap profile so e.g. the JVM examples get their larger
  # resources. `id`/`applied_configuration` are server outputs and are stripped.
  local out; out="$(mktemp -t core-manifest-XXXXXX).json"
  TEMPLATE="$MANIFEST_TEMPLATE" SNAPEND_NAME="$SNAPEND_NAME" COMPANY_ID="$COMPANY_ID" \
  BFOLDER="$1" BLANG="$2" BVER="$3" python3 - "$out" <<'PY'
import json, os, sys, glob
m = json.load(open(os.environ["TEMPLATE"]))
m.pop("id", None)
m.pop("applied_configuration", None)
m["name"] = os.environ["SNAPEND_NAME"]
m["environment"] = "DEVELOPMENT"
lang, ver, company = os.environ["BLANG"], os.environ["BVER"], os.environ["COMPANY_ID"]
# Derive the deployment_profile from this language's byosnap profile.
prof = glob.glob(os.path.join(os.environ["BFOLDER"], "**", "snapser-byosnap-profile.json"), recursive=True)
dep = None
if prof:
    t = json.load(open(prof[0])).get("dev_template", {})
    dep = {k: t[k] for k in ("cpu", "memory", "min_replicas", "env_params") if k in t}
for sd in m.get("service_definitions", []):
    if sd.get("id") == "byosnap-core":
        sd["language"] = lang
        sd["version"] = ver
        sd["author_id"] = company
        if dep:
            sd["deployment_profile"] = dep
for st in m.get("settings", []):
    if st.get("id") == "byosnap-core":
        st["version"] = ver
json.dump(m, open(sys.argv[1], "w"), indent=2)
PY
  echo "$out"
}

capture_snapend_id() { # reads create output on stdin -> prints snapend id
  # Uses `python3 -c` (NOT a heredoc) so the piped create output stays on stdin.
  python3 -c '
import sys, re, json
t = sys.stdin.read()
# Prefer the structured JSON result: {"error":false,...,"data":{...,"id":"<uuid>"}}
for line in reversed(t.splitlines()):
    line = line.strip()
    if line.startswith("{") and "data" in line:
        try:
            c = (json.loads(line).get("data") or {}).get("id")
            if c:
                print(c); sys.exit(0)
        except Exception:
            pass
m = re.search(r"Cluster ID assigned:\s*([0-9a-fA-F-]+)", t)
print(m.group(1) if m else "")
'
}

# ---- Run -------------------------------------------------------------------
if [ -z "$START_VERSION" ]; then
  START_VERSION="$(compute_start_version)"
  echo ">> Auto-selected START_VERSION=$START_VERSION (server's latest byosnap-core + 1)"
fi

declare -a RESULTS
i=0
for name in "${LANG_DIRS[@]}"; do
  dir="$SCRIPT_DIR/$name"
  ver="$(bump_patch "$START_VERSION" "$i")"; i=$((i + 1))
  if [ ! -d "$dir" ]; then RESULTS+=("$name  SKIP:missing-folder"); continue; fi
  lang="$(profile_language "$dir")"

  echo; echo "==== [$name] publish $BYOSNAP_ID $ver (language=$lang) ===="
  pub=(snapctl byosnap publish --byosnap-id "$BYOSNAP_ID" --version "$ver"
       --path "$dir" --resources-path "$dir/snapser-resources" --blocking)
  [ -n "$PLATFORM_OVERRIDE" ] && pub+=(--platform-override "$PLATFORM_OVERRIDE")
  if ! "${pub[@]}"; then
    RESULTS+=("$name  PUBLISH:FAIL")
    echo ">> publish failed for $name"
    [ "$STOP_ON_FAIL" = "true" ] && { echo ">> STOP_ON_FAIL=true — fix and re-run."; break; }
    continue
  fi

  if [ -z "$SNAPEND_ID" ]; then
    echo "---- generate manifest (snapctl) + create Snapend '$SNAPEND_NAME' ----"
    manifest="$(gen_manifest "$dir" "$lang" "$ver")" || { RESULTS+=("$name  PUBLISH:OK MANIFEST:FAIL"); [ "$STOP_ON_FAIL" = "true" ] && break || continue; }
    out="$(snapctl snapend create --application-id "$APP_ID" --name "$SNAPEND_NAME" \
           --env "$SNAPEND_ENV" --manifest-path-filename "$manifest" --blocking 2>&1)"
    echo "$out"; rm -f "$manifest"
    SNAPEND_ID="$(printf '%s' "$out" | capture_snapend_id)"
    if [ -z "$SNAPEND_ID" ]; then
      RESULTS+=("$name  PUBLISH:OK CREATE:FAIL")
      echo ">> create failed (see above). Fix, then re-run with SNAPEND_ID=<id> to continue the remaining languages."
      break
    fi
    echo ">> SNAPEND_ID=$SNAPEND_ID"
  else
    # Pass the profile path as the 3rd --byosnaps value so the update carries a
    # fresh deployment_profile (otherwise the snapend keeps the create-time
    # resources — which is why the JVM example OOM'd on the tiny default).
    prof="$(profile_path_for "$dir")"
    byospec="$BYOSNAP_ID:$ver"; [ -n "$prof" ] && byospec="$byospec:$prof"
    echo "---- update Snapend $SNAPEND_ID -> $byospec ----"
    if ! snapctl snapend update --snapend-id "$SNAPEND_ID" --byosnaps "$byospec" --blocking; then
      RESULTS+=("$name  PUBLISH:OK UPDATE:FAIL")
      [ "$STOP_ON_FAIL" = "true" ] && break || continue
    fi
  fi

  state="$(snapctl snapend state --snapend-id "$SNAPEND_ID" 2>&1 | grep -oiE 'LIVE|IN_PROGRESS|FAILED|"state"[^,}]*' | head -1)"
  echo ">> snapend state: ${state:-unknown}"
  RESULTS+=("$name  PUBLISH:OK  ONLINE:${state:-unknown}")
done

echo; echo "==================== SUMMARY ===================="
printf '  %s\n' "${RESULTS[@]}"
[ -n "$SNAPEND_ID" ] && echo "  Snapend id: $SNAPEND_ID"
echo "  (snapctl has no 'snapend delete' — remove the test Snapend via the web app when done.)"
