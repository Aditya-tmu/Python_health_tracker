import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
import matplotlib.pyplot as plt  # Importing matplotlib for visualization

# File to save user data
DATA_FILE = "user_data.csv"

# Dictionary to store user data by name
user_data = {}

# Function to load data from the CSV file
def load_data():
    global user_data
    if os.path.exists(DATA_FILE):
        user_data_df = pd.read_csv(DATA_FILE)
        if not user_data_df.empty:
            # Group data by 'Name' and create user data dict
            for name, group in user_data_df.groupby('Name'):
                user_data[name] = group.drop(columns=['Name']).reset_index(drop=True)
                user_listbox.insert(tk.END, name)  # Populate the listbox with names

# Function to save data to the CSV file
def save_to_file():
    if user_data:
        all_data = []
        for name, data in user_data.items():
            data['Name'] = name  # Add 'Name' column to the user's data
            all_data.append(data)
        # Concatenate all users' data and save to a CSV file
        full_data_df = pd.concat(all_data)
        full_data_df.to_csv(DATA_FILE, index=False)

# Function to save the input data into the user's DataFrame
def save_data():
    name = name_entry.get()
    weight = weight_entry.get()
    steps = steps_entry.get()
    calories = calories_entry.get()

    if not name or not weight or not steps or not calories:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    try:
        # Create a new DataFrame for the user if it doesn't exist
        if name not in user_data:
            user_data[name] = pd.DataFrame(columns=["Weight", "Steps", "Calories"])
            user_listbox.insert(tk.END, name)  # Add new name to the listbox

        new_data = pd.DataFrame({
            "Weight": [float(weight)],
            "Steps": [int(steps)],
            "Calories": [int(calories)]
        })

        # Check if the DataFrame is empty before concatenation
        if not user_data[name].empty:
            user_data[name] = pd.concat([user_data[name], new_data], ignore_index=True)
        else:
            user_data[name] = new_data

        messagebox.showinfo("Success", "Data saved successfully!")

        # Clear the entries after saving
        name_entry.delete(0, tk.END)
        weight_entry.delete(0, tk.END)
        steps_entry.delete(0, tk.END)
        calories_entry.delete(0, tk.END)

        # Save data to file
        save_to_file()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# Function to visualize the selected user's data
def visualize_data():
    try:
        selected_name = user_listbox.get(user_listbox.curselection())
        
        if selected_name not in user_data or user_data[selected_name].empty:
            messagebox.showwarning("No Data", "No data available for this user.")
            return

        # Plotting the user's data
        user_data[selected_name].plot(marker='o', title=f"Health Metrics for {selected_name}")
        plt.show()  # This will now work since plt is imported
    except tk.TclError:
        messagebox.showwarning("Select User", "Please select a user from the list.")

# Function to load data for the selected user
def load_user_data(event):
    try:
        selected_name = user_listbox.get(user_listbox.curselection())
        
        if selected_name in user_data and not user_data[selected_name].empty:
            # Clear previous entries
            weight_entry.delete(0, tk.END)
            steps_entry.delete(0, tk.END)
            calories_entry.delete(0, tk.END)

            # Load the latest data into the entry fields
            last_entry = user_data[selected_name].iloc[-1]
            weight_entry.insert(0, last_entry['Weight'])
            steps_entry.insert(0, last_entry['Steps'])
            calories_entry.insert(0, last_entry['Calories'])
    except tk.TclError:
        pass  # This error occurs if no selection is made

# Function to clear the selected user's data
def clear_user_data():
    try:
        selected_name = user_listbox.get(user_listbox.curselection())
        if selected_name in user_data:
            # Confirm before deleting
            if messagebox.askyesno("Delete Data", f"Are you sure you want to delete data for {selected_name}?"):
                del user_data[selected_name]
                user_listbox.delete(user_listbox.curselection())  # Remove name from the listbox
                save_to_file()  # Update the saved data
                messagebox.showinfo("Success", f"Data for {selected_name} deleted successfully.")
    except tk.TclError:
        messagebox.showwarning("Select User", "Please select a user to delete.")

# Create a function to close the application safely
def close_app():
    root.destroy()

# Creating the main window
root = tk.Tk()
root.title("Health Tracker")

# Set the window to fullscreen
root.attributes('-fullscreen', True)

# Set a background color
root.configure(bg="#e0f7fa")

# Create a frame for user selection
user_frame = tk.Frame(root, bg="#e0f7fa")
user_frame.pack(side=tk.LEFT, padx=20, pady=20)

# Create labels and entry boxes for name, weight, steps, and calories
name_label = tk.Label(root, text="Name:", bg="#e0f7fa", font=("Arial", 16))
name_label.pack(pady=10)

name_entry = tk.Entry(root, font=("Arial", 16), width=30)
name_entry.pack(pady=10)

# Clear user data button
clear_button = tk.Button(root, text="Clear User", command=clear_user_data, font=("Arial", 16), bg="red", fg="white", width=15)
clear_button.pack(pady=10)

weight_label = tk.Label(root, text="Weight (kg):", bg="#e0f7fa", font=("Arial", 16))
weight_label.pack(pady=10)

weight_entry = tk.Entry(root, font=("Arial", 16), width=30)
weight_entry.pack(pady=10)

steps_label = tk.Label(root, text="Steps:", bg="#e0f7fa", font=("Arial", 16))
steps_label.pack(pady=10)

steps_entry = tk.Entry(root, font=("Arial", 16), width=30)
steps_entry.pack(pady=10)

calories_label = tk.Label(root, text="Calories:", bg="#e0f7fa", font=("Arial", 16))
calories_label.pack(pady=10)

calories_entry = tk.Entry(root, font=("Arial", 16), width=30)
calories_entry.pack(pady=10)

# Create a listbox to show users
user_listbox = tk.Listbox(user_frame, font=("Arial", 16), width=30, height=20)
user_listbox.pack(pady=10)
user_listbox.bind("<<ListboxSelect>>", load_user_data)

# Create buttons for saving data and visualizing
button_frame = tk.Frame(root, bg="#e0f7fa")
button_frame.pack(pady=20)

save_button = tk.Button(button_frame, text="Save Data", command=save_data, font=("Arial", 16), bg="#4caf50", fg="white", width=15)
save_button.pack(side=tk.LEFT, padx=10)

visualize_button = tk.Button(button_frame, text="Visualize Data", command=visualize_data, font=("Arial", 16), bg="#2196f3", fg="white", width=15)
visualize_button.pack(side=tk.LEFT, padx=10)

# Add close button
close_button = tk.Button(root, text="Close", command=close_app, font=("Arial", 16), bg="red", fg="white", width=10)
close_button.pack(pady=20)

# Load existing data if available
load_data()

# Start the Tkinter event loop
root.mainloop()
