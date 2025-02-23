from session_manager import DatabaseSession, get_session
from datetime import datetime

from datetime import datetime, timedelta
import random

def random_date(start_date, end_date):
    # Calculate the difference between the start and end dates
    delta = end_date - start_date
    
    # Generate a random number of days to add
    random_days = random.randint(0, delta.days)
    
    # Return the new randomized date
    return start_date + timedelta(days=random_days)

# Example usage:

if __name__ == '__main__':
# API Configuration
    base_url = "http://localhost:8000"
    host = "postgres_collections_debug"
    port = 5432
    user = "admin"
    password = "password"
    database = "default"

# Step 1️⃣ — Create a session (using the helper function)
    session_id = get_session(base_url, host, port, user, password, database)

# Step 2️⃣ — Use the existing session in the context manager
    with DatabaseSession(base_url, session_id) as db_session:
        start = datetime.strptime("1970-01-01", "%Y-%m-%d")
        end = datetime.today()

        randomized_birthday = random_date(start, end).date().strftime("%Y-%m-%d")

        print("Random Birthday:", randomized_birthday)

        # ✅ Add a human
        human_data = {
            "name": "John Doe",
            "birthday": randomized_birthday,
            "birthplace": "New York",
            "gender": "male",
            "culture": "American",
            "status": "missing",
            "biography": "Test bio",
            "comments": "First entry"
        }
        add_response = db_session.post("human/session", human_data)
        human_id = add_response['human_id']
        print()
        print("Human Added:", add_response)

        # ✅ Retrieve the human
        human_ad = add_response.get("id", 16)  # Default to ID 1
        get_response = db_session.get(f"human/session/{human_ad}")
        print()
        print("Human Retrieved:", get_response)

# ✅ Add a Document
        document_data = {
            "related_human_id": human_id,  # Assuming you have a valid human_id from the human creation
            "identifier_type": "Passport",
            "source": "Government Records",
            "comments": "Verified document"
        }
        add_document_response = db_session.post("document/session", document_data)
        print()
        print("Document Added:", add_document_response)

# ✅ Retrieve the Document
        document_id = add_document_response.get("document_id", 1)  # Use returned ID or default
        get_document_response = db_session.get(f"document/session/{document_id}")
        print()
        print("Document Retrieved:", get_document_response)
# ✅ Add a Family Member
        family_data = {
            "related_human_id": human_id,  # This links to the primary human
            "relation_type": "Father",
            "human_name": "Michael Doe",
            "human_id": None,# If no existing human ID, leave as None
            "comments": "Close family member"
        }
        add_family_response = db_session.post("family/session", family_data)
        print()
        print("Family Member Added:", add_family_response)

# ✅ Retrieve the Family Member
        family_id = add_family_response.get("family_id", 1)  # Use returned ID or default
        get_family_response = db_session.get(f"family/session/{family_id}")
        print()
        print("Family Member Retrieved:", get_family_response)

