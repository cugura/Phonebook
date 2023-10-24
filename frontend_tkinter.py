import tkinter as tk
from tkinter import ttk, END
import tkinter.font as tkFont
from tkinter import *
from tkinter import messagebox
from backend import *
from widget_hover import *


class App:
    def __init__(self, root):
        self.root = root
        root.title("Phonebook")
        width = 900
        height = 475
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # Treeview
        columns = ("OIB", "Ime", "Prezime")
        self.treeview = ttk.Treeview(root, columns=columns, show='headings')
        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=130)
        self.treeview.place(x=240, y=30, height=400)

        verscrlbar = ttk.Scrollbar(self.root, orient="vertical", command=self.treeview.yview)
        verscrlbar.place(x=632, y=30, height=400)

        self.treeview.config(yscrollcommand=verscrlbar.set)

        # Listbox telefonski brojevi
        self.listbox_telefon = tk.Listbox(root)
        self.listbox_telefon.place(x=660, y=30, height=150, width=150)
        self.label_telefon = Label(root, text="Phone number")
        self.label_telefon.place(x=660, y=10)

        # Listbox mailovi
        self.listbox_malovi = tk.Listbox(root)
        self.listbox_malovi.place(x=660, y=280, height=150, width=150)
        self.label_malovi = Label(root, text="Mail")
        self.label_malovi.place(x=660, y=260)

        self.button_search = tk.Button(root)
        self.button_search["bg"] = "#FFF5E0"
        self.button_search["cursor"] = "sizing"
        ft = tkFont.Font(family='Times', size=10)
        self.button_search["font"] = ft
        self.button_search["fg"] = "#000000"
        self.button_search["justify"] = "center"
        self.button_search["text"] = "Search"
        self.button_search.place(x=150, y=30, width=55, height=30)
        self.button_search["command"] = self.search_action_button

        self.frame_around_entry = tk.LabelFrame(root, height=250, width=225, bg="#FFBFBF")
        self.frame_around_entry.place(x=5,y=70)

        self.entry_search=tk.Entry(root, bg="#FFF5E0")
        self.entry_search["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.entry_search["font"] = ft
        self.entry_search["fg"] = "#333333"
        self.entry_search["justify"] = "center"
        self.entry_search["text"] = "Search"
        self.entry_search.place(x=10,y=30,width=119,height=30)
        self.entry_search.insert(0, "Search")

        button_unos=tk.Button(root)
        button_unos["bg"] = "#8CC0DE"
        button_unos["cursor"] = "sizing"
        ft = tkFont.Font(family='Times',size=10)
        button_unos["font"] = ft
        button_unos["fg"] = "#000000"
        button_unos["justify"] = "center"
        button_unos["text"] = "Add"
        button_unos.place(x=150,y=110,width=55,height=30)
        button_unos["command"] = self.button_plus

        self.entry_oib=tk.Entry(root)
        ft = tkFont.Font(family='Times',size=10)
        self.entry_oib["font"] = ft
        self.entry_oib["fg"] = "#333333"
        self.entry_oib["justify"] = "center"
        self.entry_oib["text"] = "Add new content"
        self.entry_oib.place(x=10,y=80,width=120,height=30)
        self.entry_oib.insert(0, "Id")

        self.entry_name=tk.Entry(root)
        self.entry_name["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.entry_name["font"] = ft
        self.entry_name["fg"] = "#333333"
        self.entry_name["justify"] = "center"
        self.entry_name["text"] = "Name"
        self.entry_name.place(x=10,y=120,width=120,height=30)
        self.entry_name.insert(0, "Name")

        self.entry_surname=tk.Entry(root)
        self.entry_surname["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.entry_surname["font"] = ft
        self.entry_surname["fg"] = "#333333"
        self.entry_surname["justify"] = "center"
        self.entry_surname["text"] = "Surname"
        self.entry_surname.place(x=10,y=170,width=120,height=30)
        self.entry_surname.insert(0, "Surname")

        self.entry_phone=tk.Entry(root)
        self.entry_phone["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.entry_phone["font"] = ft
        self.entry_phone["fg"] = "#333333"
        self.entry_phone["justify"] = "center"
        self.entry_phone["text"] = "Phone"
        self.entry_phone.place(x=10,y=220,width=120,height=30)
        self.entry_phone.insert(0, "Phone")

        self.entry_email=tk.Entry(root)
        self.entry_email["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.entry_email["font"] = ft
        self.entry_email["fg"] = "#333333"
        self.entry_email["justify"] = "center"
        self.entry_email["text"] = "Email"
        self.entry_email.place(x=10,y=270,width=120,height=30)
        self.entry_email.insert(0, "Email")

        # kad se klikne da se automatski označi (widget)
        def selection_entry(event):
            event.widget.selection_range(0, END)
        self.entry_email.bind("<FocusIn>", selection_entry)
        self.entry_phone.bind("<FocusIn>", selection_entry)
        self.entry_oib.bind("<FocusIn>", selection_entry)
        self.entry_name.bind("<FocusIn>", selection_entry)
        self.entry_surname.bind("<FocusIn>", selection_entry)
        self.entry_search.bind("<FocusIn>", selection_entry)

        # Button edit Telefonski broj
        self.button_edit_telefonski_brojevi=tk.Button(root)
        self.button_edit_telefonski_brojevi["bg"] = "#8CC0DE"
        ft = tkFont.Font(family='Times',size=10)
        self.button_edit_telefonski_brojevi["font"] = ft
        self.button_edit_telefonski_brojevi["fg"] = "#000000"
        self.button_edit_telefonski_brojevi["justify"] = "center"
        self.button_edit_telefonski_brojevi["text"] = "Edit"
        self.button_edit_telefonski_brojevi.place(x=825, y=50, width=55, height=30)
        self.button_edit_telefonski_brojevi["command"] = self.edit_phone_number

        # Button delete Telefonski broj
        self.button_delete_telefonski_broj = tk.Button(root)
        self.button_delete_telefonski_broj["bg"] = "#BB2525"
        ft = tkFont.Font(family='Times', size=10)
        self.button_delete_telefonski_broj["font"] = ft
        self.button_delete_telefonski_broj["fg"] = "#000000"
        self.button_delete_telefonski_broj["justify"] = "center"
        self.button_delete_telefonski_broj["text"] = "Delete"
        self.button_delete_telefonski_broj.place(x=825, y=140, width=55, height=30)
        self.button_delete_telefonski_broj["command"] = self.delete_phone_number_listbox

        # Button add Telefonski broj
        self.button_add_telefonski_broj = tk.Button(root, bg="#8CC0DE", font="Times, 8", text="Add\n number")
        self.button_add_telefonski_broj.place(x=825, y=90, width=55, height=30)
        self.button_add_telefonski_broj["command"] = self.add_phone_number_button

        # Button edit Mail
        self.button_edit_mailovi=tk.Button(root)
        self.button_edit_mailovi["bg"] = "#8CC0DE"
        ft = tkFont.Font(family='Times',size=10)
        self.button_edit_mailovi["font"] = ft
        self.button_edit_mailovi["fg"] = "#000000"
        self.button_edit_mailovi["justify"] = "center"
        self.button_edit_mailovi["text"] = "Edit"
        self.button_edit_mailovi.place(x=825, y=300, width=55, height=30)
        self.button_edit_mailovi["command"] = self.edit_mail

        # Button delete Mail
        self.button_delete_mailovi = tk.Button(root)
        self.button_delete_mailovi["bg"] = "#BB2525"
        ft = tkFont.Font(family='Times', size=10)
        self.button_delete_mailovi["font"] = ft
        self.button_delete_mailovi["fg"] = "#000000"
        self.button_delete_mailovi["justify"] = "center"
        self.button_delete_mailovi["text"] = "Delete"
        self.button_delete_mailovi.place(x=825, y=390, width=55, height=30)
        self.button_delete_mailovi["command"] = self.delete_email_listbox

        # Button add Mail
        self.button_add_telefonski_broj = tk.Button(root, bg="#8CC0DE", font="Times, 8", text="Add\nmail")
        self.button_add_telefonski_broj.place(x=825, y=340, width=55, height=30)
        self.button_add_telefonski_broj["command"] = self.add_mail_button

        self.button_delete=tk.Button(root)
        self.button_delete["bg"] = "#BB2525"
        ft = tkFont.Font(family='Times',size=10)
        self.button_delete["font"] = ft
        self.button_delete["fg"] = "#000000"
        self.button_delete["justify"] = "center"
        self.button_delete["text"] = "Delete"
        self.button_delete.place(x=150,y=190,width=55,height=30)
        self.button_delete["command"] = self.delete_button

        # hover over - cloud
        CreateToolTip(self.entry_phone, text="Ukoliko želite unijeti više brojeva stavite delimetar ';' bez razmaka")
        CreateToolTip(self.entry_email, text="Ukoliko želite unijeti više mailova stavite delimetar ';' bez razmaka")

        # Double click na broj i mail i otvara se prozor za editiranje
        self.listbox_telefon.bind("<Double-Button-1>", self.edit_phone_number)
        self.listbox_malovi.bind("<Double-Button-1>", self.edit_mail)

        # self.selected_item = self.treeview.focus()
        global selected_item

        def update_entry_fields(event):

            """upisuje vrijednosti označenog kontakta u entry i u listbox"""
            data = self.get_selection()

            if data:
                oib = data[0]
                name = data[1]
                surname = data[2]
                phone = get_phone(oib)
                mail = get_email(oib)

                self.entry_oib.delete(0, END)
                self.entry_oib.insert(0, oib)
                self.entry_name.delete(0, END)
                self.entry_name.insert(0, name)
                self.entry_surname.delete(0, END)
                self.entry_surname.insert(0, surname)
                self.listbox_telefon.delete(0, END)
                self.listbox_malovi.delete(0, END)

                for p in phone:
                    phone_join = ";".join(map(str, phone))
                    self.entry_phone.delete(0, END)
                    # self.entry_phone.insert(0, phone_join)
                    self.listbox_telefon.insert(END, p)

                for m in mail:
                    mail_join = ";".join(map(str, mail))
                    self.entry_email.delete(0, END)
                    # self.entry_email.insert(0, mail_join)
                    self.listbox_malovi.insert(END, m)

                self.update_phone_listbox(oib)
                self.update_mail_listbox(oib)

        self.search_action_button()
        self.update_entry_fields = update_entry_fields
        self.treeview.bind("<<TreeviewSelect>>", update_entry_fields)
        self.listbox_telefon.bind("<<TreeviewSelect>>", update_entry_fields)

    def get_selection(self):
        selected_item = self.treeview.focus()
        detail = self.treeview.item(selected_item)
        values = detail["values"]

        return values

    def update_phone_listbox(self, oib):
        self.listbox_telefon.delete(0, END)
        phones = get_phone(oib)
        for p in phones:
            self.listbox_telefon.insert(END, p)

    def update_mail_listbox(self, oib):
        self.listbox_malovi.delete(0, END)
        mails = get_email(oib)
        for m in mails:
            self.listbox_malovi.insert(END, m)

    def delete_every_entry_with_treeview(self):

        """nakon brisanja korisnika u potpunosti briše sve podatke iz entry, listboxa i treeview"""

        self.entry_name.delete(0, END)
        self.entry_surname.delete(0, END)
        self.entry_oib.delete(0, END)
        self.entry_phone.delete(0, END)
        self.entry_email.delete(0, END)
        self.listbox_telefon.delete(0, END)
        self.listbox_malovi.delete(0, END)
        for item in self.treeview.get_children():
            self.treeview.delete(item)

    def button_plus(self):

        """Preuzimanje unesenih vrijednosti iz Entry polja"""

        oib = int(self.entry_oib.get())
        name = self.entry_name.get().lower()
        surname = self.entry_surname.get().lower()
        phone = self.entry_phone.get()
        mail = self.entry_email.get()

        result = add_korisnik(oib, name, surname)
        if result:
            messagebox.showinfo("Succesfull insert", f"Name: {name}\n"
                                                     f"Surname: {surname}\n"
                                                     f"OIB: {oib}\n"
                                                     f"Phone: {phone}\n"
                                                     f"Email: {mail}")

        # Ako je unesen novi broj, dodajte ga u postojeću listu brojeva
        if phone.strip():  # Provjerite da li je unesen broj telefona
            delete_phone_by_user(oib)
            self.listbox_telefon.delete(0, END)
            existing_phones = get_phone(oib)
            new_phones = phone.split(";")
            for p in new_phones:
                if p not in existing_phones:
                    existing_phones.append(p)
                    add_phone(oib, p)

            for p in existing_phones:
                self.listbox_telefon.insert(END, p)

        # Dodajte e-mail adrese u bazu
        if mail.strip():
            delete_email(oib)
            self.listbox_malovi.delete(0, END)
            mails = mail.split(";")
            for m in mails:
                add_mail(oib, m)
                self.listbox_malovi.insert(END, m)

        # Osvježite polja za unos
        self.update_entry_fields(None)
        self.search_action_button()

    def edit_phone_number(self, event=None):
        data = self.get_selection()
        if data:
            oib = data[0]
            phone = get_phone(oib)

            def open_new_window_phone():
                if self.listbox_telefon.curselection():
                    x = root.winfo_x()
                    y = root.winfo_y()
                    new_window = Toplevel(root)
                    new_window.title("Edit phone number")
                    new_window.geometry("200x150")
                    new_window.geometry("+%d+%d" % (x + 300, y + 100))

                    label_phone = Label(new_window, text="Phone number:")
                    label_phone.place(x=50, y=30)

                    entry_phone_number = Entry(new_window)
                    entry_phone_number.place(x=50, y=50)
                    listbox_selection = self.listbox_telefon.selection_get()
                    entry_phone_number.insert(0, listbox_selection)
                else:
                    messagebox.showinfo("info", "You have not selected any user")

                def button_edit_top_window():
                    new_phone_number = entry_phone_number.get()
                    edit_phone_backend(oib, new_phone_number, listbox_selection)
                    button_accept_changes.bind("<Button-1>", self.update_entry_fields)
                    self.search_action_button()
                    self.update_phone_listbox(oib)
                    self.entry_phone.delete(0, END)
                    new_window.destroy()

                if self.listbox_telefon.curselection():
                    button_accept_changes = Button(new_window, width=10, text="Save changes", command=button_edit_top_window)
                    button_accept_changes.place(x=50, y=70)

            open_new_window_phone()

        else:
            messagebox.showinfo("info", "You have not selected any user")

    def edit_mail(self, event=None):
        data = self.get_selection()
        if data:
            oib = data[0]
            mail = get_email(oib)

            def open_new_window_mail():
                if self.listbox_malovi.curselection():
                    x = root.winfo_x()
                    y = root.winfo_y()
                    new_window = Toplevel(root)
                    new_window.title("Edit mail")
                    new_window.geometry("200x150")
                    new_window.geometry("+%d+%d" % (x + 300, y + 100))

                    label_mail = Label(new_window, text="Mail:")
                    label_mail.place(x=50, y=30)

                    entry_edit_mail = Entry(new_window)
                    entry_edit_mail.place(x=50, y=50)
                    listbox_selection = self.listbox_malovi.selection_get()
                    entry_edit_mail.insert(0, listbox_selection)
                else:
                    messagebox.showinfo("info", "You have not selected any user")

                def button_edit_top_window():
                    new_mail = entry_edit_mail.get()
                    edit_mail_backend(oib, new_mail, listbox_selection)
                    button_edit_mail.bind("<Button-1>", self.update_entry_fields)
                    self.search_action_button()
                    self.update_mail_listbox(oib)
                    new_window.destroy()

                if self.listbox_malovi.curselection():
                    button_edit_mail = Button(new_window, width=10, text="Save changes", command=button_edit_top_window)
                    button_edit_mail.place(x=50, y=70)

            open_new_window_mail()
        else:
            messagebox.showinfo("info", "You have not selected any user")

    def add_phone_number_button(self, event=None):
        data = self.get_selection()
        if data:
            oib = data[0]

            x = root.winfo_x()
            y = root.winfo_y()
            new_window = Toplevel(root)
            new_window.title("Add phone number")
            new_window.geometry("200x150")
            new_window.geometry("+%d+%d" % (x + 300, y + 100))

            label_phone = Label(new_window, text="Add new phone number:")
            label_phone.place(x=50, y=30)

            entry_phone_number = Entry(new_window)
            entry_phone_number.place(x=50, y=50)

            def button_add_phone_number():
                new_phone_number = entry_phone_number.get()
                add_phone(oib, new_phone_number)
                button_add_number.bind("<Button-1>", self.update_entry_fields)
                self.search_action_button()
                self.update_phone_listbox(oib)
                new_window.destroy()

            button_add_number = Button(new_window, width=10, text="Add number", command=button_add_phone_number)
            button_add_number.place(x=75, y=80)

        else:
            messagebox.showinfo("Info", "You have`t selected any user")

    def add_mail_button(self, event=None):
        data = self.get_selection()
        if data:
            oib = data[0]

            x = root.winfo_x()
            y = root.winfo_y()
            new_window = Toplevel(root)
            new_window.title("Add mail")
            new_window.geometry("200x150")
            new_window.geometry("+%d+%d" % (x + 300, y + 100))

            label_mail = Label(new_window, text="Add new mail:")
            label_mail.place(x=50, y=30)

            entry_mail = Entry(new_window)
            entry_mail.place(x=50, y=50)

            def button_add_mail_fun():
                new_mail = entry_mail.get()
                add_mail(oib, new_mail)
                button_add_mail.bind("<Button-1>", self.update_entry_fields)
                self.search_action_button()
                self.update_mail_listbox(oib)
                new_window.destroy()

            button_add_mail = Button(new_window, width=10, text="Add mail", command=button_add_mail_fun)
            button_add_mail.place(x=75, y=80)

        else:
            messagebox.showinfo("Info", "You have`t selected any user")


    def delete_button(self):

        """za označeni kontakt iz treeview-a briše korisnika i sve podatke. Refresh-a"""

        def confirm_delete():
            result = messagebox.askquestion("Confirm delete", "Are you sure you want\ndelete this contact")
            if result.lower() == "yes":
                delete_contact()
                self.search_action_button()

        def delete_contact():
            data = self.get_selection()
            if data:
                oib = data[0]
                name = data[1]
                surname = data[2]

                delete_korisnik(oib)
                messagebox.showinfo("Succesfully deleted", f"Name: {name}\n"
                                                           f"Surname: {surname}\n"
                                                           f"OIB: {oib}")
                self.search_action_button()
                self.delete_every_entry_with_treeview()

            else:
                messagebox.showinfo("info", "You have not selected any user")
        confirm_delete()

    def delete_phone_number_listbox(self):
        data = self.get_selection()
        if data:
            oib = data[0]

            if self.listbox_telefon.selection_get():
                selected_item = self.listbox_telefon.selection_get()
                delete_phone_from_listbox(selected_item)
                messagebox.showinfo("info", "Successfully deleted")
                self.search_action_button()
                self.update_phone_listbox(oib)
                self.treeview.selection_set(self.selected_item)
            else:
                messagebox.showinfo("info", "You have not selected any number")
        else:
            messagebox.showinfo("info", "You have not selected any user")

    def delete_email_listbox(self):
        data = self.get_selection()
        if data:
            oib = data[0]

        selected_item = self.listbox_malovi.selection_get()
        delete_mail_from_listbox(selected_item)
        messagebox.showinfo("info", "Successfully deleted")
        self.search_action_button()
        self.update_mail_listbox(oib)

    def search_action_button(self):

        """prikaz u treeview"""
        selected_item = self.treeview.focus()

        for item in self.treeview.get_children():
            self.treeview.delete(item)

        query = self.entry_search.get().lower()
        data = search_contacts(query)
        available_items = self.treeview.get_children()

        for single in data:
            oib = single[0]
            phone = get_phone(oib)
            phone = ";".join(map(str, phone))
            mail = get_email(oib)
            mail = ";".join(map(str, mail))
            self.treeview.insert("", "end", values=(single[0], single[1], single[2]))

        self.entry_search.delete(0, END)
        self.treeview.update()

        if selected_item and selected_item[0] in available_items:
            self.treeview.selection_set(selected_item)
            self.treeview.focus(selected_item)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
