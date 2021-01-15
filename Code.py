from tkinter import *
deletion_cost = 0
insertion_cost = 0
change_cost = 0
swap_cost = 0

square_size = 40
animate_speed = 0.2


Left_column_value = 0
First_Word_Index = 0

Top_string_value = 0
Second_Word_Index = 0

result_text = []
counter_for_result = 0

Left_Column = []
Top_String = []
Rectangle_Map = []
Text_Map = []

all_steps = []
step_counter = 0

First_Word = ""
Second_Word = ""

animating = False
auto = False

def print_lcs(x: str, y: str, arrows,
              i: int = None, j: int = None):
    # i, j: текущие индексы первой и второй строки
    global result_text,counter_for_result

    if i is None or j is None:
        i = len(x)
        j = len(y)
    if j == 0:
        result_text.append("Спереди слова '" + x + "' удалить '" + x[0:i] + "'")
        return
    if i == 0:
        result_text.append("Сперед слова '" + x + "' добавить '" + y[0:j] + "'")
        return
    if x[i-1] == y[j-1]:
        print_lcs(x, y, arrows, i - 1, j - 1)
        result_text.append("В слове '"+ x + "' элемент '"+ x[i-1] + "' под индексом "+ str(i-1)+" так и оставить")
    elif i-2>0 and j-2>0 and x[i-1] == y[j-2] and x[i-2]==y[j-1] and arrows[i-2][j-2]<=arrows[i-1][j] and\
            arrows[i-2][j-2]<=arrows[i][j-1] and arrows[i-2][j-2]<=arrows[i-1][j-1]:
        print_lcs(x, y, arrows, i - 2, j-2)
        result_text.append("В слове '" + x +"' необходимо поменять местами элементы '"+ x[i - 1]+"'" + " и '" + x[i - 2]+
              "' под индексами "+ str(i-2)+ " и "+str(i-1)+" соответсвенно" )
    elif x[i-1] != y[j-1] and arrows[i-1][j]<=arrows[i][j-1] and arrows[i-1][j]<=arrows[i-1][j-1]:
        print_lcs(x, y, arrows, i-1, j)
        result_text.append("В слове '" + x + "' нужно удалить символ '" + x[i - 1]+"' под индексом "+ str(i-1))
    elif x[i-1] != y[j-1] and arrows[i-1][j-1]<=arrows[i][j-1] and arrows[i-1][j-1]<=arrows[i-1][j]:
        print_lcs(x, y, arrows, i - 1, j-1)
        result_text.append("В слове '" + x +"' необходимо сделать замену символа '" +x[i - 1] + "' под индексом "+ str(i-1) +
              " на символ '"+y[j-1]+"' под индексом "+ str(j-1)+ " из слова '"+ y+"'")
    else:
        print_lcs(x, y, arrows, i , j - 1)
        result_text.append("После элемента '"+x[i-1]+"'"+" под индексом "+ str(i-1) + " добавить символ "+ y[j - 1])


def on_enter_left_column(e, r):
    canvas.itemconfig(r, fill=_from_rgb((137, 66, 214)))


def on_leave_left_column(e, r):
    canvas.itemconfig(r, fill="yellow")
    if r == Left_column_value or r == Top_string_value:
        canvas.itemconfig(r, fill=_from_rgb((255, 116, 0)))


def on_click_left_column(e, r, index):
    global Left_column_value, First_Word_Index
    canvas.itemconfig(Left_column_value, fill="yellow")
    Left_column_value = r
    canvas.itemconfig(Left_column_value, fill=_from_rgb((255, 116, 0)))
    First_Word_Index = index


def on_click_top_string(e, r, index):
    global Top_string_value, Second_Word_Index
    canvas.itemconfig(Top_string_value, fill="yellow")
    Top_string_value = r
    canvas.itemconfig(Top_string_value, fill=_from_rgb((255, 116, 0)))
    Second_Word_Index = index


