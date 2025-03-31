#!/usr/bin/env bash

# Generate the swagger.json 2.X file from the code
swagger generate spec -o ./snapser-resources/swagger2x.json --scan-models

# Convert it to a swagger.json 3.X file
docker run --rm -v "${PWD}/snapser-resources:/local" openapitools/openapi-generator-cli:v7.0.1 generate \
        -i /local/swagger2x.json \
        -g openapi \
        -p outputFileName=swagger.json \
        -o /local/