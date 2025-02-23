import requests
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "your-very-secret-key"

# ✅ Default API Configuration
DEFAULT_API_CONFIG = {
    "base_url": "http://postgres_interface:8000",            # FastAPI backend
    "host": "postgres",           # PostgreSQL container name
    "port": 5432,
    "user": "admin",
    "password": "password",
    "database": "default"
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Retrieve form data or use defaults
        base_url = request.form.get("base_url", DEFAULT_API_CONFIG["base_url"])
        host = request.form.get("host", DEFAULT_API_CONFIG["host"])
        port = request.form.get("port", DEFAULT_API_CONFIG["port"])
        user = request.form.get("user", DEFAULT_API_CONFIG["user"])
        password = request.form.get("password", DEFAULT_API_CONFIG["password"])
        database = request.form.get("database", DEFAULT_API_CONFIG["database"])

        # Store API URL
        session["base_url"] = base_url

        # Build payload
        payload = {
            "host": host,
            "port": int(port),
            "user": user,
            "password": password,
            "database": database
        }

        try:
            # Create a session
            response = requests.post(f"{base_url}/session", json=payload)
            if response.status_code == 200:
                session["session_id"] = response.json().get("session_id")
                return redirect(url_for("list_tables"))
            else:
                flash(f"Error creating session: {response.text}")
        except Exception as e:
            flash(f"Connection failed: {str(e)}")

    return render_template("db_form.html", defaults=DEFAULT_API_CONFIG)

@app.route("/tables")
def list_tables():
    if "session_id" not in session:
        flash("No active session. Please login.")
        return redirect(url_for("index"))

    base_url = session["base_url"]
    sess_id = session["session_id"]

    # Fetch tables and their info
    response = requests.get(f"{base_url}/database-info", params={"session_id": sess_id})

    if response.status_code == 200:
        db_info = response.json()
        return render_template("tables.html", db_info=db_info)
    else:
        flash("Failed to fetch database info.")
        return redirect(url_for("index"))

@app.route("/table/<table_name>")
def view_table(table_name):
    if "session_id" not in session:
        flash("No active session. Please login.")
        return redirect(url_for("index"))

    base_url = session["base_url"]
    sess_id = session["session_id"]

    # Pagination setup
    page = int(request.args.get("page", 0))
    offset = page * 100

    params = {
        "session_id": sess_id,
        "table_name": table_name,
        "offset": offset,
        "limit": 100
    }

    response = requests.get(f"{base_url}/session/bundle", params=params)

    # Log for debugging
    print(f"GET {response.url} → {response.status_code}")
    print("Response:", response.text)

    if response.status_code == 200:
        table_data = response.json().get("bundle", [])
        return table_data

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
