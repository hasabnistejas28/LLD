from abc import ABC, abstractmethod

# ---------------------------
# Base Pizza Component
# ---------------------------

class Pizza(ABC):
    @abstractmethod
    def get_description(self) -> str: pass

    @abstractmethod
    def get_cost(self) -> float: pass

    @abstractmethod
    def get_size(self) -> str: pass

    @abstractmethod
    def set_size(self, size: str): pass


class Margherita(Pizza):
    base_prices = {"small": 150, "medium": 200, "large": 250}

    def __init__(self, size: str):
        self.size = size

    def get_description(self) -> str:
        return f"{self.size.capitalize()} Margherita"

    def get_cost(self) -> float:
        return self.base_prices[self.size]

    def get_size(self) -> str:
        return self.size

    def set_size(self, size: str):
        self.size = size


# ---------------------------
# Decorator for Toppings
# ---------------------------

class ToppingDecorator(Pizza, ABC):
    def __init__(self, pizza: Pizza):
        self.pizza = pizza

    def set_size(self, size: str):
        self.pizza.set_size(size)


class Corn(ToppingDecorator):
    def __init__(self, pizza: Pizza, servings: int = 1):
        super().__init__(pizza)
        self.servings = servings
        self.price_per_serving = 30

    def get_description(self) -> str:
        return self.pizza.get_description() + f", Corn x{self.servings}"

    def get_cost(self) -> float:
        return self.pizza.get_cost() + (self.price_per_serving * self.servings)

    def get_size(self) -> str:
        return self.pizza.get_size()


class Onion(ToppingDecorator):
    def __init__(self, pizza: Pizza):
        super().__init__(pizza)
        self.price = 20

    def get_description(self) -> str:
        return self.pizza.get_description() + ", Onion"

    def get_cost(self) -> float:
        return self.pizza.get_cost() + self.price

    def get_size(self) -> str:
        return self.pizza.get_size()


class CheeseBurst(ToppingDecorator):
    def __init__(self, pizza: Pizza):
        super().__init__(pizza)
        self.price = 100

    def get_description(self) -> str:
        return self.pizza.get_description() + ", Cheese Burst"

    def get_cost(self) -> float:
        return self.pizza.get_cost() + self.price

    def get_size(self) -> str:
        return self.pizza.get_size()


class Mushroom(ToppingDecorator):
    def __init__(self, pizza: Pizza):
        super().__init__(pizza)
        self.price = 40

    def get_description(self) -> str:
        return self.pizza.get_description() + ", Mushroom"

    def get_cost(self) -> float:
        return self.pizza.get_cost() + self.price

    def get_size(self) -> str:
        return self.pizza.get_size()


# ---------------------------
# Business Rules
# ---------------------------

class Rule(ABC):
    @abstractmethod
    def apply(self, pizza: Pizza, cost: float) -> float:
        pass


# ❌ Cheese Burst not allowed on small
class CheeseBurstOnSmallRule(Rule):
    def apply(self, pizza: Pizza, cost: float) -> float:
        if isinstance(pizza, CheeseBurst) and pizza.get_size() == "small":
            raise Exception("Cheese Burst cannot be added on Small pizza!")
        return cost


# ❌ Cheese Burst + Mushroom not allowed
class CheeseBurstMushroomRule(Rule):
    def apply(self, pizza: Pizza, cost: float) -> float:
        if isinstance(pizza, CheeseBurst) and isinstance(pizza.pizza, Mushroom):
            raise Exception("Cheese Burst and Mushroom cannot go together!")
        return cost


# 💰 30% off corn from 2nd serving onwards
class CornDiscountRule(Rule):
    def apply(self, pizza: Pizza, cost: float) -> float:
        if isinstance(pizza, Corn) and pizza.servings > 1:
            discounted = pizza.price_per_serving + (pizza.servings - 1) * (pizza.price_per_serving * 0.7)
            return pizza.pizza.get_cost() + discounted
        return cost


# 💰 Onion 20% off if pizza is large
class OnionLargeDiscountRule(Rule):
    def apply(self, pizza: Pizza, cost: float) -> float:
        if isinstance(pizza, Onion) and pizza.get_size() == "large":
            return pizza.pizza.get_cost() + (pizza.price * 0.8)
        return cost


# ---------------------------
# Price Calculator with Rules
# ---------------------------

class PriceCalculator:
    def __init__(self, rules: list[Rule]):
        self.rules = rules

    def calculate(self, pizza: Pizza) -> float:
        cost = pizza.get_cost()
        for rule in self.rules:
            cost = rule.apply(pizza, cost)
        return cost


# ---------------------------
# Demo
# ---------------------------

if __name__ == "__main__":
    print("=== Without Rules ===")
    pizza1 = Margherita("small")
    pizza1 = Onion(pizza1)
    print("Order:", pizza1.get_description())
    print("Price:", pizza1.get_cost())

    pizza2 = Margherita("medium")
    pizza2 = Corn(pizza2, servings=2)
    pizza2 = Mushroom(pizza2)
    print("\nOrder:", pizza2.get_description())
    print("Price:", pizza2.get_cost())

    # Convert small to large
    pizza1.set_size("large")
    print("\nAfter resizing pizza1 -> Large:")
    print("Order:", pizza1.get_description())
    print("Price:", pizza1.get_cost())

    print("\n=== With Rules Applied ===")
    pizza3 = Margherita("large")
    pizza3 = CheeseBurst(pizza3)
    pizza3 = Corn(pizza3, servings=3)
    pizza3 = Onion(pizza3)

    rules = [CheeseBurstOnSmallRule(), CheeseBurstMushroomRule(),
             CornDiscountRule(), OnionLargeDiscountRule()]
    calculator = PriceCalculator(rules)

    print("Order:", pizza3.get_description())
    print("Final Price (with discounts/rules):", calculator.calculate(pizza3))
