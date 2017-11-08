# Motion detection Telegram integrated
I needed a surveillance system for my new house but I didn’t want to buy something already assembled for three main reasons:
1. They are incredibly **expensive**. For my project, I used things that I already had, but anyway still below $35.00
2. They are deeply **insecure**: any IoT gadget can be hacked in a second and often they expose themselves over the Internet. Thanks to the Telegram bot system, my project is (almost) confined to the local network and has no open services (other than ssh).
3. It’s **fun**.

For this little home project I used:
- Onion Omega2+ ($9.00)
- Expansions header for Omega2+ ($15.00)
-  USB OTG UVC endoscope camera module with leds ($11.00)

The project is composed of 3 scripts:
- [Motion][1]: the software that monitors the webcam and takes pictures  when motion is detected. 
- `motion.py`: the script triggered by the Motion’s parameter `on_motion_detected ` , that sends the last picture taken via Telegram to my self.
- `engine.py`: the core of my script. This is the Telegram bot engine which controls the whole project.

Since I’m working on Omega2+, my working directory is `/root/motion`, so you should change all paths if you’re using a different *cwd*. In both `motion.py` and `engine.py`, **bot token** and **chat id** must be replaced with your values. I’ve chosen to hard code the chat id for security reasons.

The main script is running as daemon (you have to kill it manually when needed) and handles a Telegram bot with the following commands:

- `/snap` - *Take a snapshot and send it*: uses `fswebcam` to take a picture and immediately send it to the Telegram chat.
- `/startmotion` - *Start motion surveillance*: start the Motion software with the personalised configuration file
- `/stopmotion` - *Stop motion surveillance*: stop the Motion software with `proc.kill()`
- `/checkmotion `- *Check if motion surveillance is on*: check from `ps` if the Motion software is running
- `/sendlast` - *Send last picture taken by motion surveillance*: pictures are taken during the motion detection, the last one saved in the /pics folder is sent via Telegram
- `/cleanpics` - *Delete all pictures taken by motion surveillance*: this delete all the `.jpg` files in the pics directory.  

[1]:	https://github.com/Motion-Project/motion "Motion"