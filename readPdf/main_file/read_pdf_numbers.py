import re
import pprint
import operator
import pprint
import string
from difflib import SequenceMatcher

"""
It is a main code file that contains all the codes in a project to read pdf.   
Script to read pdf files with line numbers and without them.
"""

pp = pprint.PrettyPrinter(indent=4)
NEW_PAGE = '----------------> new page <---------------\n'


def remove_numbers(text):
    return re.sub(r'\d+', '', text)


def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))


"""
Removes number from each line from pdf file
"""


def remove_line_numbers(FILE_NAME):
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


"""
Change pgbrk to a 'NEW_LINE' mark for files
without line numbers
"""


def clean_file_without_line_numbers(FILE_NAME):
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
    threshold = 0.9

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


"""
Function deletes lines before and after page_breaker
and prints the rest of the text.

It seems to be not reasonable to open original file again,
rather than use a cleaned text, but when we clean text all 
special characters like '\n' get disappeared 
"""


def sliding_window(lines_before_pgbrk, lines_after_pgbrk, file_name, window_size=5):
    counter_lines_after_pgbrk = window_size
    # 5 is added to make a window size bigger
    # to cover possible empty lines
    line_window_size = (lines_before_pgbrk + window_size) + (window_size)

    pgbrk = False

    multiple_lines_text = []
    count = 0
    text = ''

    with open(file_name) as f:
        for i, line in enumerate(f):
            count += 1
            multiple_lines_text.append(line)

            # print the first element in a list
            if count > line_window_size:
                text += multiple_lines_text.pop(0)

                # Found the end of a page
            if line[0] == '\x0c':
                pgbrk = True

            if pgbrk:
                if counter_lines_after_pgbrk > 0:
                    counter_lines_after_pgbrk -= 1
                elif counter_lines_after_pgbrk <= 0:

                    # String to save pg_breaker
                    #                     if lines_before_pgbrk <= 0:
                    #                         idx_pgbrk = window_size - 1
                    #                     else:
                    #                         idx_pgbrk = lines_before_pgbrk + window_size
                    for i, line in enumerate(multiple_lines_text):
                        if line[0] == '\x0c':
                            idx_pgbrk = i

                    # Slicing the list in front and back sides
                    front_window = multiple_lines_text[:idx_pgbrk - lines_before_pgbrk]
                    if lines_after_pgbrk <= 0:
                        back_window = multiple_lines_text[idx_pgbrk + lines_after_pgbrk:]
                    else:
                        back_window = multiple_lines_text[idx_pgbrk + lines_after_pgbrk + 1:]

                    #                     print(f"\nmultiple_lines_text = {multiple_lines_text}\n")
                    #                     print(f"idx_pgbrk = {idx_pgbrk}, lines_before_pgbrk = {lines_before_pgbrk}, lines_after_pgbrk = {lines_after_pgbrk}")
                    #                     print(f"front_window: {front_window}")
                    #                     print(f"back_window: {back_window}")

                    #                     if i > 331:
                    #                         break
                    # Remove empty lines from the front window side
                    for i in range(len(front_window)):
                        if front_window[-1] == '\n':
                            front_window.pop()
                        else:
                            break

                    # Remove empty lines from the back window size
                    for i in range(len(back_window)):
                        if back_window[0] == '\n':
                            back_window.pop(0)
                        else:
                            break

                    # Check if the back window needs '\n'
                    if front_window and back_window and \
                            front_window[- 1][-1] != ',' and front_window[- 1][-1] != ',' and \
                            back_window[0][0].isupper():
                        back_window.insert(0, '\n')

                    front_window.append(NEW_PAGE)
                    remained_window_list = front_window + back_window
                    remained_window_text = ''

                    for line in remained_window_list:
                        remained_window_text += line

                    text += remained_window_text

                    # reset the vars
                    multiple_lines_text = []
                    pgbrk = False
                    counter_lines_after_pgbrk = window_size
                    count = 0

    # Get remained lines in a sliding window
    idx_pgbrk_remained = 0

    # Find a pgbrk index in list of a remained sliding window
    for i, line in enumerate(multiple_lines_text):
        if line[0] == '\x0c':
            idx_pgbrk_remained = i

    idx_pgbrk_remained -= lines_before_pgbrk

    while idx_pgbrk_remained >= 0:
        text += multiple_lines_text.pop(0)
        idx_pgbrk_remained -= 1

    # print(text)
    return text


