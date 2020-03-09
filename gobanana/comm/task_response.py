from gobanana import comm


class TaskResponse(comm.DataTransferObject):
    def __init__(self, task, payload):
        super().__init__(payload)
        self._task = task

    @property
    def task(self):
        return self._task
