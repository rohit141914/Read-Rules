from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorCollection

_collection: AsyncIOMotorCollection | None = None


def init_db(mongo_uri: str, db_name: str) -> None:
    from motor.motor_asyncio import AsyncIOMotorClient
    global _collection
    client = AsyncIOMotorClient(mongo_uri)
    _collection = client[db_name]["summaries"]


async def db_get(domain: str) -> dict | None:
    return await _collection.find_one({"domain": domain})


async def db_set(domain: str, result: dict, links: list | None = None, content_hash: str | None = None) -> None:
    now = datetime.now(timezone.utc)
    set_fields = {"result": result, "last_updated_at": now}
    if links:
        set_fields["links"] = links
    if content_hash:
        set_fields["content_hash"] = content_hash
    await _collection.update_one(
        {"domain": domain},
        {
            "$set": set_fields,
            "$setOnInsert": {"created_at": now},
        },
        upsert=True,
    )
