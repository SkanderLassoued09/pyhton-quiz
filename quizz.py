from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import re

root = Tk()
geometryWin = "900x450+300+200"
root.geometry(geometryWin)
# Style

root.title("Register")
global scoreUser
scoreUser = 0
var = IntVar()
# regex expession for a valid email
global emailRegex
emailRegex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
global questionNumber
questionNumber = 1

# -----------------INSERT VALUES INTO TABLE USER---------------------------
def submit():
    firstName = f_name.get()
    lastName = l_name.get()
    genderr = gender.get()
    contactNumero = contactNum.get()
    email = mail.get()
    passwWord = password.get()
    repassWord = repassword.get()
    id_profil = combo.value()
    id_level = combo1.value()

    if (firstName == "" or lastName == "" or genderr == "" or contactNumero == "" or email == "" or passwWord == "" or id_profil == 0 or id_level == 0):
        messagebox.showinfo("ERROR", "All fields are required")
    # test if the email has a vlid format using regex expression
    elif (not re.search(emailRegex,email)):
        messagebox.showinfo("ERROR", "Invalid email")
    elif (passwWord != repassWord):
        messagebox.showinfo("ERROR", "You must enter the same password")

    else:
        db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
        c = db.cursor()

        query = "insert into user (firstName,lastName, genderr, contactNumero , email, passwWord,id_profil,id_level) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        args = (firstName, lastName, genderr, contactNumero, email, passwWord, id_profil, id_level)
        c.execute(query, args)

        c.execute("commit")
        messagebox.showinfo("Done !", "Registered with success you can start the QUIZ ")
        db.close()
        return True
    return False

def startQuiz():

    # test if the form is valid
    if(submit() == False):
        return

    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    root.withdraw()
    if (id_profil == 1 and id_level == 1):
        displayQuestion1()
    elif (id_profil == 1 and id_level == 2):
        javaPro1()
    elif (id_profil == 1 and id_level == 3):
        javaExpert1()
    elif (id_profil == 2 and id_level == 1):
        pythonAmateur1()
    elif (id_profil == 2 and id_level == 2):
        pythonPro1()
    elif (id_profil == 2 and id_level == 3):
        pythonExpert1()
    elif (id_profil == 3 and id_level == 1):
        cAmateur1()
    elif (id_profil == 3 and id_level == 2):
        cPro1()
    elif (id_profil == 3 and id_level == 3):
        cExpert1()

    db.commit()
    db.close()
def destroyAllTopLevelWidgets():
    for widget in root.winfo_children():
        if isinstance(widget, Toplevel):
            widget.destroy()

def selected(userAnswer, correctAnswer):
    global scoreUser
    if (userAnswer.get() == correctAnswer):
        print("right")
        scoreUser += 1
    else:
        print("Wrong")



#-------------------HERE IS QQUESTINS JAVA AMATEUR----------------------------------

