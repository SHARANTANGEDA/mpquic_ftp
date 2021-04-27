delay = "["
for num in range(50, 86):
    delay += f'\"{num}ms\", '

delay += "]"
print(delay)