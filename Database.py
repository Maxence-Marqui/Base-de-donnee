from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3
import re


root = Tk()
root.title("Database")

#Regex patterns
sql_injection_pattern = re.compile(r"(\'\'|\&|\~|\"|\{|\}|\(|\)|\-\-|\`|\_|\\|\^|\@|\]|\[|\#|\=|\+|\°|\-\')")
prenom_pattern = re.compile(r"[0-9]")
nom_pattern = re.compile(r"[0-9]")
ville_pattern = re.compile(r"[0-9]")
etat_pattern = re.compile(r"[0-9]")
code_postal_pattern = re.compile(r"[a-zA-Z]")

def people_list():

    entry_prenom.delete(0,END)
    entry_nom.delete(0,END)
    entry_adresse.delete(0,END)
    entry_ville.delete(0,END)
    entry_etat.delete(0,END)
    entry_code_postal.delete(0,END)

    conn = sqlite3.connect('adress_book.db')
    c = conn.cursor()
    c.execute("SELECT oid, first_name, last_name FROM adresses")
    records= c.fetchall()
    liste_personne.delete(0,END)
    
    for personne in records:
        string_personne = re.sub("[(),']",'',str(personne))
        liste_personne.insert(END,string_personne+"\n")
    conn.commit()
    conn.close()    

def view_profil():

    entry_prenom.delete(0,END)
    entry_nom.delete(0,END)
    entry_adresse.delete(0,END)
    entry_ville.delete(0,END)
    entry_etat.delete(0,END)
    entry_code_postal.delete(0,END)

    string_index = ''.join(str(liste_personne.curselection()))
    index = re.sub('[(),]','',string_index)
    index = liste_personne.get(index)
    index = index.split(" ")

    conn = sqlite3.connect('adress_book.db')
    c = conn.cursor()
    c.execute("SELECT * FROM adresses WHERE oid = " + index[0])
    records = c.fetchall()

    for record in records : 
        entry_prenom.insert(0, record[0])
        entry_nom.insert(0, record[1])
        entry_adresse.insert(0, record[2])
        entry_ville.insert(0, record[3])
        entry_etat.insert(0, record[4])
        entry_code_postal.insert(0, record[5])

    conn.commit()
    conn.close()

def ajouter():
    check_box = 0
    match_count = 0
    list_to_check = [entry_prenom.get(),entry_nom.get(),entry_adresse.get(),entry_ville.get(),entry_etat.get(),entry_code_postal.get()]

    conn = sqlite3.connect('adress_book.db')
    c = conn.cursor()

    for entry_check in list_to_check:
        matches = re.search(sql_injection_pattern,entry_check)
        if matches :
            label_error = Label(root, text ="Saisies non valides")
            label_error.grid(row=8,column=1,columnspan = 2)
            label_error.after(3000, label_error.destroy)
        else:
            match_count +=1

    if match_count == 6:
        match_prenom = re.search(prenom_pattern,entry_prenom.get())
        match_nom = re.search(nom_pattern,entry_nom.get())
        match_ville = re.search(ville_pattern,entry_ville.get())
        match_etat = re.search(etat_pattern,entry_etat.get())
        match_code_postal = re.search(code_postal_pattern,entry_code_postal.get())

        if not match_prenom:
            check_box += 1
        if not match_nom:
            check_box += 1
        if not match_ville:
            check_box += 1
        if not match_etat:
            check_box += 1
        if not match_code_postal:
            check_box += 1
        
        if check_box != 5:

            label_error = Label(root, text ="Saisies non valides")
            label_error.grid(row=8,column=1,columnspan = 2)
            label_error.after(3000, label_error.destroy)
            conn.commit()
            conn.close()

    if check_box == 5:

        c.execute("SELECT oid, first_name, last_name FROM adresses WHERE first_name LIKE ? AND last_name LIKE ? AND adresse LIKE ? AND ville LIKE ? AND etat LIKE ? AND code_postal LIKE ?",((entry_prenom.get()),(entry_nom.get()),(entry_adresse.get()),(entry_ville.get()),(entry_etat.get()),(entry_code_postal.get())))
        records= c.fetchall()

        if records :
            label_error = Label(root, text ="Cette personne est déja enregistrée")
            label_error.grid(row=8,column=1,columnspan = 2)
            label_error.after(3000, label_error.destroy)

        else:
            c.execute("INSERT INTO adresses VALUES (:first_name, :last_name, :adresse, :ville, :etat, :code_postal)",
                {
                    'first_name': entry_prenom.get(),
                    'last_name' : entry_nom.get(),
                    'adresse' : entry_adresse.get(),
                    'ville' : entry_ville.get(),
                    'etat' : entry_etat.get(),
                    'code_postal' : entry_code_postal.get()
                })
                
            conn.commit()
            conn.close()

            entry_prenom.delete(0,END)
            entry_nom.delete(0,END)
            entry_adresse.delete(0,END)
            entry_ville.delete(0,END)
            entry_etat.delete(0,END)
            entry_code_postal.delete(0,END)

            label_valide = Label(root, text ="Ajout réussi")
            label_valide.grid(row=8,column=1,columnspan = 2)
            label_valide.after(3000, label_valide.destroy)

            people_list()
    
