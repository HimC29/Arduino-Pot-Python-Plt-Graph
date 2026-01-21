# Checks potentiometer readings

import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

def choosePort():
    ports = serial.tools.list_ports.comports()
    portList = []

    print("Available ports:")
    for i, port in enumerate(ports):
        print(f"{i}: {port.device}")
        portList.append(port.device)

    choice = int(input("Select port number: "))
    portVar = portList[choice]

    return serial.Serial(
        port=portVar,
        baudrate=9600,
        timeout=1
    )

def readSerial(port):
    line = port.readline().decode("utf-8", errors="ignore").strip()
    return line

plt.ion()

fig, ax = plt.subplots()
xData = deque(maxlen=300)
yData = deque(maxlen=300)
xData.append(0)
yData.append(0)

line, = ax.plot(xData, yData)

ax.set_title("Potentiometer Readings")
ax.set_xlabel("Reading")
ax.set_ylabel("Time")

def main():
    port = choosePort()
    print("Reading serial...\n")
    while(True):
        if(port.in_waiting > 0):
            try:
                serialOutput = int(readSerial(port))
            except ValueError:
                continue
            print(serialOutput)

            xData.append(xData[-1] + 1)
            yData.append(serialOutput)

            line.set_xdata(xData)
            line.set_ydata(yData)

            ax.relim()
            ax.autoscale_view()
            plt.pause(0.01)

if(__name__ == "__main__"): main()
