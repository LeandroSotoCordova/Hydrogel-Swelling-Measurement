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

def analyze_images(images):
    areas = [] # initialize an empty list to store the calculated areas

    # loop through all images in the list
    for i in range(len(images)):
        # Get contours and calculate areas
        contours, _ = cv2.findContours(images[i], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # find the contours in the binary image and calculate the area of each contour
        area_sum = 0 # initialize the area sum to zero
        for contour in contours: 
            area_sum += cv2.contourArea(contour) # add the area of each contour to the area sum
        areas.append(area_sum) # add the area sum to the list of areas

    # Calculate percentage change in area relative to initial area
    initial_area = areas[0] # get the area of the initial image
    percentage_changes = [(area / initial_area) * 100 for area in areas] # calculate the percentage change in area relative to the initial area for each image

    # Plot results
    fig, ax = plt.subplots() # create a new figure and axis object
    ax.plot(np.arange(len(percentage_changes)) * 0.5, percentage_changes) # plot the percentage changes over time
    ax.set_xlabel('Time (in hours)') # set the x-axis label
    ax.set_ylabel('Percentage change in area (relative to initial area)') # set the y-axis label
    ax.set_title('Percentage change in hydrogel area vs time') # set the plot title
    plt.show() # display the plot

    # Return average min and max values of binary images
    min_values = [] # initialize an empty list to store the minimum pixel values
    max_values = [] # initialize an empty list to store the maximum pixel values
    for i in range(len(images)):
        min_value = np.min(images[i]) # get the minimum pixel value in the binary image
        max_value = np.max(images[i]) # get the maximum pixel value in the binary image
        min_values.append(min_value) # add the minimum pixel value to the list of minimum values
        max_values.append(max_value) # add the maximum pixel value to the list of maximum values
    avg_min_value = np.mean(min_values) # calculate the average of the minimum pixel values
    avg_max_value = np.mean(max_values) # calculate the average of the maximum pixel values
    return avg_min_value, avg_max_value # return the average minimum and maximum pixel values


# Function to combine individual images to make a video that shows changes over time
def create_video(images, output_file):
    # Get the height and width of the images
    height, width = images.shape[1:]

    # Specify the codec and create a VideoWriter object to write the video file
    fourcc = cv2.VideoWriter_fourcc(*'h264')
    video_writer = cv2.VideoWriter(output_file, fourcc, 1, (width, height), isColor=False)

    # Loop over each image and write it to the video file
    for i in range(images.shape[0]):
        # Convert the image from grayscale to BGR color format, since VideoWriter expects BGR format
        video_writer.write(cv2.cvtColor(images[i, :, :], cv2.COLOR_GRAY2BGR))

    # Release the VideoWriter object
    video_writer.release()

    
def main():
    file_path = "Gel10.tif" # Replace with the desired output file path
    frames = separate_tiff_frames(file_path)
    if not frames:
        print("Error: No frames were found in the TIFF file.")
        return
    images = np.array([np.array(frame) for frame in frames])
    avg_min_value, avg_max_value = analyze_images(images)
    print("Average minimum value: ", avg_min_value)
    print("Average maximum value: ", avg_max_value)
    create_video(images, 'Gel10_video.mp4')

if __name__ == '__main__':
    main()