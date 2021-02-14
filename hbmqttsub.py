import asyncio
import logging
import random

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1

client_id = f'python-mqtt-{random.randint(0, 1000)}'

async def uptime_coro():
    C = MQTTClient(client_id)
    await C.connect('mqtt://broker.mqttdashboard.com/')
    await C.subscribe([('/simons/train', QOS_1)])
    try:
        for i in range(1, 1000):
            message = await C.deliver_message()
            packet = message.publish_packet
            print(f"{i}:  {packet.variable_header.topic_name} => {packet.payload.data}")

        await C.unsubscribe(['/simons/train'])
        await C.disconnect()
    except ClientException as ce:
        logging.error("Client exception: %s" % ce)


if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(uptime_coro())

