# BYOSnap Core Kotlin Example

A minimal starter scaffold for a new Kotlin BYOSnap, built with [Ktor](https://ktor.io/) on the Netty engine. Every endpoint Snapser expects is present, but each handler body is a stub that returns a simple placeholder and carries a `// TODO`. Use this as the starting point for your own microservice, and persist data via the Snapser Storage snap (called over the internal gateway) when you fill the stubs in.

## Application
- The main application logic is in **src/main/kotlin/com/snapser/byosnap/Application.kt**
- This example is built with Ktor (Netty engine) and served as a single runnable fat jar
- The server listens on port **5003** at host `0.0.0.0`

## Pre-Requisites

### A. JDK + Gradle
You need JDK 21 and Gradle (8.x). If you have Gradle installed you can build directly; otherwise use the Gradle wrapper (`./gradlew`) once it is generated (`gradle wrapper`).

```bash
# Build the fat jar
gradle buildFatJar

# Run locally
gradle run
# or run the produced jar directly
java -jar build/libs/byosnap-kotlin-all.jar
```

### B. Snapctl Setup
You need a valid Snapctl setup (Snapser's CLI). Follow the [tutorial](https://snapser.com/docs/guides/tutorials/setup-snapctl) if you do not have it installed. Confirm your setup:

```bash
snapctl validate
```

### C. Docker
Make sure the Docker engine is running. In Docker Desktop settings, ensure **Use containerd for pulling and storing images** is **disabled**.

## Resources
All files required by Snapctl are under the `snapser-resources/` folder:
- **Dockerfile** (repo root): BYOSnap needs a Dockerfile. Snapser uses it to containerize and deploy your application. This is a multi-stage build (`gradle:8-jdk21` to build the fat jar, `eclipse-temurin:21-jre` to run it).
- **snapser-byosnap-profile.json**: Tells Snapser about your BYOSnap's hardware, networking, and configuration requirements.
- **swagger.json**: (Recommended) A valid OpenAPI 3.x file. Snapser uses it to generate an SDK for your code and to enable this BYOSnap in the API Explorer.
- **README.md**: (Optional) A readme for your devs. Rendered on the Snapser web app.

## Tutorial
### Step 0: Read the Gotchas
- Please read the **GOTCHAS.md** before you begin development.

### Step 1: Update Code
This scaffold ships with stubbed endpoints. For this walk-through, open `Application.kt`, find the handler for `GET /v1/byosnap-core/users/{userId}/example`, and replace its `// TODO` with your own return message so you can deploy it and see it live.

### Step 2: Build
```bash
gradle buildFatJar
```

### Step 3: Publish the BYOSnap
```bash
snapctl byosnap publish --byosnap-id byosnap-core --version "v1.0.0" --path $pathToThisFolder --resources-path $pathToThisFolder/snapser-resources/
```

### Step 4: Create your cluster
#### Manual Setup
- Go to your Game on the Web portal.
- Click **Create a Snapend**.
- Give your Snapend a name and hit Continue.
- Pick **Authentication** and this **BYOSnap**.
- Keep hitting **Continue** until the Review stage, then click **Snap it**.
- Your cluster should be up in about 2-4 minutes.
- Open your Snapend, click **Snapend Configuration**, click the Authentication Snap, then the **Connector** tool, select **Anon** and hit Save.

At the end you will have a Snapend running with an Auth Snap and your BYOSnap, and a **$snapendId**. Keep a note of it. Every subsequent `byosnap publish` needs a higher version number.

### Step 5: Testing
- Open the Snapend API Explorer (under **Quick Links** on the Snapend Home page).
- Use `Authentication.AnonLogin` to create a test user.
- The API Explorer History button shows the created user's id and session token.
- Go to the BYOSnap API, add the user's session token, and call `ExampleUserAuth` (`GET /v1/byosnap-core/users/{user_id}/example`) to see your updated message.

## Development Process
### A. Running the Server Locally
```bash
gradle run
```

### B. Actively Coding
To rapidly test changes on an already-deployed BYOSnap, use `snapctl byosnap sync`. Note: sync only works if your BYOSnap was already deployed to a Snapend.

1. Update your code.
2. Update `snapser-resources/swagger.json` if you added or changed endpoints.
3. Run `snapctl byosnap sync --snapend-id $snapendId --byosnap-id byosnap-core --version $version --path $rootCodePath --resources-path $rootCodePath/snapser-resources`.

IMPORTANT: Sync reuses the published `$version` tag but keeps rebuilding and updating the remote image, so your Snapend can quickly run your latest code.

### C. Committing your BYOSnap
When you are ready to bump the version:

1. Update `snapser-resources/swagger.json` if needed.
2. Run `snapctl byosnap publish --byosnap-id byosnap-core --version $newVersion --path $rootCodePath --resources-path $rootCodePath/snapser-resources`. Make sure `$newVersion` is greater than the version currently on Snapser.
3. Any new or existing Snapend can now use the new version (`snapctl snapend update byosnaps ...` or via the web app's **Edit Snapend**).
