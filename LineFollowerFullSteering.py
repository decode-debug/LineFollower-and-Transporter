#!/usr/bin/env python3
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B
from ev3dev2.motor import MediumMotor, OUTPUT_C
from ev3dev2.motor import ServoMotor, MotorSet
from ev3dev2.motor import SpeedPercent
from simple_pid import PIDController
# Initialize the color sensor
left_color_sensor = ColorSensor(INPUT_1) # Connect to port 1 (1st port from the left)
right_color_sensor = ColorSensor(INPUT_2) # Connect to port 2 (2st port from the left)

# Initialize the motors
left_motor = LargeMotor(OUTPUT_A)  # Connect to port A (left motor)
right_motor = LargeMotor(OUTPUT_B) # Connect to port B (right motor)
steermotor = MediumMotor(OUTPUT_C) # Connect to port C (steering motor)
group = MotorSet((OUTPUT_A, OUTPUT_B))
robotsteering = ServoMotor(OUTPUT_C)

# Steering parameters
BASE = 40              # Base speed
KP   = 1.2             # Amplification of the proportional term
KI   = 0.5             # Amplification of the integral term
KD   = 0.3             # Amplification of the derivative term
SpeedCLAMP = 100       # speed clamp
ArcClamp = 90          # Arc clamp
DT = 0.02              # sampling time (50Hz)
robotsteering.reset()  # Reset the steering motor to 0 position

def set_speed_percent(group, speed=0):
    """
    Set speed for a motor or motor set in percents of max speed.
    :param group: Motor or MotorSet instance
    :param speed: Speed in percents (-100..100)
    """
    # ucinamy do zakresu
    s = max(-100, min(100, int(speed)))

    if s == 0:
        # Stop and brake
        for m in group.motors:
            m.off(brake=True)
        return

    sp = SpeedPercent(s)
    for m in group.motors:
        m.on(sp)

def turn_degrees(steermotor, LightDifference):
    """
    Turn the steering motor to a specific angle in degrees.
    :param steermotor: ServoMotor instance
    :param degrees: Angle in degrees (-90..90)
    """
    pid = PIDController(kp=KP, ki=KI, kd=KD, dt=DT, integral_limit=ArcClamp, use_angle=True)

    d = pid.compute(0, LightDifference)  # error = 0 - LightDifference

    steermotor.on_to_position(SpeedPercent(20), d, brake=False, block=False)



# Start the line following loop
try:
    while True:
        Leftlight = left_color_sensor.reflected_light_intensity
        RightLight = right_color_sensor.reflected_light_intensity

        LightDifference = Leftlight - RightLight

        if abs(LightDifference) < 5:
            # To do: make it steer with derivative and integral component
            set_speed_percent(group, 50)  # Move forward at 50% speed
            robotsteering.turn_degrees(0)  # No steering
        else:
            set_speed_percent(group, 30)  # Move forward at 30% speed
            robotsteering.turn_degrees(LightDifference)  # Turn left or right based on light difference

except KeyboardInterrupt:
    print("Line following stopped by user.")


group.stop() # Ensure the robot is stopped at the start
steermotor.stop() # Ensure the steering motor is stopped at the start