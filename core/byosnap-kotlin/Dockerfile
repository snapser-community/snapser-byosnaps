# Multi-stage build for the Kotlin / Ktor BYOSnap.
# Stage 1 builds a single runnable fat jar with Gradle; stage 2 runs it on a
# slim JRE image.

ARG PLATFORM=linux/arm64

# ---- Build stage ----
FROM --platform=$PLATFORM gradle:8-jdk21 AS build
WORKDIR /home/gradle/src

# Copy the Gradle build definition first so dependency resolution can be cached.
COPY build.gradle.kts settings.gradle.kts gradle.properties ./

# Copy the rest of the source and build the fat jar. The Ktor Gradle plugin
# (io.ktor.plugin) provides the `buildFatJar` task, which produces
# build/libs/<name>-all.jar — a single self-contained runnable jar.
COPY src ./src
RUN gradle buildFatJar --no-daemon

# ---- Runtime stage ----
FROM --platform=$PLATFORM eclipse-temurin:21-jre AS runtime
WORKDIR /app

# Copy the fat jar produced above to a stable name.
COPY --from=build /home/gradle/src/build/libs/*-all.jar app.jar

# Expose the RESTful server port. Must match SERVER_PORT in Application.kt and
# the external_port in snapser-resources/snapser-byosnap-profile.json.
EXPOSE 5003

ENTRYPOINT ["java", "-jar", "app.jar"]
