"""
process_image.py

This script processes a map image by plotting points based on latitude and longitude data extracted from JSON files.
Each point represents the geolocation of an IP address. The script reads JSON files from a specified directory,
converts latitude and longitude data to pixel coordinates, and plots these coordinates as white dots on the map image.
The processed image is then saved to a specified output path.

Author: Daryl Allen
"""

import json
import os
from PIL import Image, ImageDraw

def lat_long_to_pixels(latitude, longitude, img_width=850, img_height=425):
    """
    Convert latitude and longitude to pixel coordinates on the map image.

    :param latitude: Latitude of the point.
    :param longitude: Longitude of the point.
    :param img_width: Width of the map image in pixels.
    :param img_height: Height of the map image in pixels.
    :return: Pixel coordinates (x, y) on the map image.
    """
    lines_per_pixel_x = 360 / img_width
    lines_per_pixel_y = 180 / img_height

    x_pixel = round((longitude + 180) / lines_per_pixel_x)

    # Invert the y-coordinate so that lower latitudes are higher on the image
    y_pixel = img_height - round((latitude + 90) / lines_per_pixel_y)

    return x_pixel, y_pixel

def process_image(api_results_dir, base_image_path, output_image_path):
    """
    Process the map image by plotting points from latitude and longitude data in JSON files.

    :param api_results_dir: Directory containing JSON files with latitude and longitude data.
    :param base_image_path: Path to the base map image.
    :param output_image_path: Path to save the processed map image.
    """
    image = Image.open(base_image_path)
    draw = ImageDraw.Draw(image)

    for filename in os.listdir(api_results_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(api_results_dir, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                latitude = data.get('latitude')
                longitude = data.get('longitude')
                if latitude is not None and longitude is not None:
                    x, y = lat_long_to_pixels(latitude, longitude)
                    # Plot the point as a white dot
                    draw.ellipse((x-2, y-2, x+2, y+2), fill='white', outline='white')

    image.save(output_image_path)


# Define paths for the input and output
api_results_dir = '/home/daryl/PycharmProjects/gpu_processing_tests/sub_projects/api_results'
base_image_path = '/home/daryl/PycharmProjects/gpu_processing_tests/sub_projects/processed_image.jpg'
output_image_path = '/home/daryl/PycharmProjects/gpu_processing_tests/sub_projects/processed_image_with_dots.jpg'

# Process the image by plotting points from JSON data
process_image(api_results_dir, base_image_path, output_image_path)
