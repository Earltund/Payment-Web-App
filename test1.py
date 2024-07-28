import requests
import csv
import json
import os

# Replace 'your_secret_key' with your actual Paystack secret key
paystack_secret_key = 'sk_test_d9614e43d32f4a71b4d0097a4fb62c125d5f3ba7'
api_base_url = 'https://api.paystack.co/'


def get_transactions():
    # Specify the endpoint for getting transactions
    endpoint = 'transaction'

    # Construct the full URL
    url = api_base_url + endpoint

    # Set up headers with the secret key
    headers = {
        'Authorization': f'Bearer {paystack_secret_key}',
        'Content-Type': 'application/json',
    }

    # Set up parameters for the request (optional)
    params = {
        'status': 'success',  # You can customize this based on your requirements
    }

    # Make the API request
    try:
        response = requests.get(url, headers=headers, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            transactions = response.json()['data']
            return transactions
            
        else:
            print(f"Error: {response.status_code}, {response.json()}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    
def save_to_json(data, output_folder, output_filename='transactions.json'):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Construct the output file path
    output_path = os.path.join(output_folder, output_filename)

    # Write data to JSON file
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

    print(f"Data saved to {output_path}")


def json_to_csv(transactions, csv_file):
    # Open the CSV file in write mode
    with open(csv_file, 'w', newline='') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)

        # Write the header using the keys from the first JSON object
        header_written = False
        for item in transactions:
            if not header_written:
                csv_writer.writerow(item.keys())
                header_written = True

            # Write each row of data
            csv_writer.writerow(item.values())


if __name__ == '__main__':
    transactions = get_transactions()

    if transactions:
        print("Transactions:")
        for transaction in transactions:
            print(transaction)
         # Replace 'your_output_folder' with the desired output folder path
    output_folder = '/Users/ASUS/Documents/409'

    

    if transactions:
        save_to_json(transactions, output_folder)
    else:
        print("Failed to retrieve transactions.")
  
  # Replace 'your_json_data.json' with the path to your JSON file
    json_file_path = 'transactions.json'
    
    # Replace 'output.csv' with the desired output CSV file path
    csv_output_path = 'output.csv'

    try:
        with open(json_file_path, 'r') as jsonfile:
            # Load JSON data
            json_data = json.load(jsonfile)

            # Convert JSON to CSV
            json_to_csv(json_data, csv_output_path)

        print(f"Conversion successful. CSV file saved at {csv_output_path}")

    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' does not exist.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