def draw_matrix():
    global Left_Column
    global Top_String
    global Rectangle_Map
    global Text_Map
    global Left_column_value, Top_string_value
    global First_Word_Index, Second_Word_Index
    canvas.delete("all")

    First_Word_Size = len(First_Word)
    Second_Word_Size = len(Second_Word)

    Left_Column = [0]*(First_Word_Size+2)
    Top_String = [0]*(Second_Word_Size+1)

    for i in range(First_Word_Size+2):  # Рисую столбец левых значений
        Left_Column[i] = canvas.create_rectangle(3, 3 + i*square_size,
                        (square_size+3), (square_size + 3) + i*square_size,
                        fill="yellow",
                        outline='blue',
                        width=3, )
        if i != 0 and i != 1:
            canvas.tag_bind(Left_Column[i], "<Enter>", lambda e, r=Left_Column[i]: on_enter_left_column(e, r))
            canvas.tag_bind(Left_Column[i], "<Leave>", lambda e, r=Left_Column[i]: on_leave_left_column(e, r))
            canvas.tag_bind(Left_Column[i], "<Button-1>", lambda e, r=Left_Column[i], index=i-1:
                                            on_click_left_column(e, r, index))
        if i == 1:
            canvas.create_text(square_size // 2, square_size // 2 + i * square_size,
                               text="⦰", font=("Comic Sans MS", 14, "bold"))
        if i > 1:
            temp = canvas.create_text(square_size // 2, square_size // 2 + i * square_size,
                                text=First_Word[i-2], font=("Comic Sans MS", 14, "bold"))
            canvas.tag_bind(temp, "<Enter>", lambda e, r=Left_Column[i]: on_enter_left_column(e, r))
            canvas.tag_bind(temp, "<Button-1>", lambda e, r=Left_Column[i], index=i-1:
                                            on_click_left_column(e, r, index))

    for i in range(Second_Word_Size+1):  # Рисую столбец верхних значений
        Top_String[i] = canvas.create_rectangle(3+square_size + i*square_size, 3,
                        (2*square_size+3) + i*square_size, 3+square_size,
                        fill="yellow",
                        outline='blue',
                        width=3, )
        if i != 0:
            canvas.tag_bind(Top_String[i], "<Enter>", lambda e, r=Top_String[i]: on_enter_left_column(e, r))
            canvas.tag_bind(Top_String[i], "<Leave>", lambda e, r=Top_String[i]: on_leave_left_column(e, r))
            canvas.tag_bind(Top_String[i], "<Button-1>", lambda e, r=Top_String[i],index = i:
                                            on_click_top_string(e, r, index))

        if i == 0:
            temp = canvas.create_text(3+square_size + square_size//2,square_size // 2,
                               text="⦰", font=("Comic Sans MS",
                                               14, "bold"))
        if i > 0:
            temp = canvas.create_text((3+square_size) + square_size//2 + i*square_size    , square_size // 2,
                               text=Second_Word[i-1], font=("Comic Sans MS",
                                               14, "bold"))
            canvas.tag_bind(temp, "<Enter>", lambda e, r=Top_String[i]: on_enter_left_column(e, r))
            canvas.tag_bind(temp, "<Button-1>", lambda e, r=Top_String[i],index = i: on_click_top_string(e, r, index))

    canvas.itemconfig(Left_Column[-1], fill=_from_rgb((255, 116, 0)))
    canvas.itemconfig(Top_String[-1], fill=_from_rgb((255, 116, 0)))
    Left_column_value = Left_Column[-1]
    First_Word_Index = First_Word_Size
    Top_string_value = Top_String[-1]
    Second_Word_Index = Second_Word_Size

    Rectangle_Map = [[0]*(Second_Word_Size+1) for i in range(First_Word_Size+1)]  # двумерный массив, в который потом
    # записывать все квадраты rectanglemap[i][j] = canvas.create_rectange

    Text_Map = [[0]*(Second_Word_Size+1) for i in range(First_Word_Size+1)]
    for i in range(First_Word_Size+1):
        for j in range(Second_Word_Size+1):
            Rectangle_Map[i][j] = canvas.create_rectangle(3+square_size + j*square_size, 3+square_size + i*square_size,
                                                          square_size+(square_size + 3) + j*square_size,
                                                          square_size+(square_size + 3) + i*square_size,
                        fill="red",
                        outline='blue',
                        width=3, )
            Text_Map[i][j] = canvas.create_text(3+square_size + square_size//2 +j * square_size,
                                                3+square_size + square_size//2 +i * square_size,
                               text="0", font=("Comic Sans MS", 14, "bold"))
            t, Matrix = Damerau_Levenshtein_Distance(First_Word,Second_Word)
            if i == 0:
                canvas.itemconfig(Text_Map[i][j], text=str(Matrix[i][j]))
            if j == 0:
                canvas.itemconfig(Text_Map[i][j], text=str(Matrix[i][j]))

    canvas.config(scrollregion=(0, 0, square_size*(Second_Word_Size+2)+5, square_size*(First_Word_Size+2) + 5))


