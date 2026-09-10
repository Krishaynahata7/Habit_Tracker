"""
Unit tests for habit.py, developed in isolation as i have mentioned in the conception phase roadmap.
"""

import sys
import os
from datetime import datetime

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from habit import Habit


def test_create_valid_habit():
    h = Habit("Read", "daily")
    assert h.name == "Read"
    assert h.periodicity == "daily"
    assert h.completions == []
    assert isinstance(h.created_at, datetime)


def test_empty_name_raises():
    with pytest.raises(ValueError):
        Habit("", "daily")


def test_invalid_periodicity_raises():
    with pytest.raises(ValueError):
        Habit("Read", "monthly")


def test_check_off_appends_timestamp():
    h = Habit("Read", "daily")
    when = datetime(2026, 1, 1, 9, 0)
    returned = h.check_off(when)
    assert returned == when
    assert h.completions == [when]


def test_check_off_defaults_to_now():
    h = Habit("Read", "daily")
    before = datetime.now()
    h.check_off()
    after = datetime.now()
    assert len(h.completions) == 1
    assert before <= h.completions[0] <= after


def test_to_dict_from_dict_roundtrip():
    created = datetime(2026, 1, 1, 8, 0)
    completions = [datetime(2026, 1, 1, 9, 0), datetime(2026, 1, 2, 9, 0)]
    h = Habit("Read", "daily", created_at=created, completions=completions)

    data = h.to_dict()
    assert data["name"] == "Read"
    assert data["periodicity"] == "daily"
    assert data["created_at"] == created.isoformat()
    assert data["completions"] == [c.isoformat() for c in completions]

    rebuilt = Habit.from_dict(data)
    assert rebuilt == h


def test_equality_is_value_based():
    created = datetime(2026, 1, 1)
    h1 = Habit("Read", "daily", created_at=created)
    h2 = Habit("Read", "daily", created_at=created)
    assert h1 == h2

    h2.check_off(datetime(2026, 1, 2))
    assert h1 != h2