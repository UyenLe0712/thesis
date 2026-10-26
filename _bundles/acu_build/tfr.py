# Đọc TFRecord (GZIP) của AndroidControl bằng Python thuần, không cần TensorFlow.
# Khung TFRecord: uint64 độ dài · uint32 crc · dữ liệu · uint32 crc. Dữ liệu là tf.train.Example (protobuf).
import gzip, struct


def _varint(b, i):
    x = s = 0
    while True:
        c = b[i]; i += 1
        x |= (c & 0x7F) << s; s += 7
        if c < 0x80:
            return x, i


def _fields(b):
    i, n = 0, len(b)
    while i < n:
        k, i = _varint(b, i); f, t = k >> 3, k & 7
        if t == 2:
            L, i = _varint(b, i); yield f, b[i:i + L]; i += L
        elif t == 0:
            v, i = _varint(b, i); yield f, v
        elif t == 5:
            yield f, b[i:i + 4]; i += 4
        elif t == 1:
            yield f, b[i:i + 8]; i += 8
        else:
            raise ValueError(f"wire type {t}")


def _feature(b):
    for f, v in _fields(b):
        if f == 1:                                        # bytes_list
            return [x for g, x in _fields(v) if g == 1]
        if f == 2:                                        # float_list (packed)
            out = []
            for g, x in _fields(v):
                out += list(struct.unpack(f"<{len(x)//4}f", x)) if isinstance(x, (bytes, bytearray)) and len(x) % 4 == 0 else []
            return out
        if f == 3:                                        # int64_list (packed)
            out = []
            for g, x in _fields(v):
                if isinstance(x, int):
                    out.append(x)
                else:
                    j = 0
                    while j < len(x):
                        y, j = _varint(x, j); out.append(y - (1 << 64) if y >= 1 << 63 else y)
            return out
    return []


def example(b):
    d = {}
    for f, feats in _fields(b):
        if f != 1:
            continue
        for g, ent in _fields(feats):
            key = val = None
            for h, x in _fields(ent):
                if h == 1: key = x.decode()
                elif h == 2: val = _feature(x)
            d[key] = val
    return d


def records(path):
    with gzip.open(path, "rb") as f:
        while True:
            h = f.read(12)
            if len(h) < 12:
                return
            L = struct.unpack("<Q", h[:8])[0]
            yield f.read(L); f.read(4)
