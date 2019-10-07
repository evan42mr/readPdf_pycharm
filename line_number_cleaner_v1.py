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
                if line_without_number.strip():
                    print(f"line: {line} spaces = {line_leading_spaces}")
                    break

print(line_leading_spaces)
text = ''
with open(FILE_NAME) as f:
    char_num = 0
    for line in f:
        if line.strip() and (line[0].isdigit() or line[1].isdigit() or line[2].isdigit()) and line.find('......') == -1:
            # Found a line with the number at the beginning
            if line.split()[0].isdigit():
                # Slice the line so the sentence starts after the number
                # Discard if the line is empty

                # Position number of the digit of each line, plus it's length
                char_num = line.find(line.split()[0]) + len(line.split()[0])
                line_without_number = line[char_num + line_leading_spaces:]
                # print(line_without_number)
                text += line_without_number

        # Line without a number
        else:
            # Found the end of a page
            if line[0] == '\x0c':
                # print(NEW_PAGE)
                line = line[1:]
                text += NEW_PAGE

            if len(line) - len(line.lstrip(' ')) >= 1:
                # print(line[line_leading_spaces + char_num:])
                text += line[line_leading_spaces + char_num:]
            else:
                # print(line)
                text += line

print(text)

#                 if line_leading_spaces != 0:
#                     if line_leading_spaces in dict_of_spaces:
#                         dict_of_spaces[line_leading_spaces] += 1
#                     else:
#                         dict_of_spaces[line_leading_spaces] = 1


# -------------------------------------------------------------------
#                 # count the leading spaces in a string
#                 if len(line) - len(line.lstrip(' ')) < 2:
#                     tokens = re.findall('\s+', line.lstrip())
#                     if len(tokens[0]) == 1:
#                         print(f"{line.find(line.split()[0])} : |{line.rstrip()} : print->{line[line.find(line.split()[0]) + len(line[line.find(line.split()[0]):]):]}")
#                         # lst_spaces.append(line[line.find(line.split()[0]) + len(line[line.find(line.split()[0]):]):])

#                     elif len(tokens[0]) in dict_of_spaces:
#                         dict_of_spaces[len(tokens[0])] += 1
#                     else:
#                         dict_of_spaces[len(tokens[0])] = 1

# print(lst_spaces)
# pprint.pprint(dict_of_spaces, width=1)

# print(max(dict_of_spaces.items(), key=operator.itemgetter(1))[0])
# print(min(dict_of_spaces.items(), key=operator.itemgetter(1))[0])




