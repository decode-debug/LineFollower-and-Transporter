# Line Follower (EV3, Python, ev3dev2)

Easy and scalable set of scripts to drive LEGO Mindstorm EV3 robot booted from Ubuntu using Python + ev3dev2.
The repository includes multiple variants of increasing complexity, from drive left, right, or forward to full steering axis control with a PID-based turning angle and speed.

---

## 🚗 Robot Program Variants

### `linefollower.py`

A line-following program. This script uses a differential drive (tank drive) configuration.

Motors: 2 × Large Motors (Ports A & B) used for propulsion and steering.

Sensors: 2 × Color Sensors (Ports 1 & 2) for line detection.

Algorithm: Implements a PID controller for line following. The robot calculates an error (error = R - L) based on the difference in reflected light intensity from both sensors. This correction is then used to dynamically adjust the speeds of the left and right motors, steering the robot to stay on the line's edge.

---

### `transporter.py`

An advanced version of the line-following robot, which can also react to colored markers and operate a gripper. It uses a Finite State Machine (FSM) to manage its behavior.

Motors: 2 × Large Motors (Ports A & B) for propulsion (tank drive) and 1 × Medium Motor (Port C) as a gripper (optional).

Sensors: 2 × Color Sensors (Ports 1 & 2) for line and color detection.

#### Algorithm:

Line Following: Uses a P (Proportional) controller to follow the black line.

State Machine (FSM): The robot operates in one of several states:

FOLLOW_BLACK: Follows the black line while searching for colors (e.g., red, green).

ROTATING: After detecting a new color with one sensor, it rotates to align both sensors on that color.

FOLLOW_COLOR: Follows a colored line (e.g., red).

ACTION: When both sensors detect a colored marker, the robot stops to perform a gripper action.

###### Gripper Action:

If the gripper is open (grip_state == "open"), the robot closes the gripper (grabs an object), turns 180 degrees, and continues driving.

If the gripper is closed (grip_state == "closed"), the robot opens the gripper (drops the object), reverses, turns 180 degrees, and continues driving.

---

## 🧱 Hardware Requirements

- LEGO Mindstorms EV3 running ev3dev (Python 3)
- 2 × Large motors (drive) — **ports A & B**
- 1 × Medium motor (steering) — **port C** *(only for Transporter)*
- 2 × Color sensors — **INPUT_1** (left), **INPUT_2** (right)

---

## ⚙️ Default Wiring

| Component          | Port       |
|--------------------|------------|
| Left drive motor   | OUTPUT_A   |
| Right drive motor  | OUTPUT_B   |
| Steering motor     | OUTPUT_C   |
| Left color sensor  | INPUT_1    |
| Right color sensor | INPUT_2    |

---

## 💾 Installation (on brick or Linux-based PC)

1. **Flash ev3dev** onto your EV3 brick.  
   - Download the latest image from [ev3dev.org](https://www.ev3dev.org/).  
   - Flash it to a microSD card and boot your EV3 from it.  
   - Connect to the brick via SSH or Visual Studio Code with the *ev3dev-browser* extension.

2. **Install Python and dependencies** (usually preinstalled):
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   pip3 install --user python-ev3dev2