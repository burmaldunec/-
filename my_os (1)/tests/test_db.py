"""Модульные тесты слоя данных db.py."""
from src import db

def setup():
    """Очистка тестовых данных перед запуском."""
    db.init_db()
    db.execute_delete("users", {"login": "db_test_user"})

def test_insert():
    user_id = db.execute_insert("users", {
        "login": "db_test_user",
        "password_hash": "hash123",
        "role": "user"
    })
    assert user_id > 0
    print("[PASS] test_insert: запись создана")

def test_select():
    users = db.execute_select("users", {"login": "db_test_user"})
    assert len(users) == 1
    assert users[0]["login"] == "db_test_user"
    print("[PASS] test_select: запись найдена")

def test_select_all():
    users = db.execute_select("users")
    assert len(users) >= 1
    print("[PASS] test_select_all: список получен")

def test_update():
    db.execute_update("users", {"role": "admin"}, {"login": "db_test_user"})
    users = db.execute_select("users", {"login": "db_test_user"})
    assert users[0]["role"] == "admin"
    print("[PASS] test_update: запись обновлена")

def test_delete():
    db.execute_delete("users", {"login": "db_test_user"})
    users = db.execute_select("users", {"login": "db_test_user"})
    assert len(users) == 0
    print("[PASS] test_delete: запись удалена")

def test_select_empty():
    users = db.execute_select("users", {"login": "non_existent_user_xyz"})
    assert len(users) == 0
    print("[PASS] test_select_empty: пустой результат корректен")

if __name__ == "__main__":
    setup()
    test_insert()
    test_select()
    test_select_all()
    test_update()
    test_delete()
    test_select_empty()
    print("\n[SUCCESS] Все тесты db.py пройдены.")