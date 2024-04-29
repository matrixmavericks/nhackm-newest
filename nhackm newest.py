import tkinter as tk
from tkinter import ttk, messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import aiml
import boto3

class CreditBuilderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Credit Builder Club")
        self.master.geometry("800x600")

        self.current_club = None
        self.kernel = aiml.Kernel()

        self.create_tabs()

    def create_tabs(self):
        self.tabControl = ttk.Notebook(self.master)

        self.tab_management = ttk.Frame(self.tabControl)
        self.tab_chat = ttk.Frame(self.tabControl)
        self.tab_visualize = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab_management, text="Management")
        self.tabControl.add(self.tab_chat, text="Chat")
        self.tabControl.add(self.tab_visualize, text="Visualize")

        self.tabControl.pack(expand=1, fill="both")

        self.create_management_tab()
        self.create_chat_tab()
        self.create_visualize_tab()

    def create_management_tab(self):
        frame = ttk.Frame(self.tab_management, padding=20, style='TFrame')
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Select Club:", style='TLabel').grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.club_selection_var = tk.StringVar()
        self.club_selection_dropdown = ttk.Combobox(frame, textvariable=self.club_selection_var, state="readonly")
        self.club_selection_dropdown["values"] = ["Club A", "Club B", "Club C"]
        self.club_selection_dropdown.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Load Club Data", command=self.load_club_data, style='TButton').grid(row=1, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Add Member", command=self.add_member, style='TButton').grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Remove Member", command=self.remove_member, style='TButton').grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Export Club Data", command=self.export_club_data, style='TButton').grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Contribute", command=self.contribute, style='TButton').grid(row=5, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Provide Loan", command=self.provide_loan, style='TButton').grid(row=6, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="View Member List", command=self.view_member_list, style='TButton').grid(row=7, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="View Member Details", command=self.view_member_details, style='TButton').grid(row=8, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="View Club Summary", command=self.view_club_summary, style='TButton').grid(row=9, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Sort Member List", command=self.sort_member_list, style='TButton').grid(row=10, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Search Member", command=self.search_member, style='TButton').grid(row=11, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Exit Club", command=self.exit_club, style='TButton').grid(row=12, column=0, columnspan=2, pady=5)

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
            messagebox.showinfo("Success", "Member list sorted by credit score.")
        else:
            messagebox.showerror("Error", "No club data loaded.")

    def search_member(self):
        member_id = self.member_id_var.get()
        if member_id:
            if self.current_club:
                if self.current_club.search_member(member_id):
                    messagebox.showinfo("Success", f"Member '{member_id}' found in the club.")
                else:
                    messagebox.showinfo("Not Found", f"Member '{member_id}' not found in the club.")
            else:
                messagebox.showerror("Error", "No club data loaded.")
        else:
            messagebox.showerror("Error", "Please enter a member ID.")

    def exit_club(self):
        self.current_club = None
        messagebox.showinfo("Success", "Exited club.")

    def create_chat_tab(self):
        # Chat interface here
        pass

    def create_visualize_tab(self):
        frame = ttk.Frame(self.tab_visualize, padding=20, style='TFrame')
        frame.pack(expand=True, fill="both")

        ttk.Button(frame, text="Generate Bar Chart", command=self.generate_bar_chart, style='TButton').pack(pady=5)
        ttk.Button(frame, text="Generate Pie Chart", command=self.generate_pie_chart, style='TButton').pack(pady=5)

    def generate_bar_chart(self):
        if self.current_club:
            data = self.current_club.get_data_for_chart()
            plt.figure(figsize=(10, 6))
            plt.bar(data.keys(), data.values(), color='skyblue')
            plt.xlabel('Member ID')
            plt.ylabel('Credit Score')
            plt.title('Credit Score Distribution of Club Members')
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
    def __init__(self, membership_fee):
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

if __name__ == "__main__":
    root = tk.Tk()
    app = CreditBuilderApp(root)
    root.mainloop()
