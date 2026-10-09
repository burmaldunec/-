from src import db
from src.kernel import kernel_instance


def create_process(name, owner, memory):
    """Создаёт процесс. Возвращает PID > 0 или -1 при нехватке памяти."""
    if not kernel_instance.allocate_memory(memory):
        return -1
    pid = db.execute_insert('processes', {
        'name': name,
        'owner': owner,
        'memory_used': memory,
        'state': 'ready',
    })
    return pid


def list_processes():
    return db.execute_select('processes')


def get_process(pid):
    rows = db.execute_select('processes', {'pid': pid})
    return rows[0] if rows else None


def terminate_process(pid):
    p = get_process(pid)
    if p is None:
        return False
    kernel_instance.free_memory(p['memory_used'])
    db.execute_delete('processes', {'pid': pid})
    return True


def process_count():
    return len(db.execute_select('processes'))


def schedule_round_robin():
    procs = db.execute_select('processes')
    if not procs:
        return None
    p = procs[0]
    db.execute_update('processes', {'state': 'running'}, {'pid': p['pid']})
    p['state'] = 'running'
    return p