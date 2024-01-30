import os
import sys

from pages.Window import Window

# Create in-memory SQLite database
# conn = sqlite3.connect(':memory:')
# c = conn.cursor()
# c.execute('''CREATE TABLE users
#              (username text, voice_sample text, photo text)''')


def main():
    # Get a list of all files in the current directory
    files = os.listdir()

    # Iterate over all files
    for file in files:
        print(file)
        # If the file name contains the specific string
        if "voice_sample" in file or "opencv_frame" in file:
            # Delete the file
            os.remove(file)

    window = Window()
    window.start()


if __name__ == "__main__":
    main()