# RPI0

My plan is to build a car / truck that I can steer with Xbox controller.

Rpi0 will handle all of the logic and arduino is here for better PWM, ADC inputs (monitoring battery voltage), faster GPIO handling.

Arduino - blinkers, lights, servo (aka steering wheel) and stepper control, gearbox (in a distant future...), checking voltage on a battery pack, gathering data from LIDAR (ultrasonic for now tho).
RPI Zero (maybe something more powerful later) - gathering all data from sensors on arduino through serial, getting steering from controller, processing all of that data and based on that sending commands to arduino.

Body of that truck will be 3D printed as well as all the other parts (ofc excluding engine, servo etc).
Later on I plan to stream video through wifi so I can see where am I going :D
