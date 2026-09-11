from app.db.neo4j import get_session


def run(state: dict) -> dict:
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
