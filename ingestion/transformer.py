def normalize_coin(record, source):
    if source == "coinpaprika":
        usd = record["quotes"]["USD"]
        return {
            "symbol": record["symbol"],
            "name": record["name"],
            "price_usd": usd["price"],
            "market_cap_usd": usd["market_cap"],
            "volume_24h_usd": usd["volume_24h"],
            "source": source,
            "last_updated": record["last_updated"]
        }

    if source == "coingecko":
        return {
            "symbol": record["symbol"].upper(),
            "name": record["name"],
            "price_usd": record["current_price"],
            "market_cap_usd": record["market_cap"],
            "volume_24h_usd": record["total_volume"],
            "source": source,
            "last_updated": record["last_updated"]
        }
