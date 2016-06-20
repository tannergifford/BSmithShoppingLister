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
    recipeLocation = filedialog.askopenfilename(filetypes=(("Beersmith Recipe Files", "*.bsmx"), ("All files", "*.*")))
    if recipeLocation:
        try:
            textbox.delete(0, END)
            textbox.insert(END, recipeLocation)
        except:
            messagebox.showerror("Open Source File", "Failed to read file \n'%s'"%recipeLocation)
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
    for r in sorted(recipeList):
        listbox.insert(END, r)

def BuildList():
    active = listbox.get(ACTIVE)
    recipeLocation = textbox.get()
    regex = re.compile("(<Recipe><_MOD_>\d{4}-\d{2}-\d{2}</_MOD_>.<F_R_NAME>"+active+"</F_R_NAME>.*?</Recipe>)", re.MULTILINE|re.DOTALL)

    bs_file = open(recipeLocation, 'r')
    text = bs_file.read()
    bs_file.close()

    directory = "C:/Users/" + os.getlogin() + "/Desktop/Recipes/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    out_file = open(directory + active+"_recipe.txt","w")
    out_file.write(active + " ingredients\n")

    match = regex.search(text)
    if match:
        messagebox.showinfo("Recipe Found", active + " recipe found")
        text = match.group(0)
    else:
        messagebox.showerror("Selected", "No match or Selection")
        return

    # Grain
    regex = re.compile("(<Grain>.*?</Grain>)", re.MULTILINE|re.DOTALL)
    grain_t_dict = {}
    grain_c_dict = {}
    grain_o_dict = {}
    grain_q_dict = {}
    out_file.write("\nGrain: \n")
    for match in regex.finditer(text,re.S):
        grain = regex.search(match.group(1))
        grain = grain.group(0)
        grain_type = (re.search(r"<F_G_TYPE>(.+)</F_G_TYPE>", grain)).group(1)
        if grain_type == "1":
            grain_type = "LME"
        elif grain_type == "3":
            grain_type = "Adjunct"
        elif grain_type == "4":
            grain_type = "DME"
        elif grain_type == "0":
            grain_type = "Grain"
        else:
            grain_type = "Unknown"
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
    for grains in grain_q_dict:
        out_file.write("Name: " + grains + "\n")
        out_file.write("Origin: " + grain_o_dict[grains] + "\n")
        out_file.write("Type: " + grain_t_dict[grains] +"\n")
        out_file.write("Color: " + str(grain_c_dict[grains]) + " SRM\n")
        out_file.write("Quantity: " + str(round(grain_q_dict[grains],2)) + "oz\n")
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

    for hop in hops_q_dict:
        out_file.write("Name: " + hop +" "+ str(hops_aa_dict[hop]) + " AA\n")
        out_file.write("Origin: " + hops_o_dict[hop] + "\n")
        out_file.write("Quantity: " + str(round(hops_q_dict[hop], 2)) + "oz\n")
        out_file.write("\n")

    # Yeast
    regex = re.compile("(<Yeast>.*?</Yeast>)", re.MULTILINE|re.DOTALL)
    yeast_l_dict = {}
    yeast_q_dict = {}
    yeast_s_dict = {}
    yeast_i_dict = {}
    out_file.write("Yeast: \n")
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
    for yeasts in yeast_q_dict:
        out_file.write("Name: " + yeasts + " " + yeast_i_dict[yeasts] + "\n")
        out_file.write("Lab: " + yeast_l_dict[yeasts] + "\n")
        out_file.write("Quantity: " + str(round(yeast_q_dict[yeasts],2)) + "\n")
        out_file.write("Starter Size: " + str(round(yeast_s_dict[yeasts],2)) + "L\n")
        out_file.write("\n")

    # Misc
    regex = re.compile("(<Misc>.*?</Misc>)", re.MULTILINE|re.DOTALL)
    out_file.write("Miscellaneous: \n")
    for match in regex.finditer(text,re.S):
        misc = regex.search(match.group(1))
        misc = misc.group(0)
        misc_name = (re.search(r"<F_M_NAME>(.+)</F_M_NAME>", misc)).group(1)
        misc_use = (re.search(r"<F_M_USE_FOR>(.+)</F_M_USE_FOR>", misc)).group(1)
        misc_quantity = (re.search(r"<F_M_AMOUNT>(.+)</F_M_AMOUNT>", misc)).group(1)
        misc_units = (re.search(r"<F_M_UNITS>(.+)</F_M_UNITS>", misc)).group(1)
        units_dict = {'0':'mg', '1':'g', '2':'oz', '3':'lb', '4':'kg', '5':'ml', '6':'tsp', '7':'tbsp', '8':'Cup', '9':'pt', '10':'qt', '11':'l', '12':'gal', '13':'Items',}
        unit = units_dict[misc_units]
        out_file.write("Name: " + misc_name + "\n")
        out_file.write("Use: " + misc_use + "\n")
        out_file.write("Quantity: " + misc_quantity[:-5] + " " + unit +"\n")
        out_file.write("\n")

	# Close up shop
    out_file.close()
    os.startfile(directory + active+"_recipe.txt")
	
# Set up main window
root.geometry("350x400")
root.resizable(0,0)
root.configure(background='#595959')
root.iconbitmap('icon.ico')
root.title("BSmith Shopping Lister")

# Create recipe file location textbox
textbox = Entry(root, bg="#d9d9d9", width=50)
if os.path.exists(recipeLoc):
    textbox.insert(END,recipeLoc)
else:
    textbox.insert(END,"Browse for Beer Smith Recipes")
textbox.pack(pady=5)

# Create Browse button
Button(root, text="Browse", bg="#808080", command=openFile).pack(pady=5)

# Create List Recipes button
Button(root, text="List Recipes", bg="#808080", command=RecipeList).pack(pady=5)

# Create frame for listbox
frame = Frame(root, bd=2, relief=SUNKEN)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
xscrollbar.grid(row=1, column=0, sticky=E+W)
yscrollbar = Scrollbar(frame)
yscrollbar.grid(row=0, column=1, sticky=N+S)
listbox = Listbox(frame, bd=0, width=50,
    bg="#d9d9d9",
    height=14,
    xscrollcommand=xscrollbar.set,
    yscrollcommand=yscrollbar.set)
listbox.grid(row=0, column=0, sticky=N+S+E+W)
xscrollbar.config(command=listbox.xview)
yscrollbar.config(command=listbox.yview)
frame.pack(pady=5)

# Create Build button
Button(root, text="Build Shopping List", bg="#808080", command=BuildList).pack(pady=5)

root.mainloop()