def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1+1):
        d[(i, -1)] = i+1
    for j in range(-1, lenstr2+1):
        d[(-1, j)] = j+1

    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = change_cost
            d[(i, j)] = min(
                          d[(i-1, j)] + deletion_cost,  # deletion
                          d[(i, j-1)] + insertion_cost,  # insertion
                          d[(i-1, j-1)] + cost,  # substitution
                        )
            if i and j and s1[i] == s2[j-1] and s1[i-1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i-2, j-2] + swap_cost)  # transposition

    for i in range(len(d)):
        for j in range(len(d[i])):
            print(d[i][j], end=" ")
        print()
    print("--------------")
    return d[lenstr1-1, lenstr2-1]


def animate_steps_next():
    global step_counter
    print(Rectangle_Map)
    print(all_steps[step_counter])
    t,Matrix = Damerau_Levenshtein_Distance(First_Word[0:First_Word_Index], Second_Word[0:Second_Word_Index])
    if all_steps[step_counter][1] == 'select':
        print("??")
        canvas.itemconfig(all_steps[step_counter][0], fill = "green")

    if all_steps[step_counter][1] == 'min':
        print("??")
        canvas.itemconfig(all_steps[step_counter][0], fill = "pink")


    if all_steps[step_counter][1] == 'reset':
        canvas.itemconfig(Text_Map[all_steps[step_counter][0][0]][all_steps[step_counter][0][1]],
                          text = str(Matrix[all_steps[step_counter][0][0]][all_steps[step_counter][0][1]]))

        canvas.itemconfig(Rectangle_Map[all_steps[step_counter][0][0]][all_steps[step_counter][0][1]], fill = "red")
        canvas.itemconfig(Rectangle_Map[all_steps[step_counter][0][0]-1][all_steps[step_counter][0][1]], fill="red")
        canvas.itemconfig(Rectangle_Map[all_steps[step_counter][0][0]][all_steps[step_counter][0][1]-1], fill="red")
        canvas.itemconfig(Rectangle_Map[all_steps[step_counter][0][0]-1][all_steps[step_counter][0][1]-1], fill="red")
        canvas.itemconfig(Rectangle_Map[all_steps[step_counter][0][0] - 2][all_steps[step_counter][0][1] - 2],
                              fill="red")

        text.insert(1.0, "Нашел значение для елемента ["+str(all_steps[step_counter][0][0])+","+
                    str(all_steps[step_counter][0][1])+"], оно равно "+
                    str(Matrix[all_steps[step_counter][0][0]][all_steps[step_counter][0][1]])+"\n")
    step_counter+=1
    if(step_counter>-1):
        Prev_Button.config(state="active")
    if(step_counter >= len(all_steps)):
        Next_Button.config(state="disable")

def animate_steps_prev():
    global step_counter
    step_counter -= 1

    print(Rectangle_Map)
    print(all_steps[step_counter])
    t,Matrix = Damerau_Levenshtein_Distance(First_Word[0:First_Word_Index], Second_Word[0:Second_Word_Index])
    if all_steps[step_counter][1] == 'select':
        print("??")
        canvas.itemconfig(all_steps[step_counter][0], fill = "red")

    if all_steps[step_counter][1] == 'min':
        print("??")
        canvas.itemconfig(all_steps[step_counter][0], fill = "red")

    if all_steps[step_counter][1] == 'reset':
        canvas.itemconfig(Text_Map[all_steps[step_counter][0][0]][all_steps[step_counter][0][1]],
                          text = "0")

        canvas.itemconfig(Rectangle_Map[all_steps[step_counter][0][0]][all_steps[step_counter][0][1]], fill = "green")
        canvas.itemconfig(Rectangle_Map[all_steps[step_counter][0][0]-1][all_steps[step_counter][0][1]], fill="pink")
        canvas.itemconfig(Rectangle_Map[all_steps[step_counter][0][0]][all_steps[step_counter][0][1]-1], fill="pink")
        canvas.itemconfig(Rectangle_Map[all_steps[step_counter][0][0]-1][all_steps[step_counter][0][1]-1], fill="pink")
        if all_steps[step_counter][0][0]-2>0 and all_steps[step_counter][0][1] >0 and\
            First_Word[all_steps[step_counter][0][0]-1] == Second_Word[all_steps[step_counter][0][1]-2] and\
            First_Word[all_steps[step_counter][0][0]-2] == Second_Word[all_steps[step_counter][0][1]-1]:
            canvas.itemconfig(Rectangle_Map[all_steps[step_counter][0][0] - 2][all_steps[step_counter][0][1] - 2],
                              fill="pink")
    if (step_counter == 0):
        Prev_Button.config(state="disable")
        return
    if(step_counter < len(all_steps)):
        Next_Button.config(state = "active")


