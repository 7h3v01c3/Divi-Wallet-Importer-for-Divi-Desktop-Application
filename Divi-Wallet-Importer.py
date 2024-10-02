import customtkinter as ctk
import os
import shutil
import logging
import sys
import time
import threading
import subprocess
from PIL import Image, ImageTk, ImageSequence, ImageFont
from mnemonic import Mnemonic
import json
import datetime
import psutil



# Function to create log directory and log the error only when an error occurs
def log_error(error_message):
    # Define the log directory path (e.g., on the Desktop in a folder called DWtoDD_logs)
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    log_directory = os.path.join(desktop_path, "DWtoDD_logs")

    # Only create the log directory and log file when an error occurs
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Define the full path to the log file
    log_file_path = os.path.join(log_directory, "error_log.log")

    # Set up logging to only log errors and to the specified file
    logging.basicConfig(filename=log_file_path, level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Log the error
    logging.error(error_message)

log_file = os.path.join(os.path.expanduser('~'), 'divi_app_debug.log')
sys.stdout = open(log_file, 'w')
sys.stderr = open(log_file, 'w')

print("Logging started...")

# Simulate an error for testing
# def simulate_error():
#     try:
#         raise ValueError("This is a test error for logging purposes")
#     except Exception as e:
#         log_error(f"An error occurred: {str(e)}")
#
# # Call this function to simulate an error and test the logging
# simulate_error()

# Initialize BIP39 Mnemonic for English wordlist
mnemo = Mnemonic("english")

# Get the current date and time
backuptime = datetime.datetime.now()

# Format the date and time as 'year-month-day-hour-min-sec'
formatted_time = backuptime.strftime('%Y-%m-%d-%H-%M-%S')

# Use the formatted time in the backup file name
name_of_backup = f"wallet_backup_{formatted_time}.dat"

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for both dev and PyInstaller .exe """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Function to load the .ttf file and return the font family name
def load_custom_font(ttf_path):
    try:
        # Use PIL to load the font and extract its family name
        font_name = ImageFont.truetype(ttf_path)
        return font_name.getname()[0]  # Returns the family name (e.g., "Roboto")
    except IOError:
        print(f"Font file not found: {ttf_path}")
        return None

# Define the path to the Roboto font files in the "fonts" directory in the project root
roboto_regular_path = os.path.join(os.getcwd(), "fonts", "Roboto-Regular.ttf")
roboto_bold_path = os.path.join(os.getcwd(), "fonts", "Roboto-Bold.ttf")

# Load the fonts from the .ttf files and retrieve their family names
roboto_regular = load_custom_font(roboto_regular_path)
roboto_bold = load_custom_font(roboto_bold_path)

# Load GIF for animation
gif_path = resource_path("images/gears_larger.gif")


# Validate the mnemonic using checksum
def validate_mnemonic_checksum(mnemonic):
    return mnemo.check(mnemonic)


def update_status_message(message, message_type="info", hide_after=3000):
    try:
        print(f"Updating status message to: {message}")
        sys.stdout.flush()  # Ensure the message is printed immediately

        # Define colors and background styles for different message types
        if message_type == "warning":
            text_color = "#FFA500"  # Orange for warnings
            bg_color = "#FFFFFF"  # White background for the message
            frame_color = "#D3D3D3"  # Light grey border for frame
        elif message_type == "error":
            text_color = "#FF6347"  # Red for errors
            bg_color = "#FFFFFF"  # White background for the message
            frame_color = "#D3D3D3"  # Light grey border for frame
        elif message_type == "success":
            text_color = "#32CD32"  # Green for success
            bg_color = "#FFFFFF"  # White background for the message
            frame_color = "#D3D3D3"  # Light grey border for frame
        else:
            text_color = "#000000"  # Black for informational messages
            bg_color = "#FFFFFF"  # White background for the message
            frame_color = "#D3D3D3"  # Light grey border for frame

        # Show the frame and configure the text, color, and background
        root.after(0, lambda: status_frame.grid())  # Show the status frame when a message appears
        root.after(0, lambda: status_label.configure(text=message, text_color=text_color, fg_color=bg_color))

        # Reconfigure the frame and ensure it's sized dynamically
        root.after(0, lambda: status_frame.configure(fg_color=frame_color, border_width=2))

        # Center the message and make the label expand to fit the text
        root.after(0, lambda: status_label.grid(sticky="ew"))  # Center the label text horizontally
        root.after(0, lambda: status_frame.grid_columnconfigure(0, weight=1))  # Make the frame expand horizontally

        root.after(0, root.update)  # Ensure the UI is refreshed

        # Optionally hide the message after some time
        if hide_after > 0:
            root.after(hide_after, hide_status_message)

    except Exception as e:
        logging.exception(f"Error updating status message: {str(e)}")


def hide_status_message():
    """Function to hide the status frame and clear the message."""
    status_label.configure(text="")
    status_frame.grid_remove()  # Hide the frame


def clear_previous_elements():
    try:
        for widget in root.grid_slaves():
            if widget not in {logo_label, status_label}:  # Exclude the logo and status label from being cleared
                widget.grid_forget()
    except Exception as e:
        logging.exception(f"Error in clearing previous elements: {str(e)}")


# Function to display loading animation
def display_loading_animation():
    try:
        gif = Image.open(gif_path)
        frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]  # Load frames

        def update_frame(idx=0):
            gif_label.configure(image=frames[idx])  # Update gif_label with the current frame
            root.after(42, update_frame, (idx + 1) % len(frames))  # Update every 42ms

        update_frame()  # Start animation loop
    except Exception as e:
        logging.exception(f"Error displaying loading animation: {str(e)}")



# Function to ask Yes/No with embedded buttons
def ask_yes_no(question):
    global yes_button, no_button, question_label

    clear_previous_elements()

    # Ensure the grid columns are equally weighted to center everything
    for i in range(8):  # Assuming the grid has 8 columns
        root.grid_columnconfigure(i, weight=1)

    # Question Label - Centered across columns
    question_label = ctk.CTkLabel(root, text=question, font=(roboto_regular, 16))
    question_label.grid(row=3, column=1, columnspan=6, pady=20, sticky="ew")  # Span across columns 1-6, centered

    # Create Yes and No buttons with custom colors
    yes_button = ctk.CTkButton(
        root, text="Yes", command=lambda: set_answer(True),
        fg_color="#5D5E63",
        hover_color="#323235"
    )
    no_button = ctk.CTkButton(
        root, text="No", command=lambda: set_answer(False),
        fg_color="#5D5E63",  # Red color for No
        hover_color="#323235"  # Darker red on hover
    )

    # Center the Yes and No buttons by spanning 2 columns in the middle (columns 3 and 4)
    yes_button.grid(row=4, column=3, pady=10, padx=5, sticky="ew")  # Center on column 3
    no_button.grid(row=4, column=4, pady=10, padx=5, sticky="ew")  # Center on column 4

    # Wait for the user's response
    root.wait_variable(var_answer)

    # Return True for Yes, False for No
    return var_answer.get()


def set_answer(answer):
    var_answer.set(answer)

def on_submit():
    try:
        print("Submit button clicked")
        sys.stdout.flush()  # Ensure the message is written to the log file immediately

        mnemonic_words = [entry.get().strip().lower() for entry in entries]
        print(f"Collected mnemonic words: {mnemonic_words}")
        sys.stdout.flush()

        # Check for empty fields
        if not all(mnemonic_words):
            print("Please fill all 12 fields before submitting.")
            sys.stdout.flush()
            update_status_message("Please fill all 12 fields before submitting.", "warning")  # Show warning message
            return

        # Validate the mnemonic phrase
        valid, message = validate_mnemonic(mnemonic_words)
        print(f"Validation result: {valid}, {message}")
        sys.stdout.flush()

        if valid:
            print("Mnemonic seed phrase is valid! Starting recovery...")
            sys.stdout.flush()
            update_status_message("Mnemonic seed phrase is valid! Starting recovery...", "success")
            clear_previous_elements()
            gif_label.grid(row=3, column=1, columnspan=6, pady=20, sticky="ew")
            display_loading_animation()
            root.after(500, run_divid, mnemonic_words)
        else:
            print("Invalid seed words.")
            sys.stdout.flush()
            update_status_message("Invalid seed words, please try again.", "error")  # Error message
            root.after(3000, reset_form_and_status)
    except Exception as e:
        print(f"Exception in on_submit: {str(e)}")
        sys.stdout.flush()
        update_status_message(f"An error occurred: {str(e)}", "error")


def reset_form_and_status():
    try:
        clear_mnemonic_entries()
        update_status_message("", "info")  # Clear the status message

        # Optionally, reset the status frame's appearance as well
        root.after(0, lambda: status_frame.configure(fg_color="#D3D3D3"))  # Reset to default frame color

        # Provide a default instruction again (optional)
        update_status_message("Enter your 12-word mnemonic. Ensure all words are lowercase and no extra spaces.")
    except Exception as e:
        logging.exception(f"Error resetting form and status: {str(e)}")


def validate_mnemonic(words):
    try:
        print(f"Validating words: {words}")
        sys.stdout.flush()
        if len(words) != 12:
            print("Validation failed: Incorrect number of words")
            sys.stdout.flush()
            return False, "The mnemonic seed phrase for Divi Wallet Mobile must be exactly 12 words."
        mnemonic = " ".join(words)
        if not validate_mnemonic_checksum(mnemonic):
            print("Validation failed: Checksum invalid")
            sys.stdout.flush()
            return False, "Invalid mnemonic seed phrase. Please try again."
        print("Validation succeeded")
        sys.stdout.flush()
        return True, "Mnemonic seed phrase is valid!"
    except Exception as e:
        logging.exception(f"Error validating mnemonic: {str(e)}")
        return False, "An error occurred during validation."


def clear_mnemonic_entries():
    try:
        for entry in entries:
            entry.delete(0, 'end')  # Clear all text fields
    except Exception as e:
        logging.exception(f"Error clearing mnemonic entries: {str(e)}")


def display_mnemonic_form():
    try:
        global entries, status_frame

        # Clear previous elements
        clear_previous_elements()

        # Create 8 grid columns with equal weight to center everything
        for i in range(8):
            root.grid_columnconfigure(i, weight=1)

        # Add some space above row 1 (label row)
        root.grid_rowconfigure(0, minsize=60)

        # Instruction Label - Centered and placed above inputs
        instruction_label.grid(row=1, column=1, columnspan=6, pady=(20, 0), sticky="ew")

        # Create 12 entry fields for mnemonic words (two rows, six columns)
        entries = []
        for row in range(2):  # Two rows for mnemonic input fields
            for col in range(6):  # Six columns for the 12 words
                entry = ctk.CTkEntry(root, width=100, font=(roboto_regular, 14))  # Using roboto_regular with size 14
                entry.grid(row=row + 2, column=col + 1, padx=5, pady=5)  # Placing input fields in grid
                entries.append(entry)

        # Submit button placed in the center, spanning 2 columns
        submit_button = ctk.CTkButton(
            root, text="Submit", command=on_submit, font=(roboto_regular, 16), width=200,  # Using roboto_regular with size 16
            fg_color="#5D5E63",
            hover_color="#323235"
        )
        submit_button.grid(row=5, column=3, columnspan=2, pady=20)  # Center button on columns 3 and 4

        # Add status frame but keep it hidden initially
        status_frame = ctk.CTkFrame(root, fg_color="#D3D3D3", corner_radius=5, width=300)
        status_frame.grid(row=6, column=2, columnspan=4, pady=10, padx=10, sticky="ew")
        status_frame.grid_remove()  # Initially hidden

        # Status label inside the frame
        global status_label
        status_label = ctk.CTkLabel(status_frame, text="", font=(roboto_regular, 12), fg_color="#FFFFFF")  # Using roboto_regular with size 12
        status_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        print("Submit button and status frame initialized")
        sys.stdout.flush()

    except Exception as e:
        logging.exception(f"Error displaying mnemonic form: {str(e)}")



import subprocess
import os
import logging

def run_divid(mnemonic_words):
    try:
        appdata_path = os.getenv('APPDATA')
        if appdata_path:
            # Change the working directory to where divid.exe and divi-cli.exe are located
            divi_dir = os.path.join(appdata_path, "Divi Desktop", "divid", "unpacked", "divi_win_64")
            os.chdir(divi_dir)

            divi_daemon_path = os.path.join(divi_dir, "divid.exe")
            mnemonic_str = " ".join(mnemonic_words)

            # Log the paths and the command for debugging
            logging.debug(f"divi_daemon_path: {divi_daemon_path}")
            logging.debug(f"Command: divid.exe -mnemonic={mnemonic_str} -force_rescan=1")

            if not os.path.exists(divi_daemon_path):
                update_status_message(f"divid.exe not found at path: {divi_daemon_path}", "error")
                return

            command = [divi_daemon_path, f'-mnemonic={mnemonic_str}', "-force_rescan=1"]
            logging.debug(f"Executing command: {command}")

            # Setup to suppress command windows more aggressively
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS,
                                       startupinfo=startupinfo)
            if process:
                update_status_message("Daemon started in the background. Monitoring recovery process...")
                recovery_thread = threading.Thread(target=monitor_recovery_status)
                recovery_thread.daemon = True
                recovery_thread.start()
            else:
                update_status_message("Failed to start daemon.", "error")
        else:
            update_status_message("APPDATA environment variable not found.", "error")
    except Exception as e:
        logging.exception(f"Error in run_divid: {str(e)}")
        update_status_message(f"Error starting daemon: {str(e)}", "error")

def is_process_running(process_name):
    """Check if a process with a given name is running on Windows."""
    for proc in psutil.process_iter(['pid', 'name']):
        if process_name.lower() in proc.info['name'].lower():
            return True
    return False

def monitor_recovery_status():
    try:
        # Windows path for Divi CLI
        divi_cli_path = os.path.join(os.getenv('APPDATA'), "Divi Desktop", "divid", "unpacked", "divi_win_64",
                                     "divi-cli.exe")

        # Check if the daemon process is running first
        while True:
            if not is_process_running("divid.exe"):
                update_status_message("Waiting for Divi daemon to start...", "info")
                time.sleep(5)  # Retry every 5 seconds
                continue

            result = subprocess.run([divi_cli_path, "getinfo"], capture_output=True, text=True)

            output = result.stderr.strip() if result.stderr else result.stdout.strip()

            if output.startswith("error:"):
                # Check if output is not empty and is valid JSON
                try:
                    error_msg = json.loads(output.replace("error: ", ""))
                except json.JSONDecodeError:
                    logging.error(f"Failed to parse JSON: {output}")
                    update_status_message("Working on wallet recovery, this may take a few more moments.", "info")
                    time.sleep(5)  # Wait and retry
                    continue

                message = error_msg.get("message", "")

                if "Loading block index" in message:
                    update_status_message("Loading blockchain data... Please wait.")
                elif "Loading wallet" in message:
                    percent = message.split("(")[1].split("%")[0].strip() + "%"
                    update_status_message(f"Wallet recovery in progress... {percent} complete.")
                elif "Scanning chain for wallet updates" in message:
                    update_status_message("Divi Core is scanning for transaction history... Please wait.")
                    time.sleep(5)
                    launch_divi_desktop()
                    return
            else:
                # If there's no error, the recovery is likely complete
                update_status_message("Recovery complete. Opening Divi Desktop...")
                time.sleep(2)
                launch_divi_desktop()
                return

            time.sleep(5)  # Wait before polling again
    except Exception as e:
        logging.exception(f"Error monitoring recovery status: {str(e)}")
        update_status_message(f"Error in recovery process: {str(e)}", "error")



def launch_divi_desktop():
    try:
        update_status_message("In a moment Divi Wallet Importer will close open Divi Desktop Application.")
        time.sleep(2)
        update_status_message("Divi Desktop Application now opening. Please be patient while it syncs and rescans.")
        time.sleep(1)
        divi_desktop_path = "C:/Program Files/Divi Desktop/Divi Desktop.exe"
        os.startfile(divi_desktop_path)
        root.quit()
    except Exception as e:
        logging.exception(f"Could not launch Divi Desktop: {str(e)}")
        update_status_message(f"Could not launch Divi Desktop: {str(e)}")

# Function to check if wallet.dat exists and handle the flow
def check_wallet_and_handle_flow():
    divi_path = os.path.join(os.getenv('APPDATA'), 'DIVI')
    wallet_path = os.path.join(divi_path, 'wallet.dat')

    root.grid_rowconfigure(1, minsize=60)  # Adding space above for the status label
    logging.debug(f"Checking wallet.dat at path: {wallet_path}")

    # 1. If `wallet.dat` exists
    if os.path.exists(wallet_path):
        # Ask to backup and rename it
        backup_result = ask_yes_no(
            f"A wallet.dat file was found.\n\n It will be backed up as {name_of_backup}.\nDo you want to continue?"
        )

        # Convert response to boolean
        backup_result = backup_result == "1"  # "1" -> True, "0" -> False

        if backup_result:  # If user chooses to backup
            if rename_wallet():  # If backup succeeded
                update_status_message("Backup complete. Proceeding with recovery.", "success")
                display_mnemonic_form()  # Proceed with seed recovery
            else:  # If backup failed
                update_status_message("Backup failed. Cannot proceed.", "error")
        else:  # If user cancels backup, use display_message_and_wait
            display_message_and_wait("Backup canceled. Exiting the app...", action="quit")

    else:
        # 2. If `wallet.dat` does NOT exist
        handle_no_wallet()


# Function to display the message and wait for a moment before closing or redirecting
def display_message_and_wait(message, action=None):


    # Create a label to display the message
    info_label = ctk.CTkLabel(root, text=message, font=(roboto_regular, 14))
    info_label.grid(row=6, column=2, columnspan=4, pady=10, padx=10, sticky="ew")

    # Update the UI immediately so the message is shown
    root.update()

    # Wait for 3 seconds to allow the user to read the message
    time.sleep(3)

    # Perform the action after the delay
    if action == 'quit':
        root.quit()
    elif action == 'redirect_to_discord':
        subprocess.run(["start", "https://discord.gg/diviproject"], shell=True)
        root.quit()
    elif action == 'redirect_to_download':
        subprocess.run(["start", "https://diviproject.org/downloads"], shell=True)
        root.quit()


# Updated handle_no_wallet function
def handle_no_wallet():
    # Ask if the user has already backed up the wallet.dat
    backup_check = ask_yes_no("Have you already backed up the `wallet.dat`?")
    backup_check = backup_check == "1"  # Convert to True if "1", False if "0"

    if not backup_check:  # If NO (responded with False), continue with further checks
        # Ask if Divi Desktop is installed
        divi_installed = ask_yes_no("Do you have Divi Desktop Application installed?")
        divi_installed = divi_installed == "1"  # Convert to boolean

        if divi_installed:  # If Yes (responded with True)
            # If Divi Desktop is installed, check if it's fully synced
            synced = ask_yes_no("Is Divi Desktop Application showing synced?")
            synced = synced == "1"  # Convert to boolean

            if synced:  # If Yes (responded with True)
                # If synced, ask if they want to continue recovery without wallet.dat
                continue_recovery = ask_yes_no("Do you want to continue with seed recovery without a wallet.dat file?")
                continue_recovery = continue_recovery == "1"  # Convert to boolean

                if continue_recovery:  # If Yes (responded with True)
                    # Proceed with seed recovery
                    display_mnemonic_form()
                else:
                    # If NO (responded with False), redirect to Discord for support
                    display_message_and_wait("Redirecting to Discord for support...", action='redirect_to_discord')
            else:
                # If Divi Desktop is not synced, prompt to sync and retry
                display_message_and_wait("Please sync your Divi Desktop and try again.", action='quit')
        else:
            # If Divi Desktop is not installed, redirect to download link
            display_message_and_wait("Redirecting to Divi Desktop download page...", action='redirect_to_download')
    else:
        # If YES (responded with True), they already backed up wallet.dat, proceed to seed recovery
        display_mnemonic_form()


# Function to rename wallet.dat and remove divitxs.db
def rename_wallet():
    divi_path = os.path.join(os.getenv('APPDATA'), 'DIVI')
    wallet_path = os.path.join(divi_path, 'wallet.dat')
    backup_path = os.path.join(divi_path, name_of_backup)

    # Rename wallet.dat
    if os.path.exists(wallet_path):
        try:
            shutil.move(wallet_path, backup_path)
            logging.info(f"Successfully renamed wallet.dat to {name_of_backup}")
            update_status_message(f"wallet.dat renamed to {name_of_backup}")

            # Call the function to remove divitxs.db
            remove_divitxs_db()

            return True
        except Exception as e:
            logging.error(f"Failed to backup wallet.dat: {str(e)}")
            update_status_message("Backup Failed")
            return False
    else:
        update_status_message("wallet.dat not found")
        return False


# Function to remove divitxs.db file (handles non-existence gracefully)
def remove_divitxs_db():
    divi_folder_path = os.path.join(os.getenv('APPDATA'), "Divi Desktop")
    divitxs_db_path = os.path.join(divi_folder_path, "divitxs.db")

    if os.path.exists(divitxs_db_path):
        try:
            os.remove(divitxs_db_path)
            logging.info(f"Successfully removed {divitxs_db_path}")
            update_status_message(f"Successfully removed {divitxs_db_path}")
        except Exception as e:
            logging.error(f"Failed to remove {divitxs_db_path}: {str(e)}")
            update_status_message(f"Failed to remove {divitxs_db_path}: {str(e)}")
    else:
        logging.info(f"{divitxs_db_path} does not exist.")
        update_status_message(f"{divitxs_db_path} does not exist.")

# Set up the CustomTkinter window
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Divi Wallet Importer for Divi Desktop")
root.geometry("800x400")

for i in range(8):
    root.grid_columnconfigure(i, weight=1)

var_answer = ctk.StringVar()

try:
    root.iconbitmap(resource_path("images/divi-logomark-red.ico"))
except Exception as e:
    print(f"Error loading icon: {e}")

try:
    logo_image_path = resource_path("images/divi-logomark-red.png")
    logo_image = ctk.CTkImage(light_image=Image.open(logo_image_path), size=(50, 50))
    logo_label = ctk.CTkLabel(root, image=logo_image, text="")
    logo_label.place(x=10, y=10)
except Exception as e:
    print(f"Error loading logo: {e}")

instruction_label = ctk.CTkLabel(root, text="Enter your 12-word seeds from Divi Wallet Mobile.", font=(roboto_regular, 16), width=300)
instruction_label.grid_remove()

status_label = ctk.CTkLabel(root, text="Setting Up...",font=(roboto_regular, 12))
status_label.grid(row=5, column=0, columnspan=7, pady=60, sticky="ew")

gif_label = ctk.CTkLabel(root, text="")

entries = []

root.after(1000, check_wallet_and_handle_flow)
root.mainloop()
