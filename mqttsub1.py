import logging
import random

import paho.mqtt.client as mqtt
from bricknil import attach, start
from bricknil.hub import PoweredUpHub
from bricknil.sensor import TrainMotor
from curio import UniversalQueue, sleep, spawn

broker = 'broker.mqttdashboard.com'
port = 1883
topic = "/simons/train"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

def on_message(client, userdata, message):
    #print("message received " ,str(message.payload.decode("utf-8")))
    q.put(str(message.payload.decode("utf-8")))

async def start_MQTT():
    client = mqtt.Client(client_id)
    client.on_message=on_message
    client.connect(broker, port)
    client.subscribe(topic)
    client.loop_start()

q = UniversalQueue()

@attach(TrainMotor, name='motor')
class Train(PoweredUpHub):
    currentSpeed = 0

    async def run(self):
        self.message_info("Now up and Running")
        m = await spawn(start_MQTT)
        self.message_info("Started MQTT")
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

    async def start_train(self):
        self.message_info('Starting')
        if self.currentSpeed < 80:
            self.currentSpeed += 10
        await self.motor.ramp_speed(self.currentSpeed, 2000)

    async def faster_train(self):
        self.message_info('Increasing speed')
        if self.currentSpeed < 80:
            self.currentSpeed += 10
        await self.motor.ramp_speed(self.currentSpeed, 2000)

    async def slower_train(self):
        self.message_info('Decreasing speed')
        if self.currentSpeed > -80:
            self.currentSpeed -= 10
        await self.motor.ramp_speed(self.currentSpeed, 2000)

    async def stop_train(self):
        self.message_info('Coming to a stop')
        await self.motor.ramp_speed(0, 5000)
        await sleep(1)

async def system():
    Train('My train')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start(system)

