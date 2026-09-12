import json

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Request, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.postgres import get_db
from app.schemas.messenger import (
    ConnectResponse,
    ConversationDetailOut,
    ConversationOut,
    ImportExportResponse,
    SyncResponse,
)
from app.services.auth_service import AuthenticatedUser, get_current_user
from app.services.job_service import create_job, update_job
from app.services.quota_service import check_and_increment
from app.services.messenger_service import (
    build_oauth_url,
    exchange_code_for_token,
    get_conversation_detail,
    list_conversations,
    parse_export_messages,
    resolve_team_id_by_page,
    save_messenger_account,
    verify_signature,
)
from app.workers.celery_tasks import run_messenger_import_batch, run_messenger_webhook_message

router = APIRouter(prefix="/api/messenger", tags=["messenger"])


@router.get("/connect", response_model=ConnectResponse)
def connect(current_user: AuthenticatedUser = Depends(get_current_user)):
    return ConnectResponse(redirect_url=build_oauth_url(current_user.team_id))


@router.get("/callback")
def callback(code: str, state: str, db: Session = Depends(get_db)):
    token_data = exchange_code_for_token(code)
    account = save_messenger_account(
        db,
        team_id=state,
        page_id=token_data.get("page_id", ""),
        access_token=token_data.get("access_token", ""),
    )
    return {"status": account.status}


@router.get("/webhook")
def verify_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
):
    if hub_mode == "subscribe" and hub_verify_token == settings.meta_webhook_verify_token:
        return int(hub_challenge)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="verify token mismatch")


@router.post("/webhook")
async def receive_webhook(request: Request, db: Session = Depends(get_db)):
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256", "")
    if not verify_signature(body, signature):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid signature")

    payload = json.loads(body)
    enqueued = 0
    for entry in payload.get("entry", []):
        team_id = resolve_team_id_by_page(db, entry.get("id", ""))
        if team_id is None:
            continue
        for messaging_event in entry.get("messaging", []):
            message_text = messaging_event.get("message", {}).get("text")
            sender_id = messaging_event.get("sender", {}).get("id")
            if not message_text or not sender_id:
                continue
            job = create_job(db, team_id, "messenger_sync", input_payload={"source": "webhook"})
            run_messenger_webhook_message.delay(
                str(job.id), team_id, message_text, sender_id, None, "messenger_webhook"
            )
            enqueued += 1

    return {"enqueued": enqueued}


@router.post("/import-export", response_model=ImportExportResponse)
async def import_export(
    file: UploadFile = File(...),
    channel_id: str | None = Form(default=None),
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    content = await file.read()
    try:
        messages = parse_export_messages(content)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    job = create_job(
        db, current_user.team_id, "messenger_import", input_payload={"message_count": len(messages)}
    )
    run_messenger_import_batch.delay(str(job.id), current_user.team_id, messages, channel_id)
    return ImportExportResponse(job_id=job.id, message_count=len(messages))


@router.get("/conversations", response_model=list[ConversationOut])
def conversations(
    customer: str | None = None,
    product_hint: str | None = None,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    return list_conversations(current_user.team_id, customer, product_hint)


@router.get("/conversations/detail", response_model=ConversationDetailOut)
def conversation_detail(
    customer: str,
    product: str,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    detail = get_conversation_detail(current_user.team_id, customer, product)
    if detail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="konuşma bulunamadı")
    return detail


@router.post("/sync", response_model=SyncResponse)
def sync(
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    check_and_increment(db, current_user.team_id, "messenger_sync")

    job = create_job(db, current_user.team_id, "messenger_sync", input_payload={})
    # Gerçek zamanlı sync, /connect ile bağlanmış gerçek bir Meta App/sayfa gerektirir —
    # bu ortamda yok, o yüzden job'u belirsiz şekilde "queued" bırakmak yerine dürüstçe hataya düşürüyoruz.
    update_job(
        db,
        str(job.id),
        status_="error",
        error_message="Bağlı bir Messenger sayfası yok — önce /connect ile bağlanman gerekiyor.",
    )
    return SyncResponse(job_id=job.id)
