import os

def load_css_files(directory):
    """
    Load CSS files from a specified directory and return them as a list.

    Parameters:
    - directory (str): The directory path containing CSS files.

    Returns:
    - list: A list of CSS file paths.
    """
    css_files = []
    # Check if the directory exists
    if os.path.exists(directory):
        # Iterate over files in the directory
        for file in os.listdir(directory):
            # Check if the file is a CSS file
            if file.endswith(".css"):
                # Construct the file path and add it to the list
                css_files.append(os.path.join("/assets", os.path.relpath(os.path.join(directory, file), 'assets')))
    else:
        print(f"Directory '{directory}' does not exist.")

    return css_files