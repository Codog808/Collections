from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from session_manager import create_session, get_session, close_session
from app import PostgresUser, create_new_database, populate_database_with_schema
from typing import Type, Dict, Optional

app = FastAPI()

# Database configuration model.
class DBConfig(BaseModel):
    host: str = "postgres"
    port: int = 5432
    user: str
    password: str
    database: str

# Entity models
class HumanCreate(BaseModel):
    name: str
    birthday: str
    birthplace: str
    gender: str
    culture: str
    status: Optional[str] = "missing"
    biography: Optional[str]
    comments: Optional[str]

class HumanUpdate(BaseModel):
    name: Optional[str] = None
    birthday: Optional[str] = None
    birthplace: Optional[str] = None
    gender: Optional[str] = None
    culture: Optional[str] = None
    status: Optional[str] = None
    biography: Optional[str] = None
    comments: Optional[str] = None

class DocumentCreate(BaseModel):
    related_human_id: int
    identifier_type: str
    source: str
    comments: Optional[str]

class DocumentUpdate(BaseModel):
    related_human_id: Optional[int] = None
    identifier_type: Optional[str] = None
    source: Optional[str] = None
    comments: Optional[str] = None

class FamilyCreate(BaseModel):
    related_human_id: int
    relation_type: str
    human_name: str
    human_id: Optional[int]
    comments: Optional[str]

class FamilyUpdate(BaseModel):
    related_human_id: Optional[int] = None
    relation_type: Optional[str] = None
    human_name: Optional[str] = None
    human_id: Optional[int] = None
    comments: Optional[str] = None

# Map entity names to their models
models_config: Dict[str, Dict[str, Type[BaseModel]]] = {
    "human": {"create": HumanCreate, "update": HumanUpdate},
    "document": {"create": DocumentCreate, "update": DocumentUpdate},
    "family": {"create": FamilyCreate, "update": FamilyUpdate}
}

def create_crud_routes(entity_name: str, create_model: Type[BaseModel], update_model: Type[BaseModel]):
    base_url = f"/{entity_name}/session"

    @app.post(f"{base_url}", status_code=201)
    def create_entity(session_id: str, payload: create_model):
        master = get_session(session_id)
        if not master:
            raise HTTPException(status_code=404, detail="Session not found.")
        user_interface = getattr(PostgresUser(master), f"create_{entity_name}")
        entity_id = user_interface(**payload.dict())
        return {f"{entity_name}_id": entity_id}

    @app.get(f"{base_url}/{{entity_id}}")
    def read_entity(session_id: str, entity_id: int):
        master = get_session(session_id)
        if not master:
            raise HTTPException(status_code=404, detail="Session not found.")
        user_interface = getattr(PostgresUser(master), f"read_{entity_name}")
        entity = user_interface(entity_id)
        if not entity:
            raise HTTPException(status_code=404, detail=f"{entity_name.capitalize()} not found.")
        return entity

    @app.put(f"{base_url}/{{entity_id}}")
    def update_entity(session_id: str, entity_id: int, payload: update_model):
        master = get_session(session_id)
        if not master:
            raise HTTPException(status_code=404, detail="Session not found.")
        update_data = {k: v for k, v in payload.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields provided for update.")
        user_interface = getattr(PostgresUser(master), f"update_{entity_name}")
        user_interface(entity_id, **update_data)
        return {"message": f"{entity_name.capitalize()} updated successfully"}

    @app.delete(f"{base_url}/{{entity_id}}")
    def delete_entity(session_id: str, entity_id: int):
        master = get_session(session_id)
        if not master:
            raise HTTPException(status_code=404, detail="Session not found.")
        user_interface = getattr(PostgresUser(master), f"delete_{entity_name}")
        user_interface(entity_id)
        return {"message": f"{entity_name.capitalize()} deleted successfully"}

# Dynamically create CRUD routes for each model
for entity, models in models_config.items():
    create_crud_routes(entity, models["create"], models["update"])

# Session endpoints
@app.post("/session")
def create_db_session(db_config: DBConfig):
    try:
        session_id = create_session(db_config)
        return {"session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/session/close")
def close_db_session(session_id: str):
    try:
        close_session(session_id)
        return {"message": "Session closed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Database info endpoint: Return summary statistics for humans, documents, and families.
@app.get("/database-info")
def get_database_info(session_id: str):
    master = get_session(session_id)
    if not master:
        raise HTTPException(status_code=404, detail="Session not found.")
    try:
        user_interface = PostgresUser(master)
        info = user_interface.get_database_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

        # Endpoint to create a new database and populate it with the schema from init.sql.
@app.post("/database/create")
def create_and_populate_database(session_id: str, new_database: str):
    master = get_session(session_id)
    if not master:
         raise HTTPException(status_code=404, detail="Session not found.")
    try:
         # Create the new database.
         creation_message = create_new_database(master, new_database)
         
         # Build a configuration dict for the new database using the current connection's details.
         new_db_config = {
             'host': master.host,
             'port': master.port,
             'user': master.user,
             'password': master.password,
             'database': new_database
         }
         
         # Populate the new database with the schema from init.sql.
         schema_message = populate_database_with_schema(new_db_config)
         
         return {"message": f"{creation_message} {schema_message}"}
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))


@app.get("/session/bundle")
def get_bundle(session_id: str, table_name: str, offset: int = 0, limit: int = 100):
    """
    Fetch paginated data from the specified table.
    """
    try:
        # ✅ Get active session
        master = get_session(session_id)
        if not master:
            raise HTTPException(status_code=404, detail="Session not found.")

        # ✅ Initialize PostgresUser for DB operations
        user_interface = PostgresUser(master)

        # ✅ Dynamically fetch bundle using PostgresUser
        bundle = user_interface.get_bundle(table_name=table_name, offset=offset, limit=limit)

        # ✅ If no data found or table doesn't exist
        if not bundle:
            raise HTTPException(status_code=404, detail=f"No data found for table '{table_name}'.")

        return {"bundle": bundle}

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print("❌ Error in get_bundle:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

