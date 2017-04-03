import logging
import json
from uuid import uuid4
import os

from celery import Celery
from flask import Flask, jsonify, request, current_app
from marshmallow import fields, Schema
from marshmallow.validate import Range, Length


class DataSchema(Schema):
    uuid = fields.UUID(required=True)
    name = fields.String(required=True, validate=Length(max=255))
    x = fields.Float(required=True)
    y = fields.Float(required=True)
    id = fields.Integer(required=True)
    fake_name = fields.String(allow_none=True, validate=Length(max=128))
    fake_uuid = fields.UUID(required=True)


def init_logging(app):
    """
    Add a Streamhandler to the Flask default logger
    """
    sh = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] - [%(asctime)s] - server - %(message)s')
    sh.setFormatter(formatter)
    app.logger.addHandler(sh)
    app.logger.setLevel(logging.INFO)

def init_celery(app):
    broker = os.environ.get('BROKER_URL', 'localhost')
    celery = Celery(app.import_name, broker='amqp://rabbit:rabbit@{}//'.format(broker))
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

    return celery


app = Flask(__name__)
init_logging(app)
celery = init_celery(app)


@celery.task
def process_data(data):
    current_app.logger.info("[x] Processed {0}".format(data))


@app.route('/')
def status(uuid):
    return jsonify(status='purple bro')


@app.route('/<uuid:uuid>')
def serve(uuid):
    return jsonify(uuid=uuid, data={'data_uuid': str(uuid4())})


@app.route('/<uuid:uuid>/noise', methods=['POST'])
def noise(uuid):
    data = DataSchema(many=True).load(request.get_json(force=True))
    assert not data.errors
    process_data.delay(data.data)
    app.logger.info('Noise made {}'.format(str(uuid)))
    return jsonify(uuid=uuid, status='processing'), 204
