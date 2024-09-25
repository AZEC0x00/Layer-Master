import os
import logging
from tkinter import messagebox
from psd_tools import PSDImage
from PIL import Image, ImageDraw, ImageFont

# Suppress warnings from psd_tools
logging.getLogger('psd_tools').setLevel(logging.ERROR)

class PSDEditor:
    """Handles PSD file operations and manipulations."""
    def __init__(self):
        self.psd = None
        self.layer_replacements = {}  # Stores image replacements per layer
        self.layer_text_edits = {}    # Stores text edits per layer
        self.font_cache = {}          # Cache for loaded fonts
        self.missing_fonts = set()    # Track missing fonts to avoid repeated warnings
        self.custom_font_path = None  # Path to custom font loaded by the user
        self.selected_font_name = None  # Name of the font selected by the user

    def open_psd(self, file_path):
        try:
            self.psd = PSDImage.open(file_path)
            self.layer_replacements.clear()
            self.layer_text_edits.clear()
            self.missing_fonts.clear()
        except Exception as e:
            print(f"Error opening PSD file: {e}")
            self.psd = None
            raise

    def get_composite_image(self):
        if self.psd is not None:
            return self._render_psd()
        else:
            return None

    def _render_psd(self):
        """Render the PSD with simulated changes."""
        composite_image = Image.new('RGBA', self.psd.size)
        for layer in self.psd:
            if not layer.is_visible():
                continue
            layer_image = self.get_layer_image(layer)
            if layer_image:
                # Align layer position
                position = layer.offset
                temp_image = Image.new('RGBA', self.psd.size)
                temp_image.paste(layer_image, position)
                composite_image = Image.alpha_composite(composite_image, temp_image)
        return composite_image.convert('RGB')

    def get_layer_info(self):
        layer_info = []
        if self.psd is not None:
            for index, layer in enumerate(self.psd):
                info = {
                    'name': layer.name,
                    'visible': layer.visible,
                    'kind': layer.kind,
                    'index': index
                }
                layer_info.append(info)
        return layer_info

    def get_layer_image(self, layer):
        """Get the layer image, applying any replacements or text edits."""
        try:
            if layer.layer_id in self.layer_replacements:
                # Use the replacement image
                return self.layer_replacements[layer.layer_id]
            elif layer.kind == 'type':
                # Render the text with edits
                text = self.layer_text_edits.get(layer.layer_id, layer.text)
                return self._render_text_layer(layer, text)
            else:
                return layer.composite()
        except Exception as e:
            print(f"Error getting layer image: {e}")
            return None

    def _render_text_layer(self, layer, text):
        """Render a text layer with the given text."""
        try:
            # Use selected font if available
            if self.selected_font_name:
                font_name = self.selected_font_name
                font_size = self._get_font_size(layer)
                fill_color = self._get_fill_color(layer)
            else:
                # Extract font properties from layer
                font_name, font_size, fill_color = self._extract_font_properties(layer)

            # Attempt to load the font
            font = self._load_font(font_name, font_size)

            # Create an image with transparent background
            img = Image.new('RGBA', layer.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # Draw the text
            draw.text((0, 0), text, font=font, fill=fill_color)

            return img
        except Exception as e:
            print(f"Error rendering text layer: {e}")
            return layer.composite()

    def _extract_font_properties(self, layer):
        """Extract font name, size, and fill color from the text layer."""
        try:
            # Default values
            font_name = 'Arial'
            font_size = 20
            fill_color = (255, 255, 255, 255)  # White color

            # Extract font size
            engine_data = layer.engine_dict
            styles = engine_data['StyleRun']['RunArray'][0]['StyleSheet']['StyleSheetData']

            font_size = int(styles.get('FontSize', font_size))

            # Extract font name
            font_set = engine_data['ResourceDict']['FontSet']
            font_index = styles['Font']
            font_name = font_set[font_index]['Name']

            # Extract fill color
            fill_color_values = styles.get('FillColor', {}).get('Values', [1, 1, 1])
            fill_color = tuple(int(c * 255) for c in fill_color_values)
            if len(fill_color) == 3:
                fill_color = (*fill_color, 255)  # Add alpha channel

            return font_name, font_size, fill_color
        except Exception as e:
            print(f"Error extracting font properties: {e}")
            return 'Arial', 20, (255, 255, 255, 255)

    def _get_font_size(self, layer):
        """Get font size from layer."""
        try:
            engine_data = layer.engine_dict
            styles = engine_data['StyleRun']['RunArray'][0]['StyleSheet']['StyleSheetData']
            font_size = int(styles.get('FontSize', 20))
            return font_size
        except Exception as e:
            print(f"Error getting font size: {e}")
            return 20

    def _get_fill_color(self, layer):
        """Get fill color from layer."""
        try:
            styles = layer.engine_dict['StyleRun']['RunArray'][0]['StyleSheet']['StyleSheetData']
            fill_color_values = styles.get('FillColor', {}).get('Values', [1, 1, 1])
            fill_color = tuple(int(c * 255) for c in fill_color_values)
            if len(fill_color) == 3:
                fill_color = (*fill_color, 255)  # Add alpha channel
            return fill_color
        except Exception as e:
            print(f"Error getting fill color: {e}")
            return (255, 255, 255, 255)

    def _load_font(self, font_name, font_size):
        """Load the font, using cache and handling missing fonts."""
        try:
            # Check if the font is already loaded
            font_key = (font_name, font_size)
            if font_key in self.font_cache:
                return self.font_cache[font_key]

            # Use custom font if loaded
            if self.custom_font_path:
                font = ImageFont.truetype(self.custom_font_path, font_size)
            else:
                # Attempt to load the font from system fonts
                font = ImageFont.truetype(font_name, font_size)
            self.font_cache[font_key] = font
            return font
        except IOError:
            if font_name not in self.missing_fonts:
                self.missing_fonts.add(font_name)
                print(f"Font '{font_name}' not found.")
            # Use default font
            return ImageFont.load_default()

    def load_custom_font(self, font_path):
        """Load a custom font specified by the user."""
        self.custom_font_path = font_path
        self.font_cache.clear()  # Clear font cache to use the new font

    def select_font(self, font_name):
        """Select a font to use for text rendering."""
        self.selected_font_name = font_name
        self.font_cache.clear()  # Clear font cache to use the new font

    def toggle_layer_visibility(self, layer_index):
        try:
            layer = self.psd[layer_index]
            layer.visible = not layer.visible
        except Exception as e:
            print(f"Error toggling layer visibility: {e}")
            messagebox.showerror("Error", f"Failed to toggle layer visibility: {e}")

    def replace_layer_image(self, layer_index, image_path):
        try:
            layer = self.psd[layer_index]
            new_image = Image.open(image_path).convert('RGBA')
            # Resize the image to match the layer size
            new_image = new_image.resize((layer.width, layer.height), Image.LANCZOS)
            # Store the replacement image
            self.layer_replacements[layer.layer_id] = new_image
        except Exception as e:
            print(f"Error replacing layer image: {e}")
            messagebox.showerror("Error", f"Failed to replace layer image: {e}")

    def edit_layer_text(self, layer_index, new_text):
        try:
            layer = self.psd[layer_index]
            self.layer_text_edits[layer.layer_id] = new_text
        except Exception as e:
            print(f"Error editing layer text: {e}")
            messagebox.showerror("Error", f"Failed to edit layer text: {e}")

    def get_selected_layer_image(self, layer_index):
        """Get the image of the selected layer, considering replacements and edits."""
        try:
            layer = self.psd[layer_index]
            layer_image = self.get_layer_image(layer)
            # Create an image the size of the PSD
            full_image = Image.new('RGBA', self.psd.size)
            # Paste the layer image at its offset
            position = layer.offset
            full_image.paste(layer_image, position)
            return full_image.convert('RGB')
        except Exception as e:
            print(f"Error getting selected layer image: {e}")
            return None
