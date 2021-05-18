def peek(f, size):
    pos = f.tell()
    data = f.read(size)
    f.seek(pos)

    return data