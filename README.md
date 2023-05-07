# Hydrogel-Swelling-Measurement
This Python script analyzes multi-frame TIFF images of hydrogels to determine the change in area over time. It separates individual frames from the TIFF file, processes them to calculate the area of each gel, and then creates a video that shows the changes in the gel area over time.

# Requirements
- numpy
- opencv-python
- matplotlib
- pillow

# Usage
1. Save the hydrogel images in a multi-frame TIFF file with the desired name (e.g., "Gel10.tif").
2. Update the file_path variable in the main() function with the path to the TIFF file.
3. Run the script.

The script will generate a video file named "Gel10_video.mp4" that shows the changes in the hydrogel area over time. The video will be saved in the same directory as the script.

Note: If the TIFF file contains no frames, an error message will be displayed.
