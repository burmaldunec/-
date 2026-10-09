"""Функциональные тесты планировщика."""
from src import db, scheduler
from src.kernel import kernel_instance


def setup():
    """Очистка процессов с префиксом ft и освобождение памяти."""
    procs = db.execute_select('processes')
    for p in procs:
        if p['name'].startswith('ft_'):
            kernel_instance.free_memory(p['memory_used'])
            db.execute_delete('processes', {'pid': p['pid']})


def test_create_process():
    pid = scheduler.create_process('ft_app', 'admin', 10)
    assert pid > 0
    print("[PASS] FT-11: создание процесса")


def test_memory_overflow():
    pid = scheduler.create_process('ft_huge', 'admin', 5000)
    assert pid == -1
    print("[PASS] FT-12: переполнение памяти")


def test_list_processes():
    scheduler.create_process('ft_p1', 'admin', 5)
    scheduler.create_process('ft_p2', 'admin', 5)
    procs = scheduler.list_processes()
    assert len(procs) >= 2
    print("[PASS] FT-13: список процессов")


def test_get_process():
    pid = scheduler.create_process('ft_get', 'admin', 5)
    p = scheduler.get_process(pid)
    assert p is not None
    assert p['pid'] == pid
    print("[PASS] FT-14: получение процесса по PID")


def test_get_missing():
    assert scheduler.get_process(99999) is None
    print("[PASS] FT-15: несуществующий PID")


def test_terminate_frees_memory():
    pid = scheduler.create_process('ft_term', 'admin', 7)
    before = kernel_instance.memory_used
    result = scheduler.terminate_process(pid)
    assert result is True
    assert kernel_instance.memory_used == before - 7
    print("[PASS] FT-16: завершение и освобождение памяти")


def test_terminate_missing():
    assert scheduler.terminate_process(99999) is False
    print("[PASS] FT-17: завершение несуществующего процесса")


def test_round_robin():
    p1 = scheduler.create_process('ft_rr1', 'admin', 5)
    p2 = scheduler.create_process('ft_rr2', 'admin', 5)
    proc = scheduler.schedule_round_robin()
    assert proc is not None
    print("[PASS] FT-18: round robin")


def test_process_count():
    before = scheduler.process_count()
    scheduler.create_process('ft_cnt1', 'admin', 3)
    scheduler.create_process('ft_cnt2', 'admin', 3)
    scheduler.create_process('ft_cnt3', 'admin', 3)
    assert scheduler.process_count() == before + 3
    print("[PASS] FT-19: подсчёт процессов")


if __name__ == "__main__":
    setup()
    test_create_process()
    test_memory_overflow()
    test_list_processes()
    test_get_process()
    test_get_missing()
    test_terminate_frees_memory()
    test_terminate_missing()
    test_round_robin()
    test_process_count()
    print("\nВсе функциональные тесты планировщика пройдены.")