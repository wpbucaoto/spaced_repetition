Spaced Repetition Program

This program implements a spaced repetition system (SRS) to enhance learning retention
by scheduling review dates for topics based on the Ebbinghaus forgetting curve. It utilizes
a SQLite database to store topics and their associated review dates.

Features:
- Log new topics with calculated review dates.
- Monthly and weekly reviews to display topics that need review within the current month or week.
- Option to delete all stored topics.

Database Structure:
The program maintains a single table 'topics' in the SQLite database 'spaced_repetition.db':
- id: INTEGER (Primary Key)
- topic: TEXT (Name of the topic)
- initial_date: TEXT (Date when the topic was logged)
- review_dates: TEXT (Comma-separated list of review dates)

Functions:
- calculate_review_dates(initial_date): Computes review dates based on an initial date.
- log_topic(topic): Logs a new topic with calculated review dates into the database.
- monthly_review(): Displays topics scheduled for review within the current month.
- weekly_review(): Displays topics scheduled for review within the current week.
- delete_all_topics(): Deletes all entries from the 'topics' table.

Usage:
Upon running the program, users can log new topics, review topics scheduled for the current
month or week, delete all stored topics, or exit the program.

Note:
Ensure 'sqlite3' and 'json' Python modules are installed for proper functionality.

Author: Wilson Bucaoto
Last Updated: 25 June 2023
