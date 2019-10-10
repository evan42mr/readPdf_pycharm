import re
import pprint
import operator

NEW_PAGE = '----------------> new page <---------------\n'


def remove_numbers(text):
    return re.sub(r'\d+', '', text)


FILE_NAME = 'ABB1F.txt'
# FILE_NAME = 'Shipyard.txt'


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
                    #                     print(f"line: {line} spaces = {line_leading_spaces}")
                    break

# print(line_leading_spaces)
text = ''

with open(FILE_NAME) as f:
    # length of the number character on a line
    char_num = 2
    count = 0
    lst_line = []
    for i, line in enumerate(f):

        #         if i > 81:
        #             count += 1
        #             lst_line.append(line)
        #         if count == 15:
        #             break

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
            #             print(f"curr_line_spaces: {len(line) - len(line.lstrip(' '))}, line_leading_spaces: {line_leading_spaces}, char_num: {char_num}")
            if len(line) - len(line.lstrip(' ')) >= line_leading_spaces + char_num:

                #                 print(f"line if:{line[line_leading_spaces + char_num:]}")
                text += line[line_leading_spaces + char_num:]
            else:
                #                 print(f"line else: {line}")
                text += line

print(text)
# print(lst_line)

# TODO:
"""
Update the code so it preserves the empty lines,
instead of removing them 
"""




