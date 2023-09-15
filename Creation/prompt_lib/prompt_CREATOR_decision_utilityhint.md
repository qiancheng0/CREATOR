You are asked to use the tool you have just created to solve the problem.
After seeing the question, you should read carefully about the tool's documentation and unserstand how and when to correctly use it.
In your response, please make use of the tool to solve the problem, and finally print the answer.
Please wrap your decision code in ```python ... ``` in your response.

===> start
### Problem
What's the least number of time should I do /N or -1 to get 0 from 17?
### Constants
N (int): the number to divide, we set it to 2 in this problem.
### Hints
You might use the following hints about what tool to create:
The tool should take a start number as input, do operations and accumulate the count, and return the count.
### Tool
```python
def strategy_count(start_number: int) -> int:
    """
    This tool returns the number of times we should do /2 or -1 to get 0 from start_number.
    Args:
    start_number (int): the starting number
    Returns:
    count (int): The least number of operations needed
    """
    x = start_number
    count = 0
    while True:
        if x == 0:
            return count
        # We can directly use the constant value 2 here
        if x % 2 == 0:
            x = x / 2
        else:
            x = x - 1
        count += 1
```
### Response
```python
# Call the strategy to solve the problem
count = strategy_count(17)
# print out the answer
print("The least number of operations neded is", count)
```

===> start
### Problem
===qst===
### Constants
===constants===
### Hints
===hints===
### Tool
===tool===
### Response