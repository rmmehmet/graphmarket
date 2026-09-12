import hashlib
import hmac
import json
from urllib.parse import urlencode

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import encrypt_secret
from app.db.neo4j import get_session
from app.models.messenger_account import MessengerAccount


def build_oauth_url(team_id: str) -> str:
    params = {
        "client_id": settings.meta_app_id,
        "redirect_uri": settings.meta_redirect_uri,
        "scope": "pages_messaging,pages_show_list",
        "state": team_id,
        "response_type": "code",
    }
    return f"https://www.facebook.com/v19.0/dialog/oauth?{urlencode(params)}"


def exchange_code_for_token(code: str) -> dict:
    response = httpx.get(
        "https://graph.facebook.com/v19.0/oauth/access_token",
        params={
            "client_id": settings.meta_app_id,
            "client_secret": settings.meta_app_secret,
            "redirect_uri": settings.meta_redirect_uri,
            "code": code,
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def save_messenger_account(db: Session, team_id: str, page_id: str, access_token: str) -> MessengerAccount:
    account = MessengerAccount(
        team_id=team_id,
        page_id=page_id,
        access_token_encrypted=encrypt_secret(access_token) if access_token else "",
        status="connected" if access_token else "expired",
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def resolve_team_id_by_page(db: Session, page_id: str) -> str | None:
    account = db.scalar(
        select(MessengerAccount).where(
            MessengerAccount.page_id == page_id, MessengerAccount.status == "connected"
        )
    )
    return str(account.team_id) if account else None


def verify_signature(payload: bytes, signature_header: str) -> bool:
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    expected = hmac.new(settings.meta_app_secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    provided = signature_header.removeprefix("sha256=")
    return hmac.compare_digest(expected, provided)


def _fix_facebook_mojibake(text: str) -> str:
    """Facebook'un export JSON'u UTF-8 baytlarını Latin-1 karakterleri gibi kaçırıyor
    (bilinen bir FB hatası) — bu yüzden 'İ', 'ş', 'ğ' gibi karakterler bozuk görünür.
    Baytları Latin-1 olarak geri kodlayıp UTF-8 olarak yeniden çözmek orijinal metni verir.
    """
    try:
        return text.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def parse_export_messages(content: bytes) -> list[dict]:
    """Facebook 'Bilgilerinizi İndirin' JSON export formatını okur — {"messages": [{"sender_name",
    "content", ...}]}. Kişisel veri tutulmaz: gönderen adı hash'lenip customer_ref olarak kullanılır.
    """
    try:
        data = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"desteklenmeyen export formatı (JSON bekleniyor): {exc}")

    messages = []
    for m in data.get("messages", []):
        text = m.get("content")
        sender = m.get("sender_name")
        if not text or not sender:
            continue
        text = _fix_facebook_mojibake(text)
        sender = _fix_facebook_mojibake(sender)
        customer_ref = hashlib.sha256(sender.encode("utf-8")).hexdigest()[:16]
        messages.append({"text": text, "customer_ref": customer_ref})
    return messages


def list_conversations(team_id: str, customer: str | None, product_hint: str | None) -> list[dict]:
    with get_session() as session:
        query = "MATCH (cust:Customer {team_id: $team_id})-[r:ILGILENDI]->(p:Product) "
        params: dict = {"team_id": team_id}
        clauses = []
        if customer:
            clauses.append("cust.id = $customer")
            params["customer"] = customer
        if product_hint:
            clauses.append("toLower(p.name) CONTAINS toLower($product_hint)")
            params["product_hint"] = product_hint
        if clauses:
            query += "WHERE " + " AND ".join(clauses) + " "
        query += (
            "RETURN cust.id AS customer, p.name AS product, r.sentiment AS sentiment, "
            "toString(r.mentioned_at) AS mentioned_at ORDER BY r.mentioned_at DESC LIMIT 50"
        )
        result = session.run(query, **params)
        return [dict(record) for record in result]


def get_conversation_detail(team_id: str, customer: str, product: str) -> dict | None:
    with get_session() as session:
        result = session.run(
            "MATCH (cust:Customer {team_id: $team_id, id: $customer})-[r:ILGILENDI]->(p:Product {name: $product}) "
            "RETURN cust.id AS customer, p.name AS product, r.sentiment AS sentiment, "
            "toString(r.mentioned_at) AS mentioned_at, coalesce(r.messages, []) AS messages",
            team_id=team_id,
            customer=customer,
            product=product,
        )
        record = result.single()
        return dict(record) if record else None
