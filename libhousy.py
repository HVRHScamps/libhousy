from networktables import NetworkTables
import random
class motor:
    '''abstraction for FRC motor controller / motor controller group'''
    def __init__(self,name):
        self.name = name
        self.control = NetworkTables.getTable("control")
    def Set(self,value):
        '''Sets motor speed in a range from -1 to 1
        where -1 is full reverse, 1 is full forward, and 0 is stopped'''
        if abs(value) > 1: raise ValueError("Out of range input supplied!!")
        else: self.control.putNumber(self.name,value)

class pneumatic:
    '''abstraction for FRC Double Solenoid class'''
    def __init__(self,name):
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
    def __init__(self,name,index):
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

class robot:
    def __init__(self):
        self.control = NetworkTables.getTable("control")
        self.sensors = NetworkTables.getTable("sensors")
        # motors
        self.lDrive = motor("driveL")
        self.rDrive = motor("driveR")
        self.beltZ1 = motor("beltZ1")
        self.beltZ2 = motor("beltZ2")
        self.beltZ3 = motor("beltZ3")
        self.shootWheel = motor("shootWhl")
        self.pickupMotor = motor("pickupM")
        self.colorPanelMotor = motor("clrPnlM")
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
        