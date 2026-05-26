import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
import os
from datetime import datetime
import random
import logging
import hashlib
from typing import Optional, Dict, List

# ====================== CONFIGURATION ======================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

logging.basicConfig(
    filename="jambobank.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

class Transaction:
    def __init__(self, trans_type: str, amount: float, balance_after: float):
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.type = trans_type
        self.amount = amount
        self.balance_after = balance_after

    def to_dict(self) -> Dict:
        return {
            "date": self.date,
            "type": self.type,
            "amount": self.amount,
            "balance_after": self.balance_after
        }

    @staticmethod
    def from_dict(data: Dict):
        t = Transaction(data["type"], data["amount"], data["balance_after"])
        t.date = data["date"]
        return t


class Account:
    def __init__(self):
        self.name: str = ""
        self.phone: str = ""
        self.id_number: str = ""
        self.account_number: str = ""
        self.pin: str = ""
        self.balance: float = 0.0
        self.transactions: List[Dict] = []
        self.created_at: str = datetime.now().strftime("%Y-%m-%d")

    def generate_account_number(self) -> str:
        return "JB" + ''.join(random.choices("0123456789", k=10))

    def hash_pin(self, pin: str) -> str:
        return hashlib.sha256(pin.encode()).hexdigest()

    def set_pin(self, pin: str):
        self.pin = self.hash_pin(pin)

    def verify_pin(self, entered_pin: str) -> bool:
        return self.pin == self.hash_pin(entered_pin)

    def add_transaction(self, trans_type: str, amount: float):
        new_balance = self.balance
        if trans_type == "Withdrawal":
            new_balance -= amount
        else:
            new_balance += amount

        trans = Transaction(trans_type, amount, new_balance)
        self.transactions.insert(0, trans.to_dict())
        if len(self.transactions) > 20:
            self.transactions.pop()

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "phone": self.phone,
            "id_number": self.id_number,
            "account_number": self.account_number,
            "pin": self.pin,
            "balance": self.balance,
            "transactions": self.transactions,
            "created_at": self.created_at
        }

    @staticmethod
    def from_dict(data: Dict):
        acc = Account()
        acc.name = data.get("name", "")
        acc.phone = data.get("phone", "")
        acc.id_number = data.get("id_number", "")
        acc.account_number = data.get("account_number", "")
        acc.pin = data.get("pin", "")
        acc.balance = data.get("balance", 0.0)
        acc.transactions = data.get("transactions", [])
        acc.created_at = data.get("created_at", "")
        return acc


