def normalize_coin(record, source):
    if source == "coinpaprika":
        usd = record["quotes"]["USD"]
        symbol = record.get("symbol", "").strip()
        name = record.get("name", "").strip()
        canonical = (symbol + ":" + name).lower()
        return {
            "canonical_id": canonical,
            "symbol": symbol,
            "name": name,
            "price_usd": usd["price"],
            "market_cap_usd": usd["market_cap"],
            "volume_24h_usd": usd["volume_24h"],
            "source": source,
            "last_updated": record.get("last_updated")
        }

    if source == "coingecko":
        symbol = record.get("symbol", "").strip()
        name = record.get("name", "").strip()
        canonical = (symbol + ":" + name).lower()
        return {
            "canonical_id": canonical,
            "symbol": symbol,
            "name": name,
            "price_usd": record.get("current_price"),
            "market_cap_usd": record.get("market_cap"),
            "volume_24h_usd": record.get("total_volume"),
            "source": source,
            "last_updated": record.get("last_updated")
        }
