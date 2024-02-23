"""
PROJECT 2 - OASIS INFOBYTE

BMI Calculator

Decription:
Develop a graphical BMI calculator with a user-friendly interface 
(GUI) usinglibraries like Tkinter. Allow users to input weight and height, 
calculate BMI, and visualize the result. Enable data storage for multiple users, 
historical data viewing, and BMI trend analysis through statistics and graphs.

BMI Categories:
Underweight = <18.5
Normal weight = 18.5–24.9
Overweight = 25–29.9
Obesity = BMI of 30 or greater
"""

import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sqlite3 as sql
import matplotlib.pyplot as plt

BG1 = "#facb02"
FONT1 = ('Verdana', 13)

conn = sql.connect("bmi_data.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS bmi_data(\
    ID  INTEGER PRIMARY KEY AUTOINCREMENT,\
    weight DOUBLE NOT NULL,\
    height DOUBLE NOT NULL,\
    bmi DOUBLE NOT NULL,\
    result TEXT NOT NULL,\
    enteredTime DATETIME DEFAULT CURRENT_TIMESTAMP)")

cursor.execute("SELECT * from bmi_data")
rows = cursor.fetchall()
# print(rows)

def bmiCalculator():

    try:
        wgt = float(wgt_ip.get())
        hgt = float(hgt_ip.get())
        bmi = wgt / (hgt*hgt)
        
        if bmi <= 18.5:
            res = "Underweight"
        elif  bmi >= 18.5 and bmi < 25:
            res = "Normal Weight"
        elif bmi>=25.0 and bmi< 30:
            res = "Overweight"
        else:
            res = "Obese"

        res_lab.config(text=f"BMI = {bmi:.2f} kg/m^2")
        res_lab2.config(text=f"Result: {res}")

        cursor.execute("INSERT INTO bmi_data(weight, height, bmi, result) VALUES (?,?,?,?)", (wgt, hgt, bmi, res))
        conn.commit()

        wgt_ip.delete(0,'end')
        hgt_ip.delete(0,'end')

        trend.config(state='normal')

    except:
        messagebox.showerror("Error","Enter the details")

def bmiVisualiser():
    cursor.execute("SELECT bmi,enteredTime FROM bmi_data ORDER BY enteredTime")
    result = cursor.fetchall()

    if len(result)<2:
        messagebox.showerror("Info", "Not enough data to visualise")
        return

    bmi_val = []
    recordedtime_val = []

    for row in result:
        bmi_val.append(row[0])
        recordedtime_val.append(row[1])
    
    plt.figure(figsize= (9,6)) #Size of figure
    plt.plot(recordedtime_val, bmi_val , marker="o")#Plotting graph with markers
    plt.xlabel('Date & Time') #Labels for x and y axis
    plt.ylabel('Body Mass Index') #Labels for x and y axis
    plt.title('BMI over time') #Title of the plot
    plt.xticks(rotation=45) #Rotating x-axis labels so they can fit better
    plt.show()

root = tk.Tk()
root.title("Oasis InfoByte")
root.geometry("450x250+750+150")
root.config(background= BG1)

lab1 = Label(root, text='Metric BMI Calculator', font= ('Verdana', 13,'italic'), background= BG1)
lab1.place(x=9,y=9)

wgt_lab = Label(root, text="Weight (in kgs) = ", font=FONT1, background=BG1)
wgt_lab.place(x=9,y=60)

hgt_lab = Label(root, text="Height (in m) = ", font=FONT1, background=BG1)
hgt_lab.place(x=9,y=100)

wgt_ip = Entry(root, width=4, font=FONT1)
hgt_ip = Entry(root, width=4, font=FONT1)
wgt_ip.place(x=190,y=60)
hgt_ip.place(x=190, y=100)

calc = Button(root, text = "Calculate BMI", font=FONT1, command=bmiCalculator, background="light green")
calc.place(x=290,y=60)

res_lab = Label(root,background=BG1, font= ('Verdana', 13, 'bold'))
res_lab.place(x=10,y=160)

res_lab2 = Label(root,background=BG1, font=FONT1)
res_lab2.place(x=10,y=200)

trend = Button(root, text = "Visualise", font=FONT1, command=bmiVisualiser, background="light green", state="disabled")
trend.place(x=290,y=100)

root.mainloop()