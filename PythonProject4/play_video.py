import cv2
import screeninfo


def play_video(video_path, speed_factor=1.0, target_width=640):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get the original frames per second (FPS)
    fps = cap.get(cv2.CAP_PROP_FPS)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    aspect_ratio = width / height;
    target_height = int(target_width / aspect_ratio)

    screen = screeninfo.get_monitors()[0]
    x = screen.width - target_width - 20
    y = screen.height - target_height - 90

    # Loop through the video frames
    window_name = "fruit"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # Remove borders
    cv2.resizeWindow(window_name, target_width, target_height)  # Keep custom size
    cv2.moveWindow(window_name, x, y)  # Move to bottom-right

    while True:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video from the beginning
        while True:
            ret, frame = cap.read()

            if not ret:
                break  # End of video (this case should not occur as we reset the frame)

            # Display the frame in an OpenCV window
            frame_resized = cv2.resize(frame, (target_width, target_height))
            cv2.imshow("fruit", frame_resized)

            # Adjust the wait time to control playback speed
            # Speed factor > 1.0 slows the video down, < 1.0 speeds it up
            wait_time = int(1000 / (fps * speed_factor))

            # Break the loop if the user presses 'q'
            if cv2.waitKey(wait_time) & 0xFF == ord(' '):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video from the beginning
                break

    cap.release()
    cv2.destroyAllWindows()


# Path to your video file (MP4)
video_path = "C:/Users/16142/Downloads/peas better - Made with Clipchamp.mp4"

# Set speed factor: 1.0 for normal speed, 0.5 for half speed, 2.0 for double speed, etc.
speed_factor = 3  # Change this to adjust speed (e.g., 0.5 for slower, 2.0 for faster)
target_width = 700

# Play the video with adjusted speed
play_video(video_path, speed_factor, target_width)
