import pytest
import pytest_asyncio

import database.init as db_init
from database.queries import (
    approve_user,
    clear_topic,
    close_report,
    create_report,
    get_nickname,
    get_report_user_id,
    get_topic,
    get_user_id_by_topic,
    get_user_status,
    new_registration,
    reject_user,
    save_topic,
    set_nickname,
    set_pending,
)

TEST_DB = "test.db"
USER_ID = 111111111


@pytest_asyncio.fixture(autouse=True)
async def use_test_db(tmp_path, monkeypatch):
    test_db = str(tmp_path / "test.db")
    monkeypatch.setattr(db_init, "DB_PATH", test_db)
    import database.queries as q
    monkeypatch.setattr(q, "DB_PATH", test_db)
    await db_init.init_db()


@pytest.mark.asyncio
async def test_new_registration():
    await new_registration(USER_ID)
    status = await get_user_status(USER_ID)
    assert status == "new"


@pytest.mark.asyncio
async def test_set_nickname():
    await new_registration(USER_ID)
    await set_nickname(USER_ID, "TestPlayer")
    assert await get_nickname(USER_ID) == "TestPlayer"


@pytest.mark.asyncio
async def test_status_transitions():
    await new_registration(USER_ID)
    await set_pending(USER_ID)
    assert await get_user_status(USER_ID) == "pending"
    await approve_user(USER_ID)
    assert await get_user_status(USER_ID) == "approved"


@pytest.mark.asyncio
async def test_reject_user():
    await new_registration(USER_ID)
    await reject_user(USER_ID)
    assert await get_user_status(USER_ID) == "rejected"


@pytest.mark.asyncio
async def test_thread_save_and_clear():
    await new_registration(USER_ID)
    await save_topic(USER_ID, 42)
    assert await get_topic(USER_ID) == 42
    await clear_topic(USER_ID)
    assert await get_topic(USER_ID) is None


@pytest.mark.asyncio
async def test_get_user_id_by_topic():
    await new_registration(USER_ID)
    await save_topic(USER_ID, 99)
    assert await get_user_id_by_topic(99) == USER_ID
    assert await get_user_id_by_topic(0) is None


@pytest.mark.asyncio
async def test_report_lifecycle():
    await new_registration(USER_ID)
    report_id = await create_report(USER_ID, "Griefer", "Griefing", "Описание", "open")
    assert await get_report_user_id(report_id) == USER_ID
    await close_report(report_id)


@pytest.mark.asyncio
async def test_duplicate_registration():
    await new_registration(USER_ID)
    await new_registration(USER_ID)
    assert await get_user_status(USER_ID) == "new"
