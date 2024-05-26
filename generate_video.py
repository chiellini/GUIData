import cv2
import os
import glob

image_folder = r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\Documents\02paper cunmin segmentation\segmentation results\PNGS\combined_Membrane'
video_name = r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\Documents\02paper cunmin segmentation\segmentation results\PNGS\combined_Membrane\video.mp4'
IS_FLIPPED_MIRROR=False

# images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
images=glob.glob(os.path.join(image_folder,'*.png'))

# STOP_FRAME=int(len(images)*(4/5))

# print(images[:44])
# frame = cv2.imread(os.path.join(image_folder, images[0]))
frame = cv2.imread(images[0])

height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0x7634706d, 10, (width,height))

for image in images:
    if IS_FLIPPED_MIRROR:
        video.write(cv2.flip(cv2.imread(os.path.join(image_folder, image)),1))

    else:
        video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()