"""Модульные тесты компонента auth.py."""
from src.auth import hash_password, register_user, authenticate, check_permission
from src import db

def setup():
    db.init_db()
    db.execute_delete("users", {"login": "unit_user"})

def test_hash():
    h = hash_password("secret123")
    assert len(h) == 64
    assert h != "secret123"
    print("[PASS] test_hash: SHA-256 сформирован")

def test_register_unique():
    uid = register_user("unit_user", "pass123", "user")
    assert uid is not None
    duplicate = register_user("unit_user", "pass456", "user")
    assert duplicate is None
    print("[PASS] test_register_unique: дублирование предотвращено")

def test_authenticate():
    assert authenticate("unit_user", "pass123") is not None
    assert authenticate("unit_user", "wrong_pass") is None
    print("[PASS] test_authenticate: авторизация верна")

def test_admin_permissions():
    assert check_permission("admin", "delete_file", "user") is True
    assert check_permission("admin", "kill", "user") is True
    print("[PASS] test_admin_permissions: полный доступ у admin")

def test_user_permissions():
    assert check_permission("user", "delete_file", "admin") is False
    assert check_permission("user", "delete_file", "user") is True
    print("[PASS] test_user_permissions: ограничения прав у user")

if __name__ == "__main__":
    setup()
    test_hash()
    test_register_unique()
    test_authenticate()
    test_admin_permissions()
    test_user_permissions()
    print("\n[SUCCESS] Все тесты auth_unit.py пройдены.")