curl -XPOST \
-H 'App-Key: xyx' \
-H 'Content-Type: 'application/json'' \
-d '{
  "version": "v0.0.4",
  "exported_at": 1,
  "data": {
    "character_settings": {
      "version": "v1.0.0",
      "id": "characters",
      "endpoint": "",
      "category": "flat_form",
      "env_support": "single",
      "sections": [
        {
          "id": "registration",
          "components": [
            {
              "id": "characters",
              "type": "textarea",
              "value": "ember,bernice"
            }
          ]
        }
      ]
    }
  }
}' \
'http://localhost:5003/v1/byosnap-characters/settings/import'
