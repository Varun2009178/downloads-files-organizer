import os
import shutil
import logging
import time
import threading
import sys

# Path to the Downloads folder
downloads_path = os.path.join(os.environ['HOME'], 'Downloads')
contents = os.listdir(downloads_path)

# Set up logging
logging.basicConfig(filename='file_organizer.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelnames)s - %(message)s')

# Function to categorize and move files
def categorize_file(downloads_path, file_name):
    extension = os.path.splitext(file_name)[1].lower()
    
    # Define paths for different file categories
    image_path = os.path.join(downloads_path, "Images")
    doc_path = os.path.join(downloads_path, "Documents")
    audio_path = os.path.join(downloads_path, "Audio")
    video_path = os.path.join(downloads_path, "Videos")
    other_path = os.path.join(downloads_path, "Other")

    # Create the appropriate folder if it doesn't exist
    if extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        target_path = image_path
    elif extension in ['.doc', '.docx', '.pdf', '.txt', '.rtf']:
        target_path = doc_path
    elif extension in ['.mp3', '.wav', '.ogg', '.flac']:
        target_path = audio_path
    elif extension in ['.mp4', '.avi', '.mkv', '.mov', '.wmv']:
        target_path = video_path
    else:
        target_path = other_path
    
    # Ensure the target folder exists
    if not os.path.isdir(target_path):
        os.makedirs(target_path, exist_ok=True)
    
    # Define the complete path for the file
    complete_path = os.path.join(downloads_path, file_name)
    destination = os.path.join(target_path, file_name)
    
    # Move the file to the appropriate folder
    shutil.move(complete_path, destination)
    logging.info(f"Moved {file_name} from {complete_path} to {destination}")
    print(f"Moved {file_name} to {target_path}")

# Function to display a loading animation in the terminal
def loading_animation():
    spinner = ['|', '/', '-', '\\']
    idx = 0
    print("Files being processed... ", end="")
    
    while True:
        # Overwrite the spinner and message
        sys.stdout.write(f"\rFiles being processed... {spinner[idx]}")
        sys.stdout.flush()
        idx = (idx + 1) % len(spinner)  # Cycle through spinner states
        time.sleep(0.2)

# Main loop to process each file in the directory
def main():
    files_processed = 0
    loading_thread = threading.Thread(target=loading_animation)  # Run the spinner in a separate thread
    loading_thread.daemon = True  # Allow the thread to exit when the program exits
    loading_thread.start()

    for i in contents:
        complete_path = os.path.join(downloads_path, i)
        if os.path.isfile(complete_path):
            categorize_file(downloads_path, i)
            files_processed += 1
    
    print("\nProcessing complete!")
    print(f"Total files processed: {files_processed}")

# Running the main function
if __name__ == "__main__":
    main()
