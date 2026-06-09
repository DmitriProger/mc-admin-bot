import asyncio
import os

from database.init import init_db
from database.queries import (
    get_nickname,
    get_user_status,
    new_registration,
    set_nickname,
    set_pending,
    approve_user,
    get_thread,
    save_thread,
    clear_thread,
)

TEST_USER_ID = 999999999


async def test():
    await init_db()
    print("✅ init_db OK")

    await new_registration(TEST_USER_ID)
    print("✅ new_registration OK")

    status = await get_user_status(TEST_USER_ID)
    assert status == "new", f"❌ status={status}, expected 'new'"
    print(f"✅ get_user_status OK: {status}")

    await set_nickname(TEST_USER_ID, "TestPlayer")
    nick = await get_nickname(TEST_USER_ID)
    assert nick == "TestPlayer", f"❌ nickname={nick}"
    print(f"✅ set_nickname / get_nickname OK: {nick}")

    await set_pending(TEST_USER_ID)
    status = await get_user_status(TEST_USER_ID)
    assert status == "pending", f"❌ status={status}"
    print(f"✅ set_pending OK: {status}")

    await approve_user(TEST_USER_ID)
    status = await get_user_status(TEST_USER_ID)
    assert status == "approved", f"❌ status={status}"
    print(f"✅ approve_user OK: {status}")

    await save_thread(TEST_USER_ID, 12345)
    thread_id = await get_thread(TEST_USER_ID)
    assert thread_id == 12345, f"❌ thread_id={thread_id}"
    print(f"✅ save_thread / get_thread OK: {thread_id}")

    await clear_thread(TEST_USER_ID)
    thread_id = await get_thread(TEST_USER_ID)
    assert thread_id is None, f"❌ thread_id={thread_id}, expected None"
    print(f"✅ clear_thread OK: {thread_id}")

    print("\n✅ Все тесты прошли")


if __name__ == "__main__":
    asyncio.run(test())

# Запуск: python -m tests.db_test
