from networktables import NetworkTables

class motor:
    def __init__(self,name,controlTable):
        self.name = name
        self.controlTable = controlTable
    def Set(self,value):
        if abs(value) > 1: raise ValueError("Out of range input supplied!!")
        else: self.controlTable.putNumber(self.name,value)

class robot:
    def __init__(self):
        self.control = NetworkTables.getTable("control")
        self.sensors = NetworkTables.getTable("sensors")
        self.lDrive = motor("driveL",self.control)
        self.rDrive = motor("driveR",self.control)
        self.beltZ1 = motor("beltZ1",self.control)
        self.beltZ2 = motor("beltZ2",self.control)
        self.beltZ3 = motor("beltZ3",self.control)
        self.shootWheel = motor("shootWhl",self.control)
        self.pickupMotor = motor("pickupM",self.control)
        self.colorPanelMotor = motor("clrPnlM",self.control)
        

        