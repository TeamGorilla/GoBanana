import jsonpickle


class DataTransferObject(object):
    def __init__(self, payload):
        self.payload = payload

    def serialize(self):
        return jsonpickle.dumps(self)

    @classmethod
    def deserialize(cls, raw):
        return jsonpickle.loads(raw)
