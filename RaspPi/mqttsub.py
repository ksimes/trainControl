import logging
import random

import paho.mqtt.client as mqtt
from bricknil import attach, start
from bricknil.const import Color
from bricknil.hub import PoweredUpHub
from bricknil.sensor import TrainMotor, LED
from curio import UniversalQueue, sleep, spawn

broker = 'broker.mqttdashboard.com'
port = 1883
topic = "/simons/train"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
client: mqtt = None
# username = 'test'
# password = 'public'


def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    q.put(str(msg.payload.decode()))


async def startMqtt():
    global client
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()


async def endMqtt():
    global client
    client.disconnect()
    client.loop_stop()


q = UniversalQueue()


# @attach(Button, name='train_btn', capabilities=['sense_press'])
@attach(LED, name='train_led')
@attach(TrainMotor, name='motor')
class Train(PoweredUpHub):
    currentSpeed = 0

    async def run(self):
        m = await spawn(startMqtt)
        self.message_info("Now up and Running")
        await self.train_led.set_color(Color.blue)
        while True:
            item = await q.get()
            self.message_info(f"have queue item `{item}`")
            if item is not None:
                if item == "start":
                    await self.start_train()
                if item == "stop":
                    await self.stop_train()
                if item == "faster":
                    await self.faster_train()
                if item == "slower":
                    await self.slower_train()
                if item == "quit":
                    await self.quit_all()

    async def start_train(self):
        self.message_info('Starting')
        self.currentSpeed = 20
        await self.train_led.set_color(Color.green)
        await self.motor.ramp_speed(self.currentSpeed, 1000)

    async def faster_train(self):
        self.message_info('Increasing speed')
        if self.currentSpeed < 80:
            self.currentSpeed += 10
        await self.motor.ramp_speed(self.currentSpeed, 1000)

    async def slower_train(self):
        self.message_info('Decreasing speed')
        if self.currentSpeed > -80:
            self.currentSpeed -= 10
        await self.motor.ramp_speed(self.currentSpeed, 1000)

    async def stop_train(self):
        self.message_info('Coming to a stop')
        await self.motor.ramp_speed(0, 2000)
        await self.train_led.set_color(Color.blue)
        self.currentSpeed = 0
        await sleep(1)

    async def quit_all(self):
        self.message_info('quitting out')
        await self.motor.ramp_speed(0, 500)
        await endMqtt()
        await self.train_led.set_color(Color.orange)
        quit()


def connect_mqtt() -> mqtt:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    print(f"subscribed to topic `{topic}` waiting on messages")
    client.connect(broker, port)
    return client


def subscribe(client: mqtt):
    client.subscribe(topic)
    client.on_message = on_message


async def system():
    Train('My train')

if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    start(system)
