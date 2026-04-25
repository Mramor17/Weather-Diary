import storage
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.root.geometry("800x600")
        self.records = []  # list of dicts

        # ---- Input Frame ----
        input_frame = tk.LabelFrame(root, text="Add Weather Record", padx=10, pady=10)
        input_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="e")
        self.date_entry = tk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Temperature (°C):").grid(row=0, column=2, sticky="e")
        self.temp_entry = tk.Entry(input_frame, width=10)
        self.temp_entry.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Description:").grid(row=1, column=0, sticky="e")
        self.desc_entry = tk.Entry(input_frame, width=40)
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=5, sticky="w")

        tk.Label(input_frame, text="Precipitation:").grid(row=1, column=4, sticky="e")
        self.precip_var = tk.BooleanVar()
        tk.Checkbutton(input_frame, variable=self.precip_var).grid(row=1, column=5, sticky="w")

        tk.Button(input_frame, text="Add Record", command=self.add_record).grid(row=2, column=0, columnspan=6, pady=10)

        # ---- Filter Frame ----
        filter_frame = tk.LabelFrame(root, text="Filter Records", padx=10, pady=10)
        filter_frame.pack(pady=5, padx=10, fill="x")

        tk.Label(filter_frame, text="Filter by Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="e")
        self.filter_date_entry = tk.Entry(filter_frame, width=15)
        self.filter_date_entry.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Temp > (°C):").grid(row=0, column=2, sticky="e")
        self.filter_temp_entry = tk.Entry(filter_frame, width=10)
        self.filter_temp_entry.grid(row=0, column=3, padx=5)

        tk.Button(filter_frame, text="Apply Filters", command=self.display_records).grid(row=0, column=4, padx=10)
        tk.Button(filter_frame, text="Show All", command=self.show_all).grid(row=0, column=5)

        # ---- Table Frame ----
        self.tree = ttk.Treeview(root, columns=("Date", "Temp", "Description", "Precip"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Temp", text="Temp (°C)")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Precip", text="Precipitation")
        self.tree.column("Date", width=100)
        self.tree.column("Temp", width=80)
        self.tree.column("Description", width=300)
        self.tree.column("Precip", width=80)
        self.tree.pack(pady=10, fill="both", expand=True)

        # ---- Buttons for JSON ----
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Save to JSON", command=self.save_to_json).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Load from JSON", command=self.load_from_json).pack(side="left", padx=5)

        self.display_records()

    # ---------- Validation ----------
    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    # ---------- Add Record ----------
    def add_record(self):
        date = self.date_entry.get().strip()
        temp_str = self.temp_entry.get().strip()
        desc = self.desc_entry.get().strip()
        precip = self.precip_var.get()

        # Validations
        if not date or not temp_str or not desc:
            messagebox.showerror("Error", "All fields (Date, Temperature, Description) are required.")
            return
        if not self.validate_date(date):
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return
        try:
            temp = float(temp_str)
        except ValueError:
            messagebox.showerror("Error", "Temperature must be a number.")
            return

        self.records.append({
            "date": date,
            "temperature": temp,
            "description": desc,
            "precipitation": precip
        })
        self.clear_inputs()
        self.display_records()
        messagebox.showinfo("Success", "Record added!")

    def clear_inputs(self):
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set(False)

    # ---------- Filtering & Display ----------
    def display_records(self):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        filter_date = self.filter_date_entry.get().strip()
        filter_temp_str = self.filter_temp_entry.get().strip()
        filter_temp = None
        if filter_temp_str:
            try:
                filter_temp = float(filter_temp_str)
            except ValueError:
                messagebox.showerror("Error", "Filter temperature must be a number.")
                return

        for rec in self.records:
            # Apply filters
            if filter_date and rec["date"] != filter_date:
                continue
            if filter_temp is not None and rec["temperature"] <= filter_temp:
                continue

            precip_text = "Yes" if rec["precipitation"] else "No"
            self.tree.insert("", tk.END, values=(
                rec["date"],
                rec["temperature"],
                rec["description"],
                precip_text
            ))

    def show_all(self):
        self.filter_date_entry.delete(0, tk.END)
        self.filter_temp_entry.delete(0, tk.END)
        self.display_records()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
