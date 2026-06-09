import asyncio

from database.queries import get_thread, save_thread

TEST_USER_ID = 6764515798


async def test():
    await save_thread(TEST_USER_ID, 99999)
    result = await get_thread(TEST_USER_ID)
    assert result == 99999, f"❌ topic_id={result}, expected 99999"
    print(f"✅ save_thread / get_thread OK: {result}")


if __name__ == "__main__":
    asyncio.run(test())

# Запуск: python -m tests.thread_test