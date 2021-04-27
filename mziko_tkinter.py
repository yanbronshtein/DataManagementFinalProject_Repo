from tkinter import *
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
from pprint import *
import tkinter as tk


def convert(entered_amount, currencies):
    cy = currency.get()
    # entered_amound = float(entered_amount)

    if cy == 1:  # GEL

        GEL_to_buy_entry.insert(0, str(entered_amount * 1))
        GEL_to_sell_entry.insert(0, str(entered_amount * 1))
        USD_to_buy_entry.insert(0, str(entered_amount * currencies[0]))
        USD_to_sell_entry.insert(0, str(entered_amount * currencies[1]))
        EURO_to_buy_entry.insert(0, str(entered_amount * currencies[2]))
        EURO_to_sell_entry.insert(0, str(entered_amount * currencies[3]))


    elif cy == 2:  # USD
        GEL_to_buy_entry.insert(0, str(entered_amount / currencies[0]))
        GEL_to_sell_entry.insert(0, str(entered_amount / currencies[1]))
        USD_to_buy_entry.insert(0, str(entered_amount * 1))
        USD_to_sell_entry.insert(0, str(entered_amount * 1))
    #        EURO_to_buy_entry.insert(0, str(entered_amount* ???))
    #        EURO_to_sell_entry.insert(0, str(entered_amount* ???))

    elif cy == 3:  # EURO
        GEL_to_buy_entry.insert(0, str(entered_amount / currencies[2]))
        GEL_to_sell_entry.insert(0, str(entered_amount / currencies[3]))
        #        USD_to_buy_entry.insert(0, str(entered_amount*???))
        #        USD_to_sell_entry.insert(0, str(entered_amount *???))
        EURO_to_buy_entry.insert(0, str(entered_amount * 1))
        EURO_to_sell_entry.insert(0, str(entered_amount * 1))


def parsing(banks):
    if banks == 1:
        r = requests.get("https://conditions.bog.ge/en/services/treasury-operations/exchange-rates")  # Bank of Georgia
        c = r.content
        soup = BeautifulSoup(c, "html.parser")

        data = soup.find_all("td")

        USD_to_buy = float(data[12].text.strip())
        USD_to_sell = float(data[13].text.strip())
        EURO_to_buy = float(data[17].text.strip())
        EURO_to_sell = float(data[18].text.strip())

        return USD_to_buy, USD_to_sell, EURO_to_buy, EURO_to_sell


    elif banks == 2:
        r = requests.get("https://www.tbcbank.ge/web/ka/web/guest/exchange-rates")  # TBC Bank
        c = r.content
        soup = BeautifulSoup(c, "html.parser")

        data = soup.find_all("div", {"class": "currRate"})

        USD_to_buy = float(data[0].text.strip())
        USD_to_sell = float(data[1].text.strip())
        EURO_to_buy = float(data[2].text.strip())
        EURO_to_sell = float(data[3].text.strip())

        return USD_to_buy, USD_to_sell, EURO_to_buy, EURO_to_sell

    elif banks == 3:
        r = requests.get("https://www.nbg.gov.ge/index.php?m=582")  # National Bank
        c = r.content
        soup = BeautifulSoup(c, "html.parser")

        data = soup.find_all("td", {"bgcolor": "#f9f9f9"})
        data1 = soup.find_all("td", {"bgcolor": "#ffffff"})

        USD_to_buy = float(data[102].text.strip())
        USD_to_sell = float(data[102].text.strip())
        EURO_to_buy = float(data1[32].text.strip())
        EURO_to_sell = float(data1[32].text.strip())

        return USD_to_buy, USD_to_sell, EURO_to_buy, EURO_to_sell


def do_convert(event):
    try:
        entered_amount = float(amount1.get())

    except:
        pass

    try:
        currencies = parsing(banks.get())
    except:
        pass

    convert(entered_amount, currencies)


main_window = Tk()

main_window.title("Currency Converter")

# To let consumers choose the bank
banks = IntVar()

Bank_of_Georgia = Radiobutton(main_window, text='Bank of Georgia ', font=(' Verdana ', 12), variable=banks, value=1)
Bank_TBC = Radiobutton(main_window, text='TBC Bank ', font=(' Verdana ', 12), variable=banks, value=2)
National_Bank = Radiobutton(main_window, text='National Bank ', font=(' Verdana ', 12), variable=banks, value=3)

Bank_of_Georgia.grid(row=0, column=0)
Bank_TBC.grid(row=0, column=1)
National_Bank.grid(row=0, column=2)

currency = IntVar()

# To let consumers choose the currency
GEL = Radiobutton(main_window, text='GEL', font=(' Verdana ', 12), variable=currency, value=1)
USD = Radiobutton(main_window, text='USD ', font=(' Verdana ', 12), variable=currency, value=2)
EURO = Radiobutton(main_window, text='EUR', font=(' Verdana ', 12), variable=currency, value=3)

GEL.grid(row=1, column=0)
USD.grid(row=1, column=1)
EURO.grid(row=1, column=2)

# To let the consumer enter the amount


amount = Label(main_window, text='Amount:  ', font=(' Verdana ', 12))
amount1 = Entry(main_window, font=('Verdana', 12), width=23)
amount.grid(row=2, column=0)
amount1.grid(row=2, column=1)

amount1.bind("<Return>", do_convert)

# btn1 = ttk.Button(main_window, text = "Convert", command = do_convert)
# btn1.grid(row = 2, column = 2)


# Outputs
To_buy = Label(main_window, text='To Buy', font=(' Verdana ', 12))
To_sell = Label(main_window, text='To Sell', font=(' Verdana ', 12))
To_buy.grid(row=3, column=1)
To_sell.grid(row=3, column=2)

GEL1 = Label(main_window, text='GEL', font=(' Verdana ', 12))
USD1 = Label(main_window, text='USD', font=(' Verdana ', 12))
EURO1 = Label(main_window, text='EUR', font=(' Verdana ', 12))

GEL1.grid(row=4, column=0)
USD1.grid(row=5, column=0)
EURO1.grid(row=6, column=0)

GEL_to_buy_entry = ttk.Entry(main_window, font=('Verdana', 12), width=23)
USD_to_buy_entry = ttk.Entry(main_window, font=('Verdana', 12), width=23)
EURO_to_buy_entry = ttk.Entry(main_window, font=('Verdana', 12), width=23)

GEL_to_buy_entry.grid(row=4, column=1)
USD_to_buy_entry.grid(row=5, column=1)
EURO_to_buy_entry.grid(row=6, column=1)

# GEL_to_buy_entry.state(['readonly'])
# USD_to_buy_entry.state(['readonly'])
# EURO_to_buy_entry.state(['readonly'])

GEL_to_sell_entry = ttk.Entry(main_window, font=('Verdana', 12), width=23)
USD_to_sell_entry = ttk.Entry(main_window, font=('Verdana', 12), width=23)
EURO_to_sell_entry = ttk.Entry(main_window, font=('Verdana', 12), width=23)

GEL_to_sell_entry.grid(row=4, column=2)
USD_to_sell_entry.grid(row=5, column=2)
EURO_to_sell_entry.grid(row=6, column=2)

# GEL_to_sell_entry.state(['readonly'])
# USD_to_sell_entry.state(['readonly'])
# EURO_to_sell_entry.state(['readonly'])


mainloop()

