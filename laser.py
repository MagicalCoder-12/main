from PIL import Image

# File paths
red_laser_path = "D:/programs/pygame/Space/main/Assets/pixel_laser_red.png"
new_laser_path = "D:/programs/pygame/Space/main/Assets/pixel_laser_purple.png"

# Load the original image
try:
    red_laser_img = Image.open(red_laser_path)
except FileNotFoundError:
    print("Error: The specified image file does not exist.")
    exit()

# Define the threshold for red color detection
red_threshold = 100

# Change the color of the image (e.g., from red to purple)
purple_laser_img = red_laser_img.convert("RGBA")
data = purple_laser_img.getdata()
new_data = []
color_changed = False  # Flag to track if color change is successful

for item in data:
    # Check if the pixel is close to red
    if item[0] > red_threshold and item[1] < red_threshold and item[2] < red_threshold:
        # Change red pixels to purple
        new_data.append((128, 0, 128, item[3]))  # Use RGBA tuple
        color_changed = True  # Set flag to True indicating successful color change
    else:
        new_data.append(item)

if color_changed:
    # Create a new image with modified data
    purple_laser_img.putdata(new_data)

    # Save the modified image
    try:
        purple_laser_img.save(new_laser_path)
        print("Success: Color changed successfully.")
    except Exception as e:
        print(f"Error: Unable to save the modified image. {e}")
else:
    print("Error: The specified color (red) was not found in the original image.")
