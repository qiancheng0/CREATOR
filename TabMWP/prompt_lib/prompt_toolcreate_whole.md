### Instruction
You are given a question with tabular contents, and you need to create python tool (function) to solve it.
You can use pandas, numpy, math, etc. or other packages if necessary.
You are given a dataframe about a table. The first row is the name for each column. Each column is seperated by "|" and each row is seperated by "\n".
Pay attention to the format of the table, and what the question asks.
You could organize your data format in the way that is most convenient for you to solve the problem.
Please first think step by step about what tool to create, and how it is related to the problem.
In your response, please first generate the tools (functions), then call the tool to solve the problem, and finally print out your answer.
Please wrap your codes in ```python ... ``` to make it one whole code block.

### Table
Name: None
Unit: $
Content:
Date | Description | Received | Expenses | Available Funds
 | Balance: end of July | | | $260.85
8/15 | tote bag | | $6.50 | $254.35
8/16 | farmers market | | $23.40 | $230.95
8/22 | paycheck | $58.65 | | $289.60
### Question
This is Akira's complete financial record for August. How much money did Akira receive on August 22?
### Thoughts and Code
To solve the problem of finding out how much money Akira received on August 22, we need to look at the "Received" column in the row where the "Description" column contains the word "paycheck". Then we should retrieve the element, which should be the final answer.
```python
import pandas as pd
def find_received_money(df):
    """
    This function takes in a pandas dataframe of financial records, and returns the amount of money received in a given date.
    Args:
    df (pandas.DataFrame): A pandas DataFrame object containing financial records.
    The dataframe should contain "Date", "Description", "Received", "Expenses", "Available Funds".
    Returns:
    float: The amount of money received in a given date.
    """
    # get the row where description is paycheck
    paycheck_row = df[df['Description'] == 'paycheck']
    # get the 'Received' value from that row
    received_money = paycheck_row['Received'].iloc[0]
    return received_money

# Initialize the table into a dataframe
df = pd.DataFrame({
    'Date': [' ', '8/15', '8/16', '8/22'],
    'Description': ['Balance: end of July', 'tote bag', 'farmers market', 'paycheck'],
    'Received': ['', '', '', 58.65],
    'Expenses': ['', 6.50, 23.40, ''],
    'Available Funds': [260.85, 254.35, 230.95, 289.60]
})
# Call the tool to solve the problem
received = find_received_money(df)
# Print the answer
print("The amount of money received is", received)
```

### Table
Name: Orange candies per bag
Unit: bags
Content:
Stem | Leaf 
2 | 2, 3, 9
3 | 
4 | 
5 | 0, 6, 7, 9
6 | 0
7 | 1, 3, 9
8 | 5
### Question
A candy dispenser put various numbers of orange candies into bags. How many bags had at least 32 orange candies?
### Thoughts and Code
Stem and leaf is a way to organize data. Stem represents the first digit (tenth digit) of the data, and leaf represents the last digit (unit digit) of the data.
To solve the problem of finding the number of bags that had at least 32 orange candies, we need to first calculate the total number of orange candies in each bag by multiplying the stem value by 10 and adding the digits in the leaf. Then, we can filter the rows where the total number of orange candies is greater than or equal to 32 and count the number of rows.
```python
import pandas as pd
def count_bags_with_32_orange_candies(df):
    """
    This function takes in a pandas dataframe of orange candies per bag, and returns the number of bags that have at least 32 orange candies.
    Args:
    df (pandas.DataFrame): A pandas DataFrame object containing the number of orange candies per bag.
    The dataframe should contain "Stem" and "Leaf" columns.
    Returns:
    int: The number of bags that have at least 32 orange candies.
    """
    # prepare a list to calculate candies in each bag
    candies = []
    # calculate the total number of orange candies in each bag
    for i in range(len(df)):
        stem = df['Stem'][i]
        leaf = df['Leaf'][i]
        for j in range(len(leaf)):
            candies.append(stem * 10 + leaf[j])
    # filter the bags where the total number of orange candies is greater than or equal to 32
    filtered = [candy for candy in candies if candy >= 32]
    # count the number of rows
    num_bags = len(filtered)
    return num_bags

# Initialize the table into a dataframe
df = pd.DataFrame({
    'Stem': [2, 3, 4, 5, 6, 7, 8],
    'Leaf': [[2, 3, 9], [], [], [0, 6, 7, 9], [0], [1, 3, 9], [5]]
})
# Call the tool to solve the problem
num_bags = count_bags_with_32_orange_candies(df)
# Print the answer
print("The number of bags with at least 32 orange candies is", num_bags)
```

