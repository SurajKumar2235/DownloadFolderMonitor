import time
import shutil
import os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from plyer import notification
from dotenv import load_dotenv  # Import the load_dotenv function

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    filename="file_mover.log",  # Log file
    level=logging.INFO,         # Log level
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log format
)

class FileHandler(FileSystemEventHandler):
    def __init__(self, source_folder, destination_folder):
        self.source_folder = source_folder
        self.destination_folder = destination_folder

    def on_created(self, event):
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            dest_path = os.path.join(self.destination_folder, file_name)

            try:
                # Move the file
                shutil.move(event.src_path, dest_path)
                logging.info(f"Moved {file_name} from {self.source_folder} to {self.destination_folder}")
                
                # Send a notification
                notification.notify(
                    title="File Moved",
                    message=f"{file_name} has been moved to {self.destination_folder}",
                    timeout=5
                )
            except Exception as e:
                logging.error(f"Failed to move {file_name}: {str(e)}")
                notification.notify(
                    title="Error Moving File",
                    message=f"Failed to move {file_name}. Check logs for details.",
                    timeout=5
                )

def monitor_folder(source_folder, destination_folder):
    event_handler = FileHandler(source_folder, destination_folder)
    observer = Observer()
    observer.schedule(event_handler, path=source_folder, recursive=False)
    observer.start()
    logging.info(f"Started monitoring folder: {source_folder}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Stopping folder monitoring...")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # Load environment variables
    source_folder = os.getenv("SOURCE_FOLDER")
    destination_folder = os.getenv("DESTINATION_FOLDER")

    logging.info("File mover script started")
    monitor_folder(source_folder, destination_folder)