def update():

    check_box = 0
    match_count = 0
    list_to_check = [entry_prenom.get(),entry_nom.get(),entry_adresse.get(),entry_ville.get(),entry_etat.get(),entry_code_postal.get()]
    
    for entry_check in list_to_check:
        matches = re.search(sql_injection_pattern,entry_check)
        if matches:
            label_error = Label(root, text ="Saisies non valides")
            label_error.grid(row=8,column=1,columnspan = 2)
            label_error.after(3000, label_error.destroy)
        else:
            match_count +=1

    if match_count == 6:

        match_prenom = re.search(prenom_pattern,entry_prenom.get())
        match_nom = re.search(nom_pattern,entry_nom.get())
        match_ville = re.search(ville_pattern,entry_ville.get())
        match_etat = re.search(etat_pattern,entry_etat.get())
        match_code_postal = re.search(code_postal_pattern,entry_code_postal.get())

        if not match_prenom:
            check_box += 1
        if not match_nom:
            check_box += 1
        if not match_ville:
            check_box += 1
        if not match_etat:
            check_box += 1
        if not match_code_postal:
            check_box += 1

        if check_box != 5:

            label_error = Label(root, text ="Saisies non valides")
            label_error.grid(row=8,column=1,columnspan = 2)
            label_error.after(3000, label_error.destroy)
            conn.commit()
            conn.close()

    if check_box == 5:

        string_index = ''.join(str(liste_personne.curselection()))
        index = re.sub('[(),]','',string_index)
        index = liste_personne.get(index)
        index = index.split(" ")

        conn = sqlite3.connect('adress_book.db')
        c = conn.cursor()


        c.execute("""UPDATE adresses SET
            first_name = :first,
            last_name = :last,
            adresse = :address,
            ville = :city,
            etat = :state,
            code_postal = :zipcode

            WHERE oid = :oid""",
            {
            'first': entry_prenom.get(),
            'last': entry_nom.get(),
            'address' :entry_adresse.get(),
            'city' :entry_ville.get(),
            'state' : entry_etat.get(),
            'zipcode' :entry_code_postal.get(),
            'oid' : index[0]
            })
        
        conn.commit()
        conn.close()

        label_valide = Label(root, text ="Modifications enregistrées")
        label_valide.grid(row=8,column=1,columnspan = 2)
        label_valide.after(3000, label_valide.destroy)

        people_list()

def supprimer():

    string_index = ''.join(str(liste_personne.curselection()))
    index = re.sub('[(),]','',string_index)
    index = liste_personne.get(index)
    index = index.split(" ")

    conn = sqlite3.connect('adress_book.db')
    c = conn.cursor()
    c.execute("DELETE from adresses WHERE oid = " + index[0])
    conn.commit()
    conn.close()

    entry_prenom.delete(0,END)
    entry_nom.delete(0,END)
    entry_adresse.delete(0,END)
    entry_ville.delete(0,END)
    entry_etat.delete(0,END)
    entry_code_postal.delete(0,END)

    people_list()

