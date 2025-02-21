DATABASE=$1
curl -X POST "http://localhost:8000/session" \
  -H "Content-Type: application/json" \
  -d '{"host": "postgres", "port": 5432, "user": "admin", "password": "password", "database": "'$DATABASE'"}'
