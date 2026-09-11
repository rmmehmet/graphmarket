import uuid

from pydantic import BaseModel, ConfigDict


class ChannelCreate(BaseModel):
    name: str
    platform: str
    member_estimate: int | None = None


class ChannelUpdate(BaseModel):
    name: str | None = None
    platform: str | None = None
    member_estimate: int | None = None


class ChannelOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    platform: str
    member_estimate: int | None
