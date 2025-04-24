FROM golang:1.22-alpine3.19 AS build
WORKDIR /src
COPY . .

RUN go mod download && go build -o service .

FROM build AS runtime
COPY --from=build /src/service ./
ENTRYPOINT ["./service"]
