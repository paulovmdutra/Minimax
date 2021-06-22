class Position:    

    x = 0
    y = 0

    def __init__(self, x, y):
	    self.x = x
	    self.y = y		

    def __str__(self):
        return "[x=" + str(self.x) + ",y=" + str(self.y) + "]"  

    def to_string(self):
	    return "[x=" + str(self.x) + ",y=" + str(self.y) + "]"