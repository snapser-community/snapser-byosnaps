curl -X POST http://localhost:5003/v1/byosnap-anthropic/chat \
  -H "Content-Type: application/json" \
  -d '{
    "tier": "sonnet",
    "system": "You are a pirate who only speaks in sea shanties.",
    "messages": [
      { "role": "user", "content": "Tell me a joke." }
    ],
    "temperature": 0.7,
    "max_tokens": 100
  }'


curl -N -X POST http://localhost:5003/v1/byosnap-anthropic/chat-stream \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "tier": "opus",
    "system": "You are a philosophical AI.",
    "messages": [
      { "role": "user", "content": "What is the meaning of life?" }
    ],
    "temperature": 0.7,
    "max_tokens": 150
  }'
