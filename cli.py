"""
cli.py
------
The only piece of the app the user directly interacts with: a simple
numbered-menu loop built on input(). It delegates every real operation
to HabitManager, and fetches the current habit list from the manager to
hand to analytics.py - so analytics stays a decoupled, pure module that
cli.py is simply the one wiring together.
"""

import sys

import analytics
from habit_manager import HabitManager, HabitAlreadyExistsError, HabitNotFoundError

MENU = """
==================== Habit Tracker =====================
1. List all habits
2. Create a new habit
3. Check off a habit
4. Delete a habit
5. View analytics
6. Exit
==========================================================
"""


def _prompt(text):
    return input(text).strip()


def _choose_habit_name(manager):
    habits = manager.list_habits()
    if not habits:
        print("No habits yet.")
        return None
    for i, h in enumerate(habits, start=1):
        print(f"  {i}. {h.name} ({h.periodicity})")
    choice = _prompt("Enter the habit name: ")
    return choice


def action_list_habits(manager):
    habits = manager.list_habits()
    if not habits:
        print("No habits defined yet.")
        return
    print("\nYour habits:")
    for h in habits:
        print(f"  - {h.name} [{h.periodicity}] - {len(h.completions)} completions")


def action_create_habit(manager):
    name = _prompt("Habit name: ")
    periodicity = _prompt("Periodicity (daily/weekly): ").lower()
    try:
        manager.create_habit(name, periodicity)
        print(f"Created habit '{name}'.")
    except (ValueError, HabitAlreadyExistsError) as e:
        print(f"Could not create habit: {e}")


def action_check_off(manager):
    name = _choose_habit_name(manager)
    if name is None:
        return
    try:
        manager.check_off(name)
        print(f"Checked off '{name}'.")
    except HabitNotFoundError as e:
        print(f"Error: {e}")


def action_delete_habit(manager):
    name = _choose_habit_name(manager)
    if name is None:
        return
    try:
        manager.delete_habit(name)
        print(f"Deleted habit '{name}'.")
    except HabitNotFoundError as e:
        print(f"Error: {e}")


def action_view_analytics(manager):
    habits = manager.list_habits()
    if not habits:
        print("No habits to analyze yet.")
        return

    print("\n--- Analytics ---")
    print("All habits:", ", ".join(analytics.list_all_habits(habits)))

    for periodicity in ("daily", "weekly"):
        names = analytics.list_all_habits(analytics.habits_by_periodicity(habits, periodicity))
        print(f"{periodicity.capitalize()} habits:", ", ".join(names) if names else "(none)")

    print("Longest streak per habit:")
    for name, streak in analytics.longest_streak_by_name(habits).items():
        print(f"  - {name}: {streak}")

    print(f"Longest streak overall: {analytics.longest_streak_all(habits)}")


ACTIONS = {
    "1": action_list_habits,
    "2": action_create_habit,
    "3": action_check_off,
    "4": action_delete_habit,
    "5": action_view_analytics,
}


def run(manager=None):
    manager = manager or HabitManager()
    print("Welcome to your Habit Tracker.")

    while True:
        print(MENU)
        choice = _prompt("Choose an option (1-6): ")

        if choice == "6":
            print("Goodbye!")
            break

        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid choice, please pick a number from 1 to 6.")
            continue

        action(manager)


if __name__ == "__main__":
    try:
        run()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
        sys.exit(0)