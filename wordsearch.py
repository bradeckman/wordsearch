#################################################################
# FILE : wordsearch.py
# WRITER : Brad Eckman , eckmanbrad , 328958244
# EXERCISE : intro2cse ex5 2020
# DESCRIPTION: A program that counts the number of times a given list of words
#              appears in a given matrix; writes results to file.
# STUDENTS I DISCUSSED THE EXERCISE WITH: None
# WEB PAGES I USED: https://www.thetopsites.net/article/50627962.shtml
#                   https://stackoverflow.com/questions/26056949/correct-
#                   layout-for-dictionary-literals
#                   https://stackoverflow.com/questions/8899905/count-number-
#                   of-occurrences-of-a-given-substring-in-a-string
# NOTES: The overall approach to this exercise:
#           1) Format all files/inputs entered by user.
#           2) For each direction code, send to an appropriate function
#              that manipulates the matrix in such a way that it is simple to
#              search using one basic search function.
#           3) Send formatted matrix to search function and a update dictionary
#              with a tally of all words found
#           4) Write final dictionary (formatted as tuples) to output file
#################################################################

import sys
from os import path
import copy

NOTHING, NEWLINE, COMMA = '', '\n', ','
WORDS_INDEX, MATRIX_INDEX, \
OUTPUT_FILE_INDEX, DIRECTIONS_INDEX = range(4)
UP, DOWN, RIGHT, LEFT, \
D_UP_RIGHT, D_UP_LEFT, \
D_DOWN_RIGHT, D_DOWN_LEFT = VALID_DIRECTIONS = "udrlwxyz"
FIRST_OPTIONAL_ARG = 1
HOW_TO_RUN_MSG, WORDS_NOT_FOUND_MSG, \
MATRIX_NOT_FOUND_MSG, INVALID_DIRECTIONS_MSG = range(5, 9)
message_dict = {
    HOW_TO_RUN_MSG:
        "Please run the program in the following format: "
        "python3 wordsearch.py words_file.txt matrix_file.txt "
        "output_file.txt directions",
    WORDS_NOT_FOUND_MSG:
        "The words file you've entered does not exist. "
        "Try again!",
    MATRIX_NOT_FOUND_MSG:
        "The matrix file you've entered does not exist. "
        "Try again!",
    INVALID_DIRECTIONS_MSG:
        "You have entered an invalid set of directions to search for. "
        "Try again! (possible directions: udrlwxyz)"
    }


def check_input_args(args):
    """
    Checks program has been run with valid command line arguments.
    :param args: A list of arguments from the command line
    :return: Appropriate message if invalid, else - None
    """
    # User hasn't entered correct amount of args
    if len(args) != 4:
        return message_dict[HOW_TO_RUN_MSG]
    # The words file entered does not exist
    if not path.isfile(args[WORDS_INDEX]):
        return message_dict[WORDS_NOT_FOUND_MSG]
    # The matrix file entered does not exist
    if not path.isfile(args[MATRIX_INDEX]):
        return message_dict[MATRIX_NOT_FOUND_MSG]
    # Invalid string of directions
    for char in args[DIRECTIONS_INDEX]:
        if char not in VALID_DIRECTIONS:
            return message_dict[INVALID_DIRECTIONS_MSG]

    return None


def read_wordlist_file(filename):
    """
    Formats words from words file into list of words.
    :param filename: The name of the words file
    :return: A list of words
    """
    with open(filename, 'r') as f:
        words_list = f.read().splitlines()

    return words_list


def read_matrix_file(filename):
    """
    Formats letters from matrix file into 2D matrix.
    :param filename: The name of the matrix file
    :return: A 2D list of letters to search
    """
    # Create list of strings, where each char is separated by COMMA
    with open(filename, 'r') as f:
        matrix = f.read().splitlines()
    # Split at ',' to make lists of lists
    for i in range(len(matrix)):
        matrix[i] = matrix[i].split(COMMA)

    return matrix


def add_word_found(words_found, word, count):
    """
    Records a word found in the dictionary.
    :param words_found: A dict words found and tallies in format {word: count}
    :param word: The word to record in the dictionary
    :param count: An integer, the number of occurrences of word to record
    :return: None
    """
    # If we've found word already, add count to it's count. Else, create
    # new key starting at count.
    if word in words_found:
        words_found[word] += count
    else:
        words_found[word] = count


def count_word(row_str, word):
    """
    Counts the number of times a word appears in a row, taking into account
    possible overlaps.
    :param row_str: The formatted row, as a string
    :param word: The substring to count within the row
    :return: An integer, the number of occurrences of word in row_str
    """
    count = 0

    for i in range(len(row_str)):
        # No need to check if the length of word is larger than the row left
        if len(row_str[i:]) < len(word):
            break
        # Using the below logic makes sure we don't miss overlapping instances
        if row_str[i:].startswith(word):
            count += 1

    return count


def search_for_words(word_list, formatted_matrix, words_found):
    """
    Searches for words in a given formatted matrix and records findings in dict
    :param word_list: A list of words to find
    :param formatted_matrix: A 2D list of letters to search from, formatted
           according to the search direction defined
    :param words_found: A dict of words found and tallies in format
           {word: count}
    :return: None
    """
    # Iterate through rows
    for row in formatted_matrix:
        # Convert row to concatenated string
        row_str = NOTHING.join(row)
        # For each row, iterate through all words
        for word in word_list:
            # No need to send to counting function if no instances at all
            if word not in row_str:
                continue
            # Send to count instances of word, record in dictionary
            count = count_word(row_str, word)
            add_word_found(words_found, word, count)


