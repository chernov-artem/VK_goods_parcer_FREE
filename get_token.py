""" GUI для получение пользователем токена ВК"""
import tkinter
from tkinter import *
from tkinter import ttk
import webbrowser

request_token = "https://oauth.vk.com/authorize?client_id=51502375&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=135593988&response_type=token&v=5.131&state=123456"


def btn_click():
    webbrowser.open(request_token, new=2)


def btn_save():
    link_cut()
    label.config(bg="#7c7")
    label['text'] = "Токен сохранен"
    label2.config(bg="#c3c3c3")
    label2['text'] = "Можете приступать к работе с приложением"


def link_cut():
    link = url_entry.get()
    token = link[45:].split("&expires")[0]
    print(token)
    with open("token.txt", "w") as file:
        file.write(token)


root = Tk()
root['bg'] = '#fafafa'
root.title('Приложение v 1.0 ')
root.geometry('340x280')  # размеры окна

root.resizable(width=False, height=False)  # возможность растягивать окно

canvas = Canvas(root, height=640, width=480)
canvas.pack()

frame = Frame(root, bg='#999')
frame.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.97)
# кнопка 1
btn = Button(frame, text='Получить токен ВК', bg='white', command=btn_click)
btn.place(relx=0.03, rely=0.05, height=25, width=125)
# текстовое поле 1
text_label_1 = Label(frame, width=50, height=20, bg='#999')
text_label_1.place(relx=0.03, rely=0.17, height=20, width=235)
text_label_1['text'] = 'Вставьте данные из адресной строки:'

url_entry = Entry(frame, bg='white')
url_entry.place(relx=0.03, rely=0.27, height=20, width=235)

btn2 = Button(frame, text='Сохранить', bg='white', command=btn_save)
btn2.place(relx=0.5, rely=0.38, height=25, width=75)

label = Label(frame, bg="#999")
label.place(relx=0.5, rely=0.51)
label2 = Label(frame, bg='#999')
label2.place(relx=0.23, rely=0.58)

root.mainloop()
