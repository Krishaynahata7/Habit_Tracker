# Habit Tracker

A small Python backend for a habit-tracking application. It lets a user
define habits, check them off, and analyze their progress. It is not a
finished product with a GUI - it is a well-tested, well-structured data
model (object-oriented core + functional analytics). 

## Requirements
- Python 3.7+
- `pytest` (for running tests only)

## Installation
```bash
cd habit_tracker
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip3 install pytest
```

## Usage
Run the app:
```bash
python3 cli.py
```
First run auto-creates 5 example habits with 4 weeks of sample data.

**Menu:**
| Option | Action |
|---|---|
| 1 | List all habits |
| 2 | Create a new habit (name + daily/weekly) |
| 3 | Check off a habit |
| 4 | Delete a habit |
| 5 | View analytics (streaks, filtered by periodicity) |
| 6 | Exit (auto-saves) |

## Running tests
```bash
python3 -m pytest tests/ -v
```
29 tests covering `Habit`, `analytics`, and `HabitManager`.

## Structure
```
habit_tracker/
├── habit.py           # Habit class (OOP)
├── storage.py         # JSON persistence + example data
├── habit_manager.py   # create/delete/lookup habits
├── analytics.py       # functional streak analysis
├── cli.py             # menu loop
└── tests/
```