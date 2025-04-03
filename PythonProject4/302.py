import cv2
import os


def speed_up_video(input_path, output_path, speed_factor=1.9999):
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get original video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Set up video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps * speed_factor, (width, height))

    frame_skip = int(speed_factor)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Write every nth frame based on speed factor
        if frame_count % frame_skip == 0:
            out.write(frame)
        frame_count += 1

    cap.release()
    out.release()
    print(f"Video saved at: {output_path}")


# Get user input for file path
input_path = "C:/Users/16142/Downloads/peas better - Made with Clipchamp.mp4"
out_dir = os.path.dirname(input_path)
output_path = os.path.join(out_dir, "output_2.1111x.mp4")

# Process video
speed_up_video(input_path, output_path)
