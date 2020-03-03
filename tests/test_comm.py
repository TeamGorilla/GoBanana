import gobanana as gb


def test_comm():
    # initialization on the dispatcher side
    task = gb.comm.Task("secret-string")
    sender = gb.comm.TaskDispatcher(task)

    # initialization on the worker side
    worker = gb.comm.TaskWorker()

    # task dispatching on the dispatcher side
    sender.send()

    # task fetching on the worker side
    task = worker.wait()

    # task processing on the worker side
    def _process_task(task):
        request = task.payload
        if request == "secret-string":
            return "right"
        else:
            return 'wrong'

    response = gb.comm.TaskResponse(task, _process_task(task))

    # task finished on the worker side
    worker.send(response)

    # finished task retrieval on the dispatcher side
    answer = sender.wait().payload
    assert answer == "right"
