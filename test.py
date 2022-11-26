import pandas as pd
import csv

user_filename = 'User-data.csv'

with open(user_filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        split_data = row[0].split("--")

        first_name_data, last_name_data, email_data, pwd_data, prompt_diff_data, primary_lang_data, timezone_data, prog_name_data, selected_timeslots_data = split_data
        print(timezone_data)