from typing import List

from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import db, models, schemas
from app.config import get_settings

settings = get_settings()
app = FastAPI(title="App Runner + FastAPI + RDS")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def startup_event() -> None:
    # Garantimos que a tabela exista ao iniciar a aplicação.
    models.Base.metadata.create_all(bind=db.engine)


def get_db_session():
    with db.get_db() as session:
        yield session


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, session: Session = Depends(get_db_session)):
    notes: List[schemas.NoteRead] = session.query(models.Note).order_by(
        models.Note.created_at.desc()
    )
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "notes": notes},
    )


@app.post("/notes")
def create_note(
    title: str = Form(...),
    content: str = Form(...),
    session: Session = Depends(get_db_session),
):
    new_note = models.Note(title=title, content=content)
    session.add(new_note)
    session.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/api/notes", response_model=List[schemas.NoteRead])
def list_notes(session: Session = Depends(get_db_session)):
    notes = session.query(models.Note).order_by(models.Note.created_at.desc()).all()
    return notes


@app.post("/api/notes", response_model=schemas.NoteRead, status_code=201)
def create_note_api(
    payload: schemas.NoteCreate, session: Session = Depends(get_db_session)
):
    new_note = models.Note(**payload.dict())
    session.add(new_note)
    session.commit()
    session.refresh(new_note)
    return new_note


@app.get("/health")
def healthcheck():
    return {"status": "ok", "db_host": settings.db_host}


