import tkinter as tk
from tkinter import filedialog, messagebox
import json

class GradeCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Grade Calculator')
        self.file_path = None  # Keep track of the open file

        # Frame for rows
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Column titles
        titles = ['Assignment', 'Grade', 'Weight (%)', 'Toggle Grade', 'Actions']
        for i, title in enumerate(titles):
            label = tk.Label(self.main_frame, text=title)
            label.grid(row=0, column=i)

        # Initial row
        self.rows = []
        self.add_row()

        # Additional inputs for final calculations
        self.final_grade_entry = tk.Entry(root, width=10)
        self.final_grade_entry.pack(side=tk.LEFT, padx=5)
        self.final_grade_label = tk.Label(root, text="Desired Final Grade")
        self.final_grade_label.pack(side=tk.LEFT, padx=5)

        self.final_exam_entry = tk.Entry(root, width=10)
        self.final_exam_entry.pack(side=tk.LEFT, padx=5)
        self.final_exam_label = tk.Label(root, text="Final Exam Score")
        self.final_exam_label.pack(side=tk.LEFT, padx=5)

        self.required_exam_result_label = tk.Label(root, text="Needed/Result:")
        self.required_exam_result_label.pack(side=tk.LEFT, padx=5)
        self.required_exam_result = tk.Label(root, text="---")
        self.required_exam_result.pack(side=tk.LEFT, padx=5)

        # Buttons
        tk.Button(root, text='Add Row', command=self.add_row).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(root, text='Save Data', command=self.save_data).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(root, text='Load Data', command=self.load_data).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(root, text='Calculate', command=self.calculate_grades).pack(side=tk.RIGHT, padx=10, pady=10)

    def add_row(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.grid(row=len(self.rows) + 1, columnspan=5)

        entry_assignment = tk.Entry(row_frame, width=15)
        entry_assignment.pack(side=tk.LEFT, padx=5)

        entry_grade = tk.Entry(row_frame, width=10)
        entry_grade.pack(side=tk.LEFT, padx=5)

        entry_weight = tk.Entry(row_frame, width=10)
        entry_weight.pack(side=tk.LEFT, padx=5)

        toggle_btn = tk.Button(row_frame, text='Percentage', command=lambda: self.toggle_grade(toggle_btn))
        toggle_btn.pack(side=tk.LEFT, padx=5)

        remove_btn = tk.Button(row_frame, text='Remove', command=lambda: self.remove_row(row_frame))
        remove_btn.pack(side=tk.LEFT, padx=5)

        self.rows.append((entry_assignment, entry_grade, entry_weight, toggle_btn, row_frame))

    def remove_row(self, row_frame):
        row_frame.destroy()
        self.rows = [(entry_assignment, entry_grade, entry_weight, toggle_btn, frame) for entry_assignment, entry_grade, entry_weight, toggle_btn, frame in self.rows if frame != row_frame]

    def toggle_grade(self, btn):
        btn.config(text='Points' if btn.cget('text') == 'Percentage' else 'Percentage')

    def save_data(self):
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if self.file_path:
            data = [{'assignment': entry_assignment.get(), 'grade': entry_grade.get(), 'weight': entry_weight.get()} for entry_assignment, entry_grade, entry_weight, _, _ in self.rows]
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=4)

    def load_data(self):
        data_file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if data_file:
            self.file_path = data_file
            with open(data_file, 'r') as f:
                data = json.load(f)
            for entry in data:
                self.add_row()
                self.rows[-1][0].insert(0, entry['assignment'])
                self.rows[-1][1].insert(0, entry['grade'])
                self.rows[-1][2].insert(0, entry['weight'])

    def calculate_grades(self):
        total_grade = 0
        total_weight = 0
        for entry_assignment, entry_grade, entry_weight, toggle_btn, _ in self.rows:
            grade = float(entry_grade.get())
            weight = float(entry_weight.get()) / 100
            if toggle_btn.cget('text') == 'Points':
                grade = grade / 100  # Assuming the total points possible is 100
            total_grade += grade * weight
            total_weight += weight

        final_exam_score = self.final_exam_entry.get()
        desired_final_grade = self.final_grade_entry.get()

        if final_exam_score and desired_final_grade:
            messagebox.showinfo("Error", "Please enter only one value to calculate the other.")
            return

        if desired_final_grade:
            desired_final_grade = float(desired_final_grade)
            if total_weight <= 1.0:
                needed_final_exam = (desired_final_grade - total_grade) / (1 - total_weight)
                self.required_exam_result.config(text=f"{needed_final_exam:.2f}% Needed on Final")
            else:
                messagebox.showerror("Error", "Total weight cannot exceed 100%.")
        elif final_exam_score:
            final_exam_score = float(final_exam_score)
            final_grade = float((final_exam_score*(1 - total_weight)) +(total_grade))
            self.required_exam_result.config(text=f"Final Grade: {final_grade:.2f}%")

def main():
    root = tk.Tk()
    app = GradeCalculatorApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
