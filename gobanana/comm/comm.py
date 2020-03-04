import redis

from gobanana import comm


def get_client():
    return redis.Redis()


class TaskDispatcher(object):
    def __init__(self, task: 'comm.Task'):
        self._task = task
        self._client = get_client()
        self._pubsub = self._client.pubsub()

    @property
    def task(self):
        return self._task

    def send(self):
        self._pubsub.subscribe(self._task.response_channel)

        # eat the subscription confirmation message
        self._pubsub.get_message()

        self._client.publish(self._task.request_channel, self._task.serialize())

    def wait(self):
        while True:
            message = self._pubsub.get_message()
            if message['type'] in ('message', 'pmessage'):
                return comm.Task.deserialize(message['data'])


class TaskWorker(object):
    def __init__(self):
        # self.channel_pattern = channel_pattern
        self._client = get_client()
        self._pubsub = self._client.pubsub()
        self._pubsub.psubscribe(comm.channels.TASK_REQUEST_PATTERN)

    def wait(self):
        while True:
            message = self._pubsub.get_message()
            if message['type'] in ('message', 'pmessage'):
                return comm.TaskResponse.deserialize(message['data'])

    def send(self, response: 'comm.TaskResponse'):
        self._client.publish(response.task.response_channel, response.serialize())
