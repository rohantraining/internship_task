import pandas as pd
from datetime import datetime, timedelta

# Assuming the input file is a CSV file
file_path = 'Assignment_Timecard.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Convert 'Time' and 'Time Out' columns to datetime objects
df['Time'] = pd.to_datetime(df['Time'])
df['Time Out'] = pd.to_datetime(df['Time Out'])

# Sort the DataFrame by 'Employee Name' and 'Time'
df = df.sort_values(by=['Employee Name', 'Time'])

# Function to check consecutive days
def has_consecutive_days(series):
    return any((series - series.shift(1)).dt.days == 1)

# Function to check time between shifts and total hours in a single shift
def analyze_shifts(group):
    consecutive_days = has_consecutive_days(group['Time'].dt.date)
    time_between_shifts = (group['Time'] - group['Time Out'].shift(1)).astype('timedelta64[h]')
    total_hours = (group['Time Out'] - group['Time']).sum().seconds / 3600

    return consecutive_days, any((1 < time_between_shifts) & (time_between_shifts < 10)), total_hours > 14

# Group by 'Employee Name' for analysis
grouped = df.groupby('Employee Name')

# Iterate through groups and print results
for name, group in grouped:
    consecutive, time_between, total_hours = analyze_shifts(group)

    if consecutive:
        print(f"{name} has worked for 7 consecutive days.")

    if time_between:
        print(f"{name} has less than 10 hours between shifts but greater than 1 hour.")

    if total_hours:
        print(f"{name} has worked for more than 14 hours in a single shift.")
