# Recipe List - Solstice by APEERS Hackathon

## Overview

This Python application is a Tkinter-based GUI for managing a list of recipes and their prices. Users can add items to the list, view their total cost, and search for recipes based on the items in the list. The application fetches recipe data from the Edamam API and displays it in a new window.

## Features

- **Add Items:** Enter the name and price of a food item to add it to the recipe list.
- **Remove Items:** Click on an item in the list to remove it.
- **Clear List:** Remove all items from the list with a confirmation prompt.
- **Search Recipes:** Fetch and display recipes based on the items in the list.
- **View Recipe Details:** See recipe details, copy recipe URLs, or open them in a web browser.

## Requirements

- Python 3.x
- `requests` library
- `pyperclip` library
- `Pillow` library
- Internet connection for fetching recipes from the API

## Setup Instructions

1. **Install Dependencies:**

   Ensure you have Python and pip installed. Install the required Python libraries using:

   ```sh
   pip install -r requirements.txt
    mportant Note on API Key:
        Demo API Key: The API key included in the code is for demonstration purposes during this hackathon. It is intended to be used only within the scope of this event.
        Overwhelmed Key: If the provided API key becomes overwhelmed or ceases to function due to high usage, you may need to create a new API key on Edamam. Follow these steps to obtain a new key:
            Go to the Edamam Developer Portal.
            Sign in or create a new account if you don’t have one.
            Navigate to the "API Keys" section and generate a new key.
            Update the API_ID and API_KEY variables in the code with your new key.

Running the Application

To run the application, use:

python recipe-list.py

Releases

    Version 1.0: Download the latest release

    The release includes the compiled application for macOS. Download and unzip the release, and open the .app file to start the application.

Contact

For any questions or issues, please contact mail.hshah10@gmail.com.
