val kotlinVersion: String by project
val ktorVersion: String by project
val logbackVersion: String by project

plugins {
    kotlin("jvm") version "2.0.21"
    kotlin("plugin.serialization") version "2.0.21"
    id("io.ktor.plugin") version "2.3.12"
}

group = "com.snapser.byosnap"
version = "1.0.0"

// The Ktor Gradle plugin's `buildFatJar` task produces a single runnable
// uber-jar. `mainClass` tells it (and `run`) which entrypoint to launch.
application {
    mainClass.set("com.snapser.byosnap.ApplicationKt")
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("io.ktor:ktor-server-core:$ktorVersion")
    implementation("io.ktor:ktor-server-netty:$ktorVersion")
    implementation("io.ktor:ktor-server-cors:$ktorVersion")
    implementation("io.ktor:ktor-server-content-negotiation:$ktorVersion")
    implementation("io.ktor:ktor-serialization-kotlinx-json:$ktorVersion")
    implementation("ch.qos.logback:logback-classic:$logbackVersion")
}

kotlin {
    jvmToolchain(21)
}
