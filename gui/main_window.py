import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font
from PIL import Image, ImageTk
import customtkinter as ctk
from editor.psd_editor import PSDEditor
from plugins import plugin_manager

class PSDLayerEditorGUI:
    """Creates and manages the GUI for the PSD Layer Editor."""
    def __init__(self, master):
        self.master = master
        self.master.title("PSD Layer Editor")
        self.editor = PSDEditor()

        self.create_widgets()
        self.create_menu()

        # Bind resize event to update the preview
        self.master.bind('<Configure>', self.on_resize)

    def get_color(self, color_option):
        """Helper function to get the correct color based on the current theme mode."""
        if isinstance(color_option, (list, tuple)):
            mode = ctk.get_appearance_mode()
            if mode == "Light":
                return color_option[0]
            else:
                return color_option[1]
        else:
            return color_option

    def create_widgets(self):
        self.left_frame = ctk.CTkFrame(self.master, corner_radius=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.right_frame = ctk.CTkFrame(self.master, corner_radius=10)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Use tk.Listbox styled to match customtkinter theme
        bg_color = self.get_color(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        fg_color = self.get_color(ctk.ThemeManager.theme["CTkLabel"]["text_color"])

        self.layer_listbox = tk.Listbox(self.left_frame, bg=bg_color, fg=fg_color, bd=0, highlightthickness=0)
        self.layer_listbox.pack(fill=tk.Y, expand=True)
        self.layer_listbox.bind('<<ListboxSelect>>', self.on_layer_select)
        self.layer_listbox.bind('<Button-3>', self.on_right_click)

        self.toggle_visibility_btn = ctk.CTkButton(self.left_frame, text="Toggle Visibility", command=self.toggle_visibility)
        self.toggle_visibility_btn.pack(fill=tk.X, padx=5, pady=5)

        canvas_bg_color = self.get_color(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        self.canvas = tk.Canvas(self.right_frame, bg=canvas_bg_color, highlightthickness=0, bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.status_bar = ctk.CTkLabel(self.master, text="Welcome to PSD Layer Editor")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_menu(self):
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # File Menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open PSD", command=self.open_psd)
        file_menu.add_command(label="Save Composite Image", command=self.save_composite_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

        # View Menu
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Switch Theme", command=self.switch_theme)

        # Fonts Menu
        fonts_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Fonts", menu=fonts_menu)
        fonts_menu.add_command(label="Load Custom Font", command=self.load_custom_font)
        fonts_menu.add_command(label="Select Font", command=self.select_font)

        # Plugins Menu
        plugins_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Plugins", menu=plugins_menu)
        plugin_manager.populate_menu(plugins_menu, self)

    def switch_theme(self):
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Light":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")
        # Update colors after theme change
        self.update_colors()

    def update_colors(self):
        # Update colors of widgets that use colors from the theme
        bg_color = self.get_color(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        fg_color = self.get_color(ctk.ThemeManager.theme["CTkLabel"]["text_color"])

        self.layer_listbox.configure(bg=bg_color, fg=fg_color)
        canvas_bg_color = self.get_color(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        self.canvas.configure(bg=canvas_bg_color)

        # Update other widgets if necessary
        self.left_frame.configure(fg_color=bg_color)
        self.right_frame.configure(fg_color=bg_color)
        self.status_bar.configure(fg_color=bg_color)

        self.update_preview()

    def open_psd(self):
        file_path = filedialog.askopenfilename(filetypes=[("PSD files", "*.psd")])
        if file_path:
            try:
                self.editor.open_psd(file_path)
                self.update_layer_list()
                self.selected_layer_index = None
                self.update_preview()
                self.status_bar.configure(text=f"Opened PSD file: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open PSD file: {e}")
                print(f"Exception details: {e}")

    def save_composite_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")])
        if file_path:
            try:
                composite_image = self.editor.get_composite_image()
                if composite_image:
                    composite_image.save(file_path)
                    self.status_bar.configure(text=f"Saved composite image: {file_path}")
                else:
                    messagebox.showerror("Error", "No image to save.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")

    def update_layer_list(self):
        self.layer_listbox.delete(0, tk.END)
        for layer in self.editor.get_layer_info():
            name = f"{'[X]' if layer['visible'] else '[ ]'} {layer['name']}"
            self.layer_listbox.insert(tk.END, name)

    def update_preview(self):
        if self.editor.psd is None:
            self.canvas.delete("all")  # Clear the canvas if no PSD is loaded
            return  # No PSD loaded, nothing to update

        if hasattr(self, 'selected_layer_index') and self.selected_layer_index is not None:
            # Display only the selected layer
            layer_image = self.editor.get_selected_layer_image(self.selected_layer_index)
            if layer_image:
                self.display_image(layer_image)
            else:
                self.canvas.delete("all")
        else:
            # Display the composite image
            composite_image = self.editor.get_composite_image()
            if composite_image:
                self.display_image(composite_image)
            else:
                self.canvas.delete("all")

    def display_image(self, image):
        # Resize image to fit canvas while maintaining aspect ratio
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width > 1 and canvas_height > 1:
            image_aspect = image.width / image.height
            canvas_aspect = canvas_width / canvas_height

            if image_aspect > canvas_aspect:
                # Fit to width
                new_width = canvas_width
                new_height = int(canvas_width / image_aspect)
            else:
                # Fit to height
                new_height = canvas_height
                new_width = int(canvas_height * image_aspect)

            image = image.resize((new_width, new_height), Image.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(image)
            self.canvas.delete("all")
            self.canvas.create_image((canvas_width - new_width)//2, (canvas_height - new_height)//2, anchor=tk.NW, image=self.photo_image)
        else:
            image = image.resize((500, 500), Image.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

    def on_resize(self, event):
        self.update_preview()

    def on_layer_select(self, event):
        selected_indices = self.layer_listbox.curselection()
        if selected_indices:
            self.selected_layer_index = selected_indices[0]
            layer_info = self.editor.get_layer_info()[self.selected_layer_index]
            self.status_bar.configure(text=f"Selected Layer: {layer_info['name']}")
            self.update_preview()
        else:
            self.selected_layer_index = None
            self.update_preview()

    def on_right_click(self, event):
        try:
            index = self.layer_listbox.nearest(event.y)
            self.layer_listbox.selection_clear(0, tk.END)
            self.layer_listbox.selection_set(index)
            self.selected_layer_index = index
            self.layer_listbox.activate(index)
            self.show_context_menu(event)
        except Exception as e:
            print(f"Error handling right-click: {e}")

    def show_context_menu(self, event):
        self.context_menu = tk.Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="Replace Image", command=self.replace_image)
        self.context_menu.add_command(label="Edit Text", command=self.edit_text)
        self.context_menu.post(event.x_root, event.y_root)

    def replace_image(self):
        if hasattr(self, 'selected_layer_index'):
            image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            if image_path:
                self.editor.replace_layer_image(self.selected_layer_index, image_path)
                self.update_preview()
        else:
            messagebox.showinfo("Info", "Please select a layer.")

    def edit_text(self):
        if hasattr(self, 'selected_layer_index'):
            new_text = simpledialog.askstring("Edit Text", "Enter new text:")
            if new_text is not None:
                self.editor.edit_layer_text(self.selected_layer_index, new_text)
                self.update_preview()
        else:
            messagebox.showinfo("Info", "Please select a layer.")

    def load_custom_font(self):
        font_path = filedialog.askopenfilename(filetypes=[("Font files", "*.ttf;*.otf")])
        if font_path:
            self.editor.load_custom_font(font_path)
            self.status_bar.configure(text=f"Loaded custom font: {os.path.basename(font_path)}")
            self.update_preview()

    def select_font(self):
        # Get list of available fonts
        available_fonts = list(font.families())
        if not available_fonts:
            messagebox.showinfo("No Fonts Available", "No fonts are available on your system.")
            return

        # Create a new window for font selection
        font_window = ctk.CTkToplevel(self.master)
        font_window.title("Select Font")
        font_window.geometry("300x400")

        font_listbox = tk.Listbox(font_window, bg=self.get_color(ctk.ThemeManager.theme["CTkFrame"]["fg_color"]), fg=self.get_color(ctk.ThemeManager.theme["CTkLabel"]["text_color"]), bd=0, highlightthickness=0)
        font_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Populate the listbox with font names
        for f in available_fonts:
            font_listbox.insert(tk.END, f)

        # Function to handle font selection
        def select_font_command():
            selected_indices = font_listbox.curselection()
            if selected_indices:
                selected_font = font_listbox.get(selected_indices[0])
                self.editor.select_font(selected_font)
                self.status_bar.configure(text=f"Selected font: {selected_font}")
                self.update_preview()
                font_window.destroy()

        select_button = ctk.CTkButton(font_window, text="Select", command=select_font_command)
        select_button.pack(pady=5)

    def toggle_visibility(self):
        if hasattr(self, 'selected_layer_index'):
            self.editor.toggle_layer_visibility(self.selected_layer_index)
            self.update_layer_list()
            self.update_preview()
        else:
            messagebox.showinfo("Info", "Please select a layer.")

    def mainloop(self):
        self.master.mainloop()
