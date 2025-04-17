curl -X POST -H 'Gateway: internal' http://localhost:5003/v1/byosnap-gemini/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "models/gemini-2.0-flash",
    "messages": [
      { "role": "user", "content": "Summarize the plot of Inception in one sentence." }
    ],
    "temperature": 0.7,
    "max_tokens": 200
  }'



# B64_IMAGE=$(base64 -w 0 sample.png)

# curl -X POST http://localhost:5003/v1/byosnap-gemini/chat \
#   -H "Content-Type: application/json" \
#   -d "{
#     \"model\": \"models/gemini-2.0-flash-vision\",
#     \"parts\": [
#       {
#         \"inline_data\": {
#           \"mime_type\": \"image/png\",
#           \"data\": \""${B64_IMAGE}"\"
#         }
#       },
#       {
#         \"text\": \"What do you see in this image?\"
#       }
#     ],
#     \"temperature\": 0.7,
#     \"max_tokens\": 256
#   }"



curl -N -X POST -H 'Gateway: internal' http://localhost:5003/v1/byosnap-gemini/chat-stream \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "model": "models/gemini-2.0-flash",
    "messages": [
      { "role": "user", "content": "Give me a haiku about the ocean." }
    ],
    "temperature": 0.7,
    "max_tokens": 100
  }'


# B64_IMAGE=$(base64 -w 0 sample.png)

# curl -N -X POST http://localhost:5003/v1/byosnap-gemini/chat-stream \
#   -H "Content-Type: application/json" \
#   -H "Accept: text/event-stream" \
#   -d "{
#     \"model\": \"models/gemini-2.0-flash-vision\",
#     \"parts\": [
#       {
#         \"inline_data\": {
#           \"mime_type\": \"image/png\",
#           \"data\": \"${B64_IMAGE}\"
#         }
#       },
#       {
#         \"text\": \"Describe the scene in this image.\"
#       }
#     ],
#     \"temperature\": 0.7,
#     \"max_tokens\": 200
#   }"
