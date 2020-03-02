import redis

from gobanana import comm


def get_client():
    return redis.Redis()


class TaskDispatcher(object):
    def __init__(self, task: 'comm.Task'):
        self.task = task
        self.client = get_client()
        self.pubsub = self.client.pubsub()

    def send(self):
        self.pubsub.subscribe(self.task.response_channel)

        # eat the subscription confirmation message
        self.pubsub.get_message()

        self.client.publish(self.task.request_channel, self.task.serialize())

    def wait(self):
        while True:
            message = self.pubsub.get_message()
            if message['type'] in ('message', 'pmessage'):
                return comm.Task.deserialize(message['data'])


class TaskWorker(object):
    def __init__(self):
        # self.channel_pattern = channel_pattern
        self.client = get_client()
        self.pubsub = self.client.pubsub()
        self.pubsub.psubscribe(comm.channels.TASK_REQUEST_PATTERN)

    def wait(self):
        while True:
            message = self.pubsub.get_message()
            if message['type'] in ('message', 'pmessage'):
                return comm.TaskResponse.deserialize(message['data'])

    def send(self, response: 'comm.TaskResponse'):
        self.client.publish(response.task.response_channel, response.serialize())