def search():
    check_box = 0
    match_count = 0
    list_to_check = [entry_prenom.get(),entry_nom.get(),entry_adresse.get(),entry_ville.get(),entry_etat.get(),entry_code_postal.get()]

    conn = sqlite3.connect('adress_book.db')
    c = conn.cursor()

    for entry_check in list_to_check:
        matches = re.search(sql_injection_pattern,entry_check)
        if matches :
            label_error = Label(root, text ="Saisies non valides")
            label_error.grid(row=8,column=1,columnspan = 2)
            label_error.after(3000, label_error.destroy)
        else:
            match_count +=1
    
    if match_count == 6:

        match_prenom = re.search(prenom_pattern,entry_prenom.get())
        match_nom = re.search(nom_pattern,entry_nom.get())
        match_ville = re.search(ville_pattern,entry_ville.get())
        match_etat = re.search(etat_pattern,entry_etat.get())
        match_code_postal = re.search(code_postal_pattern,entry_code_postal.get())

        if not match_prenom:
            check_box += 1
        if not match_nom:
            check_box += 1
        if not match_ville:
            check_box += 1
        if not match_etat:
            check_box += 1
        if not match_code_postal:
            check_box += 1
        
        if check_box != 5:
            label_error = Label(root, text ="Saisies non valides")
            label_error.grid(row=8,column=1,columnspan = 2)
            label_error.after(3000, label_error.destroy)
            conn.commit()
            conn.close()
    
    if check_box == 5:

        liste_personne.delete(0,END)
    
        prenom = entry_prenom.get()
        nom = entry_nom.get()
        adresse = entry_adresse.get()
        ville = entry_ville.get()
        etat = entry_etat.get()
        code_postal = entry_code_postal.get()

        if prenom == "":
            prenom = "%"
        if nom == "":
            nom = "%"
        if adresse == "":
            adresse = "%"
        if ville == "":
            ville = "%"
        if etat == "":
            etat = "%"
        if code_postal == "":
            code_postal = "%"

        c.execute("SELECT oid, first_name, last_name FROM adresses WHERE first_name LIKE ? AND last_name LIKE ? AND adresse LIKE ? AND ville LIKE ? AND etat LIKE ? AND code_postal LIKE ?",((prenom),(nom),(adresse),(ville),(etat),(code_postal)))
        records= c.fetchall()

        for personne in records:
            string_personne = re.sub("[(),']",'',str(personne))
            liste_personne.insert(END,string_personne+"\n")
        conn.commit()
        conn.close()

#declaring widgets

frame = Frame(root)
scrollbar = Scrollbar(frame)
liste_personne = Listbox(frame, width= 60, yscrollcommand = scrollbar.set,exportselection = False )
scrollbar.config( command = liste_personne.yview)

frame.grid(row = 9, column = 0, columnspan = 4,padx = 10, pady = 10)
liste_personne.pack( side = LEFT, fill = BOTH )
scrollbar.pack( side = RIGHT, fill = Y )

add_button = enregistrer = Button(root, text = "Ajouter", command = ajouter)
update_button = Button(root, text = "Modifier", command = update)
delete_button = Button(root, text="Supprimer ID", command = supprimer)
view_profil_button = Button(root, text = "Voir profil", command = view_profil)
search_button = Button(root, text = "Rechercher", command = search)
stop_search = Button(root, text = "Annuler recherche", command = people_list)

add_button.grid(row=7, column = 1,padx = 10)
update_button.grid(row = 7, column= 2,padx = 10)

delete_button.grid(row = 6, column = 3,padx = 10)
search_button.grid(row = 3, column = 3, padx = 10)
view_profil_button.grid(row = 1, column= 3,padx = 10)
stop_search.grid(row = 4 ,column = 3, padx = 10)
    
empty_space_1 = Label(root, text = " ", height = 0)
empty_space_1.grid(row = 0, column = 0, columnspan = 4)

label_first_name = Label(root, text ="Prénom")
label_last_name = Label(root, text ="Nom")
label_adresse = Label(root, text ="Adresse")
label_ville = Label(root, text ="Ville")
label_etat = Label(root, text ="Etat")
label_code_postal = Label(root, text ="Code Postal")

label_first_name.grid(row=1,column=0)
label_last_name.grid(row=2,column=0)
label_adresse.grid(row=3,column=0)
label_ville.grid(row=4,column=0)
label_etat.grid(row=5,column=0)
label_code_postal.grid(row=6,column=0)

entry_prenom = Entry(root, width = 35, borderwidth = 2)
entry_nom = Entry(root, width = 35, borderwidth = 2)
entry_adresse =Entry (root, width = 35, borderwidth = 2)
entry_ville = Entry(root, width = 35, borderwidth = 2)
entry_etat = Entry(root, width = 35, borderwidth = 2)
entry_code_postal = Entry(root, width = 35, borderwidth = 2)

entry_prenom.grid(row=1,column=1,columnspan = 2,pady =3)
entry_nom.grid(row=2,column=1,columnspan = 2)
entry_adresse.grid(row=3,column=1,columnspan = 2)
entry_ville.grid(row=4,column=1,columnspan = 2)
entry_etat.grid(row=5,column=1,columnspan = 2)
entry_code_postal.grid(row=6,column=1,columnspan = 2)

people_list()

root.mainloop()