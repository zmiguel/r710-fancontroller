# R710 Fan controller

This python script checks the CPU temperatures (Using LM-Sensors).

It check this to predefined temperture values and sends an IPMI command to the controller (ip, username, password required.)

It's recommended to install this script via systemd, see the `.service` file provided. You can install it as follows:

```
# Place the file in the systemd directory
nano /etc/systemd/system/fan-controller.service

# Make executable
chmod 644 fan-controller.service

# Reload systemd, enable the service and start it.
systemctl daemon-reload
systemctl enable fan-controller.service
systemctl start fan-controller.service

# Check to see if it's running
service fan-controller status
```

This allows the script to be enabled at boot.

This script is provided as is. I am not responsible for any damage done to your server. See the license for more information.

By Marcusvb on Gitlab or Github, and modified by ZMiguel.