def displayQuestion1(row=1):
    global questionNumber

    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host = "localhost" , user = "root" , passwd = "" , database = "users")
    c = db.cursor()
    root_quiz1 = Toplevel(root)
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                   P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[1]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+ "-" +diplayQuestion +"("+ str(questionNumber)+"/4)")
        question_label.config(font = ("Arial",20,'bold'))

        question_label.grid(row=0, column=0, padx=20 , pady = 20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A , questions Q where Q.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[0]:
        print(correct)
    rightAnswer = correct
    questionNumber +=1
    #DICTIONNARY TO CREATE MULTPLE CHOICE
    v = IntVar()
    choices ={"Compiled" : 1,
              "Interepted" : 2,
               rightAnswer  : 3 ,
               "none of them": 4}
    for (text , value) in choices.items():
        radioButton =Radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radioButton.grid(row = row , column = 0 , ipady = 10  , padx = 20, sticky = W )
        row = row + 1
    v.set(0)

    #------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1 , text = "Next" , width = 20 , command = lambda: displayQuestion2(v,3))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)

    db.commit()
    db.close()
def displayQuestion2(answer,correctAnswer,row=1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)
    print(f"Score {scoreUser}")

    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    # ---------------- TO DISPLAY QUESTION N°2------------------------

    root_quiz2 = Toplevel()
    root_quiz2.title("Quiz")
    root_quiz2.geometry(geometryWin)
    # querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and
    #            "P.id_profil = '%d' L.id_level = '%d'"""(id_profil,id_level)
    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                   P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""

    for q in quest[0]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
    question_label = Label(root_quiz2, text=str(questionNumber)+"-" +diplayQuestion+"("+ str(questionNumber)+"/4)")
    question_label.config(font=("Arial", 20, 'bold'))
    question_label.grid(row=0, column=0, padx=20 , pady = 20 ,  sticky = W )
    # --------------------------------------------------------------

    # -----------------CHOICES--------------------------------------
    rightAnswerQuery = """select A.correct_answer from answer A , questions Q where Q.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[1]:
        print(correct)
    rightAnswer = correct
    v = IntVar()
    questionNumber+1
    choices ={"Oracle" : 1,
              "Google" : 2,
              "Yahoo" : 3,
              rightAnswer : 4}
    for(text , value) in choices.items():
        radioButton = Radiobutton(root_quiz2 , text = text , variable = v ,  value = value)
        radioButton.grid(row = row , column = 0 , padx = 20, pady = 10 ,  sticky = W )
        row+=1

    var.set(0)

    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz2, text="Next", width=20, command=lambda:displayQuestion3(v,4))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)


    db.commit()
    db.close()
def displayQuestion3(answer ,correctAnswer , row=1):
    global questionNumber
    selected(answer, correctAnswer)
    print(f"Score : {scoreUser}")
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    # ---------------- TO DISPLAY QUESTION N°3------------------------

    root_quiz3 = Toplevel()
    root_quiz3.title("Quiz")
    root_quiz3.geometry(geometryWin)
    # querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and
    #            "P.id_profil = '%d' L.id_level = '%d'"""(id_profil,id_level)
    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                       P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    # ---------------- TO DISPLAY QUESTION N°3------------------------
    for q in quest[2]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
    question_label = Label(root_quiz3, text=str(questionNumber) +"-"+ diplayQuestion+"("+ str(questionNumber)+"/4)")
    question_label.config(font=("Arial", 15, 'bold'))
    question_label.grid(row=0, column=0, padx=20 , pady = 10 , sticky = W)

    # -----------------CHOICES--------------------------------------
    rightAnswerQuery = """select A.correct_answer from answer A , questions Q where Q.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[2]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {rightAnswer : 1,
               "2003" : 2,
               "ciaoBonjour" : 3,
               "bonjour" : 4,}
    for (text , value) in choices.items():
        radioButton = Radiobutton(root_quiz3 , text = text , variable = v , value = value )
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row+=1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz3, text="Next", width=20, command=  lambda : displayQuestion4(v,1))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)

    db.commit()
    db.close()
def displayQuestion4(answer,correctAnswer, row=1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer,correctAnswer)
    print(f"Score : {scoreUser}")
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()

    root_quiz4 = Toplevel()
    root_quiz4.title("Quiz")
    root_quiz4.geometry(geometryWin)
    # querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and
    #            "P.id_profil = '%d' L.id_level = '%d'"""(id_profil,id_level)
    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                           P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    # ---------------- TO DISPLAY QUESTION N°4------------------------
    for q in quest[3]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
    question_label = Label(root_quiz4, text=str(questionNumber)+"-"+diplayQuestion+"("+ str(questionNumber)+"/4)")
    question_label.config(font=("Arial", 20, 'bold'))
    question_label.grid(row=0, column=0, padx=10 , sticky = W)

    # -----------------CHOICES--------------------------------------
    rightAnswerQuery = """select A.correct_answer from answer A , questions Q where Q.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[3]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {"encapsulation" : 1,
               "marginalization" : 2,
               rightAnswer  : 3,
               "inheritance" : 4}
    for (text , value) in choices.items():
        radioButton = Radiobutton(root_quiz4 , text = text , variable = v , value = value)
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W  )
        row+=1

    btnNext = Button(root_quiz4, text="Next", width=20, command=lambda: displayScore(v,3))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)


    db.commit()
    db.close()

def displayScore(answer , correctAnswer):
    destroyAllTopLevelWidgets()
    selected(answer,correctAnswer)
    print(f"Score : {scoreUser}")
    root_score = Toplevel()
    root_score.title("Final score")
    root_score.geometry(geometryWin)
    if(scoreUser > 2):
        scorerlabel = Label(root_score, text=f"You are accepted ! your final score is : {scoreUser}/4")
    else:
        scorerlabel = Label(root_score, text=f"Sorry your score is below required you have only : {scoreUser}/4")


    scorerlabel.config(font=("Arial",20,'bold'))
    scorerlabel.place(relx = 0.5 , rely = 0.5 , anchor = CENTER)


    # ------------------BUTTON RESULT-----------------------
#-------------------HERE IS QQUESTINS JAVA PRO----------------------------------
def javaPro1(row = 1):
    global questionNumber

    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                       P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[0]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20 , sticky = W)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[2]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct

    v = IntVar()
    choices = {"__" : 1,
               "0": 2,
               "String" : 3,
               rightAnswer: 4 }
    for (text, value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row+=1


    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command= lambda: javaPro2(v,4))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def javaPro2(answer , correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)

    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                       P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[1]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))
        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[3]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct

    v = IntVar()
    choices = {"Copyonwritearraylist" : 1,
               "an integer value" : 2,
               rightAnswer : 3,
               "None of the above is true.": 4}
    for (text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value)
        radioButton.grid(row = row , column = 0 , padx = 10 , pady = 10 ,sticky = W)
        row +=1
    #---------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command=lambda : javaPro3(v,3))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def javaPro3(answer , correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)

    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                       P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[2]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-"+ diplayQuestion +"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[4]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct

    v = IntVar()
    choices = {rightAnswer : 1 ,
               "It will throw an exception at runtime." : 2,
               "ClassCastException" : 3,
               "It will print calculating and will throw NoSuchMethodError" : 4}
    for (text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radioButton.grid(row = row , column = 0 , padx = 20, pady = 10 , sticky = W)
        row +=1

    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command = lambda : javaPro4(v , 1))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def javaPro4(answer , correctAnswer , row = 1 ):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)

    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                       P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[3]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[5]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct

    v = IntVar()
    choices = {"Encapsulation" : 1,
               rightAnswer : 2 ,
               "Compilation" : 3 ,
               "Polymorphisme" :4}
    for (text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value)
        radioButton.grid(row = row , column = 0 , padx = 20 , pady =10)
        row+=1

    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command= lambda : displayScore(v , 2))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
# -------------------HERE IS QQUESTINS JAVA PRO----------------------------------
def javaExpert1(row = 1):
    global questionNumber
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                           P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[0]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[6]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {rightAnswer : 1,
               "Enheritance" : 2,
               "Encapulation" : 3,
               "Polymorphisme" : 4
               }
    for (text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1, text=text, variable=v, value=value)
        radioButton.grid(row=row, column=0, padx=20, pady=10 , sticky = W)
        row += 1

    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command=lambda : javaExpert2(v,1))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def javaExpert2(answer ,correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)

    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                       P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[1]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[7]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v= IntVar()
    choices = {"Protected" : 1,
               "Encapsulation" : 2,
               rightAnswer : 3,
               "Polymorphisme" : 4
               }
    for (text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row +=1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command=lambda : javaExpert3(v,3))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def javaExpert3(answer , correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)

    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                       P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[2]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[8]:
        print(correct)
        questionNumber+1
    rightAnswer = correct

    v = IntVar()
    choices = {"Aggregation" : 1,
               rightAnswer : 2,
               "Compilation" : 3,
               "Encapsulation" : 4}
    for (text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 ,  sticky = W)
        row +=1

    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command= lambda : javaExpert4(v,2))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def javaExpert4(answer , correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                           P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[3]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-"+ diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[9]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {rightAnswer : 1,
               "Compilation" : 2,
               "Encapsulation" : 3,
               "Polymorphisme" : 4}
    for (text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row +=1

    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20 , command = lambda : displayScore(v , 1))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()

#-----------------------HERE IS QUESTIONS PYTHON AMATEUR-------------------

def pythonAmateur1(row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                               P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[0]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[22]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct

    var1 = IntVar()
    checkButton = Radiobutton(root_quiz1, text=rightAnswer, variable=var1 , value = 1)
    checkButton.config(font=("Arial", 15, 'italic'))
    checkButton.grid(row=1, column=0, padx=20, pady=20)
    v = IntVar()
    choices = {"Interpreted" : 1,
               "Compiled" : 2,
               rightAnswer : 3,
               "None of them" : 4}
    for (text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)

    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command= lambda :pythonAmateur2(v , 2))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def pythonAmateur2(answer , correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)

    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                           P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[1]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery ="""select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[23]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {"int(x)" : 1,
               rightAnswer : 2,
               "String(x)" : 3,
               "f(x)" : 4
               }
    for (text , value) in choices.item():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value)
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row +=1



    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command= lambda : pythonAmateur3(v,2))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def pythonAmateur3(answer , correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                           P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[2]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[24]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices ={"Less than" : 1,
              "Less than" : 2,
              "Equal to" : 3,
              rightAnswer : 4}
    for (text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radioButton.grid(row = row , column = 10 , padx = 20 , pady = 10 , sticky = W)
        row +=1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command=lambda : pythonAmateur4(v,4))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def pythonAmateur4(answer , correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                              P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[3]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion)
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery ="""select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[25]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct

    v = IntVar()
    choices = {"toString" : 1,
               "checkString()" : 2,
               rightAnswer : 3,
               "checkNumber" : 4}
    for(text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row+=1

    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20 , command = lambda : selected(c , 3))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
#----------------- HERE IS QUESTION PYTHON PRO ----------------------
def pythonPro1(row = 1):
    global questionNumber
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                                   P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[0]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[26]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices ={ rightAnswer : 1 ,
               "void" : 2,
               "String" : 3,
               "int" : 4}
    for (text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row +=1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command= lambda : pythonPro2(v,1))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def pythonPro2(answer , correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                               P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[1]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery ="""select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[27]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v= IntVar()
    choices = {"compare(list1,list2)" : 1,
               "c(list1,list2)" : 2,
               "==" : 3,
               rightAnswer : 4
               }
    for (text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row +=1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command=lambda : pythonPro3(v,4))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def pythonPro3(answer , correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                               P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[2]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery ="""select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[28]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {"min(str)" : 1 ,
               "minimum(String)" : 2,
               "str(min)" : 3 ,
                rightAnswer : 4}
    for (text , value ) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row +=1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command=lambda : pythonPro4(v,4))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def pythonPro4(answer , correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                                  P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[3]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[29]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {rightAnswer : 1,
               "open(file_name,open)" : 2 ,
               "open(file_name)" : 3,
               "open(open,file_name)" :4
                }
    for (text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W )
        row +=1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command = lambda : displayScore(v,1))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
# ----------------- HERE IS QUESTION PYTHON EXPERT ---------------------
def pythonExpert1(row = 1):
    global questionNumber
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                                      P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[0]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-"+ diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[30]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {"def proc" : 1 ,
               "definition" : 2 ,
               "public" : 3 ,
               rightAnswer : 4
               }
    for(text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value)
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row =+1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command= lambda : pythonExpert2(v,4))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def pythonExpert2(answer , correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                                   P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[1]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[31]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {"in" : 1,
               "true true" : 2 ,
               rightAnswer : 3 ,
                "is not true" : 4}
    for (text , value) in choices.items():
        radiobutton = Radiobutton(root_quiz1 , text = text , variable = v , value = value)
        radiobutton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row+=1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command=lambda : pythonExpert3(v ,3))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def pythonExpert3(answer , correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                                   P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[2]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery ="""select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[32]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v= IntVar()
    choices = {"list.insert(index)":1,
               rightAnswer : 2,
               "insert.list(index)":3 ,
               "list.insert(objet,index)":4}
    for (text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row +=1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command=lambda : pythonExpert4(v,2))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def pythonExpert4(answer , correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                                     P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[3]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A , questions Q where Q.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[33]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {rightAnswer : 1,
               "import m" : 2,
               "import mathematics" : 3 ,
               "import mathematics.math" : 4
               }
    for(text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radioButton.grid(row = row , column = 0 , padx = 20 , pady= 10 , sticky = W)
        row+=1
        #----------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20 , command= lambda : displayScore(v , 1))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
# ----------------- HERE IS QUESTION C AMATEUR ---------------------
def cAmateur1( row = 1):
    global questionNumber
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                                         P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[0]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[10]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {"_xcv" : 1 ,
               "32xcv" : 2 ,
               "'__6xcv" : 3 ,
               rightAnswer : 4
               }
    for(text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row +=1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command= lambda : cAmateur2(v,4))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def cAmateur2(answer , correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)

    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                                       P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[1]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"1 - " + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[11]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v= IntVar()
    choices = {"Xcv_23" : 1 ,
               rightAnswer : 2 ,
               "v12345" : 3 ,
               "GHGH1" : 4
               }
    for(text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value)
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row +=1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command=lambda :cAmateur3(v,2))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def cAmateur3(answer , correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                                       P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[2]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[12]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {"It is not standardized" : 1 ,
               "To avoid conflicts with environment variables of an operating system" : 2 ,
               rightAnswer : 3 ,
               "To avoid conflicts since assemblers and loaders use such names" : 4}
    for (text , value ) in choices.items():
        radionButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radionButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row +=1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command=lambda : cAmateur4(v,3))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def cAmateur4(answer , correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                                        P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[3]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery ="""select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[13]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v= IntVar()
    choices = {"Uppercase" : 1 ,
               rightAnswer : 2 ,
               "start with number" : 3,
               "None of thme" : 4
               }
    for (text , value) in choices.items():
        radiobutton = radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radiobutton.grid(row = row , column = 0 , padx = 20 , pady =10 , sticky = W)
        row =+1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20 , command = lambda : displayScore(v,2))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()

# ----------------- HERE IS QUESTION C PRO ---------------------
def cPro1(row = 1):
    global questionNumber
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                                         P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[0]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[14]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {rightAnswer : 1 ,
               "The assembly and loader implementation" : 2 ,
               "Langage C " : 3 ,
               "None of them" : 4
               }
    for(text , value ) in choices.items():
        radiobutton = Radiobutton(root_quiz1 , text = text , variable = v , value = value , command = lambda : selected(v,1))
        radiobutton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row+=1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command=lambda : cPro2(v,1))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def cPro2(answer , correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer , correctAnswer)
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                                       P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[1]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[15]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {"int variable_count;" : 1,
               rightAnswer : 2 ,
               "float taux;" : 3 ,
               "int nbr;" :4}
    for (text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value )
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row+=1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command=lambda :cPro3(v,2))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def cPro3(answer , correctAnswer , row = 1):
    global questionNumber
    destroyAllTopLevelWidgets()
    selected(answer,correctAnswer)
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                                       P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[2]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[16]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {"int my_nbr = 100, 000;" : 1,
               "int $my_nbr = 10000;" : 2,
               "int my nbr = 1000;" : 3,
               rightAnswer : 4}
    for (text , value) in choices.items():
        radioButton : Radiobutton(root , text = text , variable = v , value = value)
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row = +1

    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command=lambda :cPro4(v,4))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def cPro4(answer , correctAnswer , row = 1):
    global questionNumber
    selected(answer , correctAnswer)
    destroyAllTopLevelWidgets()
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                                        P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[3]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[17]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {rightAnswer : 1 ,
               "Hello World!" : 2 ,
               "Hello World! followed by rondom value" : 3 ,
               "Hello World! x;" : 4}
    for (text , value ) in choices.items():
        radoButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value)
        radoButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row = +1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20 , command = displayScore(v , 1))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
# ----------------- HERE IS QUESTION C EXPERT ---------------------
def cExpert1(answer , correctAnswer , row = 1):
    selected(answer , correctAnswer)
    destroyAllTopLevelWidgets()
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                                         P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[0]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-"+ diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery ="""select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[18]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {"Hello World! 20" :1,
               "Hello World! 9000": 2,
               rightAnswer : 3,
               "Hello World! followed by a random value":4}
    for(text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value)
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row =+1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command=cExpert2)
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def cExpert2(answer , correctAnswer , row = 1):
    global questionNumber
    selected(answer , correctAnswer)
    destroyAllTopLevelWidgets()
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                                       P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[1]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[19]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {"int PI = 3.14;" : 1,
               rightAnswer : 2,
               "double PI = 3.14;" : 3,
               "float PI = 3.14;" : 4}
    for(text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value)
        radioButton.grid(row = row , column = 0 , padx = 20 , pady = 10 , sticky = W)
        row =+1

    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command= lambda : cExpert3(v, 2))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def cExpert3(answer , correctAnswer , row = 1):
    global questionNumber
    selected(answer , correctAnswer)
    destroyAllTopLevelWidgets()
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                                       P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[2]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-" + diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery ="""select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[20]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {rightAnswer : 1,
               "This will cause a compilation error" : 2 ,
               "This will cause a runtime error" : 3,
               "It goes into an infinite loop": 4}
    for(text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1 , text = text , variable = v , value = value)
        radioButton.grid(row = row , column=0 , padx = 20 , pady = 10 ,sticky = W)
        row +=1
    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20, command=lambda : cExpert4(v,1 ))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()
def cExpert4(answer , correctAnswer , row = 1):
    global questionNumber
    selected(answer , correctAnswer)
    destroyAllTopLevelWidgets()
    id_profil = combo.value()
    id_level = combo1.value()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="users")
    c = db.cursor()
    root_quiz1 = Toplevel()
    root_quiz1.title("Quiz")
    root_quiz1.geometry(geometryWin)

    querySelect = """select Q.question from questions Q , profil P , level L where Q.id_profil = P.id_profil and Q.id_level = L.id_level and  
                                        P.id_profil = """ + str(id_profil) + " and L.id_level = " + str(id_level)
    c.execute(querySelect)
    # quest = QUESTIONS INSIDE TABLE
    quest = c.fetchall()
    diplayQuestion = ""
    for q in quest[3]:
        print(str(q))
        diplayQuestion = str(q) + "\n"
        # ---------------TO DISPLAY QUESTION N°1 FROM DATABASE----------------------
        question_label = Label(root_quiz1, text=str(questionNumber)+"-"+ diplayQuestion+"("+ str(questionNumber)+"/4)")
        question_label.config(font=("Arial", 20, 'bold'))

        question_label.grid(row=0, column=0, padx=20, pady=20)
        # --------------------------------------------------------
    # --------------Choices----------------
    rightAnswerQuery = """select A.correct_answer from answer A  where A.id_question = A.id_answer """
    c.execute(rightAnswerQuery)
    rightAnswer = c.fetchall()
    for correct in rightAnswer[21]:
        print(correct)
        questionNumber+=1
    rightAnswer = correct
    v = IntVar()
    choices = {"The special character '-'" : 1,
               "The special character '?'" : 2,
               rightAnswer : 3,
               "The name of the variable begins with an integer" :4
               }
    for(text , value) in choices.items():
        radioButton = Radiobutton(root_quiz1, text=text, variable=v, value=value)
        radioButton.grid(row=row, column=0, padx=20, pady=10 , sticky = W)
        row += 1


    # ------------------BUTTON NEXT-----------------------
    btnNext = Button(root_quiz1, text="Next", width=20 , command = lambda : displayScore(v,3))
    btnNext.place(relx=0.5, rely=0.8, anchor=NW)
    db.commit()
    db.close()

