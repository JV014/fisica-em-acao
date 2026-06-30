class Simulation:

    def __init__(self):

        self.distance = 25      # distância percorrida por questão
        self.target_x = None
        self.running = False

    def start(self, car):

        self.target_x = car.x + self.distance
        self.running = True

    def update(self, car, dt):

        if not self.running:
            return

        car.move(dt)

        if car.x >= self.target_x:

            car.x = self.target_x
            self.running = False

    def finished(self):

        return not self.running