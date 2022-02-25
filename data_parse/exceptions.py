class InvalidHeaderException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class EmptyFormatException(Exception):
    def __init__(self,message):
        self.message = message
        super().__init__(self.message)

class InvalidDataTypeException(Exception):
    def __init__(self,message):
        self.message = message
        super().__init__(self.message)


class InvalidWidthException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidFormatException(Exception):
    def __init__(self,message):
        self.message = message
        super().__init__(self.message)