"""
Unit tests for analytics.py, using both hand-built habits and the
bundled 4-week example data so the streak logic is checked
against known, deliberately-varied data.
"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import analytics
from habit import Habit
from storage import _build_example_habits


# --- Tests against small, hand-crafted habits ---

def test_habits_by_periodicity_filters_correctly():
    daily = Habit("Read", "daily")
    weekly = Habit("Clean", "weekly")
    result = analytics.habits_by_periodicity([daily, weekly], "weekly")
    assert result == [weekly]


def test_list_all_habits_returns_names():
    h1 = Habit("Read", "daily")
    h2 = Habit("Clean", "weekly")
    assert analytics.list_all_habits([h1, h2]) == ["Read", "Clean"]


def test_longest_streak_no_completions_is_zero():
    h = Habit("Read", "daily")
    assert analytics.longest_streak_for_habit(h) == 0


def test_longest_streak_daily_consecutive_days():
    base = datetime(2026, 1, 1)
    h = Habit("Read", "daily", completions=[base + timedelta(days=i) for i in range(5)])
    assert analytics.longest_streak_for_habit(h) == 5


def test_longest_streak_daily_with_gap():
    base = datetime(2026, 1, 1)
    # days 0,1,2 then gap, then day 4,5,6,7 -> longest run is 4
    days = [0, 1, 2, 4, 5, 6, 7]
    h = Habit("Read", "daily", completions=[base + timedelta(days=d) for d in days])
    assert analytics.longest_streak_for_habit(h) == 4


def test_longest_streak_ignores_duplicate_same_day_completions():
    base = datetime(2026, 1, 1, 8, 0)
    h = Habit("Read", "daily", completions=[base, base + timedelta(hours=2)])
    assert analytics.longest_streak_for_habit(h) == 1


def test_longest_streak_weekly_consecutive_weeks():
    base = datetime(2026, 1, 5)  # a Monday
    h = Habit("Clean", "weekly", completions=[base + timedelta(weeks=i) for i in range(3)])
    assert analytics.longest_streak_for_habit(h) == 3


def test_longest_streak_weekly_with_gap():
    base = datetime(2026, 1, 5)
    weeks = [0, 1, 3, 4, 5]  # gap at week 2 -> longest run is 3 (weeks 3,4,5)
    h = Habit("Clean", "weekly", completions=[base + timedelta(weeks=w) for w in weeks])
    assert analytics.longest_streak_for_habit(h) == 3


def test_longest_streak_all_takes_the_max_across_habits():
    base = datetime(2026, 1, 1)
    short = Habit("Short", "daily", completions=[base])
    long_ = Habit("Long", "daily", completions=[base + timedelta(days=i) for i in range(6)])
    assert analytics.longest_streak_all([short, long_]) == 6


def test_longest_streak_all_empty_list_is_zero():
    assert analytics.longest_streak_all([]) == 0


# --- Tests against the bundled 4-week example data ---

def test_fixture_has_five_habits_split_by_periodicity():
    habits = _build_example_habits()
    assert len(habits) == 5
    daily = analytics.habits_by_periodicity(habits, "daily")
    weekly = analytics.habits_by_periodicity(habits, "weekly")
    assert len(daily) == 3
    assert len(weekly) == 2


def test_fixture_drink_water_has_perfect_28_day_streak():
    habits = _build_example_habits()
    drink_water = next(h for h in habits if h.name == "Drink water")
    assert analytics.longest_streak_for_habit(drink_water) == 28


def test_fixture_exercise_streak_broken_by_gap_day():
    habits = _build_example_habits()
    exercise = next(h for h in habits if h.name == "Exercise")
    # 28 days, day 15 skipped -> longest run is max(15, 12) = 15
    assert analytics.longest_streak_for_habit(exercise) == 15


def test_fixture_meal_prep_has_perfect_4_week_streak():
    habits = _build_example_habits()
    meal_prep = next(h for h in habits if h.name == "Meal prep")
    assert analytics.longest_streak_for_habit(meal_prep) == 4


def test_fixture_longest_streak_by_name_covers_all_habits():
    habits = _build_example_habits()
    result = analytics.longest_streak_by_name(habits)
    assert set(result.keys()) == {h.name for h in habits}
    assert result["Drink water"] == 28