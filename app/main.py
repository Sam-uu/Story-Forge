from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .loader import init_models
from .schemas import (
    IntentRequest, IntentResponse,
    StoryRequest, StoryResponse,
    AcceptanceRequest, AcceptanceResponse,
    PipelineRequest, PipelineResponse,
)
from .pipeline import infer_intent, generate_user_story, generate_acceptance

from sqlalchemy.orm import Session
from .db import SessionLocal, engine, Base
from . import crud, schemas_db, models_db

app = FastAPI(title="Requirements → Stories → Acceptance API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    meta = init_models()
    app.state.meta = meta

@app.get("/healthz")
def healthz():
    return {"status": "ok", "meta": getattr(app.state, "meta", {})}

@app.post("/infer_intent", response_model=IntentResponse)
def api_infer_intent(req: IntentRequest):
    return IntentResponse(intent=infer_intent(req.requirement))

@app.post("/generate_user_story", response_model=StoryResponse)
def api_generate_story(req: StoryRequest):
    return StoryResponse(user_story=generate_user_story(req.requirement))

@app.post("/generate_acceptance", response_model=AcceptanceResponse)
def api_generate_acceptance(req: AcceptanceRequest):
    items = generate_acceptance(req.requirement, req.intent, req.user_story)
    return AcceptanceResponse(acceptance_criteria=items)

@app.post("/generate_all", response_model=PipelineResponse)
def api_generate_all(req: PipelineRequest):
    intent = infer_intent(req.requirement)
    story = generate_user_story(req.requirement)
    acceptance = generate_acceptance(req.requirement, intent, story)
    return PipelineResponse(intent=intent, user_story=story, acceptance_criteria=acceptance)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/cards", response_model=schemas_db.CardResponse)
def save_card(card: schemas_db.CardCreate, db: Session = Depends(get_db)):
    return crud.create_card(db, card)

@app.get("/cards", response_model=list[schemas_db.CardResponse])
def list_cards(db: Session = Depends(get_db)):
    return crud.get_cards(db)

@app.delete("/cards/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db)):
    success = crud.delete_card(db, card_id)
    return {"success": success}