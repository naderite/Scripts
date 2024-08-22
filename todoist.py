import os
import requests
import csv
from dotenv import load_dotenv

# Your Todoist API token
# Load the environment variables from .env file
load_dotenv()

# Get the API token from environment variables
API_TOKEN = os.getenv("API_TOKEN")
# Endpoint URLs
TASKS_URL = "https://api.todoist.com/rest/v2/tasks"
COMPLETED_TASKS_URL = "https://api.todoist.com/sync/v9/completed/get_all"
PROJECTS_URL = "https://api.todoist.com/rest/v2/projects"
LABELS_URL = "https://api.todoist.com/rest/v2/labels"

# Headers for authentication
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def get_project_name(project_id):
    """Fetch the project name using the project ID."""
    project_url = f"{PROJECTS_URL}/{project_id}"
    response = requests.get(project_url, headers=headers)
    if response.status_code == 200:
        return response.json().get("name", "Unknown Project")
    return "Unknown Project"


def get_labels():
    """Fetch all labels and return them as a dictionary."""
    response = requests.get(LABELS_URL, headers=headers)
    if response.status_code == 200:
        labels = response.json()
        return {label["id"]: label["name"] for label in labels}
    return {}


def fetch_completed_tasks():
    """Fetch all completed tasks with pagination."""
    completed_tasks = []
    limit = 50  # Maximum number of tasks per request
    offset = 0  # Start at the beginning

    while True:
        params = {
            "limit": limit,
            "offset": offset,
        }

        response = requests.get(COMPLETED_TASKS_URL, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json().get("items", [])
            completed_tasks.extend(data)

            # If the number of completed tasks returned is less than the limit,
            # we've reached the end of the completed tasks.
            if len(data) < limit:
                break
            offset += limit  # Increase the offset to fetch the next batch

        else:
            print(f"Failed to retrieve completed tasks: {response.status_code}")
            break

    return completed_tasks


def merge_tasks(active_tasks, completed_tasks):
    """Merge active and completed tasks, removing duplicates based on task ID."""
    tasks_by_id = {}

    # Add active tasks first
    for task in active_tasks:
        tasks_by_id[task["id"]] = task

    # Add completed tasks, overwrite if there are duplicates
    for task in completed_tasks:
        task_id = task["task_id"]
        tasks_by_id[task_id] = task

    return list(tasks_by_id.values())


def fetch_tasks():
    """Fetch tasks from Todoist and save them to a CSV file."""
    print("Fetching tasks from Todoist...")

    # Fetching active tasks
    response = requests.get(TASKS_URL, headers=headers)
    if response.status_code == 200:
        active_tasks = response.json()
        print(f"Active tasks fetched successfully. Total: {len(active_tasks)}")
    else:
        print(f"Failed to retrieve tasks: {response.status_code}")
        return

    print("Fetching completed tasks...")

    # Fetching all completed tasks with pagination
    completed_tasks = fetch_completed_tasks()
    print(f"{len(completed_tasks)} completed tasks fetched successfully.")

    # Merge active and completed tasks, removing duplicates
    all_tasks = merge_tasks(active_tasks, completed_tasks)
    print(f"Total unique tasks after merging: {len(all_tasks)}")

    labels = get_labels()  # Fetch all labels
    print("Labels fetched successfully.")

    tasks_data = []

    print("Processing tasks...")

    for task in all_tasks:
        # Handle both active and completed task data structures
        task_id = task.get("id") or task.get("task_id")
        task_name = task.get("content") or task.get("task_content")
        project_name = get_project_name(task.get("project_id", "Unknown"))
        completed = "completed_at" in task  # Completed if task has a completed_at field
        completed_date = task.get("completed_at", "Not completed")

        # Handle due date: check if 'due' exists and is not None
        due = "No due date"
        if task.get("due"):
            due = task["due"].get("date", "No due date")

        # Handle description: check if 'description' exists and is not empty
        description = task.get("description", "").strip() or "No description"

        priority = task.get("priority", "N/A")
        created_date = task.get("created_at", "Unknown date")

        # Get labels for the task with error handling for missing labels
        task_labels = []
        for label_id in task.get("labels", []):
            task_labels.append(labels.get(label_id, f"{label_id}"))
        labels_str = ", ".join(task_labels) if task_labels else "No labels"

        # Append the task data to the list
        tasks_data.append(
            {
                "Task ID": task_id,
                "Task Name": task_name,
                "Project": project_name,
                "Completed": completed,
                "Completion Date": completed_date,
                "Due Date": due,
                "Priority": priority,
                "Description": description,
                "Created Date": created_date,
                "Labels": labels_str,
            }
        )

    # Check how many tasks are in the list before saving
    print(f"Number of tasks to be written to CSV: {len(tasks_data)}")

    # Save tasks data to CSV
    print("Saving data to CSV...")
    save_to_csv(tasks_data)
    print("All tasks have been successfully retrieved, processed, and saved to CSV.")


def save_to_csv(tasks_data):
    """Save task data to a CSV file."""
    csv_file_name = "todoist_tasks.csv"
    fieldnames = [
        "Task ID",
        "Task Name",
        "Project",
        "Completed",
        "Completion Date",
        "Due Date",
        "Priority",
        "Description",
        "Created Date",
        "Labels",
    ]

    # Write the data to CSV (overwriting the file each time)
    with open(csv_file_name, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()  # Write the header row
        writer.writerows(tasks_data)  # Write all tasks

    print(f"Data has been saved to {csv_file_name}")


if __name__ == "__main__":
    fetch_tasks()
