"""Модульные тесты компонента kernel.py."""
from src.kernel import Kernel
from src.db import execute_select

def test_pid_increment():
    k = Kernel()
    pid1 = k.allocate_pid()
    pid2 = k.allocate_pid()
    assert pid2 == pid1 + 1
    print(f"[PASS] test_pid_increment: PID {pid1} -> {pid2}")

def test_memory_allocate():
    k = Kernel()
    assert k.allocate_memory(100) is True
    assert k.memory_info()["used"] == 100
    print("[PASS] test_memory_allocate: память выделена")

def test_memory_limit():
    k = Kernel()
    assert k.allocate_memory(5000) is False
    assert k.memory_info()["used"] == 0
    print("[PASS] test_memory_limit: лимит памяти сработал")

def test_free_memory():
    k = Kernel()
    k.allocate_memory(100)
    k.free_memory(100)
    assert k.memory_info()["used"] == 0
    print("[PASS] test_free_memory: память освобождена")

def test_free_more_than_used():
    k = Kernel()
    k.allocate_memory(50)
    k.free_memory(200)
    assert k.memory_info()["used"] == 0
    print("[PASS] test_free_more_than_used: отрицательный остаток предотвращен")

def test_save_memory_state():
    k = Kernel()
    k.allocate_memory(150)
    k.save_memory_state()
    states = execute_select("memory_state")
    assert len(states) >= 1
    assert states[0]["used"] == 150
    print("[PASS] test_save_memory_state: состояние памяти сохранено в БД")

if __name__ == "__main__":
    test_pid_increment()
    test_memory_allocate()
    test_memory_limit()
    test_free_memory()
    test_free_more_than_used()
    test_save_memory_state()
    print("\n[SUCCESS] Все тесты kernel_unit.py пройдены.")