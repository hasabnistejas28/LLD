from abc import ABC, abstractmethod
from typing import List, Optional


# ---------------------------
# Entities
# ---------------------------

class PackageSize:
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


class Package:
    def __init__(self, package_id: str, size: str):
        self.package_id = package_id
        self.size = size

    def __repr__(self):
        return f"Package({self.package_id}, {self.size})"


class Locker:
    def __init__(self, locker_id: str, size: str):
        self.locker_id = locker_id
        self.size = size
        self.package: Optional[Package] = None
        self.pickup_code: Optional[str] = None

    def is_free(self) -> bool:
        return self.package is None

    def assign_package(self, package: Package, code: str) -> str:
        if not self.is_free():
            raise Exception("Locker already occupied")
        if self.size not in [package.size, PackageSize.MEDIUM, PackageSize.LARGE]:
            raise Exception("Invalid locker size")
        self.package = package
        self.pickup_code = code
        return self.pickup_code

    def pickup_package(self, code: str) -> Optional[Package]:
        if self.pickup_code == code:
            pkg = self.package
            self.package = None
            self.pickup_code = None
            return pkg
        raise Exception("Invalid pickup code")

    def __repr__(self):
        return f"Locker({self.locker_id}, {self.size}, Free={self.is_free()})"


# ---------------------------
# Strategy Pattern
# ---------------------------

class LockerAssignmentStrategy(ABC):
    @abstractmethod
    def assign_locker(self, lockers, package: Package, code: str) -> Optional[Locker]:
        pass


# Strategy 1: First available of exact size
class FirstAvailableStrategy(LockerAssignmentStrategy):
    def assign_locker(self, lockers, package: Package, code: str) -> Optional[Locker]:
        for locker in lockers:
            if locker.is_free() and locker.size == package.size:
                locker.assign_package(package, code)
                return locker
        return None


# Strategy 2: Optimized — Try to minimize waste of larger lockers
class OptimizedSizeStrategy(LockerAssignmentStrategy):
    def assign_locker(self, lockers, package: Package, code: str) -> Optional[Locker]:
        # Define priority order for each package size
        priority_map = {
            PackageSize.SMALL: [PackageSize.SMALL, PackageSize.MEDIUM, PackageSize.LARGE],
            PackageSize.MEDIUM: [PackageSize.MEDIUM, PackageSize.LARGE],
            PackageSize.LARGE: [PackageSize.LARGE]
        }

        for size in priority_map[package.size]:
            for locker in lockers:
                if locker.is_free() and locker.size == size:
                    locker.assign_package(package, code)
                    return locker
        return None


# ---------------------------
# Locker System
# ---------------------------

class LockerSystem:
    def __init__(self, strategy: LockerAssignmentStrategy):
        self.lockers: List[Locker] = []
        self.strategy = strategy
        self.code_to_locker = {}
        self.code_counter = 1000  # simple incremental code

    def add_locker(self, locker: Locker):
        self.lockers.append(locker)

    def assign_package(self, package: Package) -> str:
        code = str(self.code_counter)
        self.code_counter += 1

        locker = self.strategy.assign_locker(self.lockers, package, code)
        if not locker:
            raise Exception("No locker available for this package size")
        self.code_to_locker[code] = locker
        print(f"Assigned {package} to {locker.locker_id} with code {code}")
        return code

    def pickup_package(self, code: str) -> Package:
        if code not in self.code_to_locker:
            raise Exception("Invalid pickup code")
        locker = self.code_to_locker[code]
        pkg = locker.pickup_package(code)
        del self.code_to_locker[code]
        print(f"Picked up {pkg} from {locker.locker_id}")
        return pkg

    def free_lockers_count(self, size: str) -> int:
        return sum(1 for locker in self.lockers if locker.is_free() and locker.size == size)


# ---------------------------
# Demo
# ---------------------------

if __name__ == "__main__":
    # Use Optimized strategy
    system = LockerSystem(OptimizedSizeStrategy())

    # Add lockers
    system.add_locker(Locker("L1", PackageSize.SMALL))
    system.add_locker(Locker("L2", PackageSize.MEDIUM))
    system.add_locker(Locker("L3", PackageSize.LARGE))
    system.add_locker(Locker("L4", PackageSize.SMALL))

    # Assign packages
    p1 = Package("P100", PackageSize.SMALL)
    p2 = Package("P200", PackageSize.SMALL)
    p3 = Package("P300", PackageSize.MEDIUM)
    p4 = Package("P400", PackageSize.LARGE)

    c1 = system.assign_package(p1)   # should go to L1
    c2 = system.assign_package(p2)   # should go to L4
    c3 = system.assign_package(p3)   # should go to L2
    c4 = system.assign_package(p4)   # should go to L3

    # Pickup a package
    system.pickup_package(c1)

    # Free locker count
    print("Free SMALL lockers:", system.free_lockers_count(PackageSize.SMALL))
    print("Free MEDIUM lockers:", system.free_lockers_count(PackageSize.MEDIUM))
    print("Free LARGE lockers:", system.free_lockers_count(PackageSize.LARGE))
