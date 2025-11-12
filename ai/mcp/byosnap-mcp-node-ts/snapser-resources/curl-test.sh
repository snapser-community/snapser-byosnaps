curl -X POST http://localhost:5003/v1/byosnap-mcp/mcp   -H 'Content-Type: application/json'  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'