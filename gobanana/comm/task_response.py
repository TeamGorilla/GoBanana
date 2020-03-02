from gobanana.comm.data_transfer_object import DataTransferObject


class TaskResponse(DataTransferObject):
    def __init__(self, task, payload):
        super().__init__(payload)
        self.task = task
