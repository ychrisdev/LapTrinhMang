import json

def encode(msg_type, data=None):
    return json.dumps({
        "type": msg_type,
        "data": data or {}
    }).encode()

def decode(raw_bytes):
    text = raw_bytes.decode()
    return json.loads(text)