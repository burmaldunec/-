from src.auth import register_user, authenticate, hash_password

def test_auth_flow():
    assert len(hash_password("test")) == 64
    register_user("testuser", "pass123", "user")
    assert authenticate("testuser", "pass123") is not None
    assert authenticate("testuser", "wrong") is None
    print("[PASS] test_auth_flow")

if __name__ == "__main__":
    test_auth_flow()