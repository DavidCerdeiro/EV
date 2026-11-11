from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.models.token import AppToken
from app.schemas.auth_schema import TokenPayload

def upsert_token(db: Session, payload: TokenPayload):
    stmt = insert(AppToken).values(
        application=payload.application.lower(),
        token=payload.token,
        refresh_token=payload.refresh_token
    )
    upsert_stmt = stmt.on_conflict_do_update(
        index_elements=['application'],
        set_={'token': stmt.excluded.token, 'refresh_token': stmt.excluded.refresh_token}
    )
    db.execute(upsert_stmt)
    db.commit()
    return {"message": f"Token guardado para {payload.application}"}

def get_token(db: Session, application: str):
    return db.query(AppToken).filter(AppToken.application == application.lower()).first()