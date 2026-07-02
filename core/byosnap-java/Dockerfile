# ---- Build stage ----
# Snapser BYOSnaps run on linux/arm64 by default. Override with --build-arg PLATFORM=linux/amd64.
ARG PLATFORM=linux/arm64
FROM --platform=$PLATFORM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app

# Cache dependencies first: copy the POM and resolve offline deps.
COPY pom.xml ./
RUN mvn -q -B dependency:go-offline

# Copy sources and build the fat jar. finalName=app in pom.xml => target/app.jar.
COPY src ./src
RUN mvn -q -B clean package -DskipTests

# ---- Runtime stage ----
FROM --platform=$PLATFORM eclipse-temurin:21-jre AS runtime
WORKDIR /app

# Copy the built Spring Boot fat jar.
COPY --from=build /app/target/app.jar app.jar

# Expose port 5003 for the RESTful server (matches snapser-byosnap-profile.json).
EXPOSE 5003

ENTRYPOINT ["java", "-jar", "app.jar"]