def auto_animate():
    global step_counter
    t,Matrix = Damerau_Levenshtein_Distance(First_Word[0:First_Word_Index], Second_Word[0:Second_Word_Index])
    for i in range(step_counter, len(all_steps)):
        if all_steps[i][1] == 'select':
            canvas.after(500,canvas.itemconfig(all_steps[i][0], fill = "green"))

        if all_steps[i][1] == 'min':
            canvas.after(500,canvas.itemconfig(all_steps[i][0], fill = "pink"))


        if all_steps[i][1] == 'reset':
            canvas.itemconfig(Text_Map[all_steps[i][0][0]][all_steps[i][0][1]],
                              text = str(Matrix[all_steps[i][0][0]][all_steps[i][0][1]]))

            canvas.after(500,canvas.itemconfig(Rectangle_Map[all_steps[i][0][0]][all_steps[i][0][1]], fill = "red"))
            canvas.after(500,canvas.itemconfig(Rectangle_Map[all_steps[i][0][0]-1][all_steps[i][0][1]], fill="red"))
            canvas.after(500,canvas.itemconfig(Rectangle_Map[all_steps[i][0][0]][all_steps[i][0][1]-1], fill="red"))
            canvas.after(500,canvas.itemconfig(Rectangle_Map[all_steps[i][0][0]-1][all_steps[i][0][1]-1], fill="red"))
            canvas.after(500,canvas.itemconfig(Rectangle_Map[all_steps[i][0][0] - 2][all_steps[i][0][1] - 2],
                                  fill="red"))

            text.insert(1.0, "Нашел значение для елемента ["+str(all_steps[i][0][0])+","+
                        str(all_steps[i][0][1])+"], оно равно "+
                        str(Matrix[all_steps[i][0][0]][all_steps[i][0][1]])+"\n")
        if(i>-1):
            Prev_Button.config(state="active")
        if(i >= len(all_steps)):
            Next_Button.config(state="disable")


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


def Damerau_Levenshtein_Distance_For_Anim(first_string: str, second_string: str):
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
            all_steps.append((Rectangle_Map[current_DLDmatrix_string_index][current_DLDmatrix_column_index], "select"))
            all_steps.append((Rectangle_Map[current_DLDmatrix_string_index - 1][current_DLDmatrix_column_index], "min"))
            all_steps.append((Rectangle_Map[current_DLDmatrix_string_index][current_DLDmatrix_column_index - 1], "min"))
            all_steps.append(
                (Rectangle_Map[current_DLDmatrix_string_index - 1][current_DLDmatrix_column_index - 1], "min"))

            if current_DLDmatrix_string_index-2>0 and current_DLDmatrix_column_index-2>0 and \
                    first_string[current_DLDmatrix_string_index-1] == second_string[current_DLDmatrix_column_index - 2] and\
                    first_string[current_DLDmatrix_string_index - 2] == second_string[current_DLDmatrix_column_index-1]:
                DLDmatrix[current_DLDmatrix_string_index][current_DLDmatrix_column_index] =\
                    min(DLDmatrix[current_DLDmatrix_string_index][current_DLDmatrix_column_index],
                        DLDmatrix[current_DLDmatrix_string_index - 2][current_DLDmatrix_column_index - 2] + swap_cost)  # transposition
                if DLDmatrix[current_DLDmatrix_string_index][current_DLDmatrix_column_index] == \
                        DLDmatrix[current_DLDmatrix_string_index - 2][current_DLDmatrix_column_index - 2] + swap_cost:
                    all_steps.append(
                        (Rectangle_Map[current_DLDmatrix_string_index - 2][current_DLDmatrix_column_index - 2], "min"))
            all_steps.append(((current_DLDmatrix_string_index,current_DLDmatrix_column_index), "reset"))

    return DLDmatrix[first_string_length][second_string_length], DLDmatrix


def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

