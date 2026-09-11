from datetime import datetime
from decimal import Decimal

from app.db.neo4j import get_session


def sync_product_upsert(product_id: str, name: str, category: str | None, team_id: str) -> None:
    with get_session() as session:
        session.run(
            "MERGE (p:Product {id: $id}) SET p.name = $name, p.category = $category, p.team_id = $team_id",
            id=product_id,
            name=name,
            category=category,
            team_id=team_id,
        )
        if category:
            session.run(
                "MERGE (cat:Category {name: $category, team_id: $team_id}) "
                "WITH cat MATCH (p:Product {id: $id}) "
                "MERGE (p)-[:AIT_KATEGORI]->(cat)",
                category=category,
                team_id=team_id,
                id=product_id,
            )


def sync_product_delete(product_id: str) -> None:
    with get_session() as session:
        session.run("MATCH (p:Product {id: $id}) DETACH DELETE p", id=product_id)


def sync_channel_upsert(channel_id: str, name: str, platform: str, team_id: str) -> None:
    with get_session() as session:
        session.run(
            "MERGE (c:Channel {id: $id}) SET c.name = $name, c.platform = $platform, c.team_id = $team_id",
            id=channel_id,
            name=name,
            platform=platform,
            team_id=team_id,
        )


def sync_channel_delete(channel_id: str) -> None:
    with get_session() as session:
        session.run("MATCH (c:Channel {id: $id}) DETACH DELETE c", id=channel_id)


def sync_sale_written(
    product_id: str, channel_id: str, price: Decimal, sold_at: datetime, source: str
) -> None:
    with get_session() as session:
        session.run(
            "MATCH (p:Product {id: $product_id}), (c:Channel {id: $channel_id}) "
            "MERGE (p)-[:PAYLASILDI]->(c) "
            "CREATE (pp:PricePoint {price: $price, currency: 'TRY', observed_at: $observed_at, source: $source}) "
            "MERGE (p)-[:HAS_PRICE]->(pp) "
            "MERGE (pp)-[:GECERLI_KANALDA]->(c)",
            product_id=product_id,
            channel_id=channel_id,
            price=float(price),
            observed_at=sold_at.isoformat(),
            source=source,
        )
