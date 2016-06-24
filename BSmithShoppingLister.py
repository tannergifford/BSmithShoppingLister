# Imports
import sys, os
import re
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

# Variables
recipeLoc = "C:/Users/" + os.getlogin() + "/Documents/BeerSmith2/Recipe.bsmx"
root = Tk()

# Functions
def openFile():
    recipeLocation = filedialog.askopenfilename(filetypes=(("BeerSmith Recipe Files", "Recipe*.bsmx"), ("All files", "*.*")))
    if recipeLocation:
        try:
            textbox.delete(0, END)
            textbox.insert(END, recipeLocation)
        except:
            messagebox.showerror("BeerSmith Recipe Lister", "Failed to read file \n'%s'"%recipeLocation)
        return

def RecipeList():
    recipeLocation = textbox.get()
    recipeList = []
    regex = "<F_R_NAME>(.+?)</F_R_NAME>"
    with open(recipeLocation, 'r') as file:
        lines = file.readlines()
        for line in lines:
            match = re.search(regex, line)
            if match:
                if match.group(1) not in recipeList:
                    recipeList.append(match.group(1))
    listbox.delete(0, END)
    if recipeList != []:
        for r in sorted(recipeList):
            listbox.insert(END, r)
    else:
        listbox.insert(END, "No recipes found in file")

