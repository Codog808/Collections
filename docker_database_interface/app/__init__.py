from .master import PostgresMaster
from datetime import date

# ---------------------------
# User Interface (CRUD Operations)
# ---------------------------
class PostgresUser:
    def __init__(self, master: PostgresMaster):
        self.master = master

    # --- CRUD for Humans ---
    def create_human(self, name, birthday, birthplace, gender, culture,
                     status='missing', biography=None, comments=None):
        query = """
        INSERT INTO humans (name, birthday, birthplace, gender, culture, status, biography, comments)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        params = (name, birthday, birthplace, gender, culture, status, biography, comments)
        result = self.master.execute(query, params)
        if result:
            return result[0]['id']
        else:
            raise Exception("Insertion failed, no ID returned.")

    def read_human(self, human_id):
        query = "SELECT * FROM humans WHERE id = %s;"
        params = (human_id,)
        result = self.master.execute(query, params)
        return result[0] if result else None

    def update_human(self, human_id, **kwargs):
        set_clauses = []
        values = []
        for key, value in kwargs.items():
            set_clauses.append(f"{key} = %s")
            values.append(value)
        values.append(human_id)
        set_clause = ", ".join(set_clauses)
        query = f"UPDATE humans SET {set_clause} WHERE id = %s;"
        self.master.execute(query, tuple(values))

    def delete_human(self, human_id):
        query = "DELETE FROM humans WHERE id = %s;"
        params = (human_id,)
        self.master.execute(query, params)

    # --- CRUD for Documents ---
    def create_document(self, related_human_id, identifier_type, source, comments=None):
        query = """
        INSERT INTO documents (related_human_id, identifier_type, source, comments)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """
        params = (related_human_id, identifier_type, source, comments)
        result = self.master.execute(query, params)
        if result:
            return result[0]['id']
        else:
            raise Exception("Document insertion failed.")

    def read_document(self, document_id):
        query = "SELECT * FROM documents WHERE id = %s;"
        params = (document_id,)
        result = self.master.execute(query, params)
        return result[0] if result else None

    def update_document(self, document_id, **kwargs):
        set_clauses = []
        values = []
        for key, value in kwargs.items():
            set_clauses.append(f"{key} = %s")
            values.append(value)
        values.append(document_id)
        set_clause = ", ".join(set_clauses)
        query = f"UPDATE documents SET {set_clause} WHERE id = %s;"
        self.master.execute(query, tuple(values))

    def delete_document(self, document_id):
        query = "DELETE FROM documents WHERE id = %s;"
        params = (document_id,)
        self.master.execute(query, params)

    # --- CRUD for Families ---
    def create_family(self, related_human_id, relation_type, human_name, human_id=None, comments=None):
        query = """
        INSERT INTO families (related_human_id, relation_type, human_name, human_id, comments)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        params = (related_human_id, relation_type, human_name, human_id, comments)
        result = self.master.execute(query, params)
        if result:
            return result[0]['id']
        else:
            raise Exception("family insertion failed.")

    def read_family(self, family_id):
        query = "SELECT * FROM families WHERE id = %s;"
        params = (family_id,)
        result = self.master.execute(query, params)
        return result[0] if result else None

    def update_family(self, family_id, **kwargs):
        set_clauses = []
        values = []
        for key, value in kwargs.items():
            set_clauses.append(f"{key} = %s")
            values.append(value)
        values.append(family_id)
        set_clause = ", ".join(set_clauses)
        query = f"UPDATE families SET {set_clause} WHERE id = %s;"
        self.master.execute(query, tuple(values))

    def delete_family(self, family_id):
        query = "DELETE FROM families WHERE id = %s;"
        params = (family_id,)
        self.master.execute(query, params)

# ---------------------------
# Example Usage
# ---------------------------
if __name__ == '__main__':
    # Replace with your PostgreSQL Docker connection details.
    HOST     = "127.0.0.1"    # or your Docker host IP
    PORT     = 5432
    USER     = "admin"
    PASSWORD = "password"
    DATABASE = "default"

    with PostgresMaster(HOST, PORT, USER, PASSWORD, DATABASE) as master:
        # You can execute any command via the master interface:
        version_result = master.execute("SELECT version();")
        print("PostgreSQL version:", version_result[0]['version'] if version_result else "N/A")

        user_interface = PostgresUser(master)

        # --- CRUD for Humans ---
        human_id = user_interface.create_human(
            name="Alice",
            birthday="1990-01-01",  # or date(1990, 1, 1)
            birthplace="Wonderland",
            gender="Female",
            culture="Curious",
            status="alive",  # must be valid per your schema
            biography="Adventurous and kind.",
            comments="Initial entry."
        )
        print("Created human with ID:", human_id)
        human = user_interface.read_human(human_id)
        print("Read human:", human)
        user_interface.update_human(human_id, comments="Updated comment.")
        human = user_interface.read_human(human_id)
        print("Updated human:", human)

        input()
        # --- CRUD for Documents ---
        # Note: For demonstration, use a valid human ID (e.g., 1) for related_human_id.
        document_id = user_interface.create_document(
            related_human_id=human_id,  # Replace with an existing human's ID
            identifier_type="passport",
            source="Scanned copy",
            comments="Expires in 2030."
        )
        print("Created document with ID:", document_id)
        document = user_interface.read_document(document_id)
        print("Read document:", document)
        user_interface.update_document(document_id, source="Updated scanned copy")
        document = user_interface.read_document(document_id)
        print("Updated document:", document)

        input()
        # --- CRUD for Families ---
        family_id = user_interface.create_family(
            related_human_id=human_id,  # Replace with an existing human's ID
            relation_type="mother",
            human_name="richard",
            comments="Dumb as fuck"
        )
        print("Created family with ID:", family_id)
        family = user_interface.read_family(family_id)
        print("Read family:", family)
        user_interface.update_family(family_id, comments="Updated description.")
        family = user_interface.read_family(family_id)

        user_interface.delete_human(human_id)
        print("Deleted human with ID:", human_id)

