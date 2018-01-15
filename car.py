class Car:

    def __init__(self, index, speed, color, direction, position):
        self.index = index
        self.speed = speed
        self.color = color
        self.direction = direction
        self.position = position # position is a tuple of (row, collum)

    def set_speed(self, speed):
        self.speed = speed

    def set_position(self, position):
        self.position = position

    def get_vh(self):
        return min(self.speed + 1, 5)