def find_titles(text_without_pgbrk, idx_tab, line_num, tab_end_line, title_indent_spaces):
    count_line = 0
    current_title = ''
    lst_lines = []
    page_cnt = 1

    # Last sentence is needed to store the last read line
    # to track if it is a not finished sentence of not
    last_line = ''

    for i, line in enumerate(text_without_pgbrk.splitlines()):

        # print(f"line: [{line}]")

        if line == NEW_PAGE.strip():
            # print("new page")
            page_cnt += 1
            continue
        if i > line_num and i > tab_end_line:
            if idx_tab and \
                    ' '.join(remove_numbers(line).split()).strip().upper() == \
                    ' '.join(remove_numbers(idx_tab[0]).split()).strip().upper():

                # Print lines under the previous paragraph
                if lst_lines:
                    # Print lines
                    read_lines_from_lst_lines(lst_lines)
                    lst_lines = []

                #                 sql = "INSERT INTO on_2462 (par_text, is_title, page) VALUES (%s,%s,%s)"
                #                 val = (line, True, page_cnt)
                #                 mycursor.execute(sql, val)
                #                 mydb.commit()

                current_title = idx_tab.pop(0)
                leading_spaces = len(current_title) - len(current_title.lstrip(' '))
                if leading_spaces == title_indent_spaces:
                    print(f"title: [{line}]")
                else:
                    print(f"sub_title: [{line}]")
                count_line = i

            else:
                if current_title != '':
                    # If new paragraph
                    if not line.strip():
                        # If lst_lines is not an empty list
                        if lst_lines:
                            #                             # Check if the line end with '\n' and before it has islower()
                            #                             # (Ex: and\n), means that the next line should be concatenated
                            #                             if line and line[-1] == '\n' and line[line.find('\n') - 1].islower():
                            #                                 line = line[:line.find('\n')]
                            #                                 lst_lines.append(line)
                            if (last_line and last_line.split()[-1][-1] == ','):
                                lst_lines.append(line)
                            elif last_line and last_line.split()[-1][-1] == ':':
                                if line:
                                    lst_lines.append('\n')
                                    lst_lines.append(line)
                                else:
                                    continue

                            else:
                                inner_last_line = ''
                                # Print lines
                                read_lines_from_lst_lines(lst_lines)

                                lst_lines = []

                    else:
                        lst_lines.append(line)

        last_line = line

    #     mycursor.close()
    #     mydb.close()
    return count_line


def read_lines_from_lst_lines(lst_lines):
    text = ''
    bullet_point = False
    for line in lst_lines:
        # Write the first line

        if text == '':
            if check_if_line_is_title(line):
                text += '\n' + line + '\n'
            else:
                text += line
        else:
            # Count spaces between words
            count_spaces = 0
            tokens = re.findall('\s+', line)
            for i in range(0, len(tokens)):
                # Count the max soace in the line
                if len(tokens[i]) > count_spaces:
                    count_spaces = len(tokens[i])
            # Check if the line is a bullet point or a table raw
            if count_spaces > 1:
                text = text + '\n' + line
                bullet_point = True
            else:
                # Check for the last line of the bullet point
                if bullet_point:
                    text = text + '\n' + line
                    bullet_point = False
                else:
                    #  Check if line is a title
                    if check_if_line_is_title(line):
                        print(f"Discovered title: [{line}]")
                        text = text + '\n' + line + '\n'
                    else:
                        text = text + ' ' + line

    print("text:")
    print(text)


