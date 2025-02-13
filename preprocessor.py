import pandas as pd
import re

def preprocess(data):
    pattern = r'\d{2}/\d{2}/\d{2}, \d{2}:\d{2}:\d{2}\]?\s*'  # Match date & time
    messages = re.split(pattern, data)[1:]  # Extract messages
    dates = re.findall(pattern, data)  # Extract dates

    # Ensure messages and dates have the same length
    min_len = min(len(messages), len(dates))
    messages, dates = messages[:min_len], dates[:min_len]

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Clean up message_date column
    df['message_date'] = df['message_date'].str.replace(']', '', regex=True).str.strip()

    # Convert to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M:%S', errors='coerce')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    new_messages = []

    for message in df['user_message']:
        if not isinstance(message, str):  # Ensure it's a string
            message = str(message)

        entry = message.split(': ', 1)  # Split at the first ': ' occurrence

        if len(entry) == 2:
            users.append(entry[0].strip())  # Username
            new_messages.append(entry[1].strip())  # Actual message
        else:
            users.append("Group_Notification")
            new_messages.append(entry[0].strip())

    df['user'] = users
    df['message'] = new_messages

    df.drop(columns=['user_message'], inplace=True)

    # Extract Date & Time Components
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
