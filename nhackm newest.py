import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import aiml
import random
import hashlib  
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns  

class CreditBuilderApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Credit Builder App")
        self.root.geometry("800x600")

        # Dictionary to hold user accounts
        self.users = {"admin": "adminpass"}  # Predefined admin account

        # Dictionary to hold multiple clubs
        self.clubs = {}
        self.current_club = None

        # Set Seaborn palettes
        sns.set_palette("icefire")  # Use "icefire" palette for main UI
        
        self.create_widgets()

    def create_widgets(self):
        # Set custom style for better visuals
        style = ttk.Style()
        style.theme_use("clam")  # Use the "clam" theme
        style.configure('TLabel', background='#f0f0f0')  # Set background color for labels
        
        # Set gradient background colors
        self.root.configure(bg='#f0f0f0')  # Set background color for the root window

        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.pack(expand=1, fill="both")

        # Create tabs for Account Management, Create Club, Manage Club, Chat, and Data Visualization
        self.tab_account = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_account, text="Account")

        self.tab_create = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_create, text="Create Club")

        self.tab_manage = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_manage, text="Manage Club")

        self.tab_chat = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_chat, text="Chat")

        self.tab_visualize = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_visualize,text="Data Visualization")

        # Create widgets for each tab
        self.create_account_tab()
        self.create_create_tab()
        self.create_manage_tab()
        self.create_chat_tab()
        self.create_visualize_tab()

        # Load AIML kernel and bootstrap
        self.kernel = aiml.Kernel()
        self.create_aiml_brain()

    def create_aiml_brain(self):
        # Predefined AIML patterns and responses
        aiml_brain = """
            + CLUB_MEMBERSHIP
                - As a member of our credit score club, you can contribute to building a strong credit history by making regular payments and managing your finances responsibly.
            + CREDIT_SCORE
                - Your credit score is a numerical representation of your creditworthiness. It's calculated based on various factors such as payment history, credit utilization, length of credit history, types of credit accounts, and recent credit inquiries.
            + IMPROVE_CREDIT
                - To improve your credit score, focus on paying your bills on time, keeping your credit card balances low, avoiding opening too many new accounts, and maintaining a healthy mix of credit types.
            + CHECK_CREDIT_SCORE
                - You can check your credit score for free through various online platforms or by requesting a credit report from credit bureaus. Remember to review your credit report regularly for any errors or discrepancies.
            + CLUB_SERVICES
                - Our credit score club offers services such as credit counseling, financial education workshops, and credit-building opportunities to help you achieve your financial goals.
        """

        # Load predefined AIML brain
        self.kernel.learn(aiml_brain)

    def create_account_tab(self):
        frame = ttk.Frame(self.tab_account, padding=20, style='TFrame')
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Username:", style='TLabel').grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.username_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.username_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Password:", style='TLabel').grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, show="*").grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Login", command=self.login, style='TButton').grid(row=2, column=0, pady=5, sticky=tk.E)
        ttk.Button(frame, text="Register", command=self.register_user, style='TButton').grid(row=2, column=1, pady=5, sticky=tk.W)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        if username and password:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if username in self.users and self.users[username] == hashed_password:
                # Disable account tab after successful login
                self.tab_control.tab(0, state="disabled")
                messagebox.showinfo("Success", f"Welcome, {username}!")
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        else:
            messagebox.showerror("Error", "Please enter a username and password.")

    def register_user(self):
        username = self.username_var.get()
        password = self.password_var.get()
        if username and password:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if username not in self.users:
                self.users[username] = hashed_password
                messagebox.showinfo("Success", "Account created successfully. You can now login.")
            else:
                messagebox.showerror("Error", "Username already exists. Please choose another username.")
        else:
            messagebox.showerror("Error", "Please enter a username and password.")

    def create_create_tab(self):
        frame = ttk.Frame(self.tab_create, padding=20, style='TFrame')
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Club Name:", style='TLabel').grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.club_name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.club_name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Membership Fee ($):", style='TLabel').grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.membership_fee_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.membership_fee_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Create Club", command=self.create_club, style='TButton').grid(row=2, column=0, columnspan=2, pady=5)

    def create_club(self):
        club_name = self.club_name_var.get()
        if club_name:
            if club_name not in self.clubs.keys():
                membership_fee = float(self.membership_fee_var.get()) if self.membership_fee_var.get() else 0
                self.clubs[club_name] = CreditBuilderClub(membership_fee)
                self.club_selection_dropdown["values"] = list(self.clubs.keys())
                self.club_selection_dropdown.current(0)
                messagebox.showinfo("Success", f"Club '{club_name}' created.")
            else:
                messagebox.showerror("Error", f"Club '{club_name}' already exists.")
        else:
            messagebox.showerror("Error", "Please enter a club name.")

    def create_manage_tab(self):
        frame = ttk.Frame(self.tab_manage, padding=20, style='TFrame')
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Select Club:", style='TLabel').grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.club_selection_var = tk.StringVar()
        self.club_selection_dropdown = ttk.Combobox(frame, textvariable=self.club_selection_var, state="readonly")
        self.club_selection_dropdown.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Load Club Data", command=self.load_club_data, style='TButton').grid(row=0, column=2, padx=5, pady=5)

        ttk.Button(frame, text="Add Member", command=self.add_member, style='TButton').grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(frame, text="Remove Member", command=self.remove_member, style='TButton').grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Export Club Data", command=self.export_club_data, style='TButton').grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(frame, text="Member ID:", style='TLabel').grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.member_id_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.member_id_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Amount:", style='TLabel').grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.amount_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.amount_var).grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Contribute", command=self.contribute, style='TButton').grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Provide Loan", command=self.provide_loan, style='TButton').grid(row=5, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="View Member List", command=self.view_member_list, style='TButton').grid(row=6, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="View Member Details", command=self.view_member_details, style='TButton').grid(row=7, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="View Club Summary", command=self.view_club_summary, style='TButton').grid(row=8, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Sort Member List", command=self.sort_member_list, style='TButton').grid(row=9, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Search Member", command=self.search_member, style='TButton').grid(row=10, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Exit Club", command=self.exit_club, style='TButton').grid(row=11, column=0, columnspan=2, pady=5)

    def load_club_data(self):
        club_name = self.club_selection_var.get()
        if club_name:
            self.current_club = self.clubs[club_name]
            messagebox.showinfo("Success", f"Club '{club_name}' data loaded.")
        else:
            messagebox.showerror("Error", "Please select a club.")

    def add_member(self):
        member_id = self.member_id_var.get()
        if member_id:
            if self.current_club:
                self.current_club.add_member(member_id)
                messagebox.showinfo("Success", f"Member '{member_id}' added to the club.")
            else:
                messagebox.showerror("Error", "No club data loaded.")
        else:
            messagebox.showerror("Error", "Please enter a member ID.")

    def remove_member(self):
        member_id = self.member_id_var.get()
        if member_id:
            if self.current_club:
                self.current_club.remove_member(member_id)
                messagebox.showinfo("Success", f"Member '{member_id}' removed from the club.")
            else:
                messagebox.showerror("Error", "No club data loaded.")
        else:
            messagebox.showerror("Error", "Please enter a member ID.")

    def export_club_data(self):
        if self.current_club:
            self.current_club.export_data()
            messagebox.showinfo("Success", "Club data exported successfully.")
        else:
            messagebox.showerror("Error", "No club data loaded.")

    def contribute(self):
        member_id = self.member_id_var.get()
        amount = float(self.amount_var.get()) if self.amount_var.get() else 0
        if member_id and amount > 0:
            if self.current_club:
                self.current_club.contribute(member_id, amount)
                messagebox.showinfo("Success", f"Contribution of ${amount} added to member '{member_id}'.")
            else:
                messagebox.showerror("Error", "No club data loaded.")
        else:
            messagebox.showerror("Error", "Please enter a valid member ID and amount.")

    def provide_loan(self):
        if self.current_club:
            self.current_club.provide_loan()
            messagebox.showinfo("Success", "Loan provided successfully.")
        else:
            messagebox.showerror("Error", "No club data loaded.")

    def view_member_list(self):
        if self.current_club:
            member_list = self.current_club.view_member_list()
            messagebox.showinfo("Member List", member_list)
        else:
            messagebox.showerror("Error", "No club data loaded.")

    def view_member_details(self):
        member_id = self.member_id_var.get()
        if member_id:
            if self.current_club:
                member_details = self.current_club.view_member_details(member_id)
                messagebox.showinfo("Member Details", member_details)
            else:
                messagebox.showerror("Error", "No club data loaded.")
        else:
            messagebox.showerror("Error", "Please enter a member ID.")

    def view_club_summary(self):
        if self.current_club:
            club_summary = self.current_club.view_club_summary()
            messagebox.showinfo("Club Summary", club_summary)
        else:
            messagebox.showerror("Error", "No club data loaded.")

    def sort_member_list(self):
        if self.current_club:
            self.current_club.sort_member_list()
            messagebox.showinfo("Success", "Member list sorted.")
        else:
            messagebox.showerror("Error", "No club data loaded.")

    def search_member(self):
        member_id = self.member_id_var.get()
        if member_id:
            if self.current_club:
                result = self.current_club.search_member(member_id)
                if result:
                    messagebox.showinfo("Success", f"Member '{member_id}' found.")
                else:
                    messagebox.showinfo("Error", f"Member '{member_id}' not found.")
            else:
                messagebox.showerror("Error", "No club data loaded.")
        else:
            messagebox.showerror("Error", "Please enter a member ID.")

    def exit_club(self):
        if self.current_club:
            self.current_club = None
            messagebox.showinfo("Success", "Exited current club.")
        else:
            messagebox.showerror("Error", "No club data loaded.")

    def create_chat_tab(self):
        frame = ttk.Frame(self.tab_chat, padding=20, style='TFrame')
        frame.pack(expand=True, fill="both")

        self.chat_history_text = tk.Text(frame, wrap=tk.WORD, state="disabled")
        self.chat_history_text.pack(expand=True, fill="both")

        self.chat_input_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.chat_input_var).pack(side=tk.LEFT, expand=True, fill="x", padx=5, pady=5)

        ttk.Button(frame, text="Send", command=self.send_message, style='TButton').pack(side=tk.RIGHT, padx=5, pady=5)

    def send_message(self):
        message = self.chat_input_var.get()
        if message:
            response = self.kernel.respond(message)
            self.update_chat_history(message, response)
            self.chat_input_var.set("")
        else:
            messagebox.showerror("Error", "Please enter a message.")

    def update_chat_history(self, message, response):
        self.chat_history_text.config(state="normal")
        self.chat_history_text.insert("end", f"You: {message}\n")
        self.chat_history_text.insert("end", f"Credit Score Club Bot: {response}\n")
        self.chat_history_text.config(state="disabled")
        self.chat_history_text.see("end")

    def create_visualize_tab(self):
        frame = ttk.Frame(self.tab_visualize, padding=20, style='TFrame')
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Select Chart Type:", style='TLabel').grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.chart_type_var = tk.StringVar()
        self.chart_type_dropdown = ttk.Combobox(frame, textvariable=self.chart_type_var, state="readonly")
        self.chart_type_dropdown["values"] = ["Bar Chart", "Pie Chart"]
        self.chart_type_dropdown.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Generate Chart", command=self.generate_chart, style='TButton').grid(row=1, column=0, columnspan=2, pady=5)

    def generate_chart(self):
        chart_type = self.chart_type_var.get()
        if chart_type:
            if chart_type == "Bar Chart":
                self.generate_bar_chart()
            elif chart_type == "Pie Chart":
                self.generate_pie_chart()

    def generate_bar_chart(self):
        if self.current_club:
            data = self.current_club.get_data_for_chart()
            plt.figure(figsize=(8, 6))
            plt.bar(data.keys(), data.values())
            plt.xlabel("Member ID")
            plt.ylabel("Credit Score")
            plt.title("Credit Scores of Club Members")
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Embedding the chart in the tkinter GUI
            canvas = FigureCanvasTkAgg(plt.gcf(), master=self.tab_visualize)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # Adding a navigation toolbar for the chart
            toolbar = NavigationToolbar2Tk(canvas, self.tab_visualize)
            toolbar.update()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            messagebox.showerror("Error", "No club data loaded.")

    def generate_pie_chart(self):
        if self.current_club:
            data = self.current_club.get_data_for_chart()
            plt.figure(figsize=(8, 6))
            plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=140)
            plt.title("Credit Score Distribution of Club Members")
            plt.tight_layout()

            # Embedding the chart in the tkinter GUI
            canvas = FigureCanvasTkAgg(plt.gcf(), master=self.tab_visualize)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # Adding a navigation toolbar for the chart
            toolbar = NavigationToolbar2Tk(canvas, self.tab_visualize)
            toolbar.update()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            messagebox.showerror("Error", "No club data loaded.")

