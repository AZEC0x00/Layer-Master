import os
import importlib

plugins = []

def load_plugins():
    plugin_dir = os.path.dirname(__file__)
    for filename in os.listdir(plugin_dir):
        if filename.endswith(".py") and filename != "__init__.py" and filename != "plugin_manager.py":
            module_name = f"plugins.{filename[:-3]}"
            module = importlib.import_module(module_name)
            if hasattr(module, 'register_plugin'):
                plugins.append(module)

def populate_menu(menu, gui_instance):
    for plugin in plugins:
        plugin_name = getattr(plugin, 'PLUGIN_NAME', plugin.__name__)
        menu.add_command(label=plugin_name, command=lambda p=plugin: p.run(gui_instance))