def Submit_clicked():
    global First_Word, Second_Word
    global change_cost, swap_cost, insertion_cost, deletion_cost
    if First_Word_Enrty.get() == "" or Second_Word_Enrty.get() == "":
        text.insert(1.0, "Одно из слов пустое\n")
        Get_Answer_Button.config(state="disable")
        Animate_Button.config(state="disable")
        return
    if int(Delete_SpinBox.get()) == 0 and int(Insert_SpinBox.get()) == 0 and int(Change_SpinBox.get())==0 and int(Swap_SpinBox.get())==0:
        text.insert(1.0, "В проверке нет смысла, настройте стоимости операций(Для информации обратитесь в окно 'О программе')\n")
        Get_Answer_Button.config(state="disable")
        Animate_Button.config(state="disable")
        return
    First_Word = First_Word_Enrty.get()
    Second_Word = Second_Word_Enrty.get()
    deletion_cost = int(Delete_SpinBox.get())
    insertion_cost = int(Insert_SpinBox.get())
    change_cost = int(Change_SpinBox.get())
    swap_cost = int(Swap_SpinBox.get())
    Get_Answer_Button.config(state = "active")
    Animate_Button.config(state = "active")
    draw_matrix()


def Get_Answer_clicked():
    global Answer_Label
    global Text_Map
    global canvas
    answer, matrix = Damerau_Levenshtein_Distance(First_Word[0:First_Word_Index], Second_Word[0:Second_Word_Index])
    Answer_Label.configure(text = "Answer: " + str(answer))
    for i in range(len(First_Word)+1):
        for j in range(len(Second_Word)+1):
            if i>First_Word_Index or j>Second_Word_Index:
                canvas.itemconfig(Text_Map[i][j], text="0")
                continue
            canvas.itemconfig(Text_Map[i][j], text=str(matrix[i][j]))

    print_lcs(First_Word[0:First_Word_Index],Second_Word[0:Second_Word_Index],matrix,None,None)

    f = open('result.txt', 'w')

    text_for_file = "Для преобразования строки "+First_Word[0:First_Word_Index] +" в строку "\
                    + Second_Word[0:Second_Word_Index] + " необходимо: "

    f.write(text_for_file + "\n")
    for i in range(len(result_text)):
        f.write(str(i+1)+")" + result_text[i] + "\n")
    f.close()
    result_text.clear()

    print(Rectangle_Map)


def Animate_clicked():
    global animating,step_counter
    if not animating:
        Next_Button.config(state="active")
        Prev_Button.config(state="disable")
        Auto_Button.config(state="disable")
        Submit_Button.config(state="disable")
        Get_Answer_Button.config(state="disable")
        Animate_Button.configure(text = "Stop Animate")
        animating= not animating
        Damerau_Levenshtein_Distance_For_Anim(First_Word[0:First_Word_Index],Second_Word[0:Second_Word_Index])
        for i in range(1,len(Text_Map)):
            for j in range(1,len(Text_Map[i])):
                canvas.itemconfig(Text_Map[i][j], text = "0")
    else:
        Next_Button.config(state="disable")
        Prev_Button.config(state="disable")
        Auto_Button.config(state="disable")
        Submit_Button.config(state="active")
        Get_Answer_Button.config(state="active")
        Animate_Button.configure(text = "Animate")
        animating = not animating
        step_counter = 0
        for i in range(len(Rectangle_Map)):
            for j in range(len(Rectangle_Map[i])):
                canvas.itemconfig(Rectangle_Map[i][j], fill = "red")
        all_steps.clear()


def Next_clicked():
    print("i was here")
    animate_steps_next()

def Prev_clicked():
    animate_steps_prev()

def Auto_clicked():
    global auto
    if not auto:
        Auto_Button.config(text="Manual")
        auto = not auto
        auto_animate()
    else:
        Auto_Button.config(text="Auto")
        auto = not auto

