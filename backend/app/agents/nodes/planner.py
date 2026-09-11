def run(state: dict) -> dict:
    category = state["category"]
    product_id = state.get("product_id")

    queries = [f"{category} pazar trendleri 2026", f"{category} fiyat aralığı"]
    if product_id:
        queries.append(f"{category} ürün rekabet analizi")

    return {"queries": queries}
