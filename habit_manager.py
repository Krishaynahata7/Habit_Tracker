"""
habit_manager.py
----------------
HabitManager is the in-memory repository of Habit objects: the single 
place responsible for creating, deleting, and looking up habits. It
talks to storage.py to load data. It deliberately does NOT
import analytics.py directly - cli.py fetches the current list of
habits from the manager and passes that data to the analytics
functions, keeping analytics.py fully decoupled and independently
testable.
"""

import storage
from habit import Habit


class HabitAlreadyExistsError(Exception):
    """Raised when creating a habit whose name is already in use."""


class HabitNotFoundError(Exception):
    """Raised when looking up, checking off, or deleting an unknown habit."""


class HabitManager:
    def __init__(self, filepath=None):
        self._filepath = filepath or storage.DEFAULT_DATA_FILE
        self._habits = storage.load_habits(self._filepath)

    def list_habits(self):
        """Return all tracked habits."""
        return list(self._habits)

    def get_habit(self, name):
        """Look up a single habit by name."""
        for habit in self._habits:
            if habit.name == name:
                return habit
        raise HabitNotFoundError(f"No habit named {name!r}.")

    def create_habit(self, name, periodicity):
        """Define and store a new habit. Raises if the name is already used."""
        if any(h.name == name for h in self._habits):
            raise HabitAlreadyExistsError(f"A habit named {name!r} already exists.")

        habit = Habit(name, periodicity)
        self._habits.append(habit)
        self.save()
        return habit

    def delete_habit(self, name):
        """Remove a habit by name."""
        habit = self.get_habit(name)
        self._habits.remove(habit)
        self.save()

    def check_off(self, name, when=None):
        """Record a completion for the named habit."""
        habit = self.get_habit(name)
        timestamp = habit.check_off(when)
        self.save()
        return timestamp

    def save(self):
        """Persist the current in-memory state to disk."""
        storage.save_habits(self._habits, self._filepath)