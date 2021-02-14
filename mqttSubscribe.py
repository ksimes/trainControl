import logging
import random

from bricknil import attach, start
from bricknil.hub import PoweredUpHub
from bricknil.sensor import TrainMotor
from curio import sleep
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1

# from paho.mqtt import client as mqtt_client

# broker = 'broker.emqx.io'
broker = 'broker.mqttdashboard.com'
port = 1883
topic = "/simons/train"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'test'
# password = 'public'


@attach(TrainMotor, name='motor')
class Train(PoweredUpHub):
    currentSpeed = 0

    async def run(self):
        self.message_info("Running")
        while True:
            # n = input("Please enter 'finish':")
            # if n.strip() == 'finish':
            #     break
            await sleep(1)


async def connect_mqtt():
    C = MQTTClient(client_id)
    await C.connect('mqtt://' + broker)
    await C.subscribe([(topic, QOS_1)])
    print(f"subscribed to topic `{topic}` waiting on messages")
    return C


async def subscribe(client: MQTTClient, train: Train):
    convertor = {
        'start': start_train,
        'faster': faster_train,
        'slower': slower_train,
        'stop': stop_train,
    }

    try:
        for i in range(1, 1000):
            message = await client.deliver_message()
            packet = message.publish_packet
            print(f"Received `{packet.variable_header.topic_name}` topic => `{packet.payload.data}`")
            func = convertor.get(packet.payload.decode(), lambda: "Invalid command")
            await func(train)

    except ClientException as ce:
        logging.error("Client exception: %s" % ce)


async def start_train(train: Train):
    print(f"Starting")
    train.message_info('Starting')
    if train.currentSpeed < 80:
        train.currentSpeed += 10
    await train.motor.ramp_speed(train.currentSpeed, 2000)


async def faster_train(train: Train):
    print(f"Increasing speed")
    train.message_info('Increasing speed')
    if train.currentSpeed < 80:
        train.currentSpeed += 10
    await train.motor.ramp_speed(train.currentSpeed, 2000)


async def slower_train(train: Train):
    print(f"Decreasing speed")
    train.message_info('Decreasing speed')
    if train.currentSpeed > -80:
        train.currentSpeed -= 10
    await train.motor.ramp_speed(train.currentSpeed, 2000)


async def stop_train(train: Train):
    print(f"Coming to a stop")
    train.message_info('Coming to a stop')
    await train.motor.ramp_speed(0, 5000)
    await sleep(1)


async def system():
    client = await connect_mqtt()
    train = Train('My train')
    await subscribe(client, train)
    client.loop_start()


if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    start(system)
