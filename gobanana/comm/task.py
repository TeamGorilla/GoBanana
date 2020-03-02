import uuid

import gobanana as gb
from gobanana.comm.data_transfer_object import DataTransferObject


class Task(DataTransferObject):
    @classmethod
    def get_id(cls):
        return str(uuid.uuid4())

    def __init__(self, payload):
        super().__init__(payload)
        self.id = self.get_id()

    @property
    def request_channel(self):
        return gb.utils.constants.TASK_REQUEST_PREFIX + self.id

    @property
    def response_channel(self):
        return gb.utils.constants.TASK_RESPONSE_PREFIX + self.id