def reverse_matrix(formatted_matrix):
    """
    Reverses each row in it's place in a matrix.
    :param formatted_matrix: A 2D list of letters to search from
    :return: The updated matrix
    """
    for row in formatted_matrix:
        row.reverse()

    return formatted_matrix


def r_format(matrix):
    """ Formats a matrix to search from left to right. """
    # We will operate on a deep copy so as to not change the matrix itself
    formatted_matrix = copy.deepcopy(matrix)
    return formatted_matrix


def l_format(matrix):
    """ Formats a matrix to search from right to left. """
    return reverse_matrix(r_format(matrix))


def d_format(matrix):
    """ Formats a matrix to search from top to bottom. """
    # We will operate on a new list so as to not change the matrix itself
    num_of_rows = len(matrix)
    row_length = len(matrix[0])

    # Format matrix from top to bottom
    formatted_matrix = []
    for i in range(row_length):
        row = []
        for j in range(num_of_rows):
            row.append(matrix[j][i])
        formatted_matrix.append(row)

    return formatted_matrix


def u_format(matrix):
    """ Formats a matrix to search from bottom to top. """
    return reverse_matrix(d_format(matrix))


def w_format(matrix):
    """ Formats a matrix to search from bottom-left to top-right. """
    # We will operate on a new list so as to not change the matrix itself
    num_of_rows = len(matrix)
    row_length = len(matrix[0])
    # Create empty list of lists of len(row_length + num_of_rows - 1)
    formatted_matrix = [[] for i in range(row_length + num_of_rows - 1)]

    # Format matrix diagonally
    for i in range(row_length):
        for j in range(num_of_rows):
            formatted_matrix[i+j].append(matrix[j][i])

    return formatted_matrix


def z_format(matrix):
    """ Formats a matrix to search from top-right to bottom-left. """
    return reverse_matrix(w_format(matrix))


def y_format(matrix):
    """ Formats a matrix to search from bottom-right to top-left. """
    # We will operate on a new list so as to not change the matrix itself
    num_of_rows = len(matrix)
    row_length = len(matrix[0])
    offset = -num_of_rows + 1
    # Create empty list of lists of len(row_length + num_of_rows - 1)
    formatted_matrix = [[] for i in range(row_length + num_of_rows - 1)]

    # Format matrix diagonally
    for i in range(row_length):
        for j in range(num_of_rows):
            formatted_matrix[i-j-offset].append(matrix[j][i])

    return formatted_matrix


def x_format(matrix):
    """ Formats a matrix to search from top-left to bottom-right. """
    return reverse_matrix(y_format(matrix))


def find_words_in_matrix(word_list, matrix, directions):
    """
    :param word_list: A list of words to find.
    :param matrix: A 2D list of letters to search
    :param directions: The appropriate direction codes
    :return: A list of tuples of words found in format (word, count)
    """
    # Initialize dictionary for words
    words_found = dict()
    # Initialize dictionary hashing each direction code to the appropriate
    # reformatting function
    direction_formats = {
         UP: u_format, DOWN: d_format,
         RIGHT: r_format, LEFT: l_format,
         D_UP_RIGHT: w_format, D_UP_LEFT: x_format,
         D_DOWN_RIGHT: y_format, D_DOWN_LEFT: z_format
         }

    # If matrix is empty, we won't find any words, so no need to search
    if matrix:
        # Iterate over characters in directions. For each direction, reformat
        # the matrix accordingly before sending to search function (all while
        # updating the words_found dictionary).
        for format_code in set(directions):  # Filter out any non-unique codes
            formatted_matrix = direction_formats[format_code](matrix)
            search_for_words(word_list, formatted_matrix, words_found)

    # Return as a list of tuples, each in format (word, count)
    return list(words_found.items())


def write_output_file(results, output_filename):
    """
    Writes results to an output file.
    :param results: A list of tuples of words found in format (word, count)
    :param output_filename: The file to write results to
    :return: None
    """
    with open(output_filename, 'w') as f:
        # Write line by line to file, in format 'word,count\n'
        for word, count in results:
            f.write(word + COMMA + str(count) + NEWLINE)


def main():
    """
    The main operating function to run the program.
    :return: None
    """
    cmd_line_args = sys.argv[FIRST_OPTIONAL_ARG:]
    # Check program has been run with correct command line arguments
    if check_input_args(cmd_line_args) is not None:
        print(check_input_args(cmd_line_args))
        sys.exit()

    # Format words and matrix from files in lists
    word_list = read_wordlist_file(cmd_line_args[WORDS_INDEX])
    matrix = read_matrix_file(cmd_line_args[MATRIX_INDEX])
    output_filename, directions = cmd_line_args[OUTPUT_FILE_INDEX:]

    # Find and capture words found in matrix, write results to output file
    words_found = find_words_in_matrix(word_list, matrix, directions)
    write_output_file(words_found, output_filename)


if __name__ == "__main__":
    main()
