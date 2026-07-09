"""Sample module for testing TestForge."""

from typing import Optional, List, Dict


def greet(name: str) -> str:
    """Return a greeting."""
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


def get_user(user_id: int, include_details: bool = False) -> Optional[Dict]:
    """Fetch user by ID."""
    if user_id <= 0:
        return None
    return {"id": user_id, "name": "Test User"}


def process_items(items: List[str]) -> List[str]:
    """Process a list of items."""
    return [item.upper() for item in items]


class Calculator:
    """A simple calculator."""

    def __init__(self, initial: int = 0):
        self.value = initial

    def add(self, amount: int) -> int:
        """Add to the current value."""
        self.value += amount
        return self.value

    def subtract(self, amount: int) -> int:
        """Subtract from current value."""
        self.value -= amount
        return self.value

    def get_value(self) -> int:
        """Get current value."""
        return self.value


async def fetch_data(url: str, timeout: int = 10) -> str:
    """Fetch data from URL."""
    return f"Data from {url}"