def settings_window():  # Функция оброботки нажатия на настройки

    def Accept_Clicked():
        global square_size
        global animate_speed
        square_size = int(Square_Size_SpinBox.get())
        animate_speed = float(Animate_Speed_SpinBox.get())
        settings.destroy()

    settings = Tk()
    settings.title("Настройки")
    settings.geometry('400x123')
    settings.resizable(width=False, height=False)
    settings.config(bg=_from_rgb((43, 98, 144)))

    Square_Size_Label = Label(settings,text ="Square size(px)" ,font=("Comic Sans MS",
                 12, "bold"),fg =_from_rgb((227, 234, 240)),bg = _from_rgb((43, 98, 144)))
    Square_Size_Label.place(x=5,y=5)

    Square_Size_SpinBox = Spinbox(settings, from_=40, to_=100)
    Square_Size_SpinBox.config(width=3, font=("Comic Sans MS", 14, "bold"), justify=CENTER,
                               buttonbackground=_from_rgb((227, 234, 240)),
                               bg=_from_rgb((227, 234, 240)))
    Square_Size_SpinBox.place(x=145, y=5)

    Animate_Speed_Label = Label(settings,text="Animate speed(s)", font=("Comic Sans MS",
                 12, "bold"),fg =_from_rgb((227, 234, 240)),bg = _from_rgb((43, 98, 144)))
    Animate_Speed_Label.place(x=5,y=40)

    Animate_Speed_SpinBox = Spinbox(settings, from_=0.2, to_=5.0,increment=0.1)
    Animate_Speed_SpinBox.config(width=3, font=("Comic Sans MS", 14, "bold"), justify=CENTER,
                               buttonbackground=_from_rgb((227, 234, 240)),
                               bg=_from_rgb((227, 234, 240)))
    Animate_Speed_SpinBox.place(x=145, y=40)


    Accept_Button = Button(settings, text = "Подтвердить", font=("Comic Sans MS", 14, "bold"),
                          bg = _from_rgb((14, 83, 167)),fg =_from_rgb((255, 156, 0)),
                          command = Accept_Clicked)
    Accept_Button.place(x=130,y=75)

    settings.mainloop()

def about_window():
    about = Tk()
    about.title("О программе")
    about.geometry('500x310')
    about.resizable(width=False, height=False)
    about.config(bg=_from_rgb((43, 98, 144)))
    main_info = Label(about, text ="    Данная программа предназначена для нахождения "
                                   "расстояния Дамерау - Левенштейна, а именно - сколько нужно сделать операций, что-бы получить из одной строки другую"
                                   ,font=("Comic Sans MS",
                 11, "bold"),fg =_from_rgb((227, 234, 240)),bg = _from_rgb((43, 98, 144)),wraplength=500)
    about1_label = Label(about, text ="     В программе есть несколько переменных, которые нужны для её работы. Это стоимости удаления,"
                                     "добавления и изменения элемента а так же стоимость свапа элементов",font=("Comic Sans MS",
                 11, "bold"),fg ="black",bg = _from_rgb((43, 98, 144)),wraplength=500)
    about2_label = Label(about, text="   Стоимости являються интуитивно понятные, то есть стоимость удаление - это как дорого избавиться от элемента,"
                                  "стоимость добавления - цена появления любого элемента, стоимость изменения - ценность замены одного элемента другим, "
                                  "и, конечно, усовершенстование Дамерау - стоимость свапа - как дорого поменять два соседние элементы."
                      , font=("Comic Sans MS",
                              11, "bold"), fg=_from_rgb((227, 234, 240)), bg=_from_rgb((43, 98, 144)), wraplength=500)
    File_label = Label(about,
                         text="     По нажатию на кнопку Get result будет создан файл с ответом на запрос. Имя файла - 'result'",
                         font=("Comic Sans MS",
                               11, "bold"), fg="black", bg=_from_rgb((43, 98, 144)), wraplength=500)
    main_info.pack(side=TOP)
    about1_label.pack(side=TOP)
    about2_label.pack(side=TOP)
    File_label.pack(side=TOP)
    about.mainloop()

MainWindow = Tk()
MainWindow.title("Расстояние Дамерау — Левенштейна")
MainWindow.geometry('700x480')
MainWindow.config(bg=_from_rgb((43, 98, 144)))
menu = Menu(MainWindow)
MainWindow.config(menu = menu)
MainWindow.resizable(width=False, height=False)
menu.add_cascade(label="Доп. настройки", command = settings_window)
menu.add_cascade(label="О программе", command = about_window)

x = (MainWindow.winfo_screenwidth() - MainWindow.winfo_reqwidth()) / 2
y = (MainWindow.winfo_screenheight() - MainWindow.winfo_reqheight()) / 2
MainWindow.wm_geometry("+%d+%d" % (x-350, y-150))

