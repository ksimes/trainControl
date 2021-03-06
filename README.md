## Starting with a SD card with clean version of Raspberian installed 
So, the first thing you need to do is to make sure that everything is up to date on the Raspberry Pi. 
I can’t underline that enough because you’ll run into weird errors if you don’t. 
Just in case, you can copy and paste the code below to make sure.

`sudo apt update -y && sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt dist-upgrade -y && sudo apt-get autoremove -y && sudo apt-get clean -y && sudo apt-get autoclean -y`

When that is done, finish off with a:

`sudo reboot .`

Now that everything is up to date, let’s add the packages we’ll need for Bluetooth.

`sudo apt-get install bluetooth bluez blueman pi-bluetooth python-dev libbluetooth-dev python3-pip -y && sudo pip3 install pybluez adafruit-ampy`

After that, we’ll have to edit the bluez.service file:

`sudo vim /etc/systemd/system/dbus-org.bluez.service`

In that file, there is a line that looks like this:

`ExecStart=/usr/lib/bluetooth/bluetoothd`

We’ll need to add a -C to that line and then add another right below, so it ends up looking like this:

`ExecStart=/usr/lib/bluetooth/bluetoothd -C
ExecStartPost=/usr/bin/sdptool add SP`

As in the last step, when everything is set up, finish off with another

`sudo reboot .`

So, why use Adafruit? Well, we want to use Bluetooth to comunicate with a Lego Hub. 
Not your average connection, I know, but seeing as we may have thousands of students playing around with these 
in the near future using Python, it would be good to get the ball rolling with a reliable library. 
We’ll need adafruit to communicate with the Hub smoothly.

After the second reboot, (the reboots are important and shouldn’t be omitted) we can now get everything configured.
First, let’s get Bluetooth up and running. We’ll start with:

`sudo service bluetooth start`

After that we’ll enter into the bluetoothctl shell with:

`sudo bluetoothctl`

Once in, we will run the following commands, one after another, hitting RETURN after each one.

`power on`

`pairable on`

`discoverable on`

`agent on`

`default-agent`

`quit`

Ok, so now we can finally use our newly configured Bluetooth to set something up! 

**Note:** We can skip this section and go straight on to setting up and configuring the LEGO train 

First, let’s run:

`bluetoothctl scan on`

To find nearby bluetooth devices. We need the MAC address of the device we want. In my case, it came out this way (the MAC below is just an example):

`[CHG] Device 40:HR:32:46:GH:00 Name LEGO: Hub@4`

Now, let’s pair and trust it, hitting RETURN after each line below.

`bluetoothctl pair 40:HR:32:46:GH:00`

`bluetoothctl trust 40:HR:32:46:GH:00`

Up to this point, we have finished the steps you would follow for any bluetooth device you’d want to connect with. 
The following will now be applied more specifically to the Lego Train, but will be similar to any type of device that requires specific command to be sent to it.

We have a few ways to work with the Train. The first way I never use, but I’ll mention it just to be thorough.

`sudo rfcomm connect hci0 40:HR:32:46:GH:00`

With that, the Hub will turn purple, confirming you are connected. To escape that, we just type ctrl + c .

### To install the BrickNil library and setup the train

BrickNil library details at https://github.com/virantha/bricknil (if the readme doesn't scan well then check https://virantha.github.io/bricknil/readme.html).
To install the BrickNil library:

`pip3 install bricknil`

which will install all the requirements to control the LEGO train hub, motors, lights and more. This library will allow us to run Python3 programs to
play with a **60197**,**60198** and a **76112** LEGO Train kit as well as the **10874** and **10875** Duplo train kits.

See https://virantha.github.io/bricknil/readme.html for more details.

Next we need the MQTT broker connection software and we can install that with:

`pip3 install paho-mqtt`

This will alow us to send messages via Python to and from the Raspberry Pi.

Copy the two files:

`mqttsub.py`

`mqttpub.py`

from the RaspPi folder to a suitable folder under your Pi home folder on the Pi.

Ignore the mqttPublish.py file for now as that is for future development. 

That's all you need to do on the Raspberry Pi.

The Angular part of the code is standard Angular version 8 and has it's own README.md in the frontEnd folder.

The PHP is in the Backend and needs to be deployed on a website preferable in the same folder (Usually HTDOCS) as the angular application.
The name of the website is hardcoded into the angular application as "simonking.website". Not through any self publicity,
but because I happened to have that hostname lying around when developing this application and it was easy to setup
a website connected to that hostname. Just change it to your website name.

Once everything is setup, your LEGO/Duplo train is ready to go on the tracks, the Rasp Pi is running and the command
`python3 mqttsub.py`
has been run and is sync'd with the train (you will need to press the button on not of the Lego controller uint and wait
until the flashing stops, the LED becomes steady and then turns blue which indicates that it connected to
the mqttsub program) and you have your website deployed and can hit the angular front end. Then just
hit the button and see if the train starts going. 

Any problems email me at simon.king at stronans.com (replacing the at with the usual symbol)
