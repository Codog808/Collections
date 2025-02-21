from .master import PostgresMaster
import os
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

    # --- New Methods for Bundling and Database Info ---

    def get_humans_bundle(self, offset=0, limit=10):
        query = "SELECT * FROM humans ORDER BY id LIMIT %s OFFSET %s;"
        params = (limit, offset)
        result = self.master.execute(query, params)
        return result

    def get_database_info(self):
        # Summary for humans
        query_humans = "SELECT COUNT(*) AS total_items, MIN(id) AS min_id, MAX(id) AS max_id FROM humans;"
        humans_stats = self.master.execute(query_humans)
        # Summary for documents
        query_documents = "SELECT COUNT(*) AS total_items, MIN(id) AS min_id, MAX(id) AS max_id FROM documents;"
        documents_stats = self.master.execute(query_documents)
        # Summary for families
        query_families = "SELECT COUNT(*) AS total_items, MIN(id) AS min_id, MAX(id) AS max_id FROM families;"
        families_stats = self.master.execute(query_families)

        return {
            "humans": humans_stats[0] if humans_stats else {},
            "documents": documents_stats[0] if documents_stats else {},
            "families": families_stats[0] if families_stats else {}
        }

def create_new_database(master, new_database: str):
    """
    Create a new database named new_database using the provided master connection.
    The master connection should be connected to a maintenance database (e.g., "postgres")
    that has permission to create new databases.
    """
    create_db_query = f"CREATE DATABASE {new_database};"
    master.execute(create_db_query)
    return f"Database '{new_database}' created successfully."


def populate_database_with_schema(new_db_config: dict, init_sql_path: str = None):
    """
    Connect to the new database using new_db_config and run the SQL schema defined in init.sql.
    new_db_config should be a dict containing keys: host, port, user, password, and database.
    By default, init.sql is assumed to be in the same directory as this __init__.py file.
    """
    if init_sql_path is None:
        init_sql_path = os.path.join(os.path.dirname(__file__), "init.sql")
    
    new_master = PostgresMaster(
        new_db_config['host'],
        new_db_config['port'],
        new_db_config['user'],
        new_db_config['password'],
        new_db_config['database']
    )
    new_master.__enter__()
    try:
        with open(init_sql_path, 'r') as f:
            init_sql = f.read()
        # Split SQL statements on semicolon; adjust if your SQL is more complex.
        statements = [stmt.strip() for stmt in init_sql.split(';') if stmt.strip()]
        for statement in statements:
            new_master.execute(statement + ';')
    finally:
        new_master.__exit__(None, None, None)
    
    return f"Database '{new_db_config['database']}' populated with schema from {init_sql_path}."

# ---------------------------
# Example Usage
# ---------------------------