class CreditBuilderClub:
    def _init_(self, membership_fee):
        self.members = {}
        self.membership_fee = membership_fee

    def add_member(self, member_id):
        self.members[member_id] = {"credit_score": random.randint(300, 850), "balance": 0}

    def remove_member(self, member_id):
        if member_id in self.members:
            del self.members[member_id]

    def export_data(self):
        with open("club_data.txt", "w") as f:
            for member_id, details in self.members.items():
                f.write(f"Member ID: {member_id}, Credit Score: {details['credit_score']}, Balance: {details['balance']}\n")

    def contribute(self, member_id, amount):
        if member_id in self.members:
            self.members[member_id]["balance"] += amount
        else:
            print("Member not found.")

    def provide_loan(self):
        for member_id, details in self.members.items():
            if details["credit_score"] >= 700:
                details["balance"] += 1000
            elif 650 <= details["credit_score"] < 700:
                details["balance"] += 500
            else:
                details["balance"] += 100

    def view_member_list(self):
        member_list = ", ".join(self.members.keys())
        return member_list

    def view_member_details(self, member_id):
        if member_id in self.members:
            details = self.members[member_id]
            return f"Member ID: {member_id}, Credit Score: {details['credit_score']}, Balance: {details['balance']}"
        else:
            return "Member not found."

    def view_club_summary(self):
        total_balance = sum([details["balance"] for details in self.members.values()])
        return f"Total Members: {len(self.members)}, Total Balance: {total_balance}"

    def sort_member_list(self):
        self.members = dict(sorted(self.members.items(), key=lambda x: x[1]["credit_score"], reverse=True))

    def search_member(self, member_id):
        return member_id in self.members

    def get_data_for_chart(self):
        return {member_id: details["credit_score"] for member_id, details in self.members.items()}


if _name_ == "_main_":
    root = tk.Tk()
    app = CreditBuilderApp(root)
    root.mainloop()
