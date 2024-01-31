import os

from pages.Window import Window


def main():
    # Get a list of all files in the current directory
    files = os.listdir()

    # Iterate over all files
    for file in files:
        # If the file name contains the specific string
        if ".jpg" in file or ".wav" in file:
            # Delete the file
            os.remove(file)

    window = Window()
    window.start()


if __name__ == "__main__":
    main()
