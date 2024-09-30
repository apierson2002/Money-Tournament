# HEADER#########################################################################
# ANDREW PIERSON's TEMPERATURE SENSOR PROGRAM
# FILENAME: temp5.py    #do not change (for startup service)
# DATE: 7/20/2024
# DESCRIPTION: This python script uses glob api to measure the
#               temperature of the walk-in cooler at the Shoals Shack. The
#               sensor is connected to a Raspberry Pi that uses the request api
#               to send a text to boss.
#
# Order some food here: www.theshoalsshack.com
#
# CODE##########################################
import os
import glob
import time
import requests
import random
import json



# Send text message
def send_text(phone, key, message):
    resp = requests.post('https://textbelt.com/text', {
        'phone': phone,
        'message': message,
        'key': key,
    })
    data = resp.json()
    return data

# Function to construct text messages
def text_builder(message_type, temp_f=None, quota=None, tempset=None):
    if message_type == 'high_temp':
        return f'Coach Bj, the walk-in is above {tempset}°F.\nTemp is: {temp_f}°F'
    elif message_type == 'still_high_temp':
        return f'It has been 20 minutes and the temperature is still {temp_f}°F!\n\nSomething could be wrong!!!'
    elif message_type == 'temp_normal':
        return f'The walk-in cooler is back to normal :) Temp: {temp_f}°F\nText quota remaining: {quota}'
    else:
        return 'Unknown message type'

contacts_file = 'contacts.json'

def load_contacts():
    if os.path.exists(contacts_file):
        with open(contacts_file, 'r') as f:
            contacts = json.load(f)
    else:
        contacts = {}
    return contacts

def save_contacts(contacts):
    with open(contacts_file, 'w') as f:
        json.dump(contacts, f)
        
def view_contacts(contacts):
    if not contacts:
        print("No contacts available.")
    else:
        print("\nContacts:")
        for name, phone in contacts.items():
            print(f"Name: {name}, Phone: {phone}")
            
def add_contact(contacts):
    name = input("Enter contact name: ")
    phone = input("Enter contact phone number (digits only, e.g., 5551234567): ")
    contacts[name] = phone
    save_contacts(contacts)
    print(f"Contact '{name}' added.")

def send_text(phone_number, message):
    resp = requests.post('https://textbelt.com/text', {
        'phone': phone_number,
        'message': message,
        'key': 'textbelt',
    })
    result = resp.json()
    if result.get('success'):
        print("Message sent successfully.")
    else:
        print("Failed to send message.")
        print(f"Error: {result.get('error')}")

def send_custom_message(contacts):
    if not contacts:
        print("No contacts available. Please add a contact first.")
        return
    print("Contacts:")
    for idx, name in enumerate(contacts.keys()):
        print(f"{idx+1}. {name}")
    choice = input("Select a contact by number: ")
    try:
        choice = int(choice)
        if 1 <= choice <= len(contacts):
            contact_name = list(contacts.keys())[choice - 1]
            phone_number = contacts[contact_name]
            message = input("Enter your message: ")
            send_text(phone_number, message)
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def main():
    contacts = load_contacts()
    while True:
        print("\nMenu:")
        print("1. Add a contact")
        print("2. Send a custom message")
        print("3. View contacts")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            send_custom_message(contacts)
        elif choice == '3':
            view_contacts(contacts)
        elif choice == '4':
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()

