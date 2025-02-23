DATABASE=$1
HOST=$2
curl -X POST "http://localhost:8000/session" \
  -H "Content-Type: application/json" \
  -d '{"host": "'$HOST'", "port": 5432, "user": "admin", "password": "password", "database": "'$DATABASE'"}'