Data_Lable = Label(MainWindow, text ="Input Data",font=("Comic Sans MS",
                 18, "bold"),fg =_from_rgb((223, 209, 54)),justify=CENTER,bg = _from_rgb((43, 98, 144)))
Data_Lable.place(x =85,y=0)


First_Word_Lable = Label(MainWindow, text ="First word:",font=("Comic Sans MS",
                 14, "bold"),fg =_from_rgb((227, 234, 240)),justify=CENTER,bg = _from_rgb((43, 98, 144)))
First_Word_Lable.place(x =5,y=35)

First_Word_Enrty = Entry(MainWindow,font=("Comic Sans MS",
                 14, "bold"),justify=CENTER,borderwidth=0, bg = _from_rgb((227, 234, 240)))
First_Word_Enrty.place(x =150,y=40,width = 150,height = 25)


Second_Word_Lable = Label(MainWindow, text ="Second word:",font=("Comic Sans MS",
                 14, "bold"),fg =_from_rgb((227, 234, 240)),justify=CENTER,bg = _from_rgb((43, 98, 144)))
Second_Word_Lable.place(x =5,y=67)

Second_Word_Enrty = Entry(MainWindow,font=("Comic Sans MS",
                 14, "bold"),justify=CENTER,textvariable=23,borderwidth=0, bg = _from_rgb((227, 234, 240)))
Second_Word_Enrty.place(x =150,y=70,width = 150,height = 25)




Submit_Button = Button(MainWindow,command = Submit_clicked,text="Submit Data",font=("Comic Sans MS",
                 18, "bold"),bg = _from_rgb((14, 83, 167)),fg =_from_rgb((255, 156, 0)),borderwidth=1,activebackground = _from_rgb((14, 83, 167)),activeforeground=_from_rgb((255, 156, 0)))
Submit_Button.place(x =320,y=330,width = 165, height = 60)

Get_Answer_Button = Button(MainWindow,command = Get_Answer_clicked,text="Get Answer",font=("Comic Sans MS",
                 18, "bold"),bg = _from_rgb((14, 83, 167)),fg =_from_rgb((255, 156, 0)),borderwidth=1,state="disabled",activebackground = _from_rgb((14, 83, 167)),activeforeground=_from_rgb((255, 156, 0)))
Get_Answer_Button.place(x =320,y=395,width = 165, height = 60)

Animate_Button = Button(MainWindow,command = Animate_clicked,text="Animate",font=("Comic Sans MS",
                 18, "bold"),bg = _from_rgb((14, 83, 167)),fg =_from_rgb((255, 156, 0)),borderwidth=1,state="disabled",activebackground = _from_rgb((14, 83, 167)),activeforeground=_from_rgb((255, 156, 0)))
Animate_Button.place(x =520,y=330,width = 165, height = 60)

Answer_Label = Label(MainWindow, text ="Answer: ???",font=("Comic Sans MS",
                 18, "bold"),fg =_from_rgb((223, 209, 54)),justify=CENTER,bg = _from_rgb((43, 98, 144)))
Answer_Label.place(x =520,y=402)



Settings_Lable = Label(MainWindow, text ="Cost Settings",font=("Comic Sans MS",
                 18, "bold"),fg =_from_rgb((223, 209, 54)),justify=CENTER,bg = _from_rgb((43, 98, 144)))
Settings_Lable.place(x =85,y=95)

Delete_Lable = Label(MainWindow, text ="Delete: ",font=("Comic Sans MS",
                 14, "bold"),fg =_from_rgb((227, 234, 240)),justify=CENTER,bg = _from_rgb((43, 98, 144)))
Delete_Lable.place(x=5,y=155)

Delete_SpinBox = Spinbox(MainWindow,from_ =0, to_=1000)
Delete_SpinBox.config(width=3,font=("Comic Sans MS",
                 14, "bold"),justify=CENTER, buttonbackground=_from_rgb((227, 234, 240)),bg = _from_rgb((227, 234, 240)))
Delete_SpinBox.place(x=85,y=155)



Insert_Lable = Label(MainWindow, text ="Insert:",font=("Comic Sans MS",
                 14, "bold"),fg =_from_rgb((227, 234, 240)),justify=CENTER,bg = _from_rgb((43, 98, 144)))
Insert_Lable.place(x=5,y=215)

Insert_SpinBox = Spinbox(MainWindow,from_ =0, to_=1000)
Insert_SpinBox.config(width=3,font=("Comic Sans MS",
                 14, "bold"),justify=CENTER, buttonbackground=_from_rgb((227, 234, 240)),bg = _from_rgb((227, 234, 240)))
