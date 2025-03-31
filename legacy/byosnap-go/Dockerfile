FROM golang:1.22.0-alpine AS build
WORKDIR /go/src
COPY . .

RUN go mod download

RUN go build -o service .

FROM golang:1.22.0-alpine AS runtime
COPY --from=build /go/src/service ./
EXPOSE 8080/tcp
ENTRYPOINT ["./service"]
