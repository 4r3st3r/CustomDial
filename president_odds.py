import network
import time
import urequests
from machine import Pin, PWM

# Constants
SSID = 'TEST'
PASSWORD = 'TEST'
API_KEY = "KEY"
API_SECTION = "politics_us_presidential_election_winner"
API_URL = f"https://api.the-odds-api.com/v4/sports/{API_SECTION}/odds/?apiKey={API_KEY}&regions=us"

# Initialize components
led = Pin('LED', Pin.OUT)
servoPin = PWM(Pin(15))
servoPin.freq(50)

def connect_wifi(ssid, password):
    """Connect to Wi-Fi."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    # Wait for connection
    while not wlan.isconnected():
        time.sleep(1)
        print("Waiting for Wi-Fi connection...")
    
    print("Connected to Wi-Fi")
    return wlan

def fetch_api_data(url):
    """Fetch JSON data from the API."""
    try:
        response = urequests.get(url)
        data = response.json()
        return data[0]  # Extract the first element of the response
    except Exception as e:
        print(f"Error fetching API data: {e}")
        return None

def extract_candidates(json_data):
    """Extract prices for Kamala Harris and Donald Trump from the API JSON."""
    candidates = {}
    try:
        outcomes = json_data.get('bookmakers')[0].get('markets')[0].get('outcomes')
        for candidate in outcomes:
            if candidate.get('name') in ['Kamala Harris', 'Donald Trump']:
                candidates[candidate.get('name')] = candidate.get('price')
    except Exception as e:
        print(f"Error extracting candidate data: {e}")
    
    return candidates

def calculate_normalized_probabilities(candidates):
    """Calculate and normalize probabilities based on decimal odds."""
    implied_probabilities = {name: 1 / price for name, price in candidates.items()}
    total_probability = sum(implied_probabilities.values())
    normalized_probabilities = {name: (prob / total_probability) * 100 for name, prob in implied_probabilities.items()}
    return normalized_probabilities

def servo(degrees):
    """Control the servo position based on degrees (0-180)."""
    degrees = max(0, min(180, degrees))  # Clamp the degrees between 0 and 180
    maxDuty = 8080
    minDuty = 2201
    newDuty = minDuty + (maxDuty - minDuty) * (degrees / 180)
    servoPin.duty_u16(int(newDuty))

def main():
    # Connect to Wi-Fi
    connect_wifi(SSID, PASSWORD)

    # Fetch API data
    json_data = fetch_api_data(API_URL)
    
    if json_data:
        # Extract candidate odds
        candidates = extract_candidates(json_data)
        
        if 'Donald Trump' in candidates:
            # Calculate normalized probabilities
            normalized_probabilities = calculate_normalized_probabilities(candidates)

            # Get Trump's chance to win
            trump_chance_to_win = normalized_probabilities.get('Donald Trump', 0)

            # Define the max size of the dial in degrees (0-180)
            dial_max_degrees = 180

            # Calculate the dial position based on Trump's probability
            dial_position = dial_max_degrees * (trump_chance_to_win / 100)

            # Move the servo to the correct position
            servo(dial_position)
            print(f"Dial should be at: {dial_position:.2f} degrees")

        else:
            print("Donald Trump data not found.")

if __name__ == "__main__":
    main()
