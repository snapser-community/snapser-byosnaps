curl -iv -X POST -H 'Gateway: internal' http://localhost:5003/v1/byosnap-openai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [
      { "role": "system", "content": "You are a helpful assistant." },
      { "role": "user", "content": "What is the capital of France?" }
    ],
    "temperature": 0.7
  }'

curl -N -X POST -H 'Gateway: internal' http://localhost:5003/v1/byosnap-openai/chat-stream \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "model": "gpt-4",
    "messages": [
      { "role": "system", "content": "You are a helpful assistant." },
      { "role": "user", "content": "Tell me a short bedtime story." }
    ],
    "temperature": 0.7
  }'


curl -iv -X POST -H 'Gateway: internal' http://localhost:5003/v1/byosnap-openai/completion \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo-instruct",
    "prompt": "Write a poem about the moon.",
    "max_tokens": 100,
    "temperature": 0.7
  }'


curl -N -X POST  -H 'Gateway: internal' http://localhost:5003/v1/byosnap-openai/completion-stream \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "model": "gpt-3.5-turbo-instruct",
    "prompt": "Describe a futuristic city.",
    "max_tokens": 100,
    "temperature": 0.7
  }'

curl -X POST  -H 'Gateway: internal' http://localhost:5003/v1/byosnap-openai/embedding \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-embedding-ada-002",
    "input": "Convert this sentence into an embedding."
  }'
