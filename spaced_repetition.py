"""
Spaced Repetition Python Script

Author: Wilson Bucaoto

Description:
This script implements a Spaced Repetition System (SRS) using SQLite, allowing users to log topics
and schedule review dates based on intervals for effective learning retention.

Functions:
- log_topic(topic): Add a new topic with calculated review dates.
- monthly_review(): List topics due for review this month.
- weekly_review(): Display topics due for review this week.
- delete_all_topics(): Remove all logged topics.

Database Structure:
- Table 'topics': id (INTEGER), topic (TEXT), initial_date (TEXT), review_dates (TEXT)

Usage:
Run the script and follow prompts to log topics, review scheduled topics, delete entries, or exit.

Note:
Requires 'sqlite3' and 'json' modules.
"""


import sqlite3
import json
from datetime import datetime, timedelta

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('spaced_repetition.db')
c = conn.cursor()

# Create a table to store topics and review dates
c.execute('''
CREATE TABLE IF NOT EXISTS topics(
    id INTEGER PRIMARY KEY,
    topic TEXT,
    initial_date TEXT,
    review_dates TEXT
)
''')
conn.commit()

def calculate_review_dates(initial_date):
    """Calculate review dates based on initial date."""
    intervals = [1, 6, 14, 30, 66, 150, 360]
    review_dates = [(initial_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in intervals]
    return review_dates

def log_topic(topic):
    """Log new topic with calculated review dates"""
    initial_date = datetime.now()
    review_dates = calculate_review_dates(initial_date)
    review_dates_str = ','.join(review_dates)

    c.execute('INSERT INTO topics (topic, initial_date, review_dates) VALUES (?, ?, ?)',
              (topic, initial_date.strftime('%Y-%m-%d'), review_dates_str))
    # Commit the transaction
    conn.commit()
    print(f"Topic '{topic}' logged with Review dates: {review_dates}")

def monthly_review():
    """Show topics that needs to be reviewed this month"""
    # Get the first day of the current month
    today = datetime.now()
    start_of_month = today.replace(day=1)
    next_month = (start_of_month + timedelta(days=30)).replace(day=1)

    # select topics and their review dates
    c.execute('SELECT topic, review_dates FROM topics')
    rows = c.fetchall()

    # Filter and display topics that need to be reviewed this month
    topics_to_review = []
    for row in rows:
        topic, review_dates_str = row
        review_dates = review_dates_str.split(',')
        for review_date in review_dates:
            review_date_dt = datetime.strptime(review_date, '%Y-%m-%d')
            if start_of_month <= review_date_dt < next_month:
                topics_to_review.append((topic, review_date))

    if topics_to_review:
        print("Topics to review this month:")
        for topic, review_date in topics_to_review:
            print(f"- {topic} (Review Date: {review_date})")
    else:
        print("No topics to review this month.")

def weekly_review():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('spaced_repetition.db')
        cursor = conn.cursor()

        # Get today's date and the start of the current week
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())  # Monday of the current week
        end_of_week = start_of_week + timedelta(days=6)  # Sunday of the current week

        # Execute SQL to select topics and their review dates within the current week
        cursor.execute('SELECT topic, review_dates FROM topics')

        # Fetch all rows and filter for topics needing review within the current week
        rows = cursor.fetchall()
        for topic, review_dates_str in rows:
            review_dates = review_dates_str.split(',')
            review_dates = [date.strip() for date in review_dates]  # Remove leading/trailing spaces

            # Filter valid dates within the current week
            review_dates_within_week = []
            for date_str in review_dates:
                try:
                    date = datetime.strptime(date_str, '%Y-%m-%d')
                    if start_of_week.date() <= date.date() <= end_of_week.date():
                        review_dates_within_week.append(date_str)
                except ValueError:
                    print(f"Ignoring invalid date format: {date_str}")

            if review_dates_within_week:
                print(f"Topic: {topic}, Review Dates: {', '.join(review_dates_within_week)}")

    except sqlite3.Error as e:
        print(f"SQLite error: {str(e)}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the connection
        if conn:
            conn.close()


def delete_all_topics():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('spaced_repetition.db')
        cursor = conn.cursor()

        # Execute SQL to delete all rows from the topics table
        cursor.execute('DELETE FROM topics')

        # Commit the transaction
        conn.commit()

        print("All entries deleted successfully.")

    except sqlite3.Error as e:
        print(f"SQLite error: {str(e)}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the connection
        if conn:
            conn.close()

def main():
    while True:
        command = input("Enter a command: 'Log Topic' or 'Monthly/Weekly Review' or 'Delete Entries' or 'Exit': ").strip()
        if command.lower() == 'log topic':
            topic = input("Enter a topic learned today").strip()
            log_topic(topic)
        elif command.lower() == 'monthly review':
            monthly_review()
        elif command.lower() == 'weekly review':
            weekly_review()
        elif command.lower() == 'delete entries':
            delete_all_topics()
        elif command.lower() == 'exit':
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == '__main__':
    main()

# Close the database connection when the program exits
conn.close()

