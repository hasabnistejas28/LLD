from abc import ABC, abstractmethod
from typing import List, Optional

# ---------------------------
# Vehicle
# ---------------------------

class VehicleType:
    BIKE = "BIKE"
    CAR = "CAR"
    TRUCK = "TRUCK"


class Vehicle:
    def __init__(self, number: str, vtype: str):
        self.number = number
        self.type = vtype

    def __repr__(self):
        return f"Vehicle({self.number}, {self.type})"


# ---------------------------
# Parking Spot
# ---------------------------

class ParkingSpot:
    def __init__(self, spot_type: str, row: int, col: int):
        self.spot_type = spot_type
        self.row = row
        self.col = col
        self.vehicle: Optional[Vehicle] = None

    def is_free(self) -> bool:
        return self.vehicle is None

    def park(self, vehicle: Vehicle) -> bool:
        if self.is_free() and self.spot_type == vehicle.type:
            self.vehicle = vehicle
            return True
        return False

    def unpark(self) -> Optional[Vehicle]:
        v = self.vehicle
        self.vehicle = None
        return v

    def __repr__(self):
        return f"Spot({self.spot_type}, {self.row},{self.col}, Free={self.is_free()})"


# ---------------------------
# Parking Floor
# ---------------------------

class ParkingFloor:
    def __init__(self, floor_num: int, rows: int, cols: int):
        self.floor_num = floor_num
        self.spots: List[List[ParkingSpot]] = [
            [None] * cols for _ in range(rows)
        ]

    def add_spot(self, spot: ParkingSpot, row: int, col: int):
        self.spots[row][col] = spot

    def get_free_spots(self, vtype: str) -> int:
        return sum(
            1 for row in self.spots for spot in row if spot and spot.is_free() and spot.spot_type == vtype
        )

    def __repr__(self):
        return f"Floor({self.floor_num})"


# ---------------------------
# Strategy Pattern
# ---------------------------

class ParkingStrategy(ABC):
    @abstractmethod
    def find_spot(self, floors: List[ParkingFloor], vehicle: Vehicle) -> Optional[ParkingSpot]:
        pass


# Strategy 1: First available spot across all floors
class FirstAvailableStrategy(ParkingStrategy):
    def find_spot(self, floors: List[ParkingFloor], vehicle: Vehicle) -> Optional[ParkingSpot]:
        for floor in floors:
            for row in floor.spots:
                for spot in row:
                    if spot and spot.park(vehicle):
                        print(f"Parked {vehicle} at Floor {floor.floor_num} Spot({spot.row},{spot.col})")
                        return spot
        return None


# Strategy 2: Always try lowest floor first
class LowestFloorStrategy(ParkingStrategy):
    def find_spot(self, floors: List[ParkingFloor], vehicle: Vehicle) -> Optional[ParkingSpot]:
        for floor in sorted(floors, key=lambda f: f.floor_num):
            for row in floor.spots:
                for spot in row:
                    if spot and spot.park(vehicle):
                        print(f"Parked {vehicle} at Floor {floor.floor_num} Spot({spot.row},{spot.col})")
                        return spot
        return None


# ---------------------------
# Parking Lot
# ---------------------------

class ParkingLot:
    def __init__(self, name: str, strategy: ParkingStrategy):
        self.name = name
        self.floors: List[ParkingFloor] = []
        self.strategy = strategy

    def add_floor(self, floor: ParkingFloor):
        self.floors.append(floor)

    def park_vehicle(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        return self.strategy.find_spot(self.floors, vehicle)

    def unpark_vehicle(self, number: str) -> Optional[Vehicle]:
        for floor in self.floors:
            for row in floor.spots:
                for spot in row:
                    if spot and spot.vehicle and spot.vehicle.number == number:
                        v = spot.unpark()
                        print(f"Unparked {v} from Floor {floor.floor_num} Spot({spot.row},{spot.col})")
                        return v
        print(f"Vehicle {number} not found!")
        return None

    def search_vehicle(self, number: str) -> Optional[str]:
        for floor in self.floors:
            for row in floor.spots:
                for spot in row:
                    if spot and spot.vehicle and spot.vehicle.number == number:
                        return f"Vehicle {number} at Floor {floor.floor_num} Spot({spot.row},{spot.col})"
        return None

    def count_free_spots(self, floor_num: int, vtype: str) -> int:
        for floor in self.floors:
            if floor.floor_num == floor_num:
                return floor.get_free_spots(vtype)
        return 0


# ---------------------------
# Demo
# ---------------------------

if __name__ == "__main__":
    # Build parking lot
    lot = ParkingLot("MyLot", FirstAvailableStrategy())

    # Floor 0: 2x2 grid
    floor0 = ParkingFloor(0, 2, 2)
    floor0.add_spot(ParkingSpot(VehicleType.CAR, 0, 0), 0, 0)
    floor0.add_spot(ParkingSpot(VehicleType.BIKE, 0, 1), 0, 1)
    floor0.add_spot(ParkingSpot(VehicleType.TRUCK, 1, 0), 1, 0)
    floor0.add_spot(ParkingSpot(VehicleType.CAR, 1, 1), 1, 1)

    lot.add_floor(floor0)

    # Vehicles
    v1 = Vehicle("KA01AB1234", VehicleType.CAR)
    v2 = Vehicle("KA02XY5678", VehicleType.BIKE)
    v3 = Vehicle("KA03ZZ9999", VehicleType.TRUCK)

    # Park vehicles
    lot.park_vehicle(v1)
    lot.park_vehicle(v2)
    lot.park_vehicle(v3)

    # Search
    print(lot.search_vehicle("KA01AB1234"))

    # Free spots
    print("Free CAR spots on Floor 0:", lot.count_free_spots(0, VehicleType.CAR))

    # Unpark
    lot.unpark_vehicle("KA01AB1234")
    print("Free CAR spots on Floor 0:", lot.count_free_spots(0, VehicleType.CAR))
