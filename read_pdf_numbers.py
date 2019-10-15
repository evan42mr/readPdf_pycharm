import re
import pprint
import operator
import pprint
from difflib import SequenceMatcher

NEW_PAGE = '----------------> new page <---------------\n'

"""
Removes number lines from pdf file
"""


def remove_numbers(FILE_NAME):
    dict_of_spaces = {}
    lst_spaces = []

    line_leading_spaces = 0
    with open(FILE_NAME) as f:
        for line in f:
            if line.strip() and (line[0].isdigit() or line[1].isdigit()) and line.find('......') == -1:
                # Found a line with the number at the beginning
                if line.split()[0].isdigit():

                    # Position number of the digit of each line, plus it's length
                    char_num = line.find(line.split()[0]) + len(line.split()[0])

                    line_without_number = line[char_num:]
                    # count the leading spaces in a string
                    line_leading_spaces = len(line_without_number) - len(line_without_number.lstrip(' '))
                    # Stopping condition is the first line with a number
                    if line_without_number.strip():
                        break
    text = ''

    with open(FILE_NAME) as f:
        # length of the number character on a line
        char_num = 2
        count = 0
        lst_line = []
        for i, line in enumerate(f):

            # Found the end of a page
            if line[0] == '\x0c':
                # print(NEW_PAGE)
                line = line[1:]
                text += NEW_PAGE

            # Check if the line is not empty and first or second characters are digits
            # And line doesn't belong to a table of contents
            if line.strip() and (line[0].isdigit() or line[1].isdigit()) \
                    and line.find('......') == -1 \
                    and line.split()[0].isdigit():  # Found a line with the number at the beginning
                # print(f"line if: {line}")
                # Slice the line so the sentence starts after the number
                # Discard if the line is empty

                # Position number of the digit of each line, plus it's length
                if line.find(line.split()[0]) + len(line.split()[0]) > 2:
                    char_num = line.find(line.split()[0]) + len(line.split()[0])

                line_without_number = line[char_num + line_leading_spaces:]

                # When concatenate '\n' to a string it just concatenate ''
                # Thus we check if line is empty or == ''
                # If line is empty, thus == ''
                if not line_without_number.strip():
                    text += '\n'
                else:
                    text += line_without_number
            else:

                # Find leading spaces of the current string are
                # larger then leading spaces of the first line, which is
                # stored in 'line_leading_spaces'
                if len(line) - len(line.lstrip(' ')) >= line_leading_spaces + char_num:
                    text += line[line_leading_spaces + char_num:]
                else:
                    text += line

    return text


# Retrieve a content table from a text
def extract_content_table(text):
    # Number of the line where table of contents ends
    tab_end_line = 0
    # Flag for the start of the table of contents
    tabStart = False
    # Flag for the end of the table of contents
    tabEnd = False
    # Count lines after expected end of the table of contents
    cnt_lines_after_expected_end = 0

    lst_idx_tab = []
    for i, line in enumerate(text.splitlines()):

        count_dots = 0
        temp_line = ''

        found_content_item = line.find('..........')

        if not tabEnd and found_content_item != -1:
            tab_end_line = i
            if not tabStart:
                tabStart = True

            lst_idx_tab.append(line[:found_content_item])
            cnt_lines_after_expected_end = 0

        if tabStart and not tabEnd and found_content_item == -1:
            cnt_lines_after_expected_end += 1
            if cnt_lines_after_expected_end > 5:
                tabEnd = True
                break

    return lst_idx_tab, tab_end_line


"""
Change pgbrk to a 'NEW_LINE' mark for files
without line numbers
"""


def clean_file_without_numbers(FILE_NAME):
    text = ''
    with open(FILE_NAME) as f:
        for line in f:

            # Found the end of a page
            if line[0] == '\x0c':

                line = line[1:]
                text += NEW_PAGE
                text += line
            else:
                text += line
    return text


def mean(a):
    return sum(a) / len(a)


# Return statistics about which lines of a pgbrk
# should be removed.
def count_pgbrk_borders(file_name):
    pagebrk = ''
    list_of_pgbrk = []
    window_size = 10

    pgbrk = False
    lines_after_pgbrk = 0

    temp_window = []
    count = 0

    # Store all the sliding windows that contain pgbrk
    for line in file_name.splitlines():

        # Create a window
        temp_window.append(line)
        # Sliding through a text lines
        if len(temp_window) > window_size:
            temp_window.pop(0)

            # Identify page breaker
        if line == NEW_PAGE.strip():
            pgbrk = True
        # Put a window with lines including pgbrk to a list
        if lines_after_pgbrk >= window_size / 2:
            list_of_pgbrk.append(temp_window)

            lines_after_pgbrk = 0
            pgbrk = False
            temp_window = []

        if pgbrk and lines_after_pgbrk < (window_size / 2) + 1:
            lines_after_pgbrk += 1

    # pgbrk to compate all other pgbrks in a text
    testing_pgbrk = list_of_pgbrk[int(len(list_of_pgbrk) / 2)]

    list_of_statistics = []

    for item in list_of_pgbrk:
        item_stats = []
        for i in range(len(item)):
            ratio = SequenceMatcher(None, testing_pgbrk[i], item[i]).ratio()
            item_stats.append(ratio)

        list_of_statistics.append(item_stats)

    # Return a list of stats
    stats_vals = list(map(mean, zip(*list_of_statistics)))
    round_stats_vals = ['%.2f' % elem for elem in stats_vals]

    # before and after pgdrk
    lines_before_pgbrk = 0
    lines_after_pgbrk = 0
    threshold = 0.93

    # lines before pgbrk
    for i in range(int((window_size / 2) - 2), -1, -1):
        if float(round_stats_vals[i]) > threshold:
            lines_before_pgbrk += 1
        else:
            break

    # lines after pgbrk

    for i in range(int((window_size / 2) + 1), len(round_stats_vals)):
        if float(round_stats_vals[i]) > threshold:
            lines_after_pgbrk += 1
        else:
            break

    return lines_before_pgbrk, lines_after_pgbrk


# TODO:
#  Implement a method to retrieve a text without content table
# and then put it to a count_pgbrk_borders
# then look at the results for Shipyeard as it has the most bias result

# FILE_NAME = 'ABB1F.txt'
FILE_NAME = 'Shipyard.txt'

cleaned_text = remove_numbers(FILE_NAME)
# ----------------------------------------

# FILE_NAME = 'KOGAS -2449.txt'
# FILE_NAME = 'ON -2462.txt'
cleaned_text = clean_file_without_numbers(FILE_NAME)

content_table, tab_end_line = extract_content_table(cleaned_text)

text_without_content_table = ''

count_pgbrk_borders(cleaned_text)

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(content_table)