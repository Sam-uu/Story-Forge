from sqlalchemy.orm import Session
from . import models_db, schemas_db

def create_card(db: Session, card: schemas_db.CardCreate):
    db_card = models_db.Card(
        intent=card.intent,
        user_story=card.user_story,
        acceptance_criteria=card.acceptance_criteria,
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def get_cards(db: Session):
    return db.query(models_db.Card).order_by(models_db.Card.id.desc()).all()

def delete_card(db: Session, card_id: int):
    card = db.query(models_db.Card).filter(models_db.Card.id == card_id).first()
    if card:
        db.delete(card)
        db.commit()
        return True
    return False
