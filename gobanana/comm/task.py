import uuid

from gobanana import comm


class Task(comm.DataTransferObject):
    @classmethod
    def get_id(cls):
        return str(uuid.uuid4())

    def __init__(self, payload):
        super().__init__(payload)
        self._id = self.get_id()

    @property
    def id(self):
        return self._id

    @property
    def request_channel(self):
        return comm.channels.TASK_REQUEST_PREFIX + self._id

    @property
    def response_channel(self):
        return comm.channels.TASK_RESPONSE_PREFIX + self._id
