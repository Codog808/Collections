# main.py - Step 2: Import dependencies, define models, and create a session endpoint.
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from session_manager import create_session, get_session, close_session
from app import PostgresUser  # Import your PostgresUser class

# Database configuration model.
class DBConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 5432
    user: str
    password: str
    database: str

app = FastAPI()

@app.post("/session")
def create_db_session(db_config: DBConfig):
    try:
        session_id = create_session(db_config)
        return {"session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# main.py - Step 3: Define operations using a session.

# Model for creating a human entry.
class HumanCreate(BaseModel):
    name: str
    birthday: str  # Use string for simplicity; in production, consider a date type.
    birthplace: str
    gender: str
    culture: str
    status: str = "missing"
    biography: str = None
    comments: str = None

class HumanUpdate(BaseModel):
    name: str = None
    birthday: str = None
    birthplace: str = None
    gender: str = None
    culture: str = None
    status: str = None
    biography: str = None
    comments: str = None

@app.post("/human/session", status_code=201)
def create_human_session(session_id: str, human: HumanCreate):
    master = get_session(session_id)
    if not master:
        raise HTTPException(status_code=404, detail="Session not found.")
    try:
        user_interface = PostgresUser(master)
        human_id = user_interface.create_human(**human.model_dump())
        return {"human_id": human_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/human/session/{human_id}")
def read_human_session(human_id: int, session_id: str): 
    master = get_session(session_id)
    if not master:
        raise HTTPException(status_code=404, detail="Session not found.")
    try:
        user_interface = PostgresUser(master)
        human = user_interface.read_human(human_id)
        if not human:
            raise HTTPException(status_code=404, detail="Human not found.")
        return human
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/human/session/{human_id}")
def update_human_session(human_id: int, session_id: str, human_update: HumanUpdate):
    """
    Update an existing human record.
    Only non-null fields in the request will be updated.
    """
    master = get_session(session_id)
    if not master:
         raise HTTPException(status_code=404, detail="Session not found.")
    try:
         user_interface = PostgresUser(master)
         # Filter out None values from the update data.
         update_data = {k: v for k, v in human_update.model_dump().items() if v is not None}
         if not update_data:
             raise HTTPException(status_code=400, detail="No fields provided for update.")
         user_interface.update_human(human_id, **update_data)
         return {"message": "Human updated successfully"}
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

@app.delete("/human/session/{human_id}")
def delete_human_session(human_id: int, session_id: str):
    """
    Delete a human record by its ID.
    """
    master = get_session(session_id)
    if not master:
         raise HTTPException(status_code=404, detail="Session not found.")
    try:
         user_interface = PostgresUser(master)
         user_interface.delete_human(human_id)
         return {"message": "Human deleted successfully"}
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

# Models for Document CRUD operations.
class DocumentCreate(BaseModel):
    related_human_id: int
    identifier_type: str
    source: str
    comments: str = None

class DocumentUpdate(BaseModel):
    related_human_id: int = None
    identifier_type: str = None
    source: str = None
    comments: str = None

# Create a Document record.
@app.post("/document/session", status_code=201)
def create_document_session(session_id: str, document: DocumentCreate):
    master = get_session(session_id)
    if not master:
         raise HTTPException(status_code=404, detail="Session not found.")
    try:
         user_interface = PostgresUser(master)
         document_id = user_interface.create_document(
             related_human_id=document.related_human_id,
             identifier_type=document.identifier_type,
             source=document.source,
             comments=document.comments
         )
         return {"document_id": document_id}
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

# Retrieve a Document record.
@app.get("/document/session/{document_id}")
def read_document_session(document_id: int, session_id: str):
    master = get_session(session_id)
    if not master:
         raise HTTPException(status_code=404, detail="Session not found.")
    try:
         user_interface = PostgresUser(master)
         document = user_interface.read_document(document_id)
         if not document:
              raise HTTPException(status_code=404, detail="Document not found.")
         return document
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

# Update a Document record.
@app.put("/document/session/{document_id}")
def update_document_session(document_id: int, session_id: str, document_update: DocumentUpdate):
    master = get_session(session_id)
    if not master:
         raise HTTPException(status_code=404, detail="Session not found.")
    try:
         user_interface = PostgresUser(master)
         update_data = {k: v for k, v in document_update.model_dump().items() if v is not None}
         if not update_data:
              raise HTTPException(status_code=400, detail="No fields provided for update.")
         user_interface.update_document(document_id, **update_data)
         return {"message": "Document updated successfully"}
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

# Delete a Document record.
@app.delete("/document/session/{document_id}")
def delete_document_session(document_id: int, session_id: str):
    master = get_session(session_id)
    if not master:
         raise HTTPException(status_code=404, detail="Session not found.")
    try:
         user_interface = PostgresUser(master)
         user_interface.delete_document(document_id)
         return {"message": "Document deleted successfully"}
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))


# Models for Family CRUD operations.
class FamilyCreate(BaseModel):
    related_human_id: int
    relation_type: str
    human_name: str
    human_id: int = None
    comments: str = None

class FamilyUpdate(BaseModel):
    related_human_id: int = None
    relation_type: str = None
    human_name: str = None
    human_id: int = None
    comments: str = None

# Create a Family record.
@app.post("/family/session", status_code=201)
def create_family_session(session_id: str, family: FamilyCreate):
    master = get_session(session_id)
    if not master:
         raise HTTPException(status_code=404, detail="Session not found.")
    try:
         user_interface = PostgresUser(master)
         family_id = user_interface.create_family(
             related_human_id=family.related_human_id,
             relation_type=family.relation_type,
             human_name=family.human_name,
             human_id=family.human_id,
             comments=family.comments
         )
         return {"family_id": family_id}
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

# Retrieve a Family record.
@app.get("/family/session/{family_id}")
def read_family_session(family_id: int, session_id: str):
    master = get_session(session_id)
    if not master:
         raise HTTPException(status_code=404, detail="Session not found.")
    try:
         user_interface = PostgresUser(master)
         family = user_interface.read_family(family_id)
         if not family:
              raise HTTPException(status_code=404, detail="Family not found.")
         return family
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

# Update a Family record.
@app.put("/family/session/{family_id}")
def update_family_session(family_id: int, session_id: str, family_update: FamilyUpdate):
    master = get_session(session_id)
    if not master:
         raise HTTPException(status_code=404, detail="Session not found.")
    try:
         user_interface = PostgresUser(master)
         update_data = {k: v for k, v in family_update.model_dump().items() if v is not None}
         if not update_data:
              raise HTTPException(status_code=400, detail="No fields provided for update.")
         user_interface.update_family(family_id, **update_data)
         return {"message": "Family updated successfully"}
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

# Delete a Family record.
@app.delete("/family/session/{family_id}")
def delete_family_session(family_id: int, session_id: str):
    master = get_session(session_id)
    if not master:
         raise HTTPException(status_code=404, detail="Session not found.")
    try:
         user_interface = PostgresUser(master)
         user_interface.delete_family(family_id)
         return {"message": "Family deleted successfully"}
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))


# main.py - Step 4: Endpoint to close a session.
@app.post("/session/close")
def close_db_session(session_id: str):
    try:
        close_session(session_id)
        return {"message": "Session closed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# main.py - Step 5: Run the FastAPI app.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

