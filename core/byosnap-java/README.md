# BYOSnap Core Java Example

A minimal starter scaffold for a Java BYOSnap, built with Spring Boot 3 (Java 21). Every endpoint Snapser expects is present, but each handler body is a STUB that returns a simple placeholder and carries a `// TODO` describing what you would implement here.

Fill in the stubs with your own logic. When you need to persist data or call other Snaps (e.g. the Snapser Storage snap), wire that logic into the TODOs.

## Features

This scaffold wires up the following Snapser BYOSnap capabilities (all stubbed):

- **Configuration Tool (UI Builder)**: GET/PUT settings endpoints for the Snapser-managed configuration UI
- **Custom HTML Configuration Tool**: GET/PUT endpoints for a custom HTML-based configuration interface
- **Custom HTML User Manager Tool**: GET/POST endpoints for per-user data via a custom HTML interface
- **Snapend Sync/Clone (Import/Export)**: Export, import, and validate-import settings across environments (dev, stage, prod)
- **GDPR User Data**: Get, update, and delete user data (right-to-be-forgotten)
- **Example Business APIs**: Five example endpoints demonstrating each Snapser auth exposure (User, Api-Key, Internal, Admin SDK, and a single multi-auth route)
- **Swagger/OpenAPI**: A hand-authored `snapser-resources/swagger.json` with `x-snapser-auth-types` extensions

## Application
- Entry point: **src/main/java/com/snapser/byosnap/Application.java**
- Constants (BYOSNAP_ID / API_PREFIX / header keys): **src/main/java/com/snapser/byosnap/AppConstants.java**
- Auth annotation + interceptor: **src/main/java/com/snapser/byosnap/auth/**
- Controllers: **src/main/java/com/snapser/byosnap/controller/**
- The server listens on port **5003**.

## Route list

| Method | Path | Auth types |
| --- | --- | --- |
| GET | `/healthz` | none (readiness) |
| GET/PUT | `/v1/byosnap-core/settings` | internal |
| GET/PUT | `/v1/byosnap-core/settings/custom` | internal |
| GET/POST | `/v1/byosnap-core/settings/users/{userId}/custom` | internal |
| GET | `/v1/byosnap-core/settings/export` | internal |
| POST | `/v1/byosnap-core/settings/import` | internal |
| POST | `/v1/byosnap-core/settings/validate-import` | internal |
| GET/PUT/DELETE | `/v1/byosnap-core/settings/users/{userId}/data` | internal |
| GET | `/v1/byosnap-core/users/{userId}/example` | user |
| GET | `/v1/byosnap-core/example/api-key` | api-key |
| GET | `/v1/byosnap-core/example/internal` | internal |
| GET | `/v1/byosnap-core/example/admin` | internal (surfaces in Admin SDK) |
| GET | `/v1/byosnap-core/users/{userId}/example/multi-auth` | user + api-key + internal |

## Prerequisites

- [JDK 21](https://adoptium.net/)
- [Maven 3.9+](https://maven.apache.org/) (or the bundled build image below)
- Docker (for building the container image)
- Snapctl, Snapser's CLI. Follow the [setup tutorial](https://snapser.com/docs/guides/tutorials/setup-snapctl) if you do not have it. Run `snapctl validate` to confirm.
- Make sure Docker Desktop's **Use containerd for pulling and storing images** setting is **disabled**.

## Development

### Run Locally

```bash
mvn spring-boot:run
```

The server starts on `http://localhost:5003`. During local development a Swagger UI is available at `http://localhost:5003/swagger` (served by springdoc). NOTE: the springdoc UI is a developer convenience only — the **authoritative** spec Snapser consumes is the hand-authored `snapser-resources/swagger.json`. If you add or change endpoints, update that file by hand.

### Build the jar

```bash
mvn clean package -DskipTests
# produces target/app.jar (finalName=app)
java -jar target/app.jar
```

### Read the Gotchas
- Please read the **GOTCHAS.md** before you begin development.

## Publish the BYOSnap

Snapser builds the container from the `Dockerfile` in this folder (multi-stage: Maven build image → JRE runtime).

```bash
snapctl byosnap publish --byosnap-id byosnap-core --version "v1.0.0" --path $pathToThisFolder --resources-path $pathToThisFolder/snapser-resources/
```
IMPORTANT: You must increment the version number (format `vX.Y.Z`) for each subsequent publish.

## Create your cluster (Manual Setup)
- Go to your Game on the Web portal and click **Create a Snapend**.
- Give your Snapend a name and hit Continue.
- Pick **Authentication** and this **BYOSnap**.
- Keep hitting **Continue** until you reach the Review stage, then click **Snap it**.
- Your cluster should be up in about 2-4 minutes. Note the resulting **$snapendId**.
- Inside the Snapend, open **Snapend Configuration** → the Authentication Snap → **Connector** tool → enable **Anon** → Save.

## Testing
- Open the Snapend API Explorer (under **Quick Links** on the Snapend Home page).
- Use `Authentication.AnonLogin` to create a test user. The History button shows the created user's id and session token.
- Go to the BYOSnap API, add the user's session token, and call `ExampleUserAuth` (`GET /v1/byosnap-core/users/{user_id}/example`) to see the response.

## Actively Coding (sync)
If you want to rapidly test changes on an already deployed BYOSnap, use `snapctl byosnap sync` (requires a Snapend where this BYOSnap is already deployed):

```bash
snapctl byosnap sync --snapend-id $snapendId --byosnap-id byosnap-core --version $version --path $pathToThisFolder --resources-path $pathToThisFolder/snapser-resources
```
Sync reuses the published `$version` tag but keeps rebuilding and updating the remote image with your latest local code.
