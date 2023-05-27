from threading import Thread


class CarsMovement(Thread):
    def __init__(self):
        super().__init__()

    def start(self):
        pass


if __name__ == '__main__':
    cars_app = CarsMovement()
    cars_app.start()
