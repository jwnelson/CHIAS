# CHIAS
Control Hardware Interfacing Arduino System
Authors: Pete Marshall and Jack Nelson

CHIAS is a dynamic robotic control system that interfaces between an on-board processor and control hardware such as 
steering servos and motor controllers on a heavily-modified RC car. CHIAS allows control over the RC vehicle to be
switched between a human operator so that the car behaves much like a normal RC vehicle, and the on-board processor,
allowing it to run its own control code.

The entire system consists of an Arduino (the Control Hardware Interfacing Arduino, or CHIA), the RC car and its 
assorted steering servos and motors, and an on-board processor connected to the CHIA over a serial line. 

The "Waldo" software are python scripts that run on the on-board processor. "waldo_record.py" records driving data
from the CHIA while the CHIAS is in manual mode, such as when an operator is driving the car like a typical RC car.
"waldo_playback" is an initial attempt at having the car retrace its steps from a previously-recorded driving file.
This method of playback is largely flawed, as it simply just reads data from a recorded file to the CHIA to run. It
does, however, represent the basic idea of the interface between the CPU and the CHIA, in that the CHIA is simply a
"dumb" component of the system and does whatever the CPU tells it to do. Thus, CHIAS gives a robotics project a
simple and adaptable Arduino-based interface for controlling various vehicles, leaving the the navigation and
decision-making work up to the CPU.
