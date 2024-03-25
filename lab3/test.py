my_list = [None, 1, 0, -1]

# Filter out None values and get the maximum
max_value = max(item for item in my_list if item is not None)

print(max_value)
