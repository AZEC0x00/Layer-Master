import customtkinter as ctk
from gui.main_window import PSDLayerEditorGUI
from plugins import plugin_manager

def main():
    # Initialize plugins
    plugin_manager.load_plugins()

    root = ctk.CTk()
    app = PSDLayerEditorGUI(root)
    app.mainloop()

if __name__ == "__main__":
    main()
