import string
from networktables import NetworkTables
import random
from sense_emu import SenseHat as fSense
from sense_hat import SenseHat

class motor:
    '''abstraction for FRC motor controller / motor controller group'''
    def __init__(self,name: string):
        self.name = name
        self.control = NetworkTables.getTable("control")
    def Set(self,value: int):
        '''Sets motor speed in a range from -1 to 1
        where -1 is full reverse, 1 is full forward, and 0 is stopped'''
        if abs(value) > 1: raise ValueError("Out of range input supplied!!")
        else: self.control.putNumber(self.name,value)

class servo:
    def __init__(self,name: string):
        self.name = name
        self.control = NetworkTables.getTable("control")
    def Set(self,value: int):
        '''sets the servo to a specified angle in degrees. Valid inputs are 0-180.'''
        if value > 180 or value < 0: raise ValueError("Out of range input supplied!!")
        else: self.control.putNumber(self.name,value)
class pneumatic:
    '''abstraction for FRC Double Solenoid class'''
    def __init__(self, name: string):
        self.control = NetworkTables.getTable("control")
    def Extend(self):
        '''sets pneumatic to kForward'''
        self.control.putNumber(self.name,1)
    def Retract(self):
        '''sets pneumatic to kReverse'''
        self.control.putNumber(self.name,-1)
    def Stop(self):
        '''sets pneumatic to kOff'''
        self.control.putNumber(self.name,0)

class encoder:
    '''abstraction for FRC Encoder (and geartooth) class'''
    def __init__(self,name: string,index: int):
        self.name = name
        self.index = index
        self.sensors = NetworkTables.getTable("sensors")
        self.control = NetworkTables.getTable("control")
    def Get(self):
        '''returns the number of encoder cycles since last reset'''
        return self.sensors.getNumber(self.name,0)
    def Reset(self):
        '''sets encoder value to 0'''
        self.control.putNumber("encRst",self.index)

class colorSensor:
    '''Abstraction for REV color sensor V3'''
    def __init__(self):
        self.sensors = NetworkTables.getTable("sensors")
    def getColor(self):
        """returns an array of RGB color values from 0-255"""
        return self.sensors.getNumberArray("colorSensor",[0,0,0])
    def getProximity(self):
        '''returns *raw* proximity value ranging from 0 to 2047 with 2047 being 
        closest to the sensor and 0 being furthest away / not detected'''
        return self.sensors.getNumber("colorProximity",0)
class fmotor:
    '''abstraction for FRC motor controller / motor controller group'''
    def __init__(self,name: string):
        self.name = name
        self.value = 0
    def Set(self,value: int):
        '''Sets motor speed in a range from -1 to 1
        where -1 is full reverse, 1 is full forward, and 0 is stopped'''
        if abs(value) > 1: raise ValueError("Out of range input supplied!!")
        else: self.value = value

class fservo:
    def __init__(self,name: string):
        self.name = name
        self.value = 0
    def Set(self,value: int):
        '''sets the servo to a specified angle in degrees. Valid inputs are 0-180.'''
        if value > 180 or value < 0: raise ValueError("Out of range input supplied!!")
        else: self.value = value
class fpneumatic:
    '''abstraction for FRC Double Solenoid class'''
    def __init__(self, name: string):
        self.name = name
        self.value = 0
    def Extend(self):
        '''sets pneumatic to kForward'''
        self.value = 1
    def Retract(self):
        '''sets pneumatic to kReverse'''
        self.value = -1
    def Stop(self):
        '''sets pneumatic to kOff'''
        self.value = 0

class fencoder:
    '''abstraction for FRC Encoder (and geartooth) class'''
    def __init__(self,name: string,index: int):
        self.value = 0
    def Get(self):
        '''returns the number of encoder cycles since last reset'''
        return self.value
    def Reset(self):
        '''sets encoder value to 0'''
        self.value = 0

class fcolorSensor:
    '''Abstraction for REV color sensor V3'''
    def __init__(self):
        self.value = [0,0,0]
        self.prox = 0
    def getColor(self):
        """returns an array of RGB color values from 0-255"""
        return self.value
    def getProximity(self):
        '''returns *raw* proximity value ranging from 0 to 2047 with 2047 being 
        closest to the sensor and 0 being furthest away / not detected'''
        return self.prox
