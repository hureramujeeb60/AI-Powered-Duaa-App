from db import AsyncSessionLocal

async def get_all_fcm_tokens():
    async with AsyncSessionLocal() as session:
        result = await session.execute("SELECT fcm_token FROM fcm_tokens")
        tokens = [row[0] for row in result.fetchall()]
    return tokens