#                             sql = "INSERT INTO on_2462 (par_text, is_title, page) VALUES (%s,%s,%s)"
#                             val = (text, False, page_cnt)
#                             mycursor.execute(sql, val)
#                             mydb.commit()

def check_if_line_is_title(line_text):
    #  Check if line is a title
    temp_line = remove_numbers(line_text)
    temp_line = remove_punctuation(temp_line)

    count_words = 0
    count_upper = 0

    for i in (temp_line.strip()).split():
        count_words += 1
        if i[0].isupper():
            count_upper += 1

    # If line has less then 7 words
    # Good chances it is a title if
    # percentage of words starting with capital letter
    # is equal or higher then 70%
    if count_words > 0 and count_words < 7 \
            and (100 / count_words) * count_upper >= 70 \
            and (temp_line.strip()).split()[-1][-1] != '.':
        return True
    else:
        return False


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
    # Leading spaces of the title, stored to distinguish from sub_titles
    title_indent_spaces = -1

    lst_idx_tab = []

    line_counter = 0
    for i, line in enumerate(text.splitlines()):

        line_counter += 1
        count_dots = 0
        temp_line = ''

        found_content_item = line.find('..........')

        if not tabEnd and found_content_item != -1:
            tab_end_line = i

            if not tabStart:
                tabStart = True

            if title_indent_spaces == -1:
                title_indent_spaces = len(line) - len(line.lstrip(' '))

            lst_idx_tab.append(line[:found_content_item])
            cnt_lines_after_expected_end = 0

        if tabStart and not tabEnd and found_content_item == -1:
            cnt_lines_after_expected_end += 1
            if cnt_lines_after_expected_end > 20:
                tabEnd = True
                break

    return lst_idx_tab, tab_end_line, title_indent_spaces
"""
Scan the text and look for titles that can be detected,
titles that can't be find are just removed from the list
and then added as just a text sentence. 

This function does a double work by scanning the text several time,
but because of the time deadlines, I didn't have time to write
something better or integrade it into find_titles function
"""
def extract_existed_content_table(content_table, text_without_pgbrk, tab_end_line):
    idx_tab = []
    line_num = 0

    while content_table:

        for i, line in enumerate(text_without_pgbrk.splitlines()):
            if i > line_num and i > tab_end_line:
                if content_table and \
                        ' '.join(remove_numbers(line).split()).strip().upper() == \
                        ' '.join(remove_numbers(content_table[0]).split()).strip().upper():
                    idx_tab.append(content_table.pop(0))
                    line_num += 1

        if content_table:
            content_table.pop(0)


    return idx_tab



# FILE_NAME = 'ABB1F.txt'
# FILE_NAME = 'Shipyard.txt'

# cleaned_text = remove_line_numbers(FILE_NAME)
# ----------------------------------------

FILE_NAME = 'KOGAS -2449.txt'
# FILE_NAME = 'ON -2462.txt'

cleaned_text = clean_file_without_line_numbers(FILE_NAME)

lines_before_pgbrk, lines_after_pgbrk = count_pgbrk_borders(cleaned_text)
# print(lines_before_pgbrk, lines_after_pgbrk)
text_without_pgbrk = sliding_window(lines_before_pgbrk, lines_after_pgbrk, FILE_NAME)

# print(text_without_pgbrk)

content_table, tab_end_line, title_indent_spaces = extract_content_table(text_without_pgbrk)
print(len(content_table))
"""
Content table should be consisted only from those titles that can be identified
in the text. Otherwise bug leads to storing the text several times in a database
"""
new_content_table = extract_existed_content_table(content_table, text_without_pgbrk, tab_end_line)

# Parameter used in a previous logic. Didn't modified the code in case it might not work correctly
line_num = 0
find_titles(text_without_pgbrk, new_content_table, 0, tab_end_line, title_indent_spaces)
