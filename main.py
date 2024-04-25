from PIL import Image, ImageDraw, ImageFont
import math
import os
import json

def hex_to_rgb(hex_color):
    """
    Convert a hexadecimal color string to an RGB tuple.

    Args:
        hex_color (str): The color in hex format.

    Returns:
        tuple: The color in RGB format.
    """
    hex_color = hex_color.lstrip('#')  # Remove the '#' character if present
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))  # Convert hex to RGB

def draw_gradient(draw, width, height, top_color, bottom_color):
    """
    Draw a vertical gradient from top_color to bottom_color on a given drawable surface.

    Args:
        draw (ImageDraw.Draw): The drawing context.
        width (int): The width of the area to fill.
        height (int): The height of the area to fill.
        top_color (tuple): RGB tuple for the top color.
        bottom_color (tuple): RGB tuple for the bottom color.
    """
    # Iterate over the height of the image
    for i in range(height):
        # Calculate blend factor based on height
        blend = (float(i) / height) * 2 if i <= height // 2 else 2 - (float(i) / height) * 2
        # Linearly interpolate between top and bottom colors
        color = [int(top_color[j] * (1 - blend) + bottom_color[j] * blend) for j in range(3)]
        draw.line([(0, i), (width, i)], tuple(color), width=1)

def draw_flower(draw, x, y, scale):
    """
    Draw a simple flower with configurable position and scale.

    Args:
        draw (ImageDraw.Draw): The drawing context.
        x (int): The x-coordinate of the flower's center.
        y (int): The y-coordinate of the flower's center.
        scale (float): Scale factor for the flower's size.
    """
    petals = 5  # Number of petals
    inner_radius = 10 * scale
    outer_radius = 30 * scale
    petal_color = 'pink'
    center_color = 'yellow'
    # Draw each petal as an ellipse
    for i in range(petals):
        angle = math.radians(i * (360 / petals))
        dx = inner_radius * math.cos(angle)
        dy = inner_radius * math.sin(angle)
        draw.ellipse([x - outer_radius + dx, y - outer_radius + dy,
                      x + outer_radius + dx, y + outer_radius + dy], fill=petal_color)
    # Draw the center of the flower
    draw.ellipse([x - inner_radius, y - inner_radius,
                  x + inner_radius, y + inner_radius], fill=center_color)

def draw_table(draw, top_left_x, top_left_y, table_data, col_widths, row_height, font_path):
    """
    Draw a table with data from a JSON file.

    Args:
        draw (ImageDraw.Draw): The drawing context.
        top_left_x (int): The x-coordinate of the top left corner of the table.
        top_left_y (int): The y-coordinate of the top left corner of the table.
        table_data (dict): Data for the table, including 'columns' and 'data' keys.
        col_widths (list of int): List of column widths.
        row_height (int): Height of each row.
        font_path (str): Path to the font file used for text.
    """
    font = ImageFont.truetype(font_path, 16)  # Load font
    y_offset = top_left_y

    # Draw header row
    for col_idx, col in enumerate(table_data['columns']):
        x_offset = top_left_x + sum(col_widths[:col_idx])
        draw.rectangle([x_offset, y_offset, x_offset + col_widths[col_idx], y_offset + row_height], fill="#FFD700", outline="black")
        draw.text((x_offset + 10, y_offset + 10), col, font=font, fill="black")

    y_offset += row_height
    # Draw data rows
    for row in table_data['data']:
        for col_idx, cell in enumerate(row):
            x_offset = top_left_x + sum(col_widths[:col_idx])
            draw.rectangle([x_offset, y_offset, x_offset + col_widths[col_idx], y_offset + row_height], fill="#E6E6FA" if col_idx % 2 == 0 else "#98FB98", outline="black")
            draw.text((x_offset + 10, y_offset + 10), cell, font=font, fill="black")
        y_offset += row_height
    
