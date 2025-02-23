import requests

def get_session(base_url, host, port, user, password, database):
    """
    Helper function to create a session and return the session_id.
    """
    url = f"{base_url}/session"
    payload = {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "database": database
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        session_id = response.json().get("session_id")
        print(f"Session created successfully: {session_id}")
        return session_id
    else:
        raise Exception(f"Failed to create session: {response.text}")


class DatabaseSession:
    """
    Context Manager for handling an existing database session.
    """

    def __init__(self, base_url, session_id):
        self.base_url = base_url
        self.session_id = session_id

    def __enter__(self):
        """
        Enter the context with an existing session.
        """
        if not self.session_id:
            raise ValueError("A valid session_id must be provided.")
        print(f"Using session: {self.session_id}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Automatically closes the session when exiting the context.
        """
        self.close_session()

    def close_session(self):
        """
        Close the existing session.
        """
        url = f"{self.base_url}/session/close?session_id={self.session_id}"
        response = requests.post(url)
        if response.status_code == 200:
            print(f"Session {self.session_id} closed successfully.")
        else:
            print(f"Error closing session: {response.text}")
        self.session_id = None

    def post(self, endpoint, data):
        """
        Send a POST request using the existing session.
        """
        url = f"{self.base_url}/{endpoint}?session_id={self.session_id}"
        response = requests.post(url, json=data)
        return response.json()

    def get(self, endpoint):
        """
        Send a GET request using the existing session.
        """
        url = f"{self.base_url}/{endpoint}?session_id={self.session_id}"
        response = requests.get(url)
        return response.json()

    def delete(self, endpoint):
        """
        Send a DELETE request using the existing session.
        """
        url = f"{self.base_url}/{endpoint}?session_id={self.session_id}"
        response = requests.delete(url)
        return response.json()

