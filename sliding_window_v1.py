"""
Program to read the pdf file and remove page breaker
with repeating sentences
"""

# import re

# def remove_numbers(text):
#     return re.sub(r'\d+', '', text)

NEW_PAGE = '----------------> new page <---------------\n'


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
        for line in f:
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
                    idx_pgbrk = lines_before_pgbrk + window_size

                    # Slicing the list in front and back sides
                    front_window = multiple_lines_text[:idx_pgbrk - 1 - lines_before_pgbrk]
                    back_window = multiple_lines_text[idx_pgbrk + lines_after_pgbrk:]

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

    while idx_pgbrk_remained != 0:
        text += multiple_lines_text.pop(0)
        idx_pgbrk_remained -= 1

    # print(text)
    return text


# Choose the number of lines before and after page breaker
file_name = 'KOGAS -2449.txt'
# file_name = 'ON -2462.txt'
# file_name = 'ABB1F.txt'
# file_name = 'Shipyard.txt'

lines_before_pgbrk = 1
lines_after_pgbrk = 1

cleaned_text = sliding_window(lines_before_pgbrk, lines_after_pgbrk, file_name)
print(cleaned_text)

# TODO
# Find page breakers and identify
# the size of it automatically

# pagebrk = ''
# with open(file_name) as f:
#     for line in f:
#         # Identify page breaker
#         if line[0] == '\x0c':
#             pagebrk = line

