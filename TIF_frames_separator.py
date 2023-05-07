from PIL import Image
import os

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

frames = separate_tiff_frames("Am-BIS-DNA Swelling 4-26-2023_1_MMStack_Pos0.tif")

print("Creating new folder..")
# Create a new folder to save the frames
if not os.path.exists("frames1"):
    os.makedirs("frames1")

print("Saving Images..")
# Save each frame as an individual image file
for i, frame in enumerate(frames):
    frame.save(f"frames1/frame_{i}.png")

print("Done")
#%%

# import os
# import imagej
# import numpy as np
# from PIL import Image

# #os.environ["JRE_HOME"] ="C:/Program Files/Java/jdk-20"

# def separate_tiff_frames(file_path):
#     print("Separating frames...")
#     # Start an ImageJ instance
#     ij = imagej.init()

#     # Open the multi-frame TIFF file in ImageJ
#     with ij.handle().context as ctx:
#         dataset = ctx.dataset().open(file_path)

#     # Extract the individual frames
#     frames = []
#     for i in range(dataset.numDimensions()):
#         frame = dataset.getPlane(i+1)
#         # Convert the frame from ImageJ's native format to a PIL Image
#         frame = Image.fromarray(np.uint8(frame))
#         frames.append(frame)

#     # Close the ImageJ instance
#     ij.dispose()

#     return frames

# frames = separate_tiff_frames("Am-BIS-DNA Swelling 4-26-2023_1_MMStack_Pos1.tif")

# print("Creating new folder..")
# # Create a new folder to save the frames
# if not os.path.exists("frames"):
#     os.makedirs("frames")

# print("Saving Images..")
# # Save each frame as an individual image file
# for i, frame in enumerate(frames):
#     frame.save(f"frames/frame_{i}.png")

# print("Done")
#%%
# from PIL import Image
# import os

# def separate_tiff_frames(file_path):
#     print("Separating frames...")
#     # Open the multi-frame TIFF file
#     tiff_image = Image.open(file_path)

#     # Get the number of frames in the TIFF file
#     num_frames = tiff_image.n_frames

#     # Create an empty list to store the separated frames
#     frames = []

#     # Iterate over each frame and extract it as a PIL image
#     for i in range(num_frames):
#         tiff_image.seek(i)
#         frame = tiff_image.copy()
        
#         # Convert the frame to a BMP image
#         bmp_frame = Image.new("RGB", frame.size, (255, 255, 255))
#         bmp_frame.paste(frame)
        
#         frames.append(bmp_frame)

#     return frames

# frames = separate_tiff_frames("Am-BIS-DNA Swelling 4-26-2023_1_MMStack_Pos1.tif")

# print("Creating new folder..")
# # Create a new folder to save the frames
# if not os.path.exists("framesBMP"):
#     os.makedirs("framesBMP")

# print("Saving Images..")
# # Save each frame as an individual image file
# for i, frame in enumerate(frames):
#     frame.save(f"framesBMP/frame_{i}.png")

# print("Done")
#%%
'''WORKS: Merge BMP images into a TIF file'''
# import imageio.v2 as imageio
# import os

# folder_path = "C:\\Users\\Leo\\Downloads\\BMP IMAGES" # Replace with the path to your folder
# file_names = sorted(os.listdir(folder_path)) # Get a sorted list of all file names in the folder

# images = [] # A list to hold all of the images

# for file_name in file_names:
#     if file_name.endswith(".bmp"): # Only process BMP files
#         file_path = os.path.join(folder_path, file_name) # Get the full path to the file
#         image = imageio.imread(file_path) # Read the image with imageio
#         images.append(image) # Add the image to the list

# output_path = "output_file.tif" # Replace with the desired output file path
# imageio.mimwrite(output_path, images) # Combine all images into a single TIFF file
