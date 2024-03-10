import math


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def get_drive_time(self, _point: "Point"):
        """Returns the drive time in minutes to provided '_point'."""

        return math.sqrt((_point.x - self.x)**2 + (_point.y - self.y)**2)
    

class Load:
    def __init__(self, load_number: int, pickup: Point, dropoff: Point):
        self.load_number = load_number
        self.pickup = pickup
        self.dropoff = dropoff
        self.drive_time = self.pickup.get_drive_time(self.dropoff)
    

MAX_SHIFT_TIME = 12.0 * 60.0 # Shift maximum is 12 hours
DEPOT = Point(0.0, 0.0) # Location drivers start and end

def get_nearest_load(current, incomplete_loads):
    min_drive_time = float('inf')
    nearest_load = None

    for load in incomplete_loads:
        drive_time = current.get_drive_time(load.pickup)
        if drive_time <= min_drive_time:
            min_drive_time = drive_time
            nearest_load = load

    return nearest_load, min_drive_time


def solve_vrp(loads):
    incomplete_loads = loads
    schedules = []

    driver = 0
    while incomplete_loads:
        current = None
        schedules.append([])
        total_drive_time = 0.0

        while True:
            if current:
                nearest_load, min_drive_time = get_nearest_load(current.dropoff, incomplete_loads)
            else:
                nearest_load, min_drive_time = get_nearest_load(DEPOT, incomplete_loads)

            if nearest_load is None:
                break
            elif (total_drive_time + min_drive_time + nearest_load.dropoff.get_drive_time(DEPOT)) > MAX_SHIFT_TIME:
                break


            schedules[driver].append(nearest_load.load_number)
            incomplete_loads.remove(nearest_load)
            total_drive_time += min_drive_time + nearest_load.drive_time
            current = nearest_load

        driver += 1

    return schedules
            

loads = [
    Load(1, Point(-50.1, 80.0), Point(90.1, 12.2)),
    Load(2, Point(-24.5, -19.2), Point(98.5, 1.8)),
    Load(3, Point(0.3, 8.9), Point(40.9, 55.0)),
    Load(4, Point(5.3, -61.1), Point(77.8, -5.4))
]


solution = solve_vrp(loads)
for schdule in solution:
    print(schdule)