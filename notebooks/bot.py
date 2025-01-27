import pandas as pd
import os

# Define the file path for the CSV
file_path = "academic_network.csv"

# Check if the file exists; if not, create it with the appropriate headers
if not os.path.exists(file_path):
    columns = ["Name", "Academic Position", "Department", "Network Node Width", "Research Interests", "Project"]
    pd.DataFrame(columns=columns).to_csv(file_path, index=False)

# Function to add data dynamically
def add_researcher():
    # Ask for researcher details
    name = input("Enter the researcher's name: ")
    position = input("Enter the researcher's academic position (e.g., Professor, Researcher): ")
    department = input("Enter the researcher's department: ")
    network_node = input("Enter the researcher's network node width (numeric): ")
    interests = input("Enter the researcher's research interests (comma-separated): ")
    project = input("Enter the researcher's project (or leave blank): ")

    # Load existing data
    data = pd.read_csv(file_path)

    # Append new data
    new_entry = {
        "Name": name,
        "Academic Position": position,
        "Department": department,
        "Network Node Width": network_node,
        "Research Interests": interests,
        "Project": project
    }
    data = pd.concat([data, pd.DataFrame([new_entry])], ignore_index=True)

    # Save back to the CSV
    data.to_csv(file_path, index=False)
    print(f"Researcher {name} has been added to {file_path}!")

# Main script loop
print("Welcome to the Researcher Database Management Script!")
while True:
    add_researcher()
    cont = input("Would you like to add another researcher? (yes/no): ").strip().lower()
    if cont != "yes":
        print("Exiting. Goodbye!")
        break
