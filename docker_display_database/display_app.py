import requests
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "your-very-secret-key"  # use a secure key in production

# Base URL for your FastAPI service
FASTAPI_BASE = "http://localhost:8000"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Retrieve database connection details from form
        db_host = request.form.get("host")
        db_port = request.form.get("port")
        db_user = request.form.get("user")
        db_password = request.form.get("password")
        db_database = request.form.get("database")
        
        # Build payload for the FastAPI /session endpoint
        payload = {
            "host": db_host,
            "port": int(db_port),
            "user": db_user,
            "password": db_password,
            "database": db_database
        }
        
        session_url = f"{FASTAPI_BASE}/session"
        try:
            resp = requests.post(session_url, json=payload)
            if resp.status_code == 200:
                session_data = resp.json()
                # Save the session token and DB config for later use
                session["session_id"] = session_data.get("session_id")
                session["db_config"] = payload
                return redirect(url_for("display"))
            else:
                flash(f"Error creating session: {resp.text}")
        except Exception as e:
            flash(f"Error creating session: {str(e)}")
    return render_template("db_form.html")

@app.route("/display")
def display():
    # Check if a session has been established
    if "session_id" not in session:
        flash("No session available. Please enter the database config.")
        return redirect(url_for("index"))
    
    sess_id = session["session_id"]
    
    # Call the FastAPI /database-info endpoint to fetch summary statistics
    db_info_url = f"{FASTAPI_BASE}/database-info"
    params = {"session_id": sess_id}
    try:
        info_resp = requests.get(db_info_url, params=params)
        if info_resp.status_code != 200:
            flash("Error fetching database info")
            return redirect(url_for("index"))
        db_info = info_resp.json()
        humans_info = db_info.get("humans", {})
        total_items = humans_info.get("total_items", 0)
        page_size = 10
        num_pages = (total_items + page_size - 1) // page_size

        # Fetch the first page of bundled human data from the FastAPI /session/bundle endpoint
        bundle_url = f"{FASTAPI_BASE}/session/bundle"
        bundle_params = {"session_id": sess_id, "offset": 0, "limit": page_size}
        bundle_resp = requests.get(bundle_url, params=bundle_params)
        if bundle_resp.status_code != 200:
            flash("Error fetching human bundle")
            return redirect(url_for("index"))
        bundle_data = bundle_resp.json().get("bundle", [])
        
        return render_template("display.html", total_items=total_items,
                               page_size=page_size, num_pages=num_pages,
                               bundle_data=bundle_data)
    except Exception as e:
        flash("Error fetching data: " + str(e))
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

