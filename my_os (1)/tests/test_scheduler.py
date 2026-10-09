"""Тесты планировщика."""

from src import scheduler
from src.kernel import kernel_instance


def test_create_process():
    pid = scheduler.create_process('app_test', 'admin')
    assert pid > 0
    print("[PASS] test_create_process")


def test_memory_limit():
    res = scheduler.create_process('huge', 'admin', 5000)
    assert res == -1
    print("[PASS] test_memory_limit")


def test_terminate_frees_memory():
    before = kernel_instance.memory_used
    pid = scheduler.create_process('temp', 'admin', 50)
    scheduler.terminate_process(pid)
    assert kernel_instance.memory_used == before
    print("[PASS] test_terminate_frees_memory")


def test_get_process():
    pid = scheduler.create_process('p_get', 'admin')
    p = scheduler.get_process(pid)
    assert p is not None
    assert p['name'] == 'p_get'
    print("[PASS] test_get_process")


def test_terminate_nonexistent():
    res = scheduler.terminate_process(-999)
    assert res is False
    print("[PASS] test_terminate_nonexistent")


def test_round_robin():
    p1 = scheduler.create_process('p1', 'admin')
    p2 = scheduler.create_process('p2', 'admin')
    curr = scheduler.schedule_round_robin()
    assert curr is not None
    print("[PASS] test_round_robin")


if __name__ == "__main__":
    test_create_process()
    test_memory_limit()
    test_terminate_frees_memory()
    test_get_process()
    test_terminate_nonexistent()
    test_round_robin()
    print("Все тесты планировщика пройдены успешно!")