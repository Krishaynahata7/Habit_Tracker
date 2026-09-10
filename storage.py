"""
storage.py
----------
Reads and writes Habit data to disk as JSON, and provides the fixture
data used the very first time the app runs: five predefined habits with
four weeks of example completion history, as described in the
conception phase ("it pre-loads five example habits with four weeks of
example data").

This module knows nothing about HabitManager or analytics; it only
translates between Habit objects and a JSON file on disk.
"""

import json
import os
from datetime import datetime, timedelta, time

from habit import Habit

DEFAULT_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "habits_data.json")

# Fixed anchor date so the bundled example data is reproducible in tests 
# and demos, rather than silently changing every day it is run.
_FIXTURE_TODAY = datetime(2026, 8, 29, 20, 0)


def load_habits(filepath=DEFAULT_DATA_FILE):
    """Load habits from filepath.

    If the file does not exist yet (first run), the five predefined
    example habits with four weeks of history are created, saved, and
    returned - matching the conception phase description of the app's
    first-launch behaviour.
    """
    if not os.path.exists(filepath):
        habits = _build_example_habits()
        save_habits(habits, filepath)
        return habits

    with open(filepath, "r", encoding="utf-8") as f:
        raw = json.load(f)

    return [Habit.from_dict(entry) for entry in raw]


def save_habits(habits, filepath=DEFAULT_DATA_FILE):
    """Persist a list of Habit objects to filepath as JSON."""
    raw = [h.to_dict() for h in habits]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(raw, f, indent=2)


def _daily_completion(days_ago):
    dt = _FIXTURE_TODAY - timedelta(days=days_ago)
    return datetime.combine(dt.date(), time(hour=8))


def _weekly_completion(weeks_ago):
    dt = _FIXTURE_TODAY - timedelta(weeks=weeks_ago)
    return datetime.combine(dt.date(), time(hour=18))


def _build_example_habits():
    """Construct the five predefined habits with four weeks of
    example completion data, deliberately varied so that analytics.py
    (streaks, filtering by periodicity) has something interesting to
    compute: some habits have a perfect streak, others may have gaps.
    """
    created = _FIXTURE_TODAY - timedelta(weeks=4)

    # 1. Perfect daily streak: completed every day for 28 days straight.
    drink_water = Habit(
        "Drink water", "daily", created_at=created,
        completions=[_daily_completion(d) for d in range(28)],
    )

    # 2. Daily habit with one gap (day 15 skipped) -> streak broken.
    exercise_days = [d for d in range(28) if d != 15]
    exercise = Habit(
        "Exercise", "daily", created_at=created,
        completions=[_daily_completion(d) for d in exercise_days],
    )

    # 3. Daily habit done sporadically -> short longest streak.
    read_days = [0, 1, 2, 5, 6, 10, 11, 12, 13, 14, 20]
    read_book = Habit(
        "Read a book", "daily", created_at=created,
        completions=[_daily_completion(d) for d in read_days],
    )

    # 4. Perfect weekly streak: completed each of the last 4 weeks.
    meal_prep = Habit(
        "Meal prep", "weekly", created_at=created,
        completions=[_weekly_completion(w) for w in range(4)],
    )

    # 5. Weekly habit with a missed week -> streak broken.
    call_weeks = [0, 1, 3]
    call_parents = Habit(
        "Call parents", "weekly", created_at=created,
        completions=[_weekly_completion(w) for w in call_weeks],
    )

    return [drink_water, exercise, read_book, meal_prep, call_parents]