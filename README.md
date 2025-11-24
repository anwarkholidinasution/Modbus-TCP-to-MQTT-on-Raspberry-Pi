# Modbus-TCP-to-MQTT-on-Raspberry-Pi

# Project Overview
This project transforms a Raspberry Pi into an edge computing device and gateway. The Raspberry Pi connects to field devices via Modbus TCP/IP as a master, polling data from sensors and transmitters. It also connects northbound through a wireless connection to send data to a website monitoring system using MQTT (Message Queuing Telemetry Transport). All applications run within Docker containers for better isolation and deployment.
