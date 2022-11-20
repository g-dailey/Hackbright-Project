import pandas as pd
import csv

filename = 'Leetcode-data - leetcode (1).csv'

with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
      split_data = row[0].split("--")
      prompt_name, prompt_link, prompt_difficulty = split_data
      print(prompt_name)

        # print(row)


# leetcode_prompt = pd.read_csv('Leetcode-data - leetcode.csv')
# leetcode_data = pd.DataFrame(leetcode_prompt)
# print(type(leetcode_data))