# ----------------- THIS FUNCTION TO CREATE A COMBOBOX SUPPORTS DICTIONARY
class DictComboBox(ttk.Combobox):
    def __init__(self, master, dictionary, *args, **kw):
        ttk.Combobox.__init__(self, master, values=list(dictionary.keys()), state='readonly', *args, **kw)
        self.dictionary = dictionary
        self.bind('<<ComboboxSelected>>', self.selected)  # purely for testing purposes

    def value(self):
        return self.dictionary[self.get()]

    def selected(self, event):  # Just to test
        print(self.value())





f_name = ttk.Entry(root, width=40)
f_name.grid(row=1, column=1, padx=10, pady=10)
l_name = ttk.Entry(root, width=40)
l_name.grid(row=2, column=1, padx=10, pady=10)
gender = StringVar()
ttk.Radiobutton(root, text="Male", variable=gender, value="Male").place(relx = 0.4, rely = 0.2, anchor = NW)
ttk.Radiobutton(root, text="Female", variable=gender, value="Female").grid(row=3, column=1, padx=10, pady=10,sticky = W)
contactNum = ttk.Entry(root, width=40)
contactNum.grid(row=4, column=1, padx=10, pady=10)
mail = ttk.Entry(root, width=40)
mail.grid(row=5, column=1, padx=10, pady=10)
password = ttk.Entry(root, width=40)
password.grid(row=6, column=1, padx=10, pady=10)
repassword = ttk.Entry(root, width=40)
repassword.grid(row=7, column=1, padx=10, pady=10)
# changes are here: use the custom DictComboBox instead of comboBox of TK to support dictionary
listeoflang = {"Choose one": 0, "Java": 1, "Python": 2, "C": 3}
combo = DictComboBox(root, listeoflang)
combo.grid(row=8, column=1, padx=10, pady=10)
combo.current(0)
listOflevel = {"Choose one": 0, "Beginner": 1, "Senior": 2, "Expert": 3}
combo1 = DictComboBox(root, listOflevel)
combo1.grid(row=9, column=1, padx=10, pady=10)
combo1.current(0)

