import json
import pickle
import pika
import time
from Utils.functions import PUSH_EXCHANGE, PULL_EXCHANGE


class ExchangeRpcReceiver(object):
    connection = None
    channel = None
    queue = None

    def __init__(self):
        self.cross = None
        self.services = None
        self.reply_to = None
        self.correlation_id = None
        self.json_obj = None

        self.connect()
        self.declare_exchanges()
        self.declare_queue()
        self.wait_message()

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        self.channel = self.connection.channel()

    def declare_exchanges(self):
        self.channel.exchange_declare(
            exchange=PUSH_EXCHANGE,
            type='fanout')
        self.channel.exchange_declare(
            exchange=PULL_EXCHANGE,
            type='fanout')

    def declare_queue(self):
        self.queue = self.channel.queue_declare(queue=self.__class__.__name__, exclusive=True)
        self.channel.queue_bind(exchange=PUSH_EXCHANGE,
                                queue=self.queue.method.queue)

        print " [*] Waiting for logs @%s" % (self.queue.method.queue,)

    def wait_message(self):
        try:
            self.channel.basic_consume(
                self.on_message_received,
                queue=self.queue.method.queue,
                no_ack=True)

            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.queue_unbind(
                exchange=PUSH_EXCHANGE,
                queue=self.queue.method.queue
            )
            print "...Exiting..."

    def on_message_received(self, ch, method, properties, body):
        try:
            self.reset_values()
            self.unserialize_message(body)
            self.set_reply_values(properties)
            self.init_task()
            self.publish_back()
        except:
            print "Opsy!"

    def publish_back(self):
        print "[*] Receiver %s" % (self.queue.method.queue,)
        print "\t [x] Received %s" % (self.json_obj['msg'],)
        print "\t [x] Publishing back to: %s\n" % (self.reply_to, )

        self.channel.basic_publish(
            exchange='',
            routing_key=self.reply_to,
            properties=pika.BasicProperties(
                correlation_id=self.correlation_id
            ),
            body=self.serialize_message()
        )

    def init_task(self):
        raise NotImplementedError

    def stop_consuming(self):
        self.channel.stop_consuming()

    def unserialize_message(self, body):
        self.json_obj = json.loads(body)
        self.cross = pickle.loads(self.json_obj['cross'])
        self.services = pickle.loads(self.json_obj['services'])

    def serialize_message(self):
        json_cross = pickle.dumps(self.cross)
        json_services = pickle.dumps(self.services)
        response = {
            "reply_queue": self.queue.method.queue,
            "msg": "It's " + str(int(round(time.time() * 1000))),
            "cross": json_cross,
            "services": json_services
        }
        return json.dumps(response)

    def set_reply_values(self, properties):
        self.reply_to = properties.reply_to
        self.correlation_id = properties.correlation_id

    def reset_values(self):
        self.cross = None
        self.services = None
        self.reply_to = None
        self.correlation_id = None
        self.json_obj = None
