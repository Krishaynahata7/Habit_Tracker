"""
analytics.py
------------
The functional counterpart to the object-oriented Habit/HabitManager
model. Every function here is pure: it takes a list of Habit objects
(or a single Habit) as input and returns a result, without mutating
anything or relying on accumulator variables. Streak counting is done
via itertools.groupby to find runs of consecutive periods, combined
with map() and functools.reduce() rather than an explicit running
counter.
"""

import functools
import itertools
from datetime import timedelta


def list_all_habits(habits):
    """Return the names of every tracked habit."""
    return list(map(lambda h: h.name, habits))


def habits_by_periodicity(habits, periodicity):
    """Return all habits that share the given periodicity, via filter()."""
    return list(filter(lambda h: h.periodicity == periodicity, habits))


def _period_index(dt, periodicity):
    """
    Map a completion timestamp to an integer 'period index' such that
    two completions are in the same period if they map to the same
    index, and consecutive periods map to consecutive integers. This
    lets streaks be found with plain integer arithmetic regardless of
    whether the habit is daily or weekly.
    """
    date = dt.date()
    if periodicity == "daily":
        return date.toordinal()
    elif periodicity == "weekly":
        monday = date - timedelta(days=date.weekday())
        return monday.toordinal() // 7
    raise ValueError(f"Unknown periodicity: {periodicity!r}")


def _consecutive_runs(sorted_unique_ints):
    """
    Split a sorted list of unique integers into runs of consecutive
    values, e.g. [1,2,3,7,8,10] -> [[1,2,3],[7,8],[10]].
    Uses the standard groupby(value - index) trick instead of a
    hand-rolled accumulator loop.
    """
    groups = itertools.groupby(enumerate(sorted_unique_ints), key=lambda pair: pair[1] - pair[0])
    return [list(map(lambda pair: pair[1], group)) for _, group in groups]


def longest_streak_for_habit(habit):
    """
    The longest run of consecutive periods (days or weeks, depending
    on the habit's periodicity) in which the habit was completed at
    least once.
    """
    periods = sorted(set(map(lambda c: _period_index(c, habit.periodicity), habit.completions)))
    if not periods:
        return 0
    run_lengths = list(map(len, _consecutive_runs(periods)))
    return functools.reduce(max, run_lengths)


def longest_streak_all(habits):
    """
    The single longest streak across every tracked habit, found by
    mapping each habit to its own longest streak and reducing to the
    maximum.
    """
    if not habits:
        return 0
    streaks = list(map(longest_streak_for_habit, habits))
    return functools.reduce(max, streaks)


def longest_streak_by_name(habits):
    """Convenience view: {habit_name: longest_streak} for every habit."""
    return {h.name: longest_streak_for_habit(h) for h in habits}