# Labels
titleLabel = Label(root , text = "We are happy to see you  !")
titleLabel.config(font=("Helvetica", 20, 'bold'))
titleLabel.place(relx = 0.8 , rely = 0.4 , anchor = "center")
f_NameL = Label(root, text="Enter your first name")
f_NameL.grid(row=1, column=0,sticky = W )
l_nameL = Label(root, text="Enter your last name ")
l_nameL.grid(row=2, column=0,sticky = W)
checkBoxL = Label(root, text=" Choose your gender")
checkBoxL.grid(row=3, column=0,sticky = W)
contactNumL = Label(root, text="Enter your number phone")
contactNumL.grid(row=4, column=0,sticky = W)
mailL = Label(root, text="Enter your E-mail")
mailL.grid(row=5, column=0,sticky = W)
passwordL = Label(root, text="Enter your password")
passwordL.grid(row=6, column=0,sticky = W)
repasswordL = Label(root, text="Re enter your password")
repasswordL.grid(row=7, column=0,sticky = W)
comboL = Label(root, text="Select your speciality")
comboL.grid(row=8, column=0,sticky = W)
combo1L = Label(root, text="Select your Level")
combo1L.grid(row=9, column=0,sticky = W)
canavas = Canvas(root , width = 250, height = 90)
canavas.place(relx = 0.6 , rely = 0.1 )
img = PhotoImage(file = "C:\\Users\\mariem\\Desktop\\itserv.png")
canavas.create_image(10,10, image = img, anchor = NW)

#-----------------REGISTER BUTTON , START QUIZ BUTTON-----------------

btnStartQuiz = ttk.Button(root, text="Start QUIZ !", command=lambda : startQuiz())
btnStartQuiz.grid(row=10, column=1, padx=10, pady=10)

root.mainloop()