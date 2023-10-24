import sqlite3
from tkinter import messagebox


def search_by_name(name):
    """name from the base"""
    with sqlite3.connect("phonebook.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Korisnici WHERE ime=?", (name,))
        fetch = c.fetchall()
        if len(fetch) == 0:
            c.execute("SELECT * FROM Korisnici")
            fetch = c.fetchall()

        c.close()
        return fetch


def search_contacts(criteria):
    """Search contacts by all criteria"""
    with sqlite3.connect("phonebook.db") as conn:
        c = conn.cursor()
        c.execute("SELECT DISTINCT Korisnici.* FROM Korisnici "
                  "LEFT JOIN Telefon ON Korisnici.oib = Telefon.korisnik_id "
                  "LEFT JOIN Mail ON Korisnici.oib = Mail.korisnik_id "
                  "WHERE Korisnici.ime LIKE ? OR "
                  "Korisnici.prezime LIKE ? OR "
                  "Korisnici.oib LIKE ? OR "
                  "Telefon.broj LIKE ? OR "
                  "Mail.email LIKE ?",
                  (f"%{criteria}%", f"%{criteria}%", f"%{criteria}%", f"%{criteria}%", f"%{criteria}%"))
        fetch = c.fetchall()

        c.close()
        return fetch


def get_phone(oib):
    """dobavlja broj telefona iz baze"""
    with sqlite3.connect("phonebook.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Telefon WHERE korisnik_id=?", (oib,))
        fetch = c.fetchall()
        data = [f[2] for f in fetch]
        c.close()
        return data


def get_email(oib):
    """mail from the baze"""
    with sqlite3.connect("phonebook.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Mail WHERE korisnik_id=?", (oib,))
        fetch = c.fetchall()
        data = [f[2] for f in fetch]
        c.close()
        return data


def add_korisnik(oib, name, surname):
    """add user to the base"""
    with sqlite3.connect("phonebook.db") as conn:
        c = conn.cursor()
        query = c.execute("SELECT oib FROM Korisnici WHERE oib=?", (oib,)).fetchone()
        if query is None:
            c.execute("INSERT INTO Korisnici (oib, ime, prezime) VALUES (?, ?, ?)", (oib, name, surname))
            conn.commit()
            return True
        else:
            messagebox.showinfo("Contact Info", f"Contact already exists:\nOIB: {query[0]}\nName: {name}\nSurname: {surname}")
            return False


def add_phone(oib, number):
    """add number if not empty"""
    if number.strip():
        with sqlite3.connect("phonebook.db") as conn:
            c = conn.cursor()
            # Check if user exists
            query = c.execute("SELECT oib FROM Korisnici WHERE oib=?", (oib,)).fetchone()
            if query is None:
                messagebox.showinfo('info', 'Contact does not exist')
            else:
                # Check existing phone numbers 
                c.execute("SELECT broj FROM Telefon WHERE korisnik_id=?", (oib,))
                existing_numbers = [row[0] for row in c.fetchall()]
                if number not in existing_numbers:
                    c.execute("INSERT INTO Telefon (korisnik_id, broj) VALUES (?, ?)", (oib, number))
                    conn.commit()
                # If number exists, do nothing


def add_mail(oib, mail):
    """add mail if not empty"""
    # if mail.strip():
    with sqlite3.connect("phonebook.db") as conn:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO Mail (korisnik_id, email) VALUES (?, ?)", (oib, mail))
        if mail == "":
            pass
        if c.rowcount == 0:
            c.execute("INSERT INTO Mail (korisnik_id, email) VALUES (?, ?)", (oib, mail))
        conn.commit()


def delete_korisnik(oib):
    """delete user and all data"""
    with sqlite3.connect("phonebook.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM Korisnici WHERE oib=?", (oib,))
        c.execute("DELETE FROM Telefon WHERE korisnik_id=?", (oib,))
        c.execute("DELETE FROM Mail WHERE korisnik_id=?", (oib,))
        conn.commit()


def delete_phone_by_user(oib):
    """delete phone number"""
    with sqlite3.connect("phonebook.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM Telefon WHERE korisnik_id=?", (oib,))
        conn.commit()


def delete_phone_from_listbox(phone):
    """delete phone number labeled in listbox"""
    with sqlite3.connect("phonebook.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM Telefon WHERE broj=?", (phone,))
        conn.commit()


def delete_mail_from_listbox(email):
    """delete mail labeled in listbox"""
    with sqlite3.connect("phonebook.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM Mail WHERE email=?", (email,))
        conn.commit()


def delete_email(oib):
    """delete email"""
    with sqlite3.connect("phonebook.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM Mail WHERE korisnik_id=?", (oib,))
        conn.commit()


def edit_korisnik(oib, ime, prezime, broj, mail):
    """edit user and all data (oib, ime, prezime, broj, mail)"""
    with sqlite3.connect("phonebook.db") as conn:
        c = conn.cursor()
        c.execute("UPDATE Korisnici SET ime=?, prezime=? WHERE oib=?", (ime, prezime, oib))
        if len(broj) == 0:
            c.execute("INSERT INTO Telefon (oib, broj) VALUES (?, ?)", (oib, broj))
        else:
            c.execute("UPDATE Telefon SET broj=? WHERE oib=?", (broj, oib))

        if len(mail) == 0:
            c.execute("INSERT INTO Mail (oib, email) VALUES (?, ?)", (oib, mail))
        else:
            c.execute("UPDATE Mail SET email=? WHERE oib=?", (mail, oib))
        conn.commit()


def edit_phone_backend(oib, number, old_phone):
    try:
        with sqlite3.connect("phonebook.db") as conn:
            c = conn.cursor()

            # Provjerite postoji li korisnik s navedenim oib-om
            c.execute("SELECT COUNT(*) FROM Telefon WHERE korisnik_id=?", (oib,))
            count = c.fetchone()[0]

            if count > 0:
                # Ako korisnik postoji, ažurirajte broj telefona
                c.execute("UPDATE Telefon SET broj=? WHERE korisnik_id=? AND broj=?", (number, oib, old_phone))
                conn.commit()
                return True
            else:
                return False  # User with thid oib does not exist
    except sqlite3.Error as e:
        print("Error in updating phone number:", str(e))
        return False


def edit_mail_backend(oib, mail, old_mail):
    try:
        with sqlite3.connect("phonebook.db") as conn:
            c = conn.cursor()

            # Provjerite postoji li korisnik s navedenim oib-om
            c.execute("SELECT COUNT(*) FROM Telefon WHERE korisnik_id=?", (oib,))
            count = c.fetchone()[0]

            if count > 0:
                # Ako korisnik postoji, ažurirajte broj telefona
                c.execute("UPDATE Mail SET email=? WHERE korisnik_id=? AND email=?", (mail, oib, old_mail))
                conn.commit()
                return True
            else:
                return False  # Korisnik s navedenim oib-om ne postoji
    except sqlite3.Error as e:
        print("Greška prilikom ažuriranja telefonskog broja:", str(e))
        return False







