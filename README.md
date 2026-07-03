# Snapser - Bring Your Own Custom Code Examples

Welcome to the Snapser Repository for Bring Your Own Custom Code Examples. This repository serves as a comprehensive showcase for various examples demonstrating the capabilities and integration possibilities of BYOSnaps within the Snapser backend. We are committed to continually expanding this collection with more innovative examples.

We also encourage contributions from our vibrant community. If you have developed a unique implementation or enhancement, feel free to share it here!

## Core Examples

Minimal starter scaffolds — the **recommended starting point** for a new BYOSnap. Every endpoint Snapser expects is wired up (auth middleware, health check, CORS, the configuration / import-export / user-data hooks, and SDK generation), but each handler is a stub with a `// TODO`. See the [Core Examples overview](https://github.com/snapser-community/snapser-byosnaps/tree/main/core) for details, or jump straight to a language:

1. **[Python Example](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/byosnap-python)**
   Minimal Python BYOSnap starter scaffold (Flask)

2. **[Go Example](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/byosnap-go)**
   Minimal Go BYOSnap starter scaffold (Gorilla Mux)

3. **[Node Typescript Example](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/byosnap-node-ts)**
   Minimal Node Typescript BYOSnap starter scaffold (tsoa)

4. **[CSharp Example](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/ByoSnapCSharp)**
   Minimal C# BYOSnap starter scaffold (ASP.NET Core)

5. **[Rust Example](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/byosnap-rust-api)**
   Minimal Rust BYOSnap starter scaffold (actix-web)

6. **[Java Example](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/byosnap-java)**
   Minimal Java BYOSnap starter scaffold (Spring Boot)

7. **[Kotlin Example](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/byosnap-kotlin)**
   Minimal Kotlin BYOSnap starter scaffold (Ktor)


## Basic Examples
1. **[CSharp Example](https://github.com/snapser-community/snapser-byosnaps/tree/main/basic/ByoSnapCSharp)**
   Basic C# BYOSnap example

2. **[Go Example](https://github.com/snapser-community/snapser-byosnaps/tree/main/basic/byosnap-go)**
   Basic Go BYOSnap example

3. **[Node Typescript Example](https://github.com/snapser-community/snapser-byosnaps/tree/main/basic/byosnap-node-ts)**
   Basic Node Typescript BYOSnap example

4. **[Python Example](https://github.com/snapser-community/snapser-byosnaps/tree/main/basic/byosnap-python)**
   Basic Python BYOSnap example


## Legacy Examples

NOTE: We are in the process of moving these under the appropriate folders like `intermediate/` and `advanced/` tutorials.

Below are some of the examples available in this repository:

1. **[Go Example](https://github.com/snapser-community/snapser-byosnaps/tree/main/legacy/byosnap-go)**
   Demonstrates how your custom code can communicate with other snaps via gRPC within your Snapser backend.

2. **[Python Example](https://github.com/snapser-community/snapser-byosnaps/tree/main/legacy/byosnap-python)**
   A basic BYOSnap that exposes a couple RESTful endpoints.

3. **[C# Example](https://github.com/snapser-community/snapser-byosnaps/tree/main/legacy/ByoSnapCSharp)**
   Showcases a simple BYOSnap designed to expose a RESTful endpoint.

4. **[Custom Events Example (Go)](https://github.com/snapser-community/snapser-byosnaps/tree/main/legacy/byosnap-rewards)**
   WIP - An illustrative example of how a BYOSnap can emit custom events in response to an API call to a BYOSnap endpoint.
