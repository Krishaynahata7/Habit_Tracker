"""
habit.py
--------
Defines the Habit class: the object-oriented core of the data model.

A Habit knows only - its name, its periodicity ('daily' or
'weekly'), when it was created, and the timestamps at which it was
completed. It has no knowledge of storage or analytics; those concerns
live in storage.py, habit_manager.py, and analytics.py respectively.
"""

from datetime import datetime

VALID_PERIODICITIES = ("daily", "weekly")


class Habit:
    """A single habit being tracked.

    Attributes:
        name (str): Name of the habit, e.g. "Drink water".
        periodicity (str): Either "daily" or "weekly".
        created_at (datetime): When the habit was first defined.
        completions (list[datetime]): Timestamps of each check-off.
    """

    def __init__(self, name, periodicity, created_at=None, completions=None):
        if not name or not isinstance(name, str):
            raise ValueError("Habit name must be a non-empty string.")
        if periodicity not in VALID_PERIODICITIES:
            raise ValueError(
                f"periodicity must be one of {VALID_PERIODICITIES}, got {periodicity!r}"
            )

        self.name = name
        self.periodicity = periodicity
        self.created_at = created_at if created_at is not None else datetime.now()
        self.completions = list(completions) if completions else []

    def check_off(self, when=None):
        """Record a completion. Defaults to the current time."""
        timestamp = when if when is not None else datetime.now()
        self.completions.append(timestamp)
        return timestamp

    def to_dict(self):
        """Serialize this habit to a plain dict of JSON-safe values."""
        return {
            "name": self.name,
            "periodicity": self.periodicity,
            "created_at": self.created_at.isoformat(),
            "completions": [c.isoformat() for c in self.completions],
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruct a Habit from a dict produced by to_dict()."""
        return cls(
            name=data["name"],
            periodicity=data["periodicity"],
            created_at=datetime.fromisoformat(data["created_at"]),
            completions=[datetime.fromisoformat(ts) for ts in data.get("completions", [])],
        )

    def __eq__(self, other):
        if not isinstance(other, Habit):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return (
            f"Habit(name={self.name!r}, periodicity={self.periodicity!r}, "
            f"completions={len(self.completions)})"
        )