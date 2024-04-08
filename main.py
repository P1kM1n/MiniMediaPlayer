import os
import pygame
import sys
import imageio
import logging

# Configure logging to output to the console
logging.basicConfig(level=logging.DEBUG)


def load_media(folder_path):
    # Get a list of all files in the specified folder
    files = os.listdir(folder_path)
    # Filter for media files (gif, image, mp4)
    media_files = [f for f in files if f.endswith(('.gif', '.png', '.jpg', '.jpeg', '.mp4'))]
    return media_files


def main(folder_path):
    # Initialize pygame
    pygame.init()

    # Load media files from the specified folder
    media_files = load_media(folder_path)

    # Check if any media files were found
    if not media_files:
        logging.error("No media files found in the specified folder.")
        return

    # Load the first media file
    current_media_index = 0
    current_media_file = os.path.join(folder_path, media_files[current_media_index])

    # Check if the file is a GIF
    is_gif = current_media_file.endswith('.gif')

    if is_gif:
        # Load the GIF using imageio
        gif_reader = imageio.get_reader(current_media_file)
        # Get the size of the first frame
        first_frame = gif_reader.get_next_data()
        frame_size = first_frame.shape[1], first_frame.shape[0]
        gif_frames = [pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB") for frame in gif_reader]
        total_frames = len(gif_frames)
        current_frame = 0
        media_size = frame_size
    else:
        # Load other types of media using pygame
        media = pygame.image.load(current_media_file)
        media_size = media.get_size()

    # Set the window size based on the dimensions of the loaded media
    screen = pygame.display.set_mode(media_size, pygame.RESIZABLE)

    logging.info(f"Loaded media: {current_media_file}, Size: {media_size}")

    # Set up the clock to control the frame rate
    clock = pygame.time.Clock()

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check for triple-click
                if event.button == 1 and event.clicks == 3:
                    running = False
            elif event.type == pygame.VIDEORESIZE:
                # Update the screen size to match the new window size
                screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)

        # Clear the screen
        screen.fill((0, 0, 0))

        # Check if the media is a GIF
        if is_gif:
            # Display the current frame of the GIF
            screen.blit(pygame.transform.scale(gif_frames[current_frame], screen.get_size()), (0, 0))
            # Move to the next frame
            current_frame = (current_frame + 1) % total_frames
        else:
            # Blit the current media onto the screen
            screen.blit(pygame.transform.scale(media, screen.get_size()), (0, 0))

        # Update the display
        pygame.display.flip()

        # Delay to control frame rate
        clock.tick(30)  # Adjust the value to control the frame rate

    # Quit pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # Specify the folder to monitor
    folder_path = "/My Friend Pedro - 20220120231057.png"
    main(folder_path)
