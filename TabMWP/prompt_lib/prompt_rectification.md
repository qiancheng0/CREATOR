### Instruction
Your original codes have met some errors when executing, please rectify your codes.
You should generate the whole one new piece of code, instead of generating a snippet.
Wrap your code in ```python\n ... \n``` to make it a one whole code block.
Pay attention to the conditions in question before modifying.
Your goal is answer the question correctly instead of just execute the code successfully.
If necessary, you can also generate a whole new tool. Change your way of thinking to solve the problem.

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
### Original Codes
```python
import pandas as pd
def find_received_money(df):
    """
    This function takes in a pandas dataframe of financial records, and returns the amount of money received in a given date.
    """
    # get the row where description is paycheck
    paycheck_row = df[df['Description'] == 'payment']
    # get the 'Received' value from that row
    received_money = paycheck_row['Received'].iloc[0]
    return received_money

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
### Error Information
Traceback (most recent call last):
  File "test_code.py", line 26, in <module>
    received = find_received_money(df)
  File "test_code.py", line 14, in find_received_money
    received_money = paycheck_row['Received'].iloc[0]
IndexError: single positional indexer is out-of-bounds
### Rectified Code
Index is out of bound, which means we haven't got any element in the paycheck row. Further checking the code, we find that the description of the paycheck is wrong. We should change it from 'payment' to 'paycheck'.
```python
import pandas as pd
def find_received_money(df):
    """
    This function takes in a pandas dataframe of financial records, and returns the amount of money received in a given date.
    """
    # Modify here from payment to paycheck, which should be in the dataframe
    paycheck_row = df[df['Description'] == 'paycheck']
    # get the 'Received' value from that row
    received_money = paycheck_row['Received'].iloc[0]
    return received_money

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
===table===
### Question
===qst===
### Original Codes
===ori===
### Error Information
===err===
### Rectified Code