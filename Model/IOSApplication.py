from Model.IOSComponent import IOSComponent


class IOSApplication(IOSComponent):
    def __init__(self):
        IOSComponent.__init__(self)
        self.plugins = []
