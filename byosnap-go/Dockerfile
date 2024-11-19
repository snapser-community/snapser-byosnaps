FROM golang:1.22-alpine3.19 as build
WORKDIR /go/src
COPY . .

RUN go mod download

RUN go build -o service .

FROM build AS runtime
COPY --from=build /go/src/service ./
EXPOSE 8080/tcp
ENTRYPOINT ["./service"]
