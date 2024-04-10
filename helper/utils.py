from config import DEFAULT_SCRAPE_PAGE_COUNT
import uuid
import datetime
import requests
import pytz
import os
from helper import network_util


def get_date_string():
    # Get the current date and time in IST
    ist = pytz.timezone('Asia/Kolkata')
    current_datetime_ist = datetime.datetime.now(ist)

    # Format the date and time
    formatted_date = current_datetime_ist.strftime("%d-%m-%Y_%H-%M-%S")

    # Combine the date, time, and UUID to form the name
    return formatted_date


def save_data_to_file(data, folder, file_name):
    # Construct the full file path
    file_path = os.path.join(folder, file_name)

    # Save the JSON data to the file
    with open(file_path, "w") as file:
        file.write(data)

    print(f"Data saved to {file_path}")


def save_img(title, folder, image_url):
    image_uuid = str(uuid.uuid4())
    local_file_path = os.path.join(folder, f"{title}_{image_uuid}.jpg")
    response = network_util.make_request(image_url, None, stream=True)
    if response.status_code == 200:
        with open(local_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)
        return os.path.abspath(local_file_path)
    return None


def ensure_folder_exists(folder_path):
    """
    Ensures that the specified folder exists, creating it if necessary.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