class robot:
    def __init__(self, fake = False):
        self.control = NetworkTables.getTable("control")
        self.sensors = NetworkTables.getTable("sensors")
        if (fake):
            self.HAT = fSense()
            # motors
            self.lDrive = fmotor("driveL")
            self.rDrive = fmotor("driveR")
            self.beltZ1 = fmotor("beltZ1")
            self.beltZ2 = fmotor("beltZ2")
            self.beltZ3 = fmotor("beltZ3")
            self.shootWheel = fmotor("shootWhl")
            self.shootAngle = fpneumatic("shootPos") 
            '''a relay, not a pneumatic but they behave the same way. call Extend or Retract until it's at a good angle then call Stop'''
            self.pickupMotor = fmotor("pickupM")
            self.colorPanelMotor = fmotor("clrPnlM")
            self.climber = fmotor("climber")
            self.climbServo = fservo("climberServo")
            # sensors
            self.shootEncoder = fencoder("shootEncoder",1)
            self.lDriveEncoder = fencoder("driveEncoderL",2)
            self.rDriveEncoder = fencoder("driveEncoderR",3)
            self.shootCounter = fencoder("shootCounter",4) #not technically an encoder
            self.colorSensor = fcolorSensor()
            # Pneumatics
            self.colorPanelPneumatic = fpneumatic("clrPnlPNM")
            self.pickupPneumatic = fpneumatic("pickupPNM")
            self.lowerTension = fpneumatic("lTensPNM")
            self.upperTension = fpneumatic("uTensPNM")
        else:
            self.HAT = SenseHat()
            # motors
            self.lDrive = motor("driveL")
            self.rDrive = motor("driveR")
            self.beltZ1 = motor("beltZ1")
            self.beltZ2 = motor("beltZ2")
            self.beltZ3 = motor("beltZ3")
            self.shootWheel = motor("shootWhl")
            self.shootAngle = pneumatic("shootPos") 
            '''a relay, not a pneumatic but they behave the same way. call Extend or Retract until it's at a good angle then call Stop'''
            self.pickupMotor = motor("pickupM")
            self.colorPanelMotor = motor("clrPnlM")
            self.climber = motor("climber")
            self.climbServo = servo("climberServo")
            # sensors
            self.shootEncoder = encoder("shootEncoder",1)
            self.lDriveEncoder = encoder("driveEncoderL",2)
            self.rDriveEncoder = encoder("driveEncoderR",3)
            self.shootCounter = encoder("shootCounter",4) #not technically an encoder
            self.colorSensor = colorSensor()
            # Pneumatics
            self.colorPanelPneumatic = pneumatic("clrPnlPNM")
            self.pickupPneumatic = pneumatic("pickupPNM")
            self.lowerTension = pneumatic("lTensPNM")
            self.upperTension = pneumatic("uTensPNM")

    def keepAlive(self):
        """feeds the RoboRio's watchdog to keep the robot enabled. This MUST be called every loop"""
        self.control.putNumber("deadman",random.random())
    
    #The following functions may seem useless and they kind of are but I don't want
    #the students making direct calls to the sense HAT because that could break other stuff
    #so we're stuck with these dumb abstractions (and yes they could just make direct robot.HAT calls
    # but I'm not going to tell them about that and hope they won't read this comment lol)
    def getYaw(self): #TODO: these are probably not accurate to how the board will be mounted in the robot
        '''returns the yaw (side-to-side pivot) of the robot in degrees''' 
        return self.HAT.get_orientation_degrees()["yaw"]
    def getRoll(self):
        '''returns the roll (side-to-side tilt) of the robot in degrees''' 
        return self.HAT.get_orientation_degrees()["roll"]
    def getPitch(self):
        '''returns the pitch (front-back tilt) of the robot in degrees''' 
        return self.HAT.get_orientation_degrees()["pitch"]
    def getAcceleration(self,axis: string):
        '''returns the acceleration in Gs for the specified axis. Valid inputs: "x", "y", "z".
        Note that the qoutation marks are required!'''
        return self.HAT.get_accelerometer_raw()[axis.lower()]