def BuildList():
    active = listbox.get(ACTIVE)
    recipeLocation = textbox.get()
    regex = re.compile("(<Recipe><_MOD_>\d{4}-\d{2}-\d{2}</_MOD_>.<F_R_NAME>"+active+"</F_R_NAME>.*?</Recipe>)", re.MULTILINE|re.DOTALL)
    bs_file = open(recipeLocation, 'r')
    text = bs_file.read()
    bs_file.close()
    match = regex.search(text)
    if not match:
        messagebox.showerror("BeerSmith Recipe Lister", "No match or Selection")
        return
    else:
        try:
            directory = "C:/Users/" + os.getlogin() + "/Desktop/Recipes/"
            if not os.path.exists(directory):
                os.makedirs(directory)
            out_file = open(directory + active+"_recipe.txt","w")
            out_file.write(active + " ingredients\n")
            out_file.write("\n")
            text = match.group(0)
            
            # Grain
            regex = re.compile("(<Grain>.*?</Grain>)", re.MULTILINE|re.DOTALL)
            grain_t_dict = {}
            grain_c_dict = {}
            grain_o_dict = {}
            grain_q_dict = {}
            grain_type_dict = {'0':'Grain', '1':'LME', '2':'Sugar', '3':'Adjunct', '4':'DME'}
            out_file.write("Grain: \n")
            for match in regex.finditer(text,re.S):
                grain = regex.search(match.group(1))
                grain = grain.group(0)
                grain_type = (re.search(r"<F_G_TYPE>(.+)</F_G_TYPE>", grain)).group(1)
                grain_type = grain_type_dict[grain_type]
                grain_name = (re.search(r"<F_G_NAME>(.+)</F_G_NAME>", grain)).group(1)
                grain_origin = re.search(r"<F_G_ORIGIN>(.+)</F_G_ORIGIN>", grain)
                if grain_origin:
                    grain_origin = grain_origin.group(1)
                else:
                    grain_origin = "Unknown"
                grain_color = float((re.search(r"<F_G_COLOR>(.+)</F_G_COLOR>", grain)).group(1))
                grain_quantity = float((re.search(r"<F_G_AMOUNT>(.+)</F_G_AMOUNT>", grain)).group(1))
                if grain_name not in grain_t_dict:
                    grain_t_dict[grain_name] = grain_type
                if grain_name not in grain_q_dict:
                    grain_q_dict[grain_name] = grain_quantity
                elif grain_name in grain_q_dict:
                    quantity = grain_q_dict.get(grain_name)
                    new_quantity = float(quantity) + grain_quantity
                    grain_q_dict[grain_name] = new_quantity
                if grain_name not in grain_o_dict:
                    grain_o_dict[grain_name] = grain_origin
                if grain_name not in grain_c_dict:
                    grain_c_dict[grain_name] = grain_color
            for key, value in sorted(grain_q_dict.items(), key=lambda item: (item[1], item[0])):
                out_file.write("    Name: " + key + "\n")
                out_file.write("    Origin: " + grain_o_dict[key] + "\n")
                out_file.write("    Type: " + grain_t_dict[key] +"\n")
                out_file.write("    Color: " + str(grain_c_dict[key]) + " SRM\n")
                out_file.write("    Quantity: " + str(round(grain_q_dict[key],2)) + "oz\n")
                out_file.write("\n")

            # Hops
            regex = re.compile("(<Hops>.*?</Hops>)", re.MULTILINE|re.DOTALL)
            hops_aa_dict = {}
            hops_q_dict = {}
            hops_o_dict = {}
            out_file.write("Hops:\n")
            for match in regex.finditer(text,re.S):
                hops = regex.search(match.group(1))
                hops = hops.group(0)
                hops_name = (re.search(r"<F_H_NAME>(.+)</F_H_NAME>", hops)).group(1)
                hops_origin = re.search(r"<F_H_ORIGIN>(.+)</F_H_ORIGIN>", hops)
                if hops_origin:
                    hops_origin = hops_origin.group(1)
                else:
                    hops_origin = "Unknown"
                hops_alpha = float((re.search(r"<F_H_ALPHA>(.+)</F_H_ALPHA>", hops)).group(1))
                hops_quantity = float((re.search(r"<F_H_AMOUNT>(.+)</F_H_AMOUNT>", hops)).group(1))
                if hops_name not in hops_aa_dict:
                    hops_aa_dict[hops_name] = hops_alpha
                if hops_name not in hops_q_dict:
                    hops_q_dict[hops_name] = hops_quantity
                elif hops_name in hops_q_dict:
                    quantity = hops_q_dict.get(hops_name)
                    new_quantity = float(quantity) + hops_quantity
                    hops_q_dict[hops_name] = new_quantity
                if hops_name not in hops_o_dict:
                    hops_o_dict[hops_name] = hops_origin
            for key, value in sorted(hops_q_dict.items(), key=lambda item: (item[1], item[0])):
                out_file.write("    Name: " + key +" "+ str(hops_aa_dict[key]) + " AA\n")
                out_file.write("    Origin: " + hops_o_dict[key] + "\n")
                out_file.write("    Quantity: " + str(round(hops_q_dict[key], 2)) + "oz\n")
                out_file.write("\n")

            # Yeast
            regex = re.compile("(<Yeast>.*?</Yeast>)", re.MULTILINE|re.DOTALL)
            yeast_l_dict = {}
            yeast_q_dict = {}
            yeast_s_dict = {}
            yeast_i_dict = {}
            for match in regex.finditer(text,re.S):
                yeast = regex.search(match.group(1))
                yeast = yeast.group(0)
                yeast_name = (re.search(r"<F_Y_NAME>(.+)</F_Y_NAME>", yeast)).group(1)
                yeast_id = (re.search(r"<F_Y_PRODUCT_ID>(.+)</F_Y_PRODUCT_ID>", yeast)).group(1)
                yeast_lab = (re.search(r"<F_Y_LAB>(.+)</F_Y_LAB>", yeast)).group(1)
                yeast_quantity = float((re.search(r"<F_Y_AMOUNT>(.+)</F_Y_AMOUNT>", yeast)).group(1))
                yeast_starter = float((re.search(r"<F_Y_STARTER_SIZE>(.+)</F_Y_STARTER_SIZE>", yeast)).group(1))
                if yeast_name not in yeast_i_dict:
                    yeast_i_dict[yeast_name] = yeast_id
                if yeast_name not in yeast_l_dict:
                    yeast_l_dict[yeast_name] = yeast_lab
                if yeast_name not in yeast_q_dict:
                    yeast_q_dict[yeast_name] = yeast_quantity
                elif yeast_name in yeast_q_dict:
                    quantity = yeast_q_dict.get(yeast_name)
                    new_quantity = float(quantity) + yeast_quantity
                    yeast_q_dict[yeast_name] = new_quantity
                if yeast_name not in yeast_s_dict:
                    yeast_s_dict[yeast_name] = yeast_starter
                elif yeast_name in yeast_s_dict:
                    quantity = yeast_s_dict.get(yeast_name)
                    new_quantity = float(quantity) + yeast_starter
                    yeast_s_dict[yeast_name] = new_quantity
            if yeast_q_dict:
                out_file.write("Yeast: \n")
                for key, value in sorted(yeast_q_dict.items(), key=lambda item: (item[1], item[0])):
                    out_file.write("    Name: " + key + " " + yeast_i_dict[key] + "\n")
                    out_file.write("    Lab: " + yeast_l_dict[key] + "\n")
                    out_file.write("    Quantity: " + str(round(yeast_q_dict[key],2)) + "\n")
                    out_file.write("    Starter Size: " + str(round(yeast_s_dict[key],2)) + "L\n")
                    out_file.write("\n")

            # Misc
            regex = re.compile("(<Misc>.*?</Misc>)", re.MULTILINE|re.DOTALL)
            units_dict = {'0':'mg', '1':'g', '2':'oz', '3':'lb', '4':'kg', '5':'ml', '6':'tsp', '7':'tbsp', '8':'Cup', '9':'pt', '10':'qt', '11':'l', '12':'gal', '13':'Items',}
            misc_q_dict = {}
            misc_use_dict = {}
            misc_units_dict = {}
            for match in regex.finditer(text,re.S):
                misc = regex.search(match.group(1))
                misc = misc.group(0)
                misc_name = (re.search(r"<F_M_NAME>(.+)</F_M_NAME>", misc)).group(1)
                misc_use = (re.search(r"<F_M_USE_FOR>(.+)</F_M_USE_FOR>", misc)).group(1)
                misc_quantity = float((re.search(r"<F_M_AMOUNT>(.+)</F_M_AMOUNT>", misc)).group(1))
                misc_units = (re.search(r"<F_M_UNITS>(.+)</F_M_UNITS>", misc)).group(1)
                if misc_name not in misc_q_dict:
                    misc_q_dict[misc_name] = misc_quantity
                elif yeast_name in yeast_q_dict:
                    quantity = misc_q_dict.get(misc_name)
                    new_quantity = float(quantity) + misc_quantity
                    misc_q_dict[misc_name] = new_quantity
                if misc_name not in misc_units_dict:
                    unit = units_dict[misc_units]
                    misc_units_dict[misc_name] = unit
                if misc_name not in misc_use_dict:
                    misc_use_dict[misc_name] = misc_use 
            if misc_q_dict:
                out_file.write("Miscellaneous: \n")
                for key, value in sorted(misc_q_dict.items(), key=lambda item: (item[1], item[0])):
                    out_file.write("    Name: " + key + "\n")
                    out_file.write("    Use: " + misc_use_dict[key] + "\n")
                    out_file.write("    Quantity: " + str(round(misc_q_dict[key],2)) + " " + misc_units_dict[key] +"\n")
                    out_file.write("\n")

            # Close up shop
            out_file.close()
            messagebox.showinfo("BeerSmith Recipe Lister", active + " recipe loaded\n\n" + "Output location: " + directory + active + "_recipe.txt")
            os.startfile(directory + active+"_recipe.txt")
        except:
            messagebox.showerror("BeerSmith Recipe Lister", "Error\n\n" + str(sys.exc_info()[1]))
        return
        
