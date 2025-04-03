import cv2
import numpy as np
import os
import moviepy.video.io.ImageSequenceClip as ImageSequenceClip
from rembg import remove  # AI-based background removal

# Input video file
input_video = "PunVHiOxUEk.mp4"

# Directory containing frames
frame_folder = "frames"

# Output video file (choose WebM or MOV)
output_video = "output_video.webm"  # Change to "output_video.mov" if needed

# Create output directory for frames
os.makedirs(frame_folder, exist_ok=True)

def remove_background(frame):
    """Removes the entire background from an image using rembg, handling empty images."""
    # Convert OpenCV BGR image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Avoid division by zero: Ensure image has valid pixel values
    if np.max(frame_rgb) == 0:
        print("Warning: Empty frame detected, skipping background removal.")
        return cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)  # Return original frame with alpha

    # Remove background using rembg
    frame_no_bg = remove(frame_rgb)

    # Ensure no NaN values in the output
    frame_no_bg = np.nan_to_num(frame_no_bg, nan=0, posinf=255, neginf=0).astype(np.uint8)

    return frame_no_bg

# Open the video file
cap = cv2.VideoCapture(input_video)
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Process frame to remove background
    processed_frame = remove_background(frame)

    # Save frame as PNG with transparency
    frame_filename = os.path.join(frame_folder, f"frame_{frame_count:04d}.png")
    cv2.imwrite(frame_filename, cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGRA))

    frame_count += 1

cap.release()
cv2.destroyAllWindows()

print(f"Frames saved in '{frame_folder}'. Now creating the final transparent video...")

# Get sorted frame filenames
frame_files = [os.path.join(frame_folder, f) for f in sorted(os.listdir(frame_folder)) if f.endswith(".png")]

# Ensure there are frames to process
if not frame_files:
    print("No frames found in the 'frames' directory!")
    exit()

# Create a video clip from the image sequence
clip = ImageSequenceClip.ImageSequenceClip(frame_files, fps=30)

# Save as WebM (VP9 supports transparency) or MOV (ProRes)
if output_video.endswith(".webm"):
    clip.write_videofile(output_video, codec="libvpx-vp9")
elif output_video.endswith(".mov"):
    clip.write_videofile(output_video, codec="prores")

print(f"Video saved as {output_video}")