class JamboBankPro:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🏦 Jambo Bank - Professional Banking")
        self.root.geometry("1020x680")
        self.root.resizable(False, False)

        self.account: Optional[Account] = None
        self.data_file = "jambobank_pro_account.json"
        self.logged_in = False

        self.load_account()
        self.show_welcome_screen()

    # ====================== UTILITY METHODS ======================
    def load_account(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.account = Account.from_dict(data)
                logging.info("Account loaded successfully")
            except Exception as e:
                logging.error(f"Failed to load account: {e}")
                self.account = None

    def save_account(self):
        if self.account:
            try:
                with open(self.data_file, "w", encoding="utf-8") as f:
                    json.dump(self.account.to_dict(), f, indent=4)
                logging.info("Account saved successfully")
            except Exception as e:
                logging.error(f"Failed to save account: {e}")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_message(self, title: str, message: str, error: bool = False):
        if error:
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)

    # ====================== SCREENS ======================
    def show_welcome_screen(self):
        self.clear_window()

        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(main_frame, text="🏦 JAMBO BANK", 
                    font=ctk.CTkFont(size=48, weight="bold")).pack(pady=40)

        ctk.CTkLabel(main_frame, text="Kenya's Most Trusted Digital Banking Platform", 
                    font=ctk.CTkFont(size=18)).pack(pady=8)

        ctk.CTkLabel(main_frame, text="Licensed by Central Bank of Kenya", 
                    font=ctk.CTkFont(size=14), text_color="gray").pack()

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=60)

        ctk.CTkButton(btn_frame, text="Create New Account", width=340, height=55,
                      font=ctk.CTkFont(size=18), command=self.show_create_account).pack(pady=12)

        ctk.CTkButton(btn_frame, text="Login to Existing Account", width=340, height=55,
                      font=ctk.CTkFont(size=18), command=self.show_login).pack(pady=12)

        footer = ctk.CTkFrame(main_frame, fg_color="transparent")
        footer.pack(side="bottom", pady=20)
        ctk.CTkButton(footer, text="Exit Application", width=200, fg_color="#8B0000",
                      command=self.root.quit).pack()

    def show_create_account(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root)
        frame.pack(fill="both", expand=True, padx=50, pady=40)

        ctk.CTkLabel(frame, text="Open New Account", font=ctk.CTkFont(size=32, weight="bold")).pack(pady=20)

        self.name_entry = ctk.CTkEntry(frame, placeholder_text="Full Name (as per ID)", width=420, height=45)
        self.name_entry.pack(pady=12)

        self.phone_entry = ctk.CTkEntry(frame, placeholder_text="Phone Number (+254...)", width=420, height=45)
        self.phone_entry.pack(pady=12)

        self.id_entry = ctk.CTkEntry(frame, placeholder_text="National ID / Passport Number", width=420, height=45)
        self.id_entry.pack(pady=12)

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=40)

        ctk.CTkButton(btn_frame, text="Create Account", width=280, height=50,
                      command=self.create_new_account).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Back", width=180, height=50,
                      command=self.show_welcome_screen).pack(side="left", padx=10)

    def create_new_account(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        id_num = self.id_entry.get().strip()

        if not name or len(name) < 3:
            self.show_message("Validation Error", "Please enter a valid full name", True)
            return
        if not phone or len(phone) < 10:
            self.show_message("Validation Error", "Please enter a valid phone number", True)
            return
        if not id_num or len(id_num) < 6:
            self.show_message("Validation Error", "Please enter a valid ID number", True)
            return

        self.account = Account()
        self.account.name = name
        self.account.phone = phone
        self.account.id_number = id_num
        self.account.account_number = self.account.generate_account_number()
        self.account.set_pin("1234")  # Default temporary PIN

        self.save_account()
        logging.info(f"New account created: {self.account.account_number}")

        info = f"🎉 Account Created Successfully!\n\n" \
               f"Account Number: {self.account.account_number}\n" \
               f"Temporary PIN : 1234\n\n" \
               f"Please change your PIN after first login."

        self.show_message("Account Created", info)
        self.show_login()

    def show_login(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root)
        frame.pack(fill="both", expand=True, padx=50, pady=40)

        ctk.CTkLabel(frame, text="Secure Login", font=ctk.CTkFont(size=32, weight="bold")).pack(pady=30)

        self.acc_entry = ctk.CTkEntry(frame, placeholder_text="Account Number", width=420, height=45)
        self.acc_entry.pack(pady=12)

        self.pin_entry = ctk.CTkEntry(frame, placeholder_text="4-Digit PIN", width=420, height=45, show="*")
        self.pin_entry.pack(pady=12)

        ctk.CTkButton(frame, text="Login", width=300, height=55,
                      font=ctk.CTkFont(size=18), command=self.perform_login).pack(pady=30)

        ctk.CTkButton(frame, text="Back to Welcome", command=self.show_welcome_screen).pack()

    def perform_login(self):
        if not self.account:
            self.show_message("Error", "No account exists. Please create one first.", True)
            return

        acc_input = self.acc_entry.get().strip()
        pin_input = self.pin_entry.get().strip()

        if acc_input == self.account.account_number and self.account.verify_pin(pin_input):
            self.logged_in = True
            logging.info(f"Successful login: {acc_input}")
            self.show_dashboard()
        else:
            logging.warning("Failed login attempt")
            self.show_message("Login Failed", "Invalid Account Number or PIN", True)

    def show_dashboard(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Top Bar
        top_bar = ctk.CTkFrame(frame, height=80)
        top_bar.pack(fill="x", pady=(0, 20))
        top_bar.pack_propagate(False)

        ctk.CTkLabel(top_bar, text=f"Welcome back, {self.account.name.split()[0]}", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(side="left", padx=30, pady=20)

        balance_str = f"KES {self.account.balance:,.2f}"
        ctk.CTkLabel(top_bar, text=balance_str, font=ctk.CTkFont(size=28, weight="bold"),
                     text_color="#00FFAA").pack(side="right", padx=30)

        # Main Content
        content = ctk.CTkFrame(frame)
        content.pack(fill="both", expand=True, padx=20, pady=10)

        buttons = [
            ("💰 Deposit", self.open_deposit),
            ("🏧 Withdraw", self.open_withdraw),
            ("📊 Balance", self.view_balance),
            ("📜 Mini Statement", self.view_statement),
            ("🔑 Change PIN", self.open_change_pin),
            ("💸 Transfer", self.open_transfer),
            ("🏦 Loan Request", self.open_loan_request),
            ("📤 Export Statement", self.export_statement),
            ("⚙️ Settings", self.open_settings),
            ("🚪 Logout", self.logout)
        ]

        for i, (text, cmd) in enumerate(buttons):
            btn = ctk.CTkButton(content, text=text, width=220, height=65,
                                font=ctk.CTkFont(size=16), command=cmd)
            btn.grid(row=i//2, column=i%2, padx=15, pady=12)

    # ====================== BANKING OPERATIONS ======================
    def open_deposit(self):
        self.open_amount_window("Deposit Funds", "#00AA00", self.process_deposit)

    def open_withdraw(self):
        self.open_amount_window("Withdraw Funds", "#AA0000", self.process_withdraw)

    def open_amount_window(self, title: str, color: str, callback):
        win = ctk.CTkToplevel(self.root)
        win.title(title)
        win.geometry("420x320")
        win.grab_set()

        ctk.CTkLabel(win, text=title, font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

        amount_entry = ctk.CTkEntry(win, placeholder_text="Enter Amount (KES)", width=340, height=50)
        amount_entry.pack(pady=15)

        def submit():
            try:
                amount = float(amount_entry.get().strip())
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                if amount > 1000000 and title.startswith("Withdraw"):
                    raise ValueError("Maximum transaction limit exceeded")
                callback(amount)
                win.destroy()
            except ValueError as e:
                self.show_message("Input Error", str(e), True)

        ctk.CTkButton(win, text=title.split()[0], fg_color=color, height=50,
                      command=submit).pack(pady=20)

    def process_deposit(self, amount: float):
        self.account.balance += amount
        self.account.add_transaction("Deposit", amount)
        self.save_account()
        self.show_message("Success", f"KES {amount:,.2f} deposited successfully!")
        self.show_dashboard()

    def process_withdraw(self, amount: float):
        if amount > self.account.balance:
            self.show_message("Error", "Insufficient balance for this withdrawal.", True)
            return
        self.account.balance -= amount
        self.account.add_transaction("Withdrawal", amount)
        self.save_account()
        self.show_message("Success", f"KES {amount:,.2f} withdrawn successfully!")
        self.show_dashboard()

    def view_balance(self):
        self.show_message("Current Balance", f"KES {self.account.balance:,.2f}")

    def view_statement(self):
        win = ctk.CTkToplevel(self.root)
        win.title("Mini Statement")
        win.geometry("720x580")

        textbox = ctk.CTkTextbox(win, width=700, height=520, font=ctk.CTkFont(family="Consolas", size=13))
        textbox.pack(padx=15, pady=15)

        header = f"JAMBO BANK MINI STATEMENT\n"
        header += f"Account: {self.account.account_number}\n"
        header += f"Name: {self.account.name}\n"
        header += f"Date: {datetime.now().strftime('%Y-%m-%d')}\n"
        header += "="*70 + "\n"
        textbox.insert("end", header)

        if not self.account.transactions:
            textbox.insert("end", "No transactions available.\n")
        else:
            for t in self.account.transactions:
                color_tag = "green" if t["type"] == "Deposit" else "red"
                line = f"{t['date']:<20} {t['type']:<12} KES {t['amount']:>12,.2f}   Bal: {t['balance_after']:>12,.2f}\n"
                textbox.insert("end", line)

        textbox.configure(state="disabled")

    def open_change_pin(self):
        win = ctk.CTkToplevel(self.root)
        win.title("Change PIN")
        win.geometry("460x420")
        win.grab_set()

        ctk.CTkLabel(win, text="Change Transaction PIN", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        old_pin = ctk.CTkEntry(win, placeholder_text="Current PIN", show="*", width=300, height=40)
        old_pin.pack(pady=8)
        new_pin = ctk.CTkEntry(win, placeholder_text="New 4-Digit PIN", show="*", width=300, height=40)
        new_pin.pack(pady=8)
        confirm_pin = ctk.CTkEntry(win, placeholder_text="Confirm New PIN", show="*", width=300, height=40)
        confirm_pin.pack(pady=8)

        def change_pin():
            if not self.account.verify_pin(old_pin.get()):
                self.show_message("Error", "Current PIN is incorrect", True)
                return
            np = new_pin.get().strip()
            if len(np) != 4 or not np.isdigit():
                self.show_message("Error", "PIN must be exactly 4 digits", True)
                return
            if np != confirm_pin.get():
                self.show_message("Error", "New PINs do not match", True)
                return

            self.account.set_pin(np)
            self.save_account()
            self.show_message("Success", "PIN changed successfully!")
            win.destroy()

        ctk.CTkButton(win, text="Update PIN", command=change_pin, height=45).pack(pady=25)

    def open_transfer(self):
        self.show_message("Coming Soon", "Inter-account & M-PESA transfers will be available in next update.")

    def open_loan_request(self):
        self.show_message("Loan Services", "Micro-loans up to KES 50,000 available.\nContact support for eligibility.")

    def export_statement(self):
        if not self.account.transactions:
            self.show_message("No Data", "No transactions to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt")],
            initialfile=f"Statement_{self.account.account_number}.txt"
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("JAMBO BANK OFFICIAL STATEMENT\n")
                    f.write(f"Account: {self.account.account_number}\n")
                    f.write(f"Customer: {self.account.name}\n\n")
                    for t in self.account.transactions:
                        f.write(f"{t['date']} | {t['type']:12} | KES {t['amount']:>10,.2f} | Bal: {t['balance_after']:>10,.2f}\n")
                self.show_message("Exported", f"Statement saved to:\n{file_path}")
            except Exception:
                self.show_message("Error", "Failed to export statement", True)

    def open_settings(self):
        self.show_message("Settings", "Account settings & preferences coming in future updates.")

    def logout(self):
        if messagebox.askyesno("Logout", "Do you want to logout?"):
            self.logged_in = False
            logging.info("User logged out")
            self.show_welcome_screen()

    def run(self):
        self.root.mainloop()


# ====================== ENTRY POINT ======================
if __name__ == "__main__":
    print("🚀 Starting Jambo Bank Professional...")
    app = JamboBankPro()
    app.run()