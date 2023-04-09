"""In this project i have made simple gui of BMI calculator """
import tkinter

root = tkinter.Tk()
root.geometry("700x195")
root.title("HMPS_PROJECT_PA54_PA55_56")

# Functiom
def calculate_bmi():
    """After click on calculate button this function get called"""
    kgs = float(entry_kg.get())
    height = float(entry_Height.get())
    age = float(entry_Age.get())
    waist = float(entry_waist.get())
    hip = float(entry_hip.get())
    bmr = round(88.362+(13.397*kgs)+(4.799*height)-(5.677*age),2)
    vif = round((waist/hip),2)
    bmi = round(kgs / (height ** 2), 2)
    body_fat = round((1.20 * bmi) + ((0.23 * age) - 16.2),2)


    Label_result['text'] = f"BMI:{bmi}%"
    Label_result1['text'] = f"BODY FAT:{body_fat}%"
    Label_result2['text'] = f"VISCERAL FAT:{vif}%"
    Label_result3['text'] = f"RESTING METABOLIC RATE:{bmr}"

# GUI
Label_kg = tkinter.Label(root, text="BMI CALCULATOR ", fg="RED", font="times 25 bold")
Label_kg.grid(column=2, row=0)

#Label_&_Entrys
Label_kg = tkinter.Label(root, text="Weight(Kg): ", fg="brown", font="times 10 bold")
Label_kg.grid(column=0, row=1)
entry_kg = tkinter.Entry(root)
entry_kg.grid(column=1, row=1)

Label_Height = tkinter.Label(root, text="Height(m): ", fg="brown", font="times 10 bold")
Label_Height.grid(column=0, row=2)
entry_Height = tkinter.Entry(root)
entry_Height.grid(column=1, row=2)

Label_Age = tkinter.Label(root, text="Age: ", fg="brown", font="times 10 bold")
Label_Age.grid(column=0, row=3)
entry_Age = tkinter.Entry(root)
entry_Age.grid(column=1, row=3)

Label_waist = tkinter.Label(root, text="Waist(cm): ", fg="brown", font="times 10 bold")
Label_waist.grid(column=0, row=4)
entry_waist = tkinter.Entry(root)
entry_waist.grid(column=1, row=4)

Label_hip = tkinter.Label(root, text="Hip(cm): ", fg="brown", font="times 10 bold")
Label_hip.grid(column=0, row=5)
entry_hip = tkinter.Entry(root)
entry_hip.grid(column=1, row=5)

#Command_Button
button_calculator = tkinter.Button(root, text="Calculate",fg = "black",
                                   font="times 12 bold", command=calculate_bmi)
button_calculator.grid(column=2, row=6)

#Report_Output
Label_report = tkinter.Label(root, text="REPORT OUTCOME ", fg="blue", font="times 10 bold")
Label_report.grid(column=2, row=1)
Label_result = tkinter.Label(root, text="BMI:", fg="blue", font="times 10 bold")
Label_result.grid(column=2, row=2)

Label_result1 = tkinter.Label(root, text="BODY FAT: ", fg="blue", font="times 10 bold ")
Label_result1.grid(column=2, row=3)

Label_result2 = tkinter.Label(root, text= "VISCERAL FAT:", fg="blue", font="times 10 bold")
Label_result2.grid(column=2, row=4)

Label_result3 = tkinter.Label(root, text= "RESTING METABOLIC RATE:",
                              fg="blue", font="times 10 bold")
Label_result3.grid(column=2, row=5)

Label_MALE = tkinter.Label(root, text="MALE    FEMALE", fg="purple", font="times 10 bold")
Label_MALE.grid(column=4, row=1)
Label_BMI = tkinter.Label(root, text="23-28%    22-28%", fg="purple", font="times 10 bold")
Label_BMI.grid(column=4, row=2)

Label_BODYFAT = tkinter.Label(root, text="17-25%    24-35%", fg="purple", font="times 10 bold ")
Label_BODYFAT.grid(column=4, row=3)

Label_VIF = tkinter.Label(root, text= "5-14%    7-16%", fg="purple", font="times 10 bold")
Label_VIF.grid(column=4, row=4)

Label_RM = tkinter.Label(root, text= "1800-2000    1600-1800", fg="purple", font="times 10 bold")
Label_RM.grid(column=4,  row=5)

root.mainloop()