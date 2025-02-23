NEW_DATABASE=$1
curl -X POST "http://localhost:8000/database/create?session_id=$YOUR_SESSION_ID&new_database=$NEW_DATABASE"
