import tkinter as tk
from tkinter import ttk
import process_todoist_data as data_processor

# Get the data from the process_data function
data = data_processor.process_data()


def generate_report():
    # Extract data from the dictionary
    tasks_yesterday = data["tasks_yesterday"]
    tasks_last_7_days = data["tasks_last_7_days"]
    tasks_last_month = data["tasks_last_month"]
    project_counts = data["df_completed"]["Project"].value_counts()
    label_counts = data["df_completed"]["Labels"].value_counts()
    tasks_completed_today = data["tasks_completed_today"]
    tasks_completed_yesterday = data["tasks_completed_yesterday"]
    tasks_tomorrow = data["tasks_tomorrow_cleaned"]
    tasks_this_week = data["tasks_this_week_cleaned"]

    # Clear all text areas
    for text_widget in [
        text_yesterday,
        text_last_7_days,
        text_last_month,
        text_project,
        text_label,
        text_today_yesterday,
        text_tomorrow,
        text_this_week,
    ]:
        text_widget.delete(1.0, tk.END)

    # Helper function to insert text with specific tags
    def insert_text(text_widget, text, tag=None):
        text_widget.insert(tk.END, text + "\n", tag)

    # Insert data into the corresponding text areas

    # Number of tasks completed
    insert_text(
        text_yesterday, f"Tasks completed yesterday: {len(tasks_yesterday)}", "content"
    )
    insert_text(
        text_last_7_days,
        f"Tasks completed in the last 7 days: {len(tasks_last_7_days)}",
        "content",
    )
    insert_text(
        text_last_month,
        f"Tasks completed in the last month: {len(tasks_last_month)}",
        "content",
    )

    # Number of tasks by project
    insert_text(
        text_project, "Number of tasks completed by project:", "section_heading"
    )
    for project, count in project_counts.items():
        insert_text(text_project, f"{project}: {count}", "content")

    # Number of tasks by label
    insert_text(text_label, "Number of tasks completed by label:", "section_heading")
    for label, count in label_counts.items():
        insert_text(text_label, f"{label}: {count}", "content")

    # Compare tasks completed today and yesterday
    insert_text(
        text_today_yesterday,
        "Number of tasks completed today: {len(tasks_completed_today)}",
        "section_heading",
    )
    insert_text(
        text_today_yesterday,
        f"Number of tasks completed yesterday: {len(tasks_completed_yesterday)}",
        "content",
    )
    insert_text(
        text_today_yesterday,
        f"You did {len(tasks_completed_today) - len(tasks_completed_yesterday)} more today!",
        "content",
    )

    # Number of tasks for tomorrow and the rest of the week
    insert_text(
        text_tomorrow,
        f"Number of tasks due tomorrow: {len(tasks_tomorrow)}",
        "section_heading",
    )
    insert_text(text_tomorrow, "Tasks for tomorrow:", "section_heading")
    text_tomorrow.insert(tk.END, tasks_tomorrow.to_string(index=False), "content")

    insert_text(
        text_this_week,
        f"Number of tasks due for the rest of the week: {len(tasks_this_week)}",
        "section_heading",
    )
    insert_text(text_this_week, "Tasks for the rest of the week:", "section_heading")
    text_this_week.insert(tk.END, tasks_this_week.to_string(index=False), "content")


# Initialize the Tkinter window
root = tk.Tk()
root.title("Todoist Task Report")

# Set window size
root.geometry("900x700")

# Create a main frame
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill="both", expand=True)

# Create frames for each section
frame_yesterday = ttk.Frame(main_frame, padding="5")
frame_yesterday.pack(fill="both", expand=True)
frame_last_7_days = ttk.Frame(main_frame, padding="5")
frame_last_7_days.pack(fill="both", expand=True)
frame_last_month = ttk.Frame(main_frame, padding="5")
frame_last_month.pack(fill="both", expand=True)
frame_project = ttk.Frame(main_frame, padding="5")
frame_project.pack(fill="both", expand=True)
frame_label = ttk.Frame(main_frame, padding="5")
frame_label.pack(fill="both", expand=True)
frame_today_yesterday = ttk.Frame(main_frame, padding="5")
frame_today_yesterday.pack(fill="both", expand=True)
frame_tomorrow = ttk.Frame(main_frame, padding="5")
frame_tomorrow.pack(fill="both", expand=True)
frame_this_week = ttk.Frame(main_frame, padding="5")
frame_this_week.pack(fill="both", expand=True)

# Create text areas for each section
text_yesterday = tk.Text(
    frame_yesterday, wrap="word", bg="#f5f5f5", fg="#333", font=("Arial", 12)
)
text_yesterday.pack(expand=True, fill="both")

text_last_7_days = tk.Text(
    frame_last_7_days, wrap="word", bg="#f5f5f5", fg="#333", font=("Arial", 12)
)
text_last_7_days.pack(expand=True, fill="both")

text_last_month = tk.Text(
    frame_last_month, wrap="word", bg="#f5f5f5", fg="#333", font=("Arial", 12)
)
text_last_month.pack(expand=True, fill="both")

text_project = tk.Text(
    frame_project, wrap="word", bg="#f5f5f5", fg="#333", font=("Arial", 12)
)
text_project.pack(expand=True, fill="both")

text_label = tk.Text(
    frame_label, wrap="word", bg="#f5f5f5", fg="#333", font=("Arial", 12)
)
text_label.pack(expand=True, fill="both")

text_today_yesterday = tk.Text(
    frame_today_yesterday, wrap="word", bg="#f5f5f5", fg="#333", font=("Arial", 12)
)
text_today_yesterday.pack(expand=True, fill="both")

text_tomorrow = tk.Text(
    frame_tomorrow, wrap="word", bg="#f5f5f5", fg="#333", font=("Arial", 12)
)
text_tomorrow.pack(expand=True, fill="both")

text_this_week = tk.Text(
    frame_this_week, wrap="word", bg="#f5f5f5", fg="#333", font=("Arial", 12)
)
text_this_week.pack(expand=True, fill="both")

# Add some styling
root.configure(bg="#e0e0e0")

# Customize text area style
for text_widget in [
    text_yesterday,
    text_last_7_days,
    text_last_month,
    text_project,
    text_label,
    text_today_yesterday,
    text_tomorrow,
    text_this_week,
]:
    text_widget.tag_configure(
        "heading", font=("Arial", 12, "bold"), foreground="#00796b"
    )
    text_widget.tag_configure(
        "section_heading", font=("Arial", 12, "bold"), foreground="#004d40"
    )
    text_widget.tag_configure("content", font=("Arial", 12), foreground="#333")

# Generate the report automatically on startup
generate_report()

# Start the Tkinter main loop
root.mainloop()
