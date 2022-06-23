import string
from networktables import NetworkTables
import random
import pygame
import enum

DONE = 2

class motor:
    """abstraction for FRC motor controller / motor controller group"""

    def __init__(self, name: string):
        self.name = name
        self.control = NetworkTables.getTable("control")


    def Set(self, value: int):
        """Sets motor speed in a range from -1 to 1
        where -1 is full reverse, 1 is full forward, and 0 is stopped"""
        if abs(value) > 1:
            raise ValueError("Out of range input supplied!!")
        else:
            self.control.putNumber(self.name, value)


class servo:
    def __init__(self, name: string):
        self.name = name
        self.control = NetworkTables.getTable("control")

    def Set(self, value: int):
        """sets the servo to a specified angle in degrees. Valid inputs are 0-180."""
        if value > 180 or value < 0:
            raise ValueError("Out of range input supplied!!")
        else:
            self.control.putNumber(self.name, value)


class pneumatic:
    """abstraction for FRC Double Solenoid class"""

    def __init__(self, name: string):
        self.name = name
        self.control = NetworkTables.getTable("control")

    def Extend(self):
        """sets pneumatic to kForward"""
        self.control.putNumber(self.name, 1)

    def Retract(self):
        """sets pneumatic to kReverse"""
        self.control.putNumber(self.name, -1)

    def Stop(self):
        """sets pneumatic to kOff"""
        self.control.putNumber(self.name, 0)


class encoder:
    """abstraction for FRC Encoder (and geartooth) class"""

    def __init__(self, name: string, index: int):
        self.name = name
        self.index = index
        self.sensors = NetworkTables.getTable("sensors")
        self.control = NetworkTables.getTable("control")

    def Get(self):
        """returns the number of encoder cycles since last reset"""
        return self.sensors.getNumber(self.name, 0)

    def Reset(self):
        """sets encoder value to 0"""
        self.control.putNumber("encRst", self.index)


class colorSensor:
    """Abstraction for REV color sensor V3"""

    def __init__(self):
        self.sensors = NetworkTables.getTable("sensors")

    def getColor(self):
        """returns an array of RGB color values from 0-255"""
        return self.sensors.getNumberArray("colorSensor", [0, 0, 0])

    def getProximity(self):
        """returns *raw* proximity value ranging from 0 to 2047 with 2047 being
        closest to the sensor and 0 being furthest away / not detected"""
        return self.sensors.getNumber("colorProximity", 0)


class controller:
    def __init__(self):
        pygame.joystick.init()
        self.backend = pygame.joystick.Joystick(0)
        self.backend.init()

    class Button(enum.Enum):
        A = 0
        B = 1
        X = 3
        Y = 4
        lBumper = 6
        rBumper = 7
        menu = 10
        hamburger = 11
        xbox = 12
        lStick = 13
        rStick = 14
        save = 15

    class Axis(enum.Enum):
        lStickX = 0
        lStickY = 1
        lTrigger = 5
        rStickX = 2
        rStickY = 3
        rTrigger = 4

    def getButton(self, button: Button):
        """Returns boolean button status of provided button. Ex: controller.getButton(controller.Button.menu) """
        return self.backend.get_button(button.value)

    def getAxis(self, axis: Axis):
        """returns value of specified axis from -1 to 1"""
        # invert Y axes because they're backward
        if axis.name.count("StickY") == 0:
            direction = 1
        else:
            direction = -1
        return self.backend.get_axis(axis.value) * direction

    def getHat(self):
        return self.backend.get_hat(0)


class SenseHat:
    def __init__(self):
        self.sensors = NetworkTables.getTable("sensors")
        self.control = NetworkTables.getTable("control")
    def set_display(self, val: int):
        self.control.putNumber("shDisplay", val)

    def get_yaw(self):
        """returns the yaw (side to side turn) value from the sense hat's IMU"""
        retn = self.sensors.getNumber("shYaw", 0)
        if retn > 180:
            retn = retn - 360
        return retn

    def get_roll(self):
        """returns the roll (sid to side tilt) value from the sense hat's IMU"""
        return self.sensors.getNumber("shRoll", 0)

    def get_pitch(self):
        """returns the pitch (front to back tilt) value from the sense hat's IMU"""
        return self.sensors.getNumber("shPitch", 0)

    def get_accel(self):
        """returns a tupple of the robot's acceleration in each axis"""
        return self.sensors.getNumberArray("shAccel", [0, 0, 0])


class fmotor:
    """abstraction for FRC motor controller / motor controller group"""

    def __init__(self, name: string):
        self.name = name
        self.value = 0

    def Set(self, value: int):
        """Sets motor speed in a range from -1 to 1
        where -1 is full reverse, 1 is full forward, and 0 is stopped"""
        if abs(value) > 1:
            raise ValueError("Out of range input supplied!!")
        else:
            self.value = value


class fservo:
    def __init__(self, name: string):
        self.name = name
        self.value = 0

    def Set(self, value: int):
        """sets the servo to a specified angle in degrees. Valid inputs are 0-180."""
        if value > 180 or value < 0:
            raise ValueError("Out of range input supplied!!")
        else:
            self.value = value


class fpneumatic:
    """abstraction for FRC Double Solenoid class"""

    def __init__(self, name: string):
        self.name = name
        self.value = 0

    def Extend(self):
        """sets pneumatic to kForward"""
        self.value = 1

    def Retract(self):
        """sets pneumatic to kReverse"""
        self.value = -1

    def Stop(self):
        """sets pneumatic to kOff"""
        self.value = 0


