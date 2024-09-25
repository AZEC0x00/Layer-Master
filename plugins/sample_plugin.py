PLUGIN_NAME = "Sample Plugin"

def register_plugin():
    pass  # For future use if needed

def run(gui_instance):
    from tkinter import messagebox
    messagebox.showinfo("Sample Plugin", "This is a sample plugin.")
