import re


def remove_numbers(text):
    return re.sub(r'\d+', '', text)


NEW_PAGE = '----------------> new page <---------------\n'

"""
Function deletes lines before and after page_breaker
and prints the rest of the text
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
            if cnt_lines_after_expected_end > 3:
                tabEnd = True
                break

    return lst_idx_tab, tab_end_line


def find_titles(cleaned_text, idx_tab, line_num, tab_end_line):
    count_line = 0
    current_title = ''
    text = ''
    lst_lines = []
    page_cnt = 0

    for i, line in enumerate(cleaned_text.splitlines()):
        if line == NEW_PAGE:
            page_cnt += 1
        if i > line_num and i > tab_end_line:
            if idx_tab and \
                    ' '.join(remove_numbers(line).split()).strip().upper() == \
                    ' '.join(remove_numbers(idx_tab[0]).split()).strip().upper():

                print(f"title: [{line}]")
                # idx_tab.pop(0)
                current_title = idx_tab.pop(0)
                count_line = i
            else:
                if current_title != '':
                    # print(line)
                    if not line.strip():
                        if lst_lines:
                            # print(f"text len({len(text)}): {text}")
                            # print(f"----->title: {current_title} text len({len(text)}): {text}")
                            print(f"text:")
                            for line in lst_lines:
                                print(f"[{line}]")
                            #                                 text += line
                            #                             print(text)
                            lst_lines = []
                    #                             text = ''
                    else:
                        lst_lines.append(line)
    return count_line


# Choose the number of lines before and after page breaker
file_name = 'KOGAS -2449.txt'
lines_before_pgbrk = 1
lines_after_pgbrk = 1

cleaned_text = sliding_window(lines_before_pgbrk, lines_after_pgbrk, file_name)
content_tab, tab_end_line = extract_content_table(cleaned_text)

# print(cleaned_text)
print(tab_end_line)

line_num = 0
find_titles(cleaned_text, content_tab, line_num, tab_end_line)

# lst_not_found_titles = []


# for i, line in enumerate(cleaned_text.splitlines()):
#     print(f"line {i}: {line}")


# while content_tab:
#     line_num = find_titles(cleaned_text, content_tab, line_num)
#     if content_tab:
#         lst_not_found_titles.append(content_tab.pop(0))

# print('\n\n')
# if not lst_not_found_titles:
#     print("--------- Process is done ---------")
# else:
#     print("--------- Something went wrong! ---------")
#     print(f"There are still {len(lst_not_found_titles)} element to search")
#     print(lst_not_found_titles)