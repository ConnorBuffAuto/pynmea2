#!/usr/bin/env python3
# Author: Connor Parish (connor@buffautomation.com)
import pynmea2
import fileinput
import numpy as np
import datetime
import matplotlib.pyplot as plt

knowns = set()
unknowns = set()
rsa_msgs = []
htd_msgs = []

for l in fileinput.input():
	try:
		loc = l.find('$')
		nmea = l[loc:len(l)]
		msg =  pynmea2.parse(nmea)
		if isinstance(msg, pynmea2.types.talker.RSA):
			rsa_msgs.append(msg)
		elif isinstance(msg, pynmea2.types.talker.HTD):
			htd_msgs.append(msg)

		code = nmea.split(',')[0]
		if(len(code) > 1):
			knowns.add(code)
	except Exception as e:
		print(l)
		print(e)
		nmea = l[l.find('$'):len(l)]
		code = nmea.split(',')[0]
		if(len(code) > 1):
			unknowns.add(code)

print("Known Codes: ")
for u in knowns:
	print(u)

print("")
print("Unknown Codes: ")
for u in unknowns:
	print(u)

rudder_pos = list()
htd_pos = list()
rads = list()
rots = list()


for msg in rsa_msgs:
	if(msg.rsa_starboard != None):
		rudder_pos.append(msg.rsa_starboard)
	else:
		rudder_pos.append(msg.rsa_port)

for msg in htd_msgs:
	if(msg.rudder_angle != None):
		htd_pos.append(msg.rudder_angle)
	if(msg.rad != None):
		rads.append(msg.rad)
	if(msg.rot != None):
		rots.append(msg.rot)


def print_fields(messages, index):
	if(len(messages) > index):
		for field in messages[index].fields:
			fel = field[1]
			print(field[0] + ": " + str(getattr(messages[index], fel)))
	else:
		print("Index out of range")


print_fields(htd_msgs, 0)

plt.figure(1)
plt.plot(rudder_pos)
plt.figure(2)
plt.plot(htd_pos)
plt.figure(3)
plt.plot(rads)
plt.figure(4)
plt.plot(rots)
plt.show()


"""
RSA
1) Starboard (or single) rudder sensor, "-" means Turn To Port
2) Status, A means data is valid
3) Port rudder sensor
4) Status, A means data is valid
5) Checksum
"""

"""
XDR
Trasducer
"""

"""
ALR
Alarm
$SGALR,time (empty),alarm id,A:threshold exceeded V:threshold not exceeded,A:acknowledged V:unacknowledged,alarm description
"""

"""
HTD
Autopilot status in AutoNav mode
"""
