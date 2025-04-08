from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..database import crud, models
from ..database.session import get_db
from ..utils.encryption import encryption_manager
import uuid

router = APIRouter()

class InstagramAccountCreate(BaseModel):
    username: str
    password: str

class InstagramAccountResponse(BaseModel):
    id: str
    username: str
    is_active: bool
    created_at: datetime
    last_used: Optional[datetime]

@router.post("/", response_model=InstagramAccountResponse)
async def create_account(account: InstagramAccountCreate, db: Session = Depends(get_db)):
    """Add a new Instagram account."""
    try:
        # Encrypt the password
        encrypted_password = encryption_manager.encrypt(account.password)
        
        # Create new account
        db_account = crud.create_instagram_account(
            db,
            account_id=str(uuid.uuid4()),
            username=account.username,
            encrypted_credentials=encrypted_password
        )
        
        return InstagramAccountResponse(
            id=db_account.id,
            username=db_account.username,
            is_active=db_account.is_active,
            created_at=db_account.created_at,
            last_used=db_account.last_used
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create account: {str(e)}"
        )

@router.get("/", response_model=List[InstagramAccountResponse])
async def list_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all Instagram accounts."""
    accounts = crud.get_instagram_accounts(db, skip=skip, limit=limit)
    return [
        InstagramAccountResponse(
            id=account.id,
            username=account.username,
            is_active=account.is_active,
            created_at=account.created_at,
            last_used=account.last_used
        )
        for account in accounts
    ]

@router.delete("/{account_id}")
async def delete_account(account_id: str, db: Session = Depends(get_db)):
    """Delete an Instagram account."""
    if crud.delete_instagram_account(db, account_id):
        return {"message": f"Account {account_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Account not found")

@router.put("/{account_id}/activate")
async def activate_account(account_id: str, db: Session = Depends(get_db)):
    """Activate an Instagram account."""
    account = crud.update_instagram_account(db, account_id, is_active=True)
    if account:
        return {"message": f"Account {account_id} activated"}
    raise HTTPException(status_code=404, detail="Account not found")

@router.put("/{account_id}/deactivate")
async def deactivate_account(account_id: str, db: Session = Depends(get_db)):
    """Deactivate an Instagram account."""
    account = crud.update_instagram_account(db, account_id, is_active=False)
    if account:
        return {"message": f"Account {account_id} deactivated"}
    raise HTTPException(status_code=404, detail="Account not found")
