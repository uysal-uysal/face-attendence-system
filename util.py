import os
import pickle

import tkinter as tk
from tkinter import messagebox

import face_recognition


def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
        window,
        text=text,
        activebackground="black",
        activeforeground="white",
        fg=fg,
        bg=color,
        command=command,
        height=2,
        width=15,
        font=('Helvetica bold', 20)
    )

    return button

global listbox
selected_lesson = ""

items = [
        "FIZ105 FIZIK LABORATUARI-1",
        "FIZ111 FIZIK-1",
        "MAT161 MATEMATIK-1",
        "TRD109 TÜRK DILI-1",
        "YDI107 INGILIZCE I",
        "YMH111 ALGORITMA VE PROG.-I",
        "YMH113 BILGISAYAR BILIMLERINE GIRIȘ",
        "YMH115 YAZILIM MÜH. ORYANTASYONU",

        "FIZ106 FIZIK LABORATUARI-II",
        "FIZ112 FIZIK - II",
        "MAT162 MATEMATIK - II",
        "TRD110 TÜRK DILI - II",
        "YDI108 INGILIZCE II",
        "YMH112 ALGORITMA VE PROGRAMLAMA-II",
        "YMH114 YAZILIM MÜH. TEMELLERI",

        "AIT209 ATATÜRK ILKELERI VE INKILAP TARIHI-I",
        "IST217 OLASILIK VE ISTATISTIK",
        "MAT215 LÍNEER CEBIR",
        "YMH211 AYRIK YAPILAR",
        "YMH213 MESLEKI INGILIZCE",
        "YMH215 SAYISAL TASARIM",
        "YMH217 NESNE TABANLI PROGRAMLAMA",

        "AIT210 Atatürk Ilkeleri ve Inkilap Tarihi II",
        "MAT220 DIFERANSIYEL DENKLEMLER",
        "YMH210 INGILIZCE ILETISIM BECERILERI",
        "YMH212 YAZILIM GEREKSINIMLERI VE ANALIZI",
        "YMH214 SAYISAL ANALIZ",
        "YMH216 YAZILIM EKONOMISI",
        "YMH218 VERI YAPILARI",
        "YMH220 ILERI PROGRAMLAMA TEKNIKLERI",

        "YMH311 YAZILIM TASARIM VE MIMARISI",
        "YMH313 ISLETIM SISTEMLERI",
        "YMH315 VERITABANI YÖNETIM SÍS.",
        "YMH317 ALGORITMA ANALIZI",
        "YMH319 PROGRAMLAMA DILLERI",
        "YMH321 BILGI SISTEMLERI VE GÜV.",
        "YMH325 MIKROISLEMCILER VE PROG.",

        "ISL451 GIRISIMCILIK-I",
        "YMH310 WEB TASARIMI VE PROG.",
        "YMH312 BIÇIMSEL DILLER VE OTOMATA TEORISI",
        "YMH314 FONKSIYONEL PROGRAMLAMA",
        "YMH322 VERI MADENCILII",
        "YMH332 AG PROGRAMLAMA",

        "YMH403 GIRISIMCILIK - II",
        "YMH451 Yapay Zeka",
        "YMH453 YAZILIM KALITE GUVENCESI VE TESTI",
        "YMH455 Bitirme Projesi",
        "YMH459 YAZILIM MUH.GUNCEL KONULAR",
        "YMH463 SAYISAL GORUNTU ISLEME YONTEMLERI",
    ]


def update_listbox():
    listbox.delete(0, tk.END)


def get_lesson_listbox(window, hgt, wdt):

    global listbox
    listbox = tk.Listbox(window, height=hgt, width=wdt)
    listbox.pack()

    for item in items:
        listbox.insert(tk.END, item)

    listbox.select_set(0)

    def on_select(event):
        global selected_lesson

        choosen = listbox.curselection()
        if choosen:
            selected_lesson = listbox.get(choosen[0])
            print(selected_lesson)

    clicked = tk.StringVar(window)
    clicked.set(items[0])
    clicked.trace_add('write', on_select)

    listbox.bind('<<ListboxSelect>>', on_select)

    return listbox


def get_dropdown(window):
    global selected_lesson

    options = [
        "YMH403 GIRISIMCILIK - II",
        "YMH451 Yapay Zeka",
        "YMH453 YAZILIM KALITE GUVENCESI VE TESTI",
        "YMH455 Bitirme Projesi",
        "YMH459 YAZILIM MUH.GUNCEL KONULAR",
        "YMH463 SAYISAL GORUNTU ISLEME YONTEMLERI"
    ]

    def update_selected_lesson():
        global selected_lesson
        selected_lesson = clicked.get()

    clicked = tk.StringVar(window)
    clicked.set(options[0])
    clicked.trace_add('write', update_selected_lesson)
    drop = tk.OptionMenu(window, clicked, *options)
    drop.pack()

    return drop


def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label


def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")
    return label


def get_entry_text(window):
    inputtxt = tk.Text(window,
                       height=2,
                       width=15, font=("Arial", 32))
    return inputtxt


def msg_box(title, description):
    messagebox.showinfo(title, description)


def recognize(img, db_path):
    # it is assumed there will be at most 1 match in the db

    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found'
    else:
        embeddings_unknown = embeddings_unknown[0]

    db_dir = sorted(os.listdir(db_path))

    match = False
    j = 0
    while not match and j < len(db_dir):
        path_ = os.path.join(db_path, db_dir[j])

        file = open(path_, 'rb')
        embeddings = pickle.load(file)

        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]
        j += 1

    if match:
        return db_dir[j - 1][:-7]
    else:
        return 'unknown_person'
