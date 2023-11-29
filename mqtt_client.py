import asyncio

from gmqtt import Client as MQTTClient
from datetime import datetime

import hashlib
import struct


class CollectorMQTTClient:
    def __init__(self, broker_host, username, password, client_id=None) -> None:
        cid = hashlib.md5(datetime.utcnow().isoformat().encode()).hexdigest()
        client_id = client_id or cid

        self.client = MQTTClient(client_id)
        self.broker_host = broker_host

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe

        self.client.set_auth_credentials(username, password)
        self.topics = set()
        self.queue_data = asyncio.Queue()

    def add_topic(self, topic):
        self.topics.add(topic)

    def remove_topic(self, topic):
        self.topics.remove(topic)

    def on_connect(self, client, flags, rc, properties):
        for topic in self.topics:
            self.client.subscribe(topic)

    def on_message(self, client, topic, payload, qos, properties):
        self.queue_data.put_nowait(payload)

    def on_disconnect(self, client, packet, exc=None):
        print('Disconnected')

    def on_subscribe(self, client, mid, qos, properties):
        print('SUBSCRIBED')

    async def main(self):
        await self.client.connect(self.broker_host)
