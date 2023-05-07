import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image

# Function to separate images in TIFF file
def separate_tiff_frames(file_path):
    print("Separating frames...")
    # Open the multi-frame TIFF file
    tiff_image = Image.open(file_path)
    
    # Get the number of frames in the TIFF file
    num_frames = tiff_image.n_frames
    
    # Create an empty list to store the separated frames
    frames = []
    
    # Iterate over each frame and extract it as a PIL image
    for i in range(num_frames):
        tiff_image.seek(i)
        frame = tiff_image.copy()
        frames.append(frame)
    
    return frames

# Function to analyze individual image and calculate area of each gel
def analyze_image(image):
    thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    areas = []
    for contour in contours:
        area = cv2.contourArea(contour)
        areas.append(area)
    binary_image = np.zeros_like(thresh)
    cv2.drawContours(binary_image, contours, -1, 255, -1)
    return binary_image

def plot_area_vs_time(images):
    initial_image = images[0]
    percentage_changes = []
    for i in range(len(images)):
        diagonal = np.diag(images[i, :, :])
        diagonal_max = np.max(diagonal)
        diagonal_min = np.min(diagonal)
        percentage_change = ((diagonal_max - diagonal_min) / np.sum(initial_image)) * 100
        percentage_changes.append(percentage_change)
        
    fig, ax = plt.subplots()
    ax.plot(np.arange(len(percentage_changes)) * 0.5, percentage_changes)
    ax.set_xlabel('Time (in hours)')
    ax.set_ylabel('Percentage change in area (L/Lo)')
    ax.set_title('Percentage change in hydrogel area vs time')
    plt.show()

# Function to combine individual images to make a video that shows changes over time
def create_video(images, output_file):
    height, width = images.shape[1:]
    fourcc = cv2.VideoWriter_fourcc(*'h264')
    video_writer = cv2.VideoWriter(output_file, fourcc, 1, (width, height), isColor=False)
    for i in range(images.shape[0]):
        video_writer.write(cv2.cvtColor(images[i, :, :], cv2.COLOR_GRAY2BGR))
    video_writer.release()
    
def main():
    file_path = "Gel10.tif" # Replace with the desired output file path
    frames = separate_tiff_frames(file_path)
    if not frames:
        print("Error: No frames were found in the TIFF file.")
        return
    images = np.array([np.array(frame) for frame in frames])
    binary_images = np.array([analyze_image(image) for image in images])
    plot_area_vs_time(binary_images)
    create_video(images, 'Gel10_video.mp4')

if __name__ == '__main__':
    main()