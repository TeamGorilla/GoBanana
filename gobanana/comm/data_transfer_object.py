import jsonpickle


class DataTransferObject(object):
    def __init__(self, payload):
        self._payload = payload

    @property
    def payload(self):
        return self._payload

    def serialize(self):
        return jsonpickle.dumps(self)

    @classmethod
    def deserialize(cls, raw):
        return jsonpickle.loads(raw)
