import string
import random

letters = string.ascii_uppercase
result_str = "".join(random.choice(letters) for i in range(6))
print(result_str)
