curl -X GET http://localhost:5003/v1/byosnap-mcp/mcp/resources/player-profile \
  -H "Auth-Type: Api-Key"

curl -X POST http://localhost:5003/v1/byosnap-mcp/mcp/tools/give-xp \
  -H "Content-Type: application/json" \
  -H "Auth-Type: Api-Key" \
  -d '{
        "user_id": "user_12345",
        "amount": 100
      }'

curl -X GET http://localhost:5003/v1/byosnap-mcp/mcp/prompts/quest-helper \
  -H "Auth-Type: Api-Key"

curl -X GET http://localhost:5003/v1/byosnap-mcp/mcp/schema/player-profile \
  -H "Auth-Type: Api-Key"

curl -X GET http://localhost:5003/v1/byosnap-mcp/mcp/manifest.json \
  -H "Auth-Type: Api-Key"