class fencoder:
    """abstraction for FRC Encoder (and geartooth) class"""

    def __init__(self, name: string, index: int):
        self.value = 0

    def Get(self):
        """returns the number of encoder cycles since last reset"""
        return self.value

    def Reset(self):
        """sets encoder value to 0"""
        self.value = 0


class fcolorSensor:
    """Abstraction for REV color sensor V3"""

    def __init__(self):
        self.value = [0, 0, 0]
        self.prox = 0

    def getColor(self):
        """returns an array of RGB color values from 0-255"""
        return self.value

    def getProximity(self):
        """returns *raw* proximity value ranging from 0 to 2047 with 2047 being
        closest to the sensor and 0 being furthest away / not detected"""
        return self.prox


class fSenseHat:
    disp = 0
    roll = 0
    pitch = 0
    yaw = 0
    accel = [0, 0, 0]

    def set_display(self, val: int):
        self.disp = val

    def get_yaw(self):
        """returns the yaw (side to side turn) value from the sense hat's IMU"""
        return self.yaw

    def get_roll(self):
        """returns the roll (sid to side tilt) value from the sense hat's IMU"""
        return self.roll

    def get_pitch(self):
        """returns the pitch (front to back tilt) value from the sense hat's IMU"""
        return self.pitch

    def get_accel(self):
        """returns a tupple of the robot's acceleration in each axis"""
        return self.accel

class fcontroller:
    def __init__(self):
        self.buttons = []
        self.axes = []
        for i in range(0, 16):
            self.buttons.append(False)
        for i in range(0, 6):
            self.axes.append(0.0)
        self.hat = (0, 0)

    class Button(enum.Enum):
        A = 0
        B = 1
        X = 3
        Y = 4
        lBumper = 6
        rBumper = 7
        menu = 10
        hamburger = 11
        xbox = 12
        lStick = 13
        rStick = 14
        save = 15

    class Axis(enum.Enum):
        lStickX = 0
        lStickY = 1
        lTrigger = 5
        rStickX = 2
        rStickY = 3
        rTrigger = 4

    def getButton(self, button: Button):
        """Returns boolean button status of provided button. Ex: controller.getButton(controller.Button.menu) """
        return self.buttons[button.value]

    def getAxis(self, axis: Axis):
        """returns value of specified axis from -1 to 1"""
        return self.axes[axis.value]

    def getHat(self):
        return self.hat

class robot:
    def __init__(self, fake=False):
        NetworkTables.initialize(server="roborio-2022-frc.local")
        self.control = NetworkTables.getTable("control")
        self.sensors = NetworkTables.getTable("sensors")
        if fake:
            # motors
            self.lDrive = fmotor("driveL")
            self.rDrive = fmotor("driveR")
            self.beltZ1 = fmotor("beltZ1")
            self.beltZ2 = fmotor("beltZ2")
            self.beltZ3 = fmotor("beltZ3")
            self.shootWheel = fmotor("shootWhl")
            self.shootAngle = fpneumatic("shootPos")
            '''a relay, not a pneumatic but they behave the same way. call Extend or Retract until it's at a good 
            angle then call Stop '''
            self.pickupMotor = fmotor("pickupM")
            self.colorPanelMotor = fmotor("clrPnlM")
            self.climber = fmotor("climber")
            self.climbServo = fservo("climberServo")
            # sensors
            self.shootEncoder = fencoder("shootEncoder", 1)
            self.lDriveEncoder = fencoder("driveEncoderL", 2)
            self.rDriveEncoder = fencoder("driveEncoderR", 3)
            self.shootCounter = fencoder("shootCounter", 4)  # not technically an encoder
            self.colorSensor = fcolorSensor()
            self.sense_hat = fSenseHat()
            # Pneumatics
            self.colorPanelPneumatic = fpneumatic("clrPnlPNM")
            self.pickupPneumatic = fpneumatic("pickupPNM")
            self.lowerTension = fpneumatic("lTensPNM")
            self.upperTension = fpneumatic("uTensPNM")
            self.controller = fcontroller()
        else:
            # motors
            self.lDrive = motor("driveL")
            self.rDrive = motor("driveR")
            self.beltZ1 = motor("beltZ1")
            self.beltZ2 = motor("beltZ2")
            self.beltZ3 = motor("beltZ3")
            self.shootWheel = motor("shootWhl")
            self.shootAngle = pneumatic("shootPos")
            '''a relay, not a pneumatic but they behave the same way. call Extend or Retract until it's at a good 
            angle then call Stop '''
            self.pickupMotor = motor("pickupM")
            self.colorPanelMotor = motor("clrPnlM")
            self.climber = motor("climber")
            self.climbServo = servo("climberServo")
            # sensors
            self.shootEncoder = encoder("shootEncoder", 1)
            self.lDriveEncoder = encoder("driveEncoderL", 2)
            self.rDriveEncoder = encoder("driveEncoderR", 3)
            self.shootCounter = encoder("shootCounter", 4)  # not technically an encoder
            self.colorSensor = colorSensor()
            self.sense_hat = SenseHat()
            # Pneumatics
            self.colorPanelPneumatic = pneumatic("clrPnlPNM")
            self.pickupPneumatic = pneumatic("pickupPNM")
            self.lowerTension = pneumatic("lTensPNM")
            self.upperTension = pneumatic("uTensPNM")
            self.controller = controller()

    def keepAlive(self):
        """feeds the RoboRio's watchdog to keep the robot enabled. This MUST be called every loop"""
        self.control.putNumber("deadman", random.random())
