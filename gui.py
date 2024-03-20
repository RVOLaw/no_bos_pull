import tkinter as tk
from tkinter import filedialog
from pathlib import Path

class GUI:
    def __init__(self, master, processing_callback):
        self.master = master
        self.master.title("NoBoS")

        self.requested_file_numbers = tk.StringVar()
        self.requested_document_types = tk.StringVar()
        self.output_path = tk.StringVar()

        self.create_widgets(processing_callback)

        self.message_label = tk.Label(self.master, text="", fg="grey")
        self.message_label.grid(row=3, column=0, columnspan=2, pady=10)

    def create_widgets(self, processing_callback):
        # File Numbers Entry
        file_numbers_label = tk.Label(self.master, text="Enter File Number(s):")
        file_numbers_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        file_numbers_entry = tk.Entry(self.master, textvariable=self.requested_file_numbers)
        file_numbers_entry.grid(row=0, column=2, columnspan=2, padx=10, pady=5)
        import_button = tk.Button(self.master, text="Import", command=self.import_file)
        import_button.grid(row=0, column=1, pady=5)

        # Output Path Entry and Browse Button
        output_path_label = tk.Label(self.master, text="Output Path:")
        output_path_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        output_path_entry = tk.Entry(self.master, textvariable=self.output_path)
        output_path_entry.grid(row=1, column=2, columnspan=2, padx=10, pady=5)
        browse_button = tk.Button(self.master, text="Browse", command=self.browse_output_path)
        browse_button.grid(row=1, column=1, padx=5, pady=5)

        # Submit Button
        submit_button = tk.Button(self.master, text="Submit", command=lambda: self.on_submit(processing_callback))
        submit_button.grid(row=2, column=2, pady=10)


    def on_submit(self, processing_callback):
        user_input = self.get_user_input()
        processing_callback(user_input)

        self.message_label.config(text="File created successfully!")

    def browse_output_path(self):
        folder_selected = filedialog.askdirectory()
        self.output_path.set(folder_selected)

    def import_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                file_numbers = file.read().splitlines()
                self.requested_file_numbers.set(','.join(file_numbers))

    def get_user_input(self):
        file_numbers_str = self.requested_file_numbers.get()
    
        # Check if the input is a file path
        if file_numbers_str.endswith('.txt'):
            with open(file_numbers_str, 'r') as file:
                file_numbers = file.read().splitlines()
        else:
            file_numbers = file_numbers_str.split(',')

        document_types_str = self.requested_document_types.get()
        output_path_str = self.output_path.get()

        document_types = document_types_str.split(',')
        output_path = Path(output_path_str)

        return file_numbers, document_types, output_path
