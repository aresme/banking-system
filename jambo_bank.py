import customtkinter as ctk
from tkinter import messagebox
import json
import os
from datetime import datetime
import random

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class JamboBank:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🏦 Jambo Bank - Kenya")
        self.root.geometry("900x620")
        self.root.resizable(False, False)

        self.account = None
        self.data_file = "jambobank_account.json"

        self.load_account()
        self.show_welcome_screen()

    def load_account(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    self.account = data
            except:
                self.account = None

    def save_account(self):
        if self.account:
            with open(self.data_file, "w") as f:
                json.dump(self.account, f, indent=4)

    # ====================== SCREENS ======================
    def show_welcome_screen(self):
        self.clear_window()

        frame = ctk.CTkFrame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="🏦 JAMBO BANK", font=ctk.CTkFont(size=42, weight="bold")).pack(pady=30)
        ctk.CTkLabel(frame, text="Kenya's Trusted Digital Bank", font=ctk.CTkFont(size=18)).pack(pady=10)

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=50)

        ctk.CTkButton(btn_frame, text="Open New Account", width=300, height=50, 
                      font=ctk.CTkFont(size=16), command=self.create_account_screen).pack(pady=12)
        
        ctk.CTkButton(btn_frame, text="Login", width=300, height=50, 
                      font=ctk.CTkFont(size=16), command=self.login_screen).pack(pady=12)

        ctk.CTkButton(btn_frame, text="Exit", width=300, height=40, 
                      fg_color="red", hover_color="darkred", command=self.root.quit).pack(pady=20)

    def create_account_screen(self):
        self.clear_window()

        frame = ctk.CTkFrame(self.root)
        frame.pack(fill="both", expand=True, padx=40, pady=40)

        ctk.CTkLabel(frame, text="Create New Account", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=20)

        self.name_entry = ctk.CTkEntry(frame, placeholder_text="Full Name", width=400, height=40)
        self.name_entry.pack(pady=10)

        self.phone_entry = ctk.CTkEntry(frame, placeholder_text="Phone Number", width=400, height=40)
        self.phone_entry.pack(pady=10)

        self.id_entry = ctk.CTkEntry(frame, placeholder_text="National ID Number", width=400, height=40)
        self.id_entry.pack(pady=10)

        ctk.CTkButton(frame, text="Create Account", width=300, height=50,
                      command=self.create_account).pack(pady=30)

        ctk.CTkButton(frame, text="Back", width=200, command=self.show_welcome_screen).pack()

    def create_account(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        id_num = self.id_entry.get().strip()

        if not name or not phone or not id_num:
            messagebox.showerror("Error", "All fields are required!")
            return

        acc_number = "JB" + ''.join(random.choices('0123456789', k=8))
        
        self.account = {
            "name": name,
            "phone": phone,
            "idNumber": id_num,
            "accountNumber": acc_number,
            "pin": "1234",  # Temporary PIN
            "balance": 0.0,
            "transactions": []
        }

        self.save_account()
        messagebox.showinfo("Success", f"Account Created!\n\nAccount Number: {acc_number}\nTemporary PIN: 1234")
        self.login_screen()

    def login_screen(self):
        self.clear_window()

        frame = ctk.CTkFrame(self.root)
        frame.pack(fill="both", expand=True, padx=40, pady=40)

        ctk.CTkLabel(frame, text="Login to Jambo Bank", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=30)

        self.acc_entry = ctk.CTkEntry(frame, placeholder_text="Account Number", width=400, height=40)
        self.acc_entry.pack(pady=10)

        self.pin_entry = ctk.CTkEntry(frame, placeholder_text="PIN", width=400, height=40, show="*")
        self.pin_entry.pack(pady=10)

        ctk.CTkButton(frame, text="Login", width=300, height=50,
                      command=self.login).pack(pady=30)

        ctk.CTkButton(frame, text="Back", width=200, command=self.show_welcome_screen).pack()

    def login(self):
        if not self.account:
            messagebox.showerror("Error", "No account found. Create one first.")
            return

        acc_input = self.acc_entry.get().strip()
        pin_input = self.pin_entry.get().strip()

        if acc_input == self.account["accountNumber"] and pin_input == self.account["pin"]:
            messagebox.showinfo("Success", "Login Successful!")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid Account Number or PIN")

    def show_dashboard(self):
        self.clear_window()
        
        frame = ctk.CTkFrame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        ctk.CTkLabel(frame, text=f"Welcome, {self.account['name'].split()[0]}!", 
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)
        
        balance_text = f"KES {self.account['balance']:,.2f}"
        ctk.CTkLabel(frame, text=balance_text, font=ctk.CTkFont(size=32, weight="bold"),
                     text_color="lightgreen").pack(pady=5)

        # Buttons Grid
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=30, fill="both", expand=True)

        buttons = [
            ("Deposit", "💰", self.deposit_window),
            ("Withdraw", "🏧", self.withdraw_window),
            ("Balance", "📊", self.show_balance),
            ("Statement", "📜", self.show_statement),
            ("Change PIN", "🔑", self.change_pin_window),
            ("Logout", "🚪", self.logout)
        ]

        for i, (text, emoji, cmd) in enumerate(buttons):
            btn = ctk.CTkButton(btn_frame, text=f"{emoji}  {text}", width=200, height=60,
                                font=ctk.CTkFont(size=16), command=cmd)
            btn.grid(row=i//2, column=i%2, padx=15, pady=15)

    def deposit_window(self):
        self.amount_window("Deposit", "green", self.make_deposit)

    def withdraw_window(self):
        self.amount_window("Withdraw", "red", self.make_withdraw)

    def amount_window(self, action, color, command):
        win = ctk.CTkToplevel(self.root)
        win.title(action)
        win.geometry("400x300")
        win.grab_set()

        ctk.CTkLabel(win, text=f"{action} Money", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        amount_entry = ctk.CTkEntry(win, placeholder_text="Amount in KES", width=300, height=40)
        amount_entry.pack(pady=10)

        def submit():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    raise ValueError
                command(amount)
                win.destroy()
            except:
                messagebox.showerror("Error", "Please enter a valid amount")

        ctk.CTkButton(win, text=action, fg_color=color, command=submit, height=45).pack(pady=20)

    def make_deposit(self, amount):
        self.account["balance"] += amount
        self.add_transaction("Deposit", amount)
        self.save_account()
        messagebox.showinfo("Success", f"KES {amount:,.2f} deposited successfully!")
        self.show_dashboard()

    def make_withdraw(self, amount):
        if amount > self.account["balance"]:
            messagebox.showerror("Error", "Insufficient funds!")
            return
        self.account["balance"] -= amount
        self.add_transaction("Withdrawal", amount)
        self.save_account()
        messagebox.showinfo("Success", f"KES {amount:,.2f} withdrawn successfully!")
        self.show_dashboard()

    def add_transaction(self, type_, amount):
        trans = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "type": type_,
            "amount": amount,
            "balance": self.account["balance"]
        }
        self.account["transactions"].insert(0, trans)  # newest first
        if len(self.account["transactions"]) > 10:
            self.account["transactions"].pop()

    def show_balance(self):
        messagebox.showinfo("Balance", f"Current Balance:\n\nKES {self.account['balance']:,.2f}")

    def show_statement(self):
        win = ctk.CTkToplevel(self.root)
        win.title("Mini Statement")
        win.geometry("600x500")

        text = ctk.CTkTextbox(win, width=580, height=450)
        text.pack(padx=10, pady=10)

        text.insert("end", f"Name: {self.account['name']}\n")
        text.insert("end", f"Account: {self.account['accountNumber']}\n")
        text.insert("end", f"Balance: KES {self.account['balance']:,.2f}\n\n")
        text.insert("end", "─" * 50 + "\n")
        text.insert("end", "DATE\t\tTYPE\t\tAMOUNT\t\tBALANCE\n")
        text.insert("end", "─" * 50 + "\n")

        for t in self.account["transactions"]:
            color = "green" if t["type"] == "Deposit" else "red"
            text.insert("end", f"{t['date']}\t{t['type']}\t\tKES {t['amount']:,.2f}\t\tKES {t['balance']:,.2f}\n")

    def change_pin_window(self):
        win = ctk.CTkToplevel(self.root)
        win.title("Change PIN")
        win.geometry("400x400")
        win.grab_set()

        ctk.CTkLabel(win, text="Change PIN", font=ctk.CTkFont(size=20)).pack(pady=15)

        old_pin = ctk.CTkEntry(win, placeholder_text="Current PIN", show="*")
        old_pin.pack(pady=8)
        
        new_pin = ctk.CTkEntry(win, placeholder_text="New 4-digit PIN", show="*")
        new_pin.pack(pady=8)
        
        confirm_pin = ctk.CTkEntry(win, placeholder_text="Confirm New PIN", show="*")
        confirm_pin.pack(pady=8)

        def change():
            if old_pin.get() != self.account["pin"]:
                messagebox.showerror("Error", "Incorrect current PIN")
                return
            if len(new_pin.get()) != 4 or not new_pin.get().isdigit():
                messagebox.showerror("Error", "PIN must be 4 digits")
                return
            if new_pin.get() != confirm_pin.get():
                messagebox.showerror("Error", "PINs do not match")
                return

            self.account["pin"] = new_pin.get()
            self.save_account()
            messagebox.showinfo("Success", "PIN changed successfully!")
            win.destroy()

        ctk.CTkButton(win, text="Change PIN", command=change).pack(pady=20)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.show_welcome_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()


# ====================== START APP ======================
if __name__ == "__main__":
    app = JamboBank()
    app.run()