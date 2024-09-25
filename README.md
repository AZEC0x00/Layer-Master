# Layer-Master
PSD Layer Editor V1
A modern, user-friendly application for viewing and editing PSD (Adobe Photoshop) files, built with a clean architecture and designed for extensibility through plugins.
### This is my attempt to create a simple but extensible psd file editor. 

![master](https://github.com/user-attachments/assets/d689aa83-b6b7-4775-b2ca-ac212ce882f8)


# 📁 Project Structure

```bash
psd_layer_editor/
├── main.py
├── editor/
│   ├── __init__.py
│   └── psd_editor.py
├── gui/
│   ├── __init__.py
│   └── main_window.py
├── plugins/
│   ├── __init__.py
│   ├── plugin_manager.py
│   └── sample_plugin.py
├── requirements.txt
└── README.md

# ✨ Features and Functions

### 🔹 PSD File Operations
- **Open PSD Files**: Load and display PSD files with all their layers.
- **View Layers**: Navigate through individual layers, view layer information, and toggle visibility.
- **Edit Text Layers**: Modify text content in text layers, with support for custom and system fonts.
- **Replace Images**: Replace images in layers while maintaining layer properties.
- **Composite Image Rendering**: Render and preview the composite image with all current edits and adjustments.
- **Save Composite Image**: Export the final image in popular formats like PNG and JPEG.

### 🔹 Custom Fonts and Typography
- **Load Custom Fonts**: Import custom font files (`.ttf`, `.otf`) to use in text layers.
- **Select System Fonts**: Choose from installed system fonts for text rendering.
- **Font Caching**: Improved performance by caching loaded fonts.

### 🔹 Modern GUI with CustomTkinter
- **Responsive Design**: Interface adapts to different screen sizes and resolutions.
- **Dark and Light Themes**: Switch between dark and light modes to suit your preference.
- **Shades of Blue**: Aesthetic appeal with blue-themed accents and rounded edges.
- **Status Bar**: Real-time updates and information displayed at the bottom.

### 🔹 Layer Management
- **Layer List View**: Easily navigate and select layers from a list.
- **Toggle Layer Visibility**: Show or hide layers to customize the composite image.
- **Context Menu**: Right-click on layers for quick access to editing options.

### 🔹 Plugin Support
- **Modular Architecture**: Designed to support plugins for extending functionality.
- **Sample Plugin Included**: Demonstrates how to create and integrate plugins.
- **Plugin Manager**: Automatically loads plugins from the `plugins/` directory.

# 🚀 Getting Started

### Prerequisites
- **Python** 3.6+

Install required packages:
```bash
pip install -r requirements.txt

Running the Application
'''bash
python main.py

🛠 Usage
Opening a PSD File
Navigate to File > Open PSD.
Select the PSD file you wish to edit.
Editing Layers
Select a Layer: Click on a layer in the list to select it.
Edit Text: Right-click on a text layer and choose Edit Text to modify its content.
Replace Image: Right-click on an image layer and choose Replace Image to swap out the image.
Toggle Visibility: Use the Toggle Visibility button to show or hide the selected layer.
Fonts and Typography
Load Custom Font: Go to Fonts > Load Custom Font to import a font file.
Select Font: Choose Fonts > Select Font to pick from installed system fonts.
Themes and Appearance
Switch Theme: Toggle between dark and light modes via View > Switch Theme.
Plugins
Access Plugins: Use the Plugins menu to access additional functionality.
Sample Plugin: Demonstrates plugin capabilities with a simple message box.
🔧 Extending with Plugins
The application is designed with extensibility in mind. Plugins can add new features or modify existing ones without altering the core codebase.

Creating a Plugin
Create a New Plugin File: Add a new .py file in the plugins/ directory.
Implement Required Functions:
register_plugin(): Optional initialization code.
run(gui_instance): The main function that executes your plugin's functionality.
Define PLUGIN_NAME: Set a user-friendly name for your plugin.
Automatic Loading: Your plugin will be loaded automatically when the application starts.
📚 Project Modules
main.py
The entry point of the application. Initializes plugins and launches the GUI.
editor/psd_editor.py
Contains the PSDEditor class responsible for all PSD file operations, including opening files, rendering images, and managing layers.
gui/main_window.py
Defines the PSDLayerEditorGUI class, which builds the application's interface, handles user interactions, and ties together the editor and plugins.
plugins/plugin_manager.py
Manages the discovery and loading of plugins. It scans the plugins/ directory and integrates plugins into the application.
plugins/sample_plugin.py
A sample plugin that demonstrates how to extend the application. It shows a message box when activated.
🌐 Future
Plugin Development Roadmap
5. History and Undo Plugin
Purpose: Implement a history panel that records user actions, allowing multiple levels of undo and redo.
Key Features:

Visual history panel displaying a list of actions.
Ability to undo and redo changes.
Jump to any previous state in the history.
Option to set the number of history states or make it unlimited.
Benefits: Enhances user control and confidence, enabling experimentation without fear of making irreversible mistakes.

14. Cloud Storage Integration Plugin
Purpose: Integrate the application with popular cloud storage services for seamless file access and collaboration.
Key Features:

Open and save PSD files directly from services like Google Drive, Dropbox, and OneDrive.
Automatic syncing of changes to the cloud.
Support for multiple accounts and providers.
Collaboration tools such as shared editing and commenting.
Benefits: Facilitates teamwork and access to files from any device, improving productivity and flexibility.

🙏 Acknowledgments
Thanks to the developers of psd-tools, Pillow, numpy, and customtkinter for their fantastic libraries.

This README was crafted to provide a comprehensive overview of the PSD Layer Editor application, highlighting its features, architecture, and future enhancements.
