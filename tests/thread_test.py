import asyncio

from database.queries import get_topic, save_topic

TEST_USER_ID = 6764515798


async def test():
    await save_topic(TEST_USER_ID, 99999)
    result = await get_topic(TEST_USER_ID)
    assert result == 99999, f"❌ topic_id={result}, expected 99999"
    print(f"✅ save_topic / get_topic OK: {result}")


if __name__ == "__main__":
    asyncio.run(test())