### Table
Name: None
Unit: $
Content:
Number of pairs of boots | Frequency
0 | 12
1 | 17
2 | 7
3 | 20
### Question
Some students compared how many pairs of boots they own. How many students own fewer than 2 pairs of boots?
### Thoughts and Code
We can use pandas to read the table and get the row where the number of pairs of boots is less than 2. Then we can sum the 'Frequency' column for that row to get the number of students that own fewer than 2 pairs of boots.
```python
import pandas as pd
def students_with_less_than_2_pairs(df):
    """
    This function takes in a pandas dataframe of pairs of boots owned by students, and returns the number of students that own fewer than 2 pairs of boots.
    Args:
    df (pandas.DataFrame): A pandas DataFrame object containing the number of pairs of boots and its frequency.
    The dataframe should contain "Number of pairs of boots" and "Frequency".
    Returns:
    int: The number of students that own fewer than 2 pairs of boots.
    """
    # get the row where the number of pairs of boots is less than 2
    less_than_2 = df[df['Number of pairs of boots'] < 2]
    # sum the 'Frequency' column for that row
    num_students = less_than_2['Frequency'].sum()
    return num_students

# The tool takes into a dataframe, so we need to convert the table into a dataframe
df = pd.DataFrame({
    'Number of pairs of boots': [0, 1, 2, 3],
    'Frequency': [12, 17, 7, 20]
})
# Call the tool to solve the problem
num_students = students_with_less_than_2_pairs(df)
# Print the answer
print("The number of students that own fewer than 2 pairs of boots is", num_students)
```

### Table
Name: Amount Dean spent on lunch
Unit: $, per day
Content:
Day | Amount spent
Tuesday | $3
Wednesday | $2
Thursday | $9
Friday | $9
Saturday | $8
### Question
In trying to calculate how much money could be saved by packing lunch, Dean recorded the amount he spent on lunch each day. According to the table, what was the rate of change between Thursday and Friday?
### Thoughts and Code
Rate of change = change in value / change in time. In this case, the change in value is the change in the amount of money spent on lunch, and the change in time is the change in the day of the week. We could create a tool that takes in the table and returns the rate of change between Thursday and Friday.
```python
import pandas as pd
def rate_of_change(df, day1, day2):
    """
    This function takes in a pandas dataframe of amounts spent on lunch and two days of the week, and returns the rate of change between those two days.
    Args:
    df (pandas.DataFrame): A pandas DataFrame object containing the days of the week and their corresponding amount spent on lunch.
    The dataframe should contain "Day" and "Amount spent".
    day1 (str): A string representing the first day of the week to calculate the rate of change.
    day2 (str): A string representing the second day of the week to calculate the rate of change.
    Returns:
    float: The rate of change between the two days.
    """
    # get the row for each day
    day1_row = df[df['Day'] == day1]
    day2_row = df[df['Day'] == day2]
    # get the amount spent for each day
    day1_amount = day1_row['Amount spent'].values[0]
    day2_amount = day2_row['Amount spent'].values[0]
    # calculate the rate of change
    rate_of_change = (day2_amount - day1_amount) / 1
    return rate_of_change

# The tool takes into a dataframe, so we need to convert the table into a dataframe
df = pd.DataFrame({
    'Day': ['Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
    'Amount spent': [3, 2, 9, 9, 8]
})
# Call the tool to solve the problem
rate = rate_of_change(df, 'Thursday', 'Friday')
# Print the answer
print("The rate of change between Thursday and Friday is $", rate, "per day.")
```

### Table
===table===
### Question
===qst===
### Thoughts and Code