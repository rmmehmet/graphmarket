from app.db.neo4j import get_session


def list_trend_signals(category: str | None) -> list[dict]:
    with get_session() as session:
        if category:
            query = (
                "MATCH (t:TrendSignal {category: $category}) "
                "RETURN t.category AS category, t.direction AS direction, t.strength AS strength, "
                "toString(t.observed_at) AS observed_at, t.source AS source "
                "ORDER BY t.observed_at DESC LIMIT 50"
            )
            result = session.run(query, category=category)
        else:
            query = (
                "MATCH (t:TrendSignal) "
                "RETURN t.category AS category, t.direction AS direction, t.strength AS strength, "
                "toString(t.observed_at) AS observed_at, t.source AS source "
                "ORDER BY t.observed_at DESC LIMIT 50"
            )
            result = session.run(query)
        return [dict(record) for record in result]


def list_competitors(category: str | None, product_id: str | None) -> list[dict]:
    with get_session() as session:
        if product_id:
            query = (
                "MATCH (comp:Competitor)-[:REKABET_EDER]->(p:Product {id: $product_id}) "
                "RETURN comp.name AS name, comp.platform AS platform, comp.anonymized AS anonymized "
                "LIMIT 50"
            )
            result = session.run(query, product_id=product_id)
        elif category:
            query = (
                "MATCH (comp:Competitor)-[:REKABET_EDER]->(p:Product {category: $category}) "
                "RETURN DISTINCT comp.name AS name, comp.platform AS platform, comp.anonymized AS anonymized "
                "LIMIT 50"
            )
            result = session.run(query, category=category)
        else:
            query = (
                "MATCH (comp:Competitor) "
                "RETURN comp.name AS name, comp.platform AS platform, comp.anonymized AS anonymized "
                "LIMIT 50"
            )
            result = session.run(query)
        return [dict(record) for record in result]
