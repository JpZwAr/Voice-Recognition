from tkinter import *

#janela principal

main = Tk()
main.title("Cristina")
largura = 300
altura = 500
largura_tela = main.winfo_screenwidth()
altura_tela = main.winfo_screenheight()
posx = largura_tela/2 - largura/2
posy = altura_tela/2 - altura/2
main.geometry("%dx%d+%d+%d" % (largura,altura,posx,posy))
main.iconbitmap("microphone.ico")
main["bg"] = "#762582"
main.resizable(width=False, height=False)

#janela de configuracao

def Config():
    config = Toplevel(main)
    config.title("Configurações")
    config.geometry("250x300+%d+%d" % (posx+130,posy+100))
    config["bg"] = "#762582"
    config.iconbitmap("gears.ico")

#imagem

sym = PhotoImage(file = r"athena.png")
micon = PhotoImage(file = r"microphoneOn.png")
micon2 = PhotoImage(file = r"microphoneOn2.png")

micoff = PhotoImage(file= r"microphoneOff.png")
micoff2 = PhotoImage(file=r"microphoneOff2.png")

eng = PhotoImage(file = r"gears.png")

#label

lb = Label(main, text="Assistente Virtual Cristina", bg="#762582", fg="#FFFFFF", font=("Helvetica","14","bold"))
lb.pack(pady="15")

logo = Label(main, image=sym, bg="#762582")
logo.pack()

#botao

valor = IntVar()

btn = Radiobutton(main, bg="#762582", activebackground="#b438c7", image=micon, selectimage=micon2, width="55", height="55", variable=valor, value=0, indicatoron=0)
btn.pack(pady="25")

btn2 = Radiobutton(main, bg="#762582", activebackground="#b438c7", image=micoff, selectimage=micoff2, width="55", height="55", variable=valor, value=1, indicatoron=0)
btn2.pack(pady="15")

btn3 = Button(main, bg="#762582", activebackground="#b438c7", image=eng, width="43", height="43", command=Config)
btn3.pack(side=BOTTOM, padx="115", pady="15")

main.mainloop()
