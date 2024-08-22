import pandas as pd
from datetime import datetime, timedelta


def process_data() -> dict:
    # Load the CSV data
    csv_file = "todoist_tasks.csv"
    df = pd.read_csv(csv_file)

    # Convert the 'Created Date', 'Due Date', and 'Completion Date' to datetime format with UTC
    df["Created Date"] = df["Created Date"].replace("Unknown date", pd.NaT)
    df["Created Date"] = pd.to_datetime(df["Created Date"], utc=True)
    df["Due Date"] = pd.to_datetime(
        df["Due Date"], format="%Y-%m-%d", errors="coerce", utc=True
    )
    df["Completion Date"] = pd.to_datetime(
        df["Completion Date"], errors="coerce", utc=True
    )

    # Filter only completed tasks
    df_completed = df[df["Completed"] == True]

    # Define time periods
    yesterday = pd.Timestamp(datetime.now() - timedelta(days=1), tz="UTC")
    last_7_days = pd.Timestamp(datetime.now() - timedelta(days=7), tz="UTC")
    last_month = pd.Timestamp(datetime.now() - timedelta(days=30), tz="UTC")

    # Tasks completed the day before
    tasks_yesterday = df_completed[df_completed["Completion Date"] >= yesterday]

    # Tasks completed in the past 7 days
    tasks_last_7_days = df_completed[df_completed["Completion Date"] >= last_7_days]

    # Tasks completed in the past month
    tasks_last_month = df_completed[df_completed["Completion Date"] >= last_month]

    # Get the current date and time
    today = datetime.now().date()

    # Get tomorrow's date
    tomorrow = today + timedelta(days=1)

    # Get the start and end of the current week (week starts on Monday)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Filter tasks due tomorrow
    tasks_tomorrow = df[df["Due Date"].dt.date == tomorrow]

    # Filter tasks due for the rest of the week (after today)
    tasks_this_week = df[
        (df["Due Date"].dt.date > today) & (df["Due Date"].dt.date <= end_of_week)
    ]

    project_counts = df_completed["Project"].value_counts()
    label_counts = df_completed["Labels"].value_counts()

    tasks_completed_today = df[df["Completion Date"].dt.date == today]
    tasks_completed_yesterday = df[df["Completion Date"].dt.date == yesterday]

    # Exclude unwanted columns by dropping them from the DataFrame
    columns_to_drop = ["Created Date", "Description", "Completed", "Completion Date"]
    tasks_tomorrow_cleaned = tasks_tomorrow.drop(
        columns=columns_to_drop, errors="ignore"
    )
    tasks_this_week_cleaned = tasks_this_week.drop(
        columns=columns_to_drop, errors="ignore"
    )

    return {
        "tasks_yesterday": tasks_yesterday,
        "tasks_last_7_days": tasks_last_7_days,
        "tasks_last_month": tasks_last_month,
        "tasks_tomorrow": tasks_tomorrow,
        "tasks_this_week": tasks_this_week,
        "df_completed": df_completed,
        "total_tasks": len(df),
        "completed_tasks_count": len(df_completed),
        "project_counts": project_counts.to_dict(),
        "label_counts": label_counts.to_dict(),
        "tasks_completed_today": tasks_completed_today,
        "tasks_completed_yesterday": tasks_completed_yesterday,
        "tasks_tomorrow_cleaned": tasks_tomorrow_cleaned,
        "tasks_this_week_cleaned": tasks_this_week_cleaned,
        "tasks_completed_today_count": len(tasks_completed_today),
        "tasks_completed_yesterday_count": len(tasks_completed_yesterday),
        "difference_today_yesterday": len(tasks_completed_today)
        - len(tasks_completed_yesterday),
    }
