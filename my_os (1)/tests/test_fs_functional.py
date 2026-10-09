"""Функциональные тесты файловой системы."""
from src import fs, db


def setup():
    """Очищаем файлы с префиксом ft."""
    files = db.execute_select('files')
    for f in files:
        if f['path'].startswith('/ft'):
            db.execute_delete('files', {'path': f['path']})


def test_create_file():
    fid = fs.create_file('/ft01.txt', 'content', 'admin')
    assert fid > 0
    assert fs.read_file('/ft01.txt') == 'content'
    print("[PASS] FT-01: создание файла")


def test_create_duplicate():
    fs.create_file('/ft02.txt', 'a', 'admin')
    result = fs.create_file('/ft02.txt', 'b', 'admin')
    assert result == -1
    print("[PASS] FT-02: дубликат отклонён")


def test_read_file():
    fs.create_file('/ft03.txt', 'hello', 'admin')
    assert fs.read_file('/ft03.txt') == 'hello'
    print("[PASS] FT-03: чтение файла")


def test_read_missing():
    assert fs.read_file('/missing.txt') == ''
    print("[PASS] FT-04: чтение несуществующего файла")


def test_write_file():
    fs.create_file('/ft05.txt', 'old', 'admin')
    fs.write_file('/ft05.txt', 'new')
    assert fs.read_file('/ft05.txt') == 'new'
    print("[PASS] FT-05: обновление содержимого")


def test_delete_file():
    fs.create_file('/ft06.txt', 'x', 'admin')
    fs.delete_file('/ft06.txt')
    assert fs.read_file('/ft06.txt') == ''
    print("[PASS] FT-06: удаление файла")


def test_list_files():
    fs.create_file('/ft07_a.txt', 'a', 'admin')
    fs.create_file('/ft07_b.txt', 'b', 'admin')
    files = fs.list_files('/ft07')
    assert '/ft07_a.txt' in files
    assert '/ft07_b.txt' in files
    print("[PASS] FT-07: список файлов по префиксу")


def test_get_owner():
    fs.create_file('/ft08.txt', 'x', 'admin')
    assert fs.get_owner('/ft08.txt') == 'admin'
    print("[PASS] FT-08: получение владельца")


def test_get_owner_missing():
    assert fs.get_owner('/missing2.txt') is None
    print("[PASS] FT-09: владелец несуществующего файла")


def test_get_file_info():
    fs.create_file('/ft09.txt', 'x', 'admin')
    info = fs.get_file_info('/ft09.txt')
    assert info is not None
    assert info['path'] == '/ft09.txt'
    assert info['owner'] == 'admin'
    print("[PASS] получение полной информации о файле")


if __name__ == "__main__":
    setup()
    test_create_file()
    test_create_duplicate()
    test_read_file()
    test_read_missing()
    test_write_file()
    test_delete_file()
    test_list_files()
    test_get_owner()
    test_get_owner_missing()
    test_get_file_info()
    print("\nВсе функциональные тесты ФС пройдены.")