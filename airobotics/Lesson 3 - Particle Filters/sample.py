import random

p = [1, 2, 3, 4]
w = [2,3,1,2]
p3 = []
for _ in range(len(p)):
    current_index = random.randrange(0, len(p))
    total_probability = sum(w)
    weighted_normalized = [x / total_probability for x in w]
    current_value = weighted_normalized[current_index]
    final_value = current_value + random.random()

    while current_value < final_value:
        current_index -= 1
        current_value += weighted_normalized[current_index]
    p3.append(p[current_index])

print p3