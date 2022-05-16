from networktables import NetworkTables

class robot:
    def __init__(self):
        self.control = NetworkTables.getTable("control")
        self.sensors = NetworkTables.getTable("sensors")
        
