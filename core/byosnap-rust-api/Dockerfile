# Build stage
FROM rust:latest AS builder

WORKDIR /app

COPY Cargo.toml Cargo.lock* ./
# Create a dummy main to cache dependencies
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release
RUN rm -rf src

COPY src ./src
RUN touch src/main.rs
RUN cargo build --release

# Runtime stage
FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

COPY --from=builder /app/target/release/byosnap-rust-api /app/byosnap-rust-api

USER appuser

EXPOSE 5003

CMD ["/app/byosnap-rust-api"]
