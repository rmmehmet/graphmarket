from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.postgres import get_db
from app.models.channel import Channel
from app.schemas.channel import ChannelCreate, ChannelOut, ChannelUpdate
from app.services.auth_service import AuthenticatedUser, get_current_user
from app.services.graph_sync import sync_channel_delete, sync_channel_upsert

router = APIRouter(prefix="/api/channels", tags=["channels"])


def _get_channel(db: Session, team_id: str, channel_id: str) -> Channel:
    channel = db.scalar(select(Channel).where(Channel.id == channel_id, Channel.team_id == team_id))
    if channel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="channel not found")
    return channel


@router.get("/", response_model=list[ChannelOut])
def list_channels(
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.scalars(select(Channel).where(Channel.team_id == current_user.team_id)).all()


@router.post("/", response_model=ChannelOut, status_code=201)
def create_channel(
    payload: ChannelCreate,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    channel = Channel(team_id=current_user.team_id, **payload.model_dump())
    db.add(channel)
    db.commit()
    db.refresh(channel)
    sync_channel_upsert(str(channel.id), channel.name, channel.platform, current_user.team_id)
    return channel


@router.put("/{channel_id}", response_model=ChannelOut)
def update_channel(
    channel_id: str,
    payload: ChannelUpdate,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    channel = _get_channel(db, current_user.team_id, channel_id)
    for key, value in payload.model_dump().items():
        if value is not None:
            setattr(channel, key, value)
    db.commit()
    db.refresh(channel)
    sync_channel_upsert(str(channel.id), channel.name, channel.platform, current_user.team_id)
    return channel


@router.delete("/{channel_id}", status_code=204)
def delete_channel(
    channel_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    channel = _get_channel(db, current_user.team_id, channel_id)
    db.delete(channel)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="channel has sales records and cannot be deleted",
        )
    sync_channel_delete(channel_id)
