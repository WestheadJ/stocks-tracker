import os


def human_size(num, suffix="B"):
    """Return human-readable file size"""
    for unit in ["", "K", "M", "G", "T", "P"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Y{suffix}"


def list_entries(dir_path):
    """Return list of (name, path, is_dir) sorted, only showing dirs + .xlsx files"""
    try:
        names = os.listdir(dir_path)
    except Exception:
        return []

    dirs, files = [], []
    for name in names:
        full = os.path.join(dir_path, name)
        if os.path.isdir(full):
            dirs.append((name, full, True))
        elif name.lower().endswith(".xlsx"):
            files.append((name, full, False))

    dirs.sort(key=lambda x: x[0].lower())
    files.sort(key=lambda x: x[0].lower())

    parent = os.path.abspath(os.path.join(dir_path, os.pardir))
    out = []
    if os.path.abspath(dir_path) != os.path.abspath(parent):
        out.append(("..", parent, True))

    return out + dirs + files
