import subprocess
import platform

TASKS_FILE = "tasks.txt"


def clear_terminal():
    system_platform = platform.system().lower()
    if system_platform == "windows":
        subprocess.run(["cls"], shell=True)
    else:
        subprocess.run(["clear"])


def show_tasks(tasks):
    print("Your tasks:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")


def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            tasks = [line.strip() for line in file.readlines()]
        return tasks
    except FileNotFoundError:
        return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        for task in tasks:
            file.write(task + "\n")


def add_task(tasks):
    new_task = input("Enter the new task: ")
    tasks.append(new_task)
    save_tasks(tasks)
    print("Task added successfully!")


def main():
    tasks = load_tasks()

    while True:
        show_tasks(tasks)

        choice = input(
            "\nDo you want to (A)dd a new task, (F)inish a task, or (Q)uit? "
        ).lower()

        if choice == "a":
            add_task(tasks)
        elif choice == "f":
            if not tasks:
                print("No tasks to finish.")
            else:
                show_tasks(tasks)
                task_number = int(input("Enter the number of the task you finished: "))
                if 1 <= task_number <= len(tasks):
                    finished_task = tasks.pop(task_number - 1)
                    save_tasks(tasks)
                    print(f"Task '{finished_task}' marked as finished.")
                else:
                    print("Invalid task number.")
        elif choice == "q":
            print("Exiting task manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 'A', 'F', or 'Q.'")


if __name__ == "__main__":
    clear_terminal()
    main()