def load_json_file(filepath):
    """
    Loads a JSON file and returns its content as a dictionary.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        dict: The content of the JSON file.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("The file was not found.")
        return {}
    except json.JSONDecodeError:
        print("The file is not a valid JSON file.")
        return {}

def create_composite_image_with_gradient(logo_path, path_img1, path_img2, path_img3, path_img4, path_out, font_path, filepath):
    """
    Create a composite image that includes a gradient background, flowers, a logo, image placeholders, and a data table.

    Args:
        logo_path (str): Path to the logo image.
        path_img1 (str): Path to the first placeholder image.
        path_img2 (str): Path to the second placeholder image.
        path_img3 (str): Path to the third placeholder image.
        path_img4 (str): Path to the fourth placeholder image.
        path_out (str): Output directory for the final image.
        font_path (str): Path to the font used in text elements.
        filepath (str): Path to the JSON data for the table.

    Returns:
        str: Path to the saved composite image.
    """
    width, height = 692, 982  # Dimensions of the composite image
    margin = 35  # Margin around the elements in the image
    composite_image = Image.new('RGBA', (width, height))
    draw = ImageDraw.Draw(composite_image)

    # Create a gradient background
    blue = hex_to_rgb('accbf2')
    orange = hex_to_rgb('fd9965')
    draw_gradient(draw, width, height, blue, orange)

    # Draw flowers in the top corners
    flower_scale = 1.5
    outer_radius = int(30 * flower_scale)
    draw_flower(draw, margin + outer_radius, margin + outer_radius, flower_scale)
    draw_flower(draw, width - margin - outer_radius, margin + outer_radius, flower_scale)

    # Add logo to the center top
    logo = Image.open(logo_path).convert("RGBA")
    logo_size = 180
    logo.thumbnail((logo_size, logo_size), Image.ANTIALIAS)
    logo_position = (int(width // 2 - logo_size // 2), int(margin + outer_radius - logo_size // 2))
    composite_image.paste(logo, logo_position, logo)

    # Setup image placeholders
    top_space = margin * 2 + int(outer_radius * flower_scale)
    placeholder_size = (300, 168)
    element_positions = [
        (margin, top_space),
        (margin, top_space + placeholder_size[1] + margin),
        (width - margin - placeholder_size[0], top_space),
        (width - margin - placeholder_size[0], top_space + placeholder_size[1] + margin),
    ]
    image_paths = [path_img1, path_img2, path_img3, path_img4]

    # Insert images into placeholders
    for position, img_path in zip(element_positions, image_paths):
        image = Image.open(img_path).convert("RGBA")
        image = image.resize(placeholder_size)
        composite_image.paste(image, position)

    # Draw table with data from JSON file
    col_widths = [200, 350]
    row_height = 40
    table_top_left_x = (width - sum(col_widths)) // 2
    table_top_left_y = max(pos[1] + placeholder_size[1] for pos in element_positions) + margin
    table_data = load_json_file(filepath)
    draw_table(draw, table_top_left_x, table_top_left_y, table_data, col_widths, row_height, font_path)

    # Save the composite image
    output_path = f'{path_out}/gradient_flowers_composite_image.png'
    composite_image.save(output_path)

    return output_path

def main():
    """
    Main function to create and save the composite image.
    """
    # Paths for images to be placed in the placeholders
    current_directory = os.getcwd()
    path_img1 = f"{current_directory}/images/1.png"
    path_img2 = f"{current_directory}/images/2.png"
    path_img3 = f"{current_directory}/images/3.png"
    path_img4 = f"{current_directory}/images/4.png"
    path_out = current_directory
    logo_path = f"{current_directory}/images/front_image.png"
    font_path = f"{current_directory}/font/Comic Sans MS Bold.ttf"
    filepath = f"{current_directory}/data/data.json"

    # Create the image and print the path
    image_path = create_composite_image_with_gradient(logo_path, path_img1, path_img2, path_img3, path_img4, path_out, font_path, filepath)
    print(f"The image has been saved to: {image_path}")

if __name__ == "__main__":
    main()
