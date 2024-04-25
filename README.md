
# Composite Image Creator

This Python script generates a composite image featuring a gradient background, decorative flowers, a centered logo, placeholder images, and a table containing data loaded from a JSON file. It's a versatile tool for creating promotional or informational graphics with customized content.

## Features

- Generates a full-size image with gradient background.
- Decorative flowers at predefined positions.
- A central logo.
- Placeholder images at specified positions.
- A data table populated from a JSON file.

## Prerequisites

Before running this script, ensure you have Python installed on your machine. Additionally, the project depends on the following Python libraries:
- Pillow

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://your-repository-url.com
   ```
2. **Navigate to the project directory:**
   ```bash
   cd path_to_directory
   ```
3. **Install required Python packages:**
   ```bash
   pip install Pillow
   ```

## Usage

To use this script, you need to have the image files and a JSON data file in the correct directories. Here's how you can run the script:

1. **Prepare your images and JSON data file:**
   Ensure that your images are placed in the `images` directory and your JSON data is in the `data` directory under the filename `data.json`.

2. **Run the script:**
   ```bash
   python main.py
   ```

   Replace `main.py` with the actual name of your Python script.

3. **View the generated image:**
   The script outputs the composite image in the project's root directory, named `gradient_flowers_composite_image.png`.

## Configuration

- **Image Paths:** Customize the paths of the placeholder images and the logo within the `main()` function.
- **Table Configuration:** Modify the column widths, row height, and font details in the `create_composite_image_with_gradient` function to suit your layout needs.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
