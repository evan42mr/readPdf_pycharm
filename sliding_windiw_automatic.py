# Choose the number of lines before and after page breaker

from difflib import SequenceMatcher
import pprint

# file_name = 'KOGAS -2449.txt'
# file_name = 'ON -2462.txt'
# file_name = 'ABB1F.txt'
file_name = 'Shipyard.txt'


# TODO
# Find page breakers and identify
# the size of it

def mean(a):
    return sum(a) / len(a)


pagebrk = ''
list_of_pgbrk = []
window_size = 10

pgbrk = False
lines_after_pgbrk = 0

with open(file_name) as f:
    temp_window = []
    count = 0

    # Store all the sliding windows that contain pgbrk
    for line in f:

        # Create a window
        temp_window.append(line)

        if len(temp_window) > window_size:
            temp_window.pop(0)

        # Identify page breaker
        if line[0] == '\x0c':
            pgbrk = True

        if lines_after_pgbrk >= 5:
            list_of_pgbrk.append(temp_window)

            lines_after_pgbrk = 0
            pgbrk = False
            temp_window = []

        if pgbrk and lines_after_pgbrk < 6:
            lines_after_pgbrk += 1

# print(list_of_pgbrk)

# print(list_of_pgbrk[int(len(list_of_pgbrk)/2)])

testing_pgbrk = list_of_pgbrk[int(len(list_of_pgbrk) / 2)]

list_of_statistics = []

for item in list_of_pgbrk:
    item_stats = []
    for i in range(len(item)):
        ratio = round(SequenceMatcher(None, testing_pgbrk[i], item[i]).ratio(), 1)
        item_stats.append(ratio)

    list_of_statistics.append(item_stats)

# pp.pprint(list_of_pgbrk[67])
# print(list_of_pgbrk[27])
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(list_of_statistics)


# print(list_of_statistics)
print(list(map(mean, zip(*list_of_statistics))))
