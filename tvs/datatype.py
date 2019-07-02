class PtrDetails:
    def __init__(self, region, ptr):
        self.region = region
        self.ptr = ptr


class UserStatusDetail:
    def __init__(self, status, location, length):
        self.status = status
        self.location = location
        self.length = length

class ToMap:
    def __init__(self, reg, p):
        self.reg = reg
        self.p = p

class ToMap1:
    def __init__(self, data_pair):
        self.data_pair=data_pair