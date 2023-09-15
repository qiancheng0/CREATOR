You are asked to write python code to solve the problem. After seeing the question, generate a code script line by line.
Add comment before each line of code to explain what the code does. Please wrap all your codes and comments in ```python ... ``` after "### Response".

Here is an demonstration example. You can follow this format, but the content of your problem and solution should be different.
### Problem
What's the least number of time should I do /N or -1 to get 0 from 17?
### Constants
N (int): the number to divide, we set it to 2 in this problem.
### Response
```python
# initialize the number
number = 17
# initialize the count
count = 0
# while the number is not 0
while number != 0:
    # if the number is even, do /2
    if number % 2 == 0:
        number = number / 2
    # if the number id odd, do -1
    else:
        number = number - 1
    # add 1 to the count
    count += 1
# print out the final count as answer
print(count)
```

### Problem
===qst===
### Constants
===constants===
### Response