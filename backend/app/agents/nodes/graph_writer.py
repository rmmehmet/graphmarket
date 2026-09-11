from app.db.neo4j import get_session


def run(state: dict) -> dict:
    if "message_text" in state:
        return _run_messenger(state)
    return _run_trend(state)


def _run_trend(state: dict) -> dict:
    category = state["category"]
    team_id = state["team_id"]
    extracted = state.get("extracted", {})

    with get_session() as session:
        session.run(
            "MERGE (cat:Category {name: $category, team_id: $team_id}) "
            "CREATE (t:TrendSignal {category: $category, direction: $direction, "
            "strength: $strength, observed_at: datetime(), source: 'trend_research_agent'}) "
            "MERGE (t)-[:ILGILI_KATEGORI]->(cat)",
            category=category,
            team_id=team_id,
            direction=extracted.get("direction", "durağan"),
            strength=extracted.get("strength", 0.5),
        )

    return {"graph_written": True}


def _run_messenger(state: dict) -> dict:
    team_id = state["team_id"]
    customer_ref = state["customer_ref"]
    channel_id = state.get("channel_id")
    extracted = state.get("extracted", {})
    product_hint = (extracted.get("product_hint") or "").strip()
    sentiment = extracted.get("sentiment") or "nötr"

    matched_product_id = None
    with get_session() as session:
        session.run(
            "MERGE (cust:Customer {id: $id}) SET cust.team_id = $team_id",
            id=customer_ref,
            team_id=team_id,
        )

        if channel_id:
            session.run(
                "MATCH (cust:Customer {id: $customer_ref}), (ch:Channel {id: $channel_id}) "
                "MERGE (cust)-[:MESAJLASTI]->(ch)",
                customer_ref=customer_ref,
                channel_id=channel_id,
            )

        if product_hint:
            result = session.run(
                "MATCH (p:Product {team_id: $team_id}) "
                "WHERE toLower(p.name) CONTAINS toLower($hint) "
                "RETURN p.id AS id LIMIT 1",
                team_id=team_id,
                hint=product_hint,
            )
            record = result.single()
            if record:
                matched_product_id = record["id"]
                session.run(
                    "MATCH (cust:Customer {id: $customer_ref}), (p:Product {id: $product_id}) "
                    "MERGE (cust)-[:ILGILENDI {mentioned_at: datetime(), sentiment: $sentiment}]->(p)",
                    customer_ref=customer_ref,
                    product_id=matched_product_id,
                    sentiment=sentiment,
                )

    return {"graph_written": True, "matched_product_id": matched_product_id}
