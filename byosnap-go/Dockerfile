FROM golang:1.19.1-alpine3.16 AS build
WORKDIR /go/src
COPY . .

RUN go mod download

RUN go build -o service .

FROM golang:1.19.1-alpine3.16 AS runtime
COPY --from=build /go/src/service ./
EXPOSE 8080/tcp
ENTRYPOINT ["./service"]