def states(*args):
    y = stringvar1.get()
    if os.path.exists(y):
        button1.config(state='normal')
        #print("enable")
    else:
        button1.config(state='disabled')
        #print("disable")
        
# Set up main window
root.geometry("400x455")
root.resizable(0,0)
root.configure(background='#009999')
root.iconbitmap('images\\icon.ico')
root.title("BeerSmith Shopping Lister")

stringvar1 = StringVar(root)
stringvar1.trace("w", states)

# Create frame for recipe location
frame = Frame(root, bd=0, relief=RAISED, width=350, bg="#009999")
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=2)
textbox = Entry(frame, bg="#f0f5f5", width=50, textvariable=stringvar1)
button = Button(frame, text="Browse", bg="#b3cccc", command=openFile, width=8)
textbox.grid(row=0, column=0, sticky=N+S+E+W, padx=5)
button.grid(row=0, column=1, sticky=N+S+E+W, padx=5)
frame.pack(pady=(10,5))

# Create List Recipes button
button1 = Button(root, text="List Recipes", state="disabled", bg="#b3cccc", command=RecipeList, width=12)
button1.pack(pady=5)

if os.path.exists(recipeLoc):
    textbox.insert(END,recipeLoc)
else:
    textbox.insert(END,"Browse for Beer Smith Recipes")

# Create frame for listbox
frame = Frame(root, bd=2, relief=SUNKEN, bg="#009999")
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
xscrollbar.grid(row=1, column=0, sticky=E+W)
yscrollbar = Scrollbar(frame)
yscrollbar.grid(row=0, column=1, sticky=N+S)
listbox = Listbox(frame, bd=0, width=60,
    bg="#f0f5f5",
    height=19,
    xscrollcommand=xscrollbar.set,
    yscrollcommand=yscrollbar.set)
listbox.grid(row=0, column=0, sticky=N+S+E+W)
xscrollbar.config(command=listbox.xview)
yscrollbar.config(command=listbox.yview)
frame.pack(pady=5)

# Create Build button
Button(root, text="Build Shopping List", bg="#b3cccc", command=BuildList).pack(pady=(5, 0))

if __name__ == "__main__":
    root.mainloop()
