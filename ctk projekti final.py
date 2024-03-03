import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ttkthemes import ThemedTk
import csv
import re

class Project:
    def __init__(self, root):
        self.timetable_courses = {}
        self.all_data = []

        # Shtoni butonin e shfletimit
        browse_button = ttk.Button(root, text="Browse", command=self.browse_file)
        browse_button.grid(row=0, column=2, padx=10, pady=10)

        # Entry for file path
        self.path_entry = ttk.Entry(root, width=50)
        self.path_entry.grid(row=0, column=1, padx=10, pady=10)

        # Department selection
        code_label = ttk.Label(root, text="Department:")
        code_label.grid(row=1, column=0, padx=10, pady=10)
        self.code_box = ttk.Combobox(root, values=('CS', 'EE', 'UNI', 'MGT', 'MATH', 'ISE', 'ECON', 'LIFE', 'IE', 'GER', 'FRE', 'ENGR', 'EECS', 'ECON', 'ECE'))
        self.code_box.grid(row=1, column=1, padx=10, pady=10)
        self.code_box.set('Select Department')

        # Year selection
        year_label = ttk.Label(root, text="Year:")
        year_label.grid(row=2, column=0, padx=10, pady=10)
        self.year_box = ttk.Combobox(root, values=('1', '2', '3', '4', '5'))
        self.year_box.grid(row=2, column=1, padx=10, pady=10)
        self.year_box.set('Select Year')

        # Display button
        display_button = ttk.Button(root, text="Display", command=self.display_semester_program)
        display_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        
        # Listbox for courses
        self.list_courses = tk.Listbox(root, height=10, width=50, selectmode=tk.MULTIPLE)
        self.list_courses.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.list_courses.bind('<<ListboxSelect>>', self.on_course_select)

        # Selected courses
        self.list_selected = tk.Listbox(root, height=10, width=50)
        self.list_selected.grid(row=4, column=2, columnspan=2, padx=10, pady=10)


        # Clear and Save buttons
        clear_button = ttk.Button(root, text="Clear", command=self.clear_selection)
        clear_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        save_button = ttk.Button(root, text="Save", command=self.save_selection)
        save_button.grid(row=5, column=2, columnspan=2, padx=10, pady=10)


         # Shtoni metodën e re për shfletimin e skedarit
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, file_path)

    
    def read_csv_file(self, file_path):
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                self.all_data = [row for row in reader if row]  # Filtrojmë rreshtat bosh
        except Exception as e:
            messagebox.showerror("Error", f"Gabim gjatë leximit të skedarit: {e}")
            return False
        return True

    def filter_courses(self, selected_code, selected_year):
        filtered_courses = []
        pattern = re.compile(r"([A-Z]+)\s+(\d+)")  # Regex për të ndarë kodin dhe numrin e kursit

        for course in self.all_data:
            match = pattern.match(course[0])
            if not match:
                continue
            code, year = match.groups()
            if (selected_year == "Select Year" or year.startswith(selected_year)) and \
               (selected_code == "Select Department" or code == selected_code):
                filtered_courses.append(course)
        return filtered_courses

    def display_semester_program(self):
        file_path = self.path_entry.get()
        if not file_path:
            messagebox.showwarning("Warning", "Ju lutemi zgjidhni një skedar!")
            return
        if not self.read_csv_file(file_path):
            return

        selected_year = self.year_box.get()
        selected_code = self.code_box.get()
        filtered_courses = self.filter_courses(selected_code, selected_year)
        self.list_courses.delete(0, tk.END)
        for course in filtered_courses:
            self.list_courses.insert(tk.END, " ".join(course))
    
    
    def on_course_select(self, event=None):
        selected_indices = self.list_courses.curselection()
        for idx in selected_indices:
            course_str = self.list_courses.get(idx)
            course_code, course_time = course_str.split()[1], course_str.split()[2:]
            #print(self.course_str)

            if len(self.list_selected.get(0, tk.END)) >= 6:
                messagebox.showwarning("Warning", "You can select at most 6 courses.")
                return

            for selected in self.list_selected.get(0, tk.END):
                selected_time = selected.split()[2:]
                if course_time == selected_time:
                    messagebox.showwarning("Warning", f"Course {course_code} has a scheduling conflict.")
                    return

            self.list_selected.insert(tk.END, course_str)


    #metoda per clear te self.list_selected
    def clear_selection(self):
        self.list_selected.delete(0, tk.END)
        self.timetable_courses.clear()
    
    #metoda per save te file
    def save_selection(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], initialfile="timetable.csv")
        if save_path:
            with open(save_path, "w", newline='', encoding="utf-8") as file:
                csv_writer = csv.writer(file)
                for course in self.list_selected.get(0, tk.END):
                    csv_writer.writerow(course.split())

if __name__ == "__main__":
    root = ThemedTk(theme="equilux")  # Përdorim të temës "equilux"
    root.title("Semester Program")

    # Definimi i ngjyrave
    dark_grey = '#333333'
    dark_blue = '#1E395B'
    
    # Konfiguroni stilin e widget-ëve
    style = ttk.Style(root)
    style.configure('TButton', font=('Helvetica', 12), background=dark_blue, foreground='white', borderwidth=1)
    style.configure('TLabel', font=('Helvetica', 12), background=dark_grey, foreground='white')
    style.configure('TEntry', font=('Helvetica', 12), fieldbackground=dark_grey, foreground='white', bordercolor=dark_blue)
    style.configure('TCombobox', font=('Helvetica', 12), fieldbackground=dark_grey, foreground='white', selectbackground=dark_blue, selectforeground='white')
    style.configure('TListbox', font=('Helvetica', 12), background=dark_grey, foreground='white', bordercolor=dark_blue, selectbackground=dark_blue, selectforeground='white')
    style.map('TCombobox', fieldbackground=[('readonly', dark_grey)])
    style.map('TEntry', fieldbackground=[('readonly', dark_grey)])
    
    # Përdorni ngjyrat e definuara për sfondin dhe ngjyrat e borderit
    style.configure('Horizontal.TScale', background=dark_grey, troughcolor=dark_blue)
    style.configure('TCheckbutton', background=dark_grey, foreground='white')
    style.configure('TRadiobutton', background=dark_grey, foreground='white')

    # Ndërrojeni ngjyrën e sfondit të dritares kryesore për të përputhur me temën
    root.configure(bg=dark_grey)

    app = Project(root)
    root.mainloop()
