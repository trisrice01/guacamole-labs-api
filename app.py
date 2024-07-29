import datetime
import flask
import time
from celery import Celery


app = flask.Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://192.168.1.164:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://192.168.1.164:6379/1'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


class TaskMetadata:
    def __init__(self, task_termination_id, termination_eta):
        self.task_termination_id = task_termination_id
        self.termination_eta = termination_eta

    def response(self):
        return {"result": "Task Completed!"}
    

@celery.task
def terminate_instance():
    time.sleep(100)
    return {"result": "Task completed!"}


@celery.task
def start_instance():
    time.sleep(10)
    eta = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=2)
    task = terminate_instance.apply_async(eta=eta)
    return {
        "result": "Task Completed!",
        "termination_id": task.id,
        "termination_eta": eta.timestamp()
    }

@app.route("/start-instance")
def start_instance_api():
    task = start_instance.apply_async()
    return flask.jsonify({
        "instance_state": task.id
    }), 202

@app.route("/instance-state/<task_id>")
def get_instance_state(task_id):
    task = start_instance.AsyncResult(task_id)

    task_state_status_codes = {
        "PENDING": 202,
        "FAILURE": 500,
        "SUCCESS": 200
    }
    status_code = task_state_status_codes.get(task.state, 200)
    task_information = {"state": task.state}
    print(task.result)
    if task.result:
        task_information.update(task.result)

    return flask.jsonify(task_information), status_code
    

@app.route("/stop-instance")
def stop_instance():
    pass