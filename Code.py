deletion_cost = 1
insertion_cost = 1
change_cost = 1
swap_cost = 1

def Damerau_Levenshtein_Distance(first_string: str, second_string: str):
    first_string_length = len(first_string)
    second_string_length = len(second_string)
    DLDmatrix = [[0] * (second_string_length+1) for i in range(first_string_length+1)]

    for current_letter_index in range(first_string_length+1):
        DLDmatrix[current_letter_index][0] = current_letter_index*deletion_cost
    for current_letter_index in range(second_string_length+1):
        DLDmatrix[0][current_letter_index] = current_letter_index*insertion_cost

    for current_DLDmatrix_string_index in range(1,first_string_length+1):
        for current_DLDmatrix_column_index in range(1, second_string_length + 1):
            if first_string[current_DLDmatrix_string_index-1] == second_string[current_DLDmatrix_column_index-1]:
                cost = 0
            else:
                cost = change_cost
            DLDmatrix[current_DLDmatrix_string_index][current_DLDmatrix_column_index] = min(
                DLDmatrix[current_DLDmatrix_string_index - 1][current_DLDmatrix_column_index] + deletion_cost,  # deletion
                DLDmatrix[current_DLDmatrix_string_index][current_DLDmatrix_column_index - 1] + insertion_cost,  # insertion
                DLDmatrix[current_DLDmatrix_string_index - 1][current_DLDmatrix_column_index - 1] + cost,  # substitution
            )
            if current_DLDmatrix_string_index-2>0 and current_DLDmatrix_column_index-2>0 and \
                    first_string[current_DLDmatrix_string_index-1] == second_string[current_DLDmatrix_column_index - 2] and\
                    first_string[current_DLDmatrix_string_index - 2] == second_string[current_DLDmatrix_column_index-1]:
                DLDmatrix[current_DLDmatrix_string_index][current_DLDmatrix_column_index] =\
                    min(DLDmatrix[current_DLDmatrix_string_index][current_DLDmatrix_column_index],
                        DLDmatrix[current_DLDmatrix_string_index - 2][current_DLDmatrix_column_index - 2] + swap_cost)  # transposition
    return DLDmatrix[first_string_length][second_string_length], DLDmatrix

print("Write first word: ")
First_Word = str(input())
print("Write second word: ")
Second_Word = str(input())
print("Choose mode, print 's' if you want to have standard costs and 'c' if you want to configure them:")
mode = str(input())

if mode == 's':
    answer, Matrix = Damerau_Levenshtein_Distance(First_Word, Second_Word)
    print("Distance between words = " + str(answer))
else:
    print("Configure deletion cost:")
    deletion_cost = int(input())
    print("Configure insertion cost:")
    insertion_cost = int(input())
    print("Configure swap cost:")
    swap_cost = int(input())
    print("Configure change cost:")
    change_cost = int(input())
    answer, Matrix = Damerau_Levenshtein_Distance(First_Word, Second_Word)
    print("Distance between words = " + str(answer))
