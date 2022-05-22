# libhousy
An easy way to interact with robot Actuators and Sensors

## Actuators
Actuators are anything that moves on the robot, including all motors and pneumatic (air) pistons. 
### Motors
Motors like the drivetrain (wheels) can be `Set` to any value between -1 and 1 where -1 is full reverse, 0 is stopped, and 1 is forward. 

### Pistons
Pistons are useful for linear motion (like the pickup arm) but can only be fully extended or retracted. To move a piston call its associated `Extend()` or `Retract()` function.

### Examples
To set the left drivetrain to half speed ahead, I would call `robot.lDrive.Set(0.5)`

To extend the pickup arm, I would call `robot.pickupPneumatic.Extend()`

## Sensors
The robot has a lot of ways to tell what's going on around and inside of it.

### Encoders
These are magnetic sensors that can tell how many times an axel has rotated. With some math we can use these to figure out how far the robot has driven and get an idea of where we are, what angle the shooter is at, or even how fast something is spinning.

To read how many times a shaft has rotated, call the corresponding Encoder's `Get()` function. If you want to reset this count to 0 (so you can figure out how far you will have gone from where you are now), call its `Reset()` function.

### Color Sensor
The color sensor can tell the color of whatever it's pointed at as well as how far away it is. 

To get the color, call `robot.colorSensor.getColor()` This returns a list of 3 numbers ranging from 0 - 255 which represent the intensity of red, green, and blue color in the target.

To get the proximity, call `robot.colorSensor.getProximity()` which returns a a number ranging from 0 to 2047 with 2047 being the closest possible value and 0 being the furthest away / out of range.

### IMU
The robot is also equipt with an inertial measurement unit which can tell the orientation and acceleration of the robot.
#### Orientation
Orientation is given by the following calls: `robot.getYaw()`, `robot.getRoll()`, and `robot.getPitch()`
#### Acceleration
Acceleraton in Gs (acceleration due to earth's gravity is 1G ≈ 9.8 m/s/s) is given by `robot.getAcceleration([string])` where `[string]` is the axis you want to read (can be "x", "y", or "z") 