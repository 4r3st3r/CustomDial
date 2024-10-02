import network
import time
import urequests
from machine import Pin, PWM

# Wi-Fi and API Constants
SSID = 'TEST'
PASSWORD = 'TEST'
API_KEY = "KEY"
API_SECTION = "politics_us_presidential_election_winner"
API_URL = f"https://api.the-odds-api.com/v4/sports/{API_SECTION}/odds/?apiKey={API_KEY}&regions=us"

# Hardware Setup
led = Pin('LED', Pin.OUT)  # LED indicator
servoPin = PWM(Pin(15))  # Servo pin setup
servoPin.freq(50)  # Servo frequency

def connect_wifi(ssid, password):
    """
    Connect to Wi-Fi using provided SSID and password.
    Will try for 15 seconds before terminating if it cannot connect.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    connection_count = 0
    while not wlan.isconnected():
        time.sleep(1)
        connection_count += 1
        print("Waiting for Wi-Fi connection...")
        
        if connection_count > 15:  # Timeout after 15 seconds
            print("Could not connect to Wi-Fi, terminating program...")
            exit()

    print("Connected to Wi-Fi")
    return wlan

def fetch_api_data(url):
    """
    Fetch JSON data from the provided API URL.
    Returns the first element of the response if successful.
    """
    try:
        response = urequests.get(url)
        data = response.json()
        return data[0]  # First entry in the response data
    except Exception as e:
        print(f"Error fetching API data: {e}")
        return None

def extract_candidates(json_data):
    """
    Extract the odds (prices) for Kamala Harris and Donald Trump from the API JSON data.
    Returns a dictionary of candidate names and their prices.
    """
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
    """
    Convert the decimal odds of each candidate into implied probabilities
    and normalize them to a percentage (0-100%).
    """
    implied_probabilities = {name: 1 / price for name, price in candidates.items()}
    total_probability = sum(implied_probabilities.values())
    normalized_probabilities = {name: (prob / total_probability) * 100 for name, prob in implied_probabilities.items()}
    
    return normalized_probabilities

def servo(degrees):
    """
    Move the servo to a specified degree (0-180).
    Degrees are clamped between 0 and 180.
    """
    degrees = max(0, min(180, degrees))  # Clamp degrees
    maxDuty = 8550
    minDuty = 1750
    newDuty = minDuty + (maxDuty - minDuty) * (degrees / 180)
    servoPin.duty_u16(int(newDuty))
    return True

def map_probability_to_dial(chance_to_win, min_prob=45, max_prob=55, dial_min_degrees=0, dial_max_degrees=180):
    """
    Map Harris' chance to win from the range (min_prob, max_prob) to the full dial range (0-180 degrees).
    Ensures that the chance stays within the expected range (45-55%).
    """
    # Clamp the probability within the defined range (45%-55%)
    if chance_to_win < min_prob:
        chance_to_win = min_prob
    elif chance_to_win > max_prob:
        chance_to_win = max_prob
    
    # Map the probability to the dial degrees (0-180)
    mapped_position = dial_min_degrees + ((chance_to_win - min_prob) / (max_prob - min_prob)) * (dial_max_degrees - dial_min_degrees)

    # Swap the degrees, to account for the fact that the servo measures from the other end
    mapped_position = 180 - mapped_position
    
    return mapped_position

def startup():
    """
    On startup, rotate the servo through several positions to indicate
    the system is working and ready.
    """
    for i in range(11):
        servo(i * (180 / 11))
        time.sleep(0.2)
    
    return True

def main():
    """
    Main execution flow:
    - Connect to Wi-Fi
    - Fetch API data for the presidential odds
    - Calculate probabilities and move the servo to reflect Kamala Harris' chance to win
    """
    # Step 1: Connect to Wi-Fi
    connect_wifi(SSID, PASSWORD)

    # Step 2: Fetch data from the API
    json_data = fetch_api_data(API_URL)
    
    if json_data:
        # Step 3: Extract candidate odds
        candidates = extract_candidates(json_data)
        
        if 'Kamala Harris' in candidates:
            # Step 4: Calculate normalized probabilities
            normalized_probabilities = calculate_normalized_probabilities(candidates)

            # Step 5: Get Harris' chance to win and map it to the dial
            harris_chance_to_win = normalized_probabilities.get('Kamala Harris', 0)
            dial_position = map_probability_to_dial(harris_chance_to_win)

            # Step 6: Move the servo to the calculated dial position
            servo(dial_position)
            print(f"Dial should be at: {dial_position:.2f} degrees, Harris chance to win: {harris_chance_to_win:.2f}%")

        else:
            print("Kamala Harris data not found.")
    else:
        print("No data fetched from API.")

if __name__ == "__main__":
    startup()  # Start the system with a startup movement
    
    while True:
        main()     # Run the main program
        time.sleep(60 * 60 * 8) # Sleep for 4 hours
