## Starting with a SD card with Raspberian installed 
So, the first thing you need to do is to make sure that everything is up to date. 
I can’t underline that enough because you’ll run into errors if you haven’t. 
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

We’ll need to add a -C to that line and then add another right below so it ends up looking like this:

`ExecStart=/usr/lib/bluetooth/bluetoothd -C
ExecStartPost=/usr/bin/sdptool add SP`

As in the last step, when everything is set up, finish off with another

`sudo reboot .`

So, why Adafruit? Well, we want to use Bluetooth to comunicate with a Lego Hub. 
Not your average connection, I know, but seeing as we may have thousands of students playing around with these 
in the near future using Python, I though it would be good to get the ball rolling. We’ll need adafruit to communicate with the Hub.
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

Ok, so now we can finally use our newly configured Bluetooth to set something up! First, let’s run:

`bluetoothctl scan on`

To find nearby bluetooth devices. We need the MAC address of the device we want. In my case, it came out this way (the MAC below is just an example):

`[CHG] Device 40:HR:32:46:GH:00 Name LEGO: Hub@4`

Now, let’s pair and trust it, hitting RETURN after each line below.

`bluetoothctl pair 40:HR:32:46:GH:00`

`bluetoothctl trust 40:HR:32:46:GH:00`

Up to this point, we have finished the steps you would follow for any bluetooth device you’d want to connect with. 
The following will now be applied more specifically to the Lego Spike Prime, but will be similar to any type of device that requires specific command to be sent to it.

We have a few ways to work with the Spike. The first way I never use, but I’ll mention it just to be thorough.

`sudo rfcomm connect hci0 40:HR:32:46:GH:00`

With that, the Hub will turn purple, confirming you are connected. To escape that, we just type ctrl + c .

Alternatively

`pip3 install bricknil`

which will install all the requirements to talk to the LEGO train hub and control motors. This will allows us to run Python3 programs to
play with 60197 Train kit.

Next we need the MQTT broker connection software and we can install that with:

`pip3 install paho-mqtt`

