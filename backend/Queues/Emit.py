import pickle
import pika
import json
from Utils.functions import PULL_EXCHANGE, PUSH_EXCHANGE


class ExchangeRpcWorker(object):
    callback_queue = None
    connection = None
    channel = None

    def __init__(self):
        self.connect()
        self.declare_queues()

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        self.channel = self.connection.channel()

    def declare_queues(self):
        self.callback_queue = self.channel.queue_declare(exclusive=True)
        self.channel.queue_bind(
            exchange=PULL_EXCHANGE,
            queue=self.callback_queue.method.queue
        )

    def publish(self):
        body_msg = self.serialize_body_msg()
        self.channel.basic_publish(
            exchange=PUSH_EXCHANGE,
            routing_key='',
            body=body_msg,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue.method.queue,
                correlation_id=self.callback_queue.method.queue,
            ),
        )
        self.log_publish()

    def wait_responses(self):
        try:
            self.channel.basic_consume(self.on_emit_callback, queue=self.callback_queue.method.queue)
            self.channel.start_consuming()
            self.connection.close()
        except KeyboardInterrupt:
            self.channel.queue_unbind(
                exchange=PULL_EXCHANGE,
                queue=self.callback_queue.method.queue
            )
            print "...Exiting..."

    def on_emit_callback(self, ch, method, properties, body):
        if properties.correlation_id == self.callback_queue.method.queue:
            self.log_callback(body)
            self.set_results_in_instance(body)
            self.check_stop_condition()

    def stop_consuming(self):
        self.channel.stop_consuming()

    #Child decides whether to stop.
    def check_stop_condition(self):
        raise NotImplementedError

    #Child decides what to do with coming data.
    def set_results_in_instance(self, body):
        raise NotImplementedError

    #Childs define how to serialize going data
    def serialize_body_msg(self):
        raise NotImplementedError

    #Childs define how to unserialize coming data
    def unserialize_body_msg(self, body):
        raise NotImplementedError

    def log_publish(self):
        raise NotImplementedError

    def log_callback(self, body):
        raise NotImplementedError
