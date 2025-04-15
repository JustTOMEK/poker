import itertools

# Example 5-element set
my_set = [1, 2, 3, 4, 5]

# Get all 3-element combinations
combinations = list(itertools.combinations(my_set, 3))

# Print the result
for combo in combinations:
    print(combo)
