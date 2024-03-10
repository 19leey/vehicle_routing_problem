import math


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def get_drive_time(self, _point: "Point"):
        """Returns the drive time in minutes one Point to another Point."""

        return math.sqrt((_point.x - self.x)**2 + (_point.y - self.y)**2)
    

class Load:
    def __init__(self, load_number: int, pickup: Point, dropoff: Point):
        self.load_number = load_number
        self.pickup = pickup
        self.dropoff = dropoff
        self.duration = self.pickup.get_drive_time(self.dropoff) # Drive time from pickup to dropoff

    def get_drive_time(self, _load: "Load"):
        """Returns the drive time in minutes one Load to another Load.
        
        Distinction is made between Point and Load due to Load having a 'pickup'
        and 'dropoff' attributes - these must be considered when calculating
        drive time between two Loads.
    
        """

        return self.dropoff.get_drive_time(_load.pickup)
    
    def get_nearest_load(self, _loads: list["Load"]):
        """Finds and returns the nearest Load in terms of drive time.
        
        Returns the nearest Load instance and the drive time in minutes to drive
        from the current Load to the nearest Load instance.
        
        """

        min_drive_time = float("inf")
        nearest_load = None

        for load in _loads:
            drive_time = self.get_drive_time(load)

            if drive_time <= min_drive_time:
                min_drive_time = drive_time
                nearest_load = load

        return nearest_load, min_drive_time

    
MAX_SHIFT_TIME = 12.0 * 60.0 # Shift maximum is 12 hours
DEPOT = Load(-1, Point(0.0, 0.0), Point(0.0, 0.0)) # Location drivers start and end


def solve_vrp(loads):
    incomplete_loads = loads
    schedules = []

    driver = 0
    while incomplete_loads:
        current = DEPOT # All drivers start at (0,0)
        schedules.append([])
        total_drive_time = 0.0

        while True:
            nearest_load, drive_time = current.get_nearest_load(incomplete_loads)
            if nearest_load is None:
                # No valid nearest Load was found
                break
            elif (total_drive_time + drive_time + nearest_load.duration + nearest_load.get_drive_time(DEPOT)) > MAX_SHIFT_TIME:
                # Invalid schedule if driver is not able to stay under maximum 12 hour shift
                # This includes returning back to (0,0)
                break

            schedules[driver].append(nearest_load.load_number)
            incomplete_loads.remove(nearest_load)
            total_drive_time += drive_time + nearest_load.duration
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