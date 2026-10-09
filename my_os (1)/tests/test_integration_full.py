"""Интеграционные тесты учебной ОС."""
from src import db, fs, scheduler
from src.auth import register_user, check_permission
from src.kernel import kernel_instance
from src.syscalls import (
    sys_login, sys_create_file, sys_read_file, sys_delete_file,
    sys_list_files, sys_exec, sys_ps, sys_kill, sys_logs
)


def setup():
    """Подготовка: очистка и регистрация пользователей."""
    db.execute_delete('users', {'login': 'int_admin'})
    db.execute_delete('users', {'login': 'int_user'})
    register_user('int_admin', 'secret123', 'admin')
    register_user('int_user', 'user1234', 'user')
    files = db.execute_select('files')
    for f in files:
        if f['path'].startswith('/int'):
            db.execute_delete('files', {'path': f['path']})
    procs = db.execute_select('processes')
    for p in procs:
        kernel_instance.free_memory(p['memory_used'])
        db.execute_delete('processes', {'pid': p['pid']})


def test_is01_create_via_shell():
    sys_login('int_admin', 'secret123')
    fid = sys_create_file('/int01.txt', 'content', 'int_admin')
    assert fid > 0
    logs = db.execute_select('syscalls_log', {'syscall_name': 'sys_create_file'})
    assert any(l['status'] == 'OK' for l in logs)
    print("[PASS] IS-01: создание файла, статус OK в журнале")


def test_is02_read_via_shell():
    sys_login('int_admin', 'secret123')
    sys_create_file('/int02.txt', 'hello', 'int_admin')
    content = sys_read_file('/int02.txt', 'int_admin')
    assert content == 'hello'
    print("[PASS] IS-02: чтение файла")


def test_is03_delete_denied():
    sys_login('int_admin', 'secret123')
    sys_create_file('/int03.txt', 'x', 'int_admin')
    result = sys_delete_file('/int03.txt', 'int_user')
    assert result is False
    logs = db.execute_select('syscalls_log', {'syscall_name': 'sys_delete_file'})
    assert any(l['status'] == 'DENIED' for l in logs)
    print("[PASS] IS-03: отказ в удалении, статус DENIED в журнале")


def test_is04_run_process():
    sys_login('int_admin', 'secret123')
    used_before = kernel_instance.memory_used
    pid = sys_exec('int04_app', 'int_admin')
    assert pid > 0
    assert kernel_instance.memory_used > used_before
    logs = db.execute_select('syscalls_log', {'syscall_name': 'sys_exec'})
    assert any(l['status'] == 'OK' for l in logs)
    print("[PASS] IS-04: запуск процесса, память выделена")


def test_is05_kill_process():
    sys_login('int_admin', 'secret123')
    pid = sys_exec('int05_app', 'int_admin')
    used_after_create = kernel_instance.memory_used
    assert sys_kill(pid, 'int_admin') is True
    assert kernel_instance.memory_used < used_after_create
    print("[PASS] IS-05: завершение процесса, память освобождена")


def test_is06_full_admin_scenario():
    sys_login('int_admin', 'secret123')
    fid = sys_create_file('/int06.txt', 'admin data', 'int_admin')
    pid = sys_exec('int06_app', 'int_admin')
    assert fid > 0
    assert pid > 0
    assert sys_read_file('/int06.txt', 'int_admin') == 'admin data'
    assert sys_kill(pid, 'int_admin') is True
    print("[PASS] IS-06: сквозной сценарий администратора")


def test_is07_user_scenario():
    sys_login('int_user', 'user1234')
    sys_create_file('/int07_user.txt', 'user data', 'int_user')
    sys_create_file('/int07_admin.txt', 'admin data', 'int_admin')
    assert sys_delete_file('/int07_user.txt', 'int_user') is True
    assert sys_delete_file('/int07_admin.txt', 'int_user') is False
    pid = sys_exec('int07_app', 'int_admin')
    assert sys_kill(pid, 'int_user') is False
    assert sys_kill(pid, 'int_admin') is True
    print("[PASS] IS-07: сценарий обычного пользователя")


def test_is08_log_completeness():
    logs = db.execute_select('syscalls_log')
    names = set(l['syscall_name'] for l in logs)
    required = {'sys_login', 'sys_create_file', 'sys_read_file',
                'sys_delete_file', 'sys_exec', 'sys_kill'}
    missing = required - names
    assert not missing, f"Не найдено: {missing}"
    print("[PASS] IS-08: журнал содержит все ключевые вызовы")


def test_is09_memory_consistency():
    """Проверка: сумма памяти всех процессов совпадает с memory_used."""
    proc = db.execute_select('processes')
    total = sum(p['memory_used'] for p in proc)
    assert total == kernel_instance.memory_used
    print("[PASS] IS-09: память согласована с процессами")


def test_is10_cleanup_after_kill():
    """Проверка: после завершения всех процессов память освобождена."""
    proc = db.execute_select('processes')
    for p in proc:
        sys_kill(p['pid'], 'int_admin')
    proc_after = db.execute_select('processes')
    assert len(proc_after) == 0
    print("[PASS] IS-10: после kill всех процессов таблица пуста")


if __name__ == '__main__':
    setup()
    test_is01_create_via_shell()
    test_is02_read_via_shell()
    test_is03_delete_denied()
    test_is04_run_process()
    test_is05_kill_process()
    test_is06_full_admin_scenario()
    test_is07_user_scenario()
    test_is08_log_completeness()
    test_is09_memory_consistency()
    test_is10_cleanup_after_kill()
    print("\nВсе интеграционные тесты пройдены.")