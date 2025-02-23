curl -X POST "http://localhost:8000/human/session?session_id=$YOUR_SESSION_ID" \
  -H "Content-Type: application/json" \
  -d '{
           "name": "Jaliceetas",
           "birthday": "1990-01-01",
           "birthplace": "Wonderland",
           "gender": "Female",
           "culture": "Curious",
           "status": "alive",
           "biography": "Adventurous",
           "comments": "Test entry"
         }'
