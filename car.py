class Car:

    def __init__(self, speed, color, direction, position):
        self.speed = speed
        self.color = color
        self.direction = direction
        self.position = position #position is a tuple of (row, collum)

    def set_speed(self, speed):
        self.speed = speed

    def set_position(self, position):
        self.position = position