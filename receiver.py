import requests
import time
import threading

def fetch_and_filter_adsb_data(callback):
    url = "https://api.adsb.lol/v2/point/28.42524/-81.30850/5"

    while True:
        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                filtered_data = []
                for aircraft in data.get('ac', []):
                    alt_baro = aircraft.get('alt_baro')
                    if alt_baro == 'ground' or (isinstance(alt_baro, int) and alt_baro <= 500):
                        filtered_data.append(aircraft)

                # Send the filtered data to the callback function
                if callback:
                    callback(filtered_data)

            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")

            time.sleep(1)  # Update interval set to 1 second

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            time.sleep(1)  # Shorter sleep duration to retry sooner

def start_receiving_data(callback):
    # Run data fetching in a separate thread to avoid blocking
    thread = threading.Thread(target=fetch_and_filter_adsb_data, args=(callback,))
    thread.daemon = True  # Ensure the thread exits when the main program exits
    thread.start()
