def run(state: dict) -> dict:
    """Trend Research (category/product_id) ve Sales Insight (question) graph'ları
    aynı Planlayıcı düğümünü paylaşır — hangi alanların dolu olduğuna göre davranır.
    """
    if "category" in state:
        category = state["category"]
        product_id = state.get("product_id")
        queries = [f"{category} pazar trendleri 2026", f"{category} fiyat aralığı"]
        if product_id:
            queries.append(f"{category} ürün rekabet analizi")
        return {"queries": queries}

    return {}
