from tkinter import *

def convert_temperature():
    try:
        temp = float(farenheit_entry.get())
        temp = (temp - 32) * 5 / 9
        celcius_entry.insert(0, str(temp))
        farenheit_entry.delete(0, END)


    except:
        temp = float(celcius_entry.get())
        temp = (temp *9/5) + 32
        farenheit_entry.insert(0, str(temp))
        celcius_entry.delete(0, END)


main_window = Tk()

main_window.title("Temperature Converter")

Fahrenheit = Label(text='Fahrenheit ', font=(' Verdana ', 12))
Celsius = Label(text='Celsius ', font=(' Verdana ', 12))

farenheit_entry = Entry(font=('Verdana', 12), width=4)
celcius_entry = Entry(font=('Verdana', 12), width=4)
print(farenheit_entry.get())
btn1 = Button(text="calculate", font=('Verdana', 12), command=convert_temperature)

Fahrenheit.grid(row=0, column=0)
Celsius.grid(row=1, column=0)

farenheit_entry.grid(row=0, column=1)
celcius_entry.grid(row=1, column=1)
btn1.grid(row=1, column=2)


mainloop()