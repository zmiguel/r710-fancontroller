"""
Python implementation of a fan controller based on HDD
and CPU temperature. This is a first draft implementation
so do not expect the most clean code. It's a simple "it works"
version.

Created by @marcusvb (GitLab & GitHub)
Edited by @ZMiguel (Everywhere)

"""
from subprocess import Popen, PIPE, STDOUT
import time
import binascii

max_cpu_temp = 80 # 100% fan
min_cpu_temp = 40 # 10% fan

sleep_time = 5
user = "root"
password = "calvin"
ip = "192.168.x.xx"

#Do a command and return the stdout of proccess
def sendcommand(cmdIn):
    p = Popen(cmdIn, shell=True, executable="/bin/bash", stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    return p.stdout.read()

#Do a ipmi command, setup for the default command.
def ipmicmd(cmdIn):
    return sendcommand("ipmitool -I lanplus -H " + ip +" -U " + user + " -P " + password + " " + cmdIn)

#Gets the CPU temperture from lm-sensors, returns the average of it.
def getcputemp():
    cmd = sendcommand('sensors -u | grep "input" | cut -d ":" -f2 | cut -d "." -f1').decode("utf-8").replace(" ","")
    templist = cmd.split("\n")
    templist.pop()
    cputemperatures = list()
    for i in templist:
        temp = int(i)
        cputemperatures.append(int(temp))

    #return the average cpu temperature
    return sum(cputemperatures) / int(len(cputemperatures))

#Main checking function which checks temperatures to the default set above.
def checktemps(last_temp: int):
    avg_cpu_temp = int(round(getcputemp()))
    print("Average CPU temp is: {}C".format(avg_cpu_temp))

    if last_temp != avg_cpu_temp:
        if (avg_cpu_temp < 40):
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x0f")
            print("Setting to 10%, Server is cool")
        elif (avg_cpu_temp >= 40 and avg_cpu_temp <=85):
            fan_speed = int(round(10 + (avg_cpu_temp - min_cpu_temp) * 2))
            fan_speed_bytes = '{:x}'.format(int(fan_speed))

            ipmi_cmd = "raw 0x30 0x30 0x02 0xff 0x{}".format(fan_speed_bytes)
            ipmicmd(ipmi_cmd)

            print("Settings fan to {}% or 0x{}".format(fan_speed, fan_speed_bytes))
        else:
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x64")
            print("Settings fan to 100%, Server is very hot")
    else:
        print("No Temperaure change...")

    return avg_cpu_temp

#Main running function.
def main():
    # set fans to manual control
    ipmicmd("raw 0x30 0x30 0x01 0x00")
    last_cpu_temp = 80
    while True:
        time.sleep(sleep_time)
        last_cpu_temp = checktemps(last_cpu_temp)
        print("Sleeping for " + str(sleep_time))
if __name__ == '__main__':
    main()
