FROM golang:1.22-alpine3.19 AS build
WORKDIR /go/src
COPY go/ .

RUN go mod download && go build -o service .

FROM build AS runtime
COPY --from=build /go/src/service ./
ENTRYPOINT ["./service"]