Insert_SpinBox.place(x=85,y=215)


Change_Lable = Label(MainWindow, text ="Change:",font=("Comic Sans MS",
                 14, "bold"),fg =_from_rgb((227, 234, 240)),justify=CENTER,bg = _from_rgb((43, 98, 144)))
Change_Lable.place(x=145,y=215)

Change_SpinBox = Spinbox(MainWindow,from_ =0, to_=1000)
Change_SpinBox.config(width=3,font=("Comic Sans MS",
                 14, "bold"),justify=CENTER, buttonbackground=_from_rgb((227, 234, 240)),bg = _from_rgb((227, 234, 240)))
Change_SpinBox.place(x=230,y=215)


Information_Lable = Label(MainWindow, text ="Information  Log",font=("Comic Sans MS",
                 18, "bold"),fg =_from_rgb((223, 209, 54)),justify=CENTER,bg = _from_rgb((43, 98, 144)))
Information_Lable.place(x =65,y=260)

Swap_Lable = Label(MainWindow, text ="Swap:",font=("Comic Sans MS",
                 14, "bold"),fg =_from_rgb((227, 234, 240)),justify=CENTER,bg = _from_rgb((43, 98, 144)))
Swap_Lable.place(x=145,y=155)

Swap_SpinBox = Spinbox(MainWindow,from_ =0, to_=1000)
Swap_SpinBox.config(width=3,font=("Comic Sans MS",
                 14, "bold"),justify=CENTER, buttonbackground=_from_rgb((227, 234, 240)),bg = _from_rgb((227, 234, 240)))
Swap_SpinBox.place(x=230,y=155)


# Настройка Лога, что нужно сделать(текстовое поле + скроллбар)
txtFrame = Frame(MainWindow, borderwidth=1, relief="sunken")
text = Text(txtFrame,width=34, height=8, borderwidth=0,bg=_from_rgb((122, 164, 199)),font=("Comic Sans MS",
                 10, "bold"))
scroll = Scrollbar(txtFrame, orient=VERTICAL, command=text.yview)
text['yscroll'] = scroll.set
scroll.configure( bg='yellow', troughcolor='red')
scroll.pack(side="right", fill="y")
text.pack(side="left", fill="both", expand=True)


txtFrame.place(x=5, y=300)
# =============================================================

text.config(yscrollcommand=scroll.set)


frame=Frame(MainWindow,width=500,height=400)
frame.place(x=310,y=5) #.grid(row=0,column=0)
canvas=Canvas(frame,bg='#FFFFFF',width=365,height=260)
hbar=Scrollbar(frame,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=canvas.xview)
vbar=Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)

canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side=LEFT,expand=True,fill=BOTH)


canvas.create_text(185, 130, text="Нажмите на кнопку 'Submit Data'\n для отображения", justify=CENTER,
                   font="Verdana 14")


Next_Button = Button(MainWindow,command = Next_clicked,text=">", font=("Comic Sans MS",
                 30, "bold"), bg=_from_rgb((14, 83, 167)), fg =_from_rgb((255, 156, 0)), justify=CENTER, borderwidth=1,
                     activebackground=_from_rgb((14, 83, 167)), activeforeground=_from_rgb((255, 156, 0)),
                     state="disable")
Next_Button.place(x=542, y=290, width=50, height=35)

Prev_Button = Button(MainWindow,command = Prev_clicked,text="<", font=("Comic Sans MS",
                 30, "bold"), bg=_from_rgb((14, 83, 167)), fg =_from_rgb((255, 156, 0)), justify=CENTER, borderwidth=1,
                     activebackground=_from_rgb((14, 83, 167)), activeforeground=_from_rgb((255, 156, 0)),
                     state="disable")
Prev_Button.place(x=398, y=290, width=50, height=35)

Auto_Button = Button(MainWindow, command=Auto_clicked,text="Auto",font=("Comic Sans MS", 18, "bold"),
                     bg=_from_rgb((14, 83, 167)),fg =_from_rgb((255, 156, 0)), justify=CENTER,
                     borderwidth=1, activebackground = _from_rgb((14, 83, 167)),
                     activeforeground=_from_rgb((255, 156, 0)),state="disable")
Auto_Button.place(x=450, y=290, width=90, height=35)

MainWindow.mainloop()
