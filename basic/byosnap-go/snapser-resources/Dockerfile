# Start from the official Golang image to create a build artifact.
# Specify the ARM64 version of the Golang image.
FROM golang:1.21-alpine AS builder

# Set the Current Working Directory inside the container
WORKDIR /app

# Copy go mod and sum files
COPY go.mod go.sum ./

# Download all dependencies. Dependencies will be cached if the go.mod and go.sum files are not changed
RUN go mod download

# Copy the source code into the container
COPY . .

# Build the Go app
# Ensure the build is for ARM64 architecture
RUN CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -o main .

# Start a new stage from scratch using an ARM64 Alpine base image
FROM alpine:latest

# We'll create a non-root user and a group to run our application
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Import the compiled executable from the first stage.
COPY --from=builder /app/main /app/main

# Copy other necessary files such as configurations if needed
# COPY --from=builder /app/configs /app/configs

# Change to a non-root user
USER appuser

# Expose port 5003 to the outside world
EXPOSE 5003

# Command to run the executable
CMD ["/app/main"]
