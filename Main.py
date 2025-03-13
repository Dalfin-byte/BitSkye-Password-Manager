import math
import secrets
import string
import sys
import os
import nacl.utils
from nacl.bindings import (
    crypto_aead_xchacha20poly1305_ietf_encrypt,
    crypto_aead_xchacha20poly1305_ietf_decrypt,
    crypto_aead_xchacha20poly1305_ietf_KEYBYTES,
    crypto_aead_xchacha20poly1305_ietf_NPUBBYTES
)

# Attempt to import Rich for enhanced terminal UI
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
except ImportError:
    Console = None

# Initialize the rich console if available
console = Console() if Console else None

def print_msg(message, style="bold cyan"):
    """Prints a styled message if Rich is available, otherwise prints plain text."""
    if console:
        console.print(message, style=style)
    else:
        print(message)

def clear_screen():
    """Clears the terminal screen."""
    if console:
        console.clear()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    """Pauses execution until the user presses Enter."""
    input("\nPress Enter to return to the menu...")

def welcome_panel():
    """Displays a welcome message in a panel."""
    welcome_text = (
        "[bold green]Welcome to the BitShark Password Generator![/bold green]\n\n"
        "This tool allows you to create secure passwords, customize character sets, "
        "and even encrypt your passwords using XChaCha20.\n\n"
        "Use the menu below to configure your settings, generate passwords, and more."
    )
    if console:
        panel = Panel(welcome_text, title="Welcome", style="bold blue")
        console.print(panel)
    else:
        print(welcome_text)

# Global settings for password generation
settings = {
    "length": 16,
    "include_upper": True,
    "include_lower": True,
    "include_digits": True,
    "include_punctuation": True,
    "custom_chars": ""
}

# Global variables for storing password and encryption data
generated_password = None
encryption_key = nacl.utils.random(crypto_aead_xchacha20poly1305_ietf_KEYBYTES)
last_nonce = None
last_ciphertext = None

def build_alphabet():
    """Constructs the effective character set based on current settings."""
    alphabet = settings["custom_chars"]  # Start with custom characters
    if settings["include_upper"]:
        alphabet += string.ascii_uppercase
    if settings["include_lower"]:
        alphabet += string.ascii_lowercase
    if settings["include_digits"]:
        alphabet += string.digits
    if settings["include_punctuation"]:
        alphabet += string.punctuation
    # Remove duplicates and return a sorted string
    return ''.join(sorted(set(alphabet)))

def generate_password():
    """Generates a single secure password based on the current settings."""
    alphabet = build_alphabet()
    if not alphabet:
        print_msg("[red]Error: No character set selected. Please enable some options or add custom characters.[/red]")
        return None
    return ''.join(secrets.choice(alphabet) for _ in range(settings["length"]))

def generate_multiple_passwords(count):
    """Generates and returns a list of multiple passwords."""
    return [generate_password() for _ in range(count)]

def encrypt_password(password, key):
    """Encrypts the provided password using XChaCha20."""
    password_bytes = password.encode('utf-8')
    nonce = nacl.utils.random(crypto_aead_xchacha20poly1305_ietf_NPUBBYTES)
    ciphertext = crypto_aead_xchacha20poly1305_ietf_encrypt(password_bytes, None, nonce, key)
    return nonce, ciphertext

def decrypt_password(nonce, ciphertext, key):
    """Decrypts the ciphertext to retrieve the original password."""
    decrypted = crypto_aead_xchacha20poly1305_ietf_decrypt(ciphertext, None, nonce, key)
    return decrypted.decode('utf-8')

def calculate_entropy():
    """Calculates and returns the estimated entropy (in bits) of a password."""
    alphabet = build_alphabet()
    if not alphabet:
        return 0
    return settings["length"] * math.log2(len(alphabet))

def show_settings():
    """Displays the current configuration settings."""
    if console:
        table = Table(title="Current Password Settings")
        table.add_column("Setting", justify="left")
        table.add_column("Value", justify="left")
        table.add_row("Password Length", str(settings["length"]))
        table.add_row("Include Uppercase", str(settings["include_upper"]))
        table.add_row("Include Lowercase", str(settings["include_lower"]))
        table.add_row("Include Digits", str(settings["include_digits"]))
        table.add_row("Include Punctuation", str(settings["include_punctuation"]))
        table.add_row("Custom Characters", settings["custom_chars"] if settings["custom_chars"] else "None")
        console.print(table)
    else:
        print_msg("Password Length: " + str(settings["length"]))
        print_msg("Include Uppercase: " + str(settings["include_upper"]))
        print_msg("Include Lowercase: " + str(settings["include_lower"]))
        print_msg("Include Digits: " + str(settings["include_digits"]))
        print_msg("Include Punctuation: " + str(settings["include_punctuation"]))
        print_msg("Custom Characters: " + (settings["custom_chars"] if settings["custom_chars"] else "None"))

def regenerate_key():
    """Generates a new encryption key for the session."""
    global encryption_key
    encryption_key = nacl.utils.random(crypto_aead_xchacha20poly1305_ietf_KEYBYTES)
    print_msg("Encryption key regenerated.", style="bold green")

def save_encrypted_to_file():
    """Saves the latest encrypted password (nonce + ciphertext) to a file."""
    if not last_ciphertext:
        print_msg("[red]Error: No encrypted password available to save.[/red]")
        return
    filename = input("Enter filename to save encrypted password (e.g., encrypted.bin): ").strip()
    try:
        with open(filename, "wb") as f:
            f.write(last_nonce + last_ciphertext)
        print_msg(f"Encrypted password saved to {filename}.", style="bold green")
    except Exception as e:
        print_msg("Failed to save file: " + str(e), style="red")

def help_menu():
    """Displays a detailed help menu for the application."""
    help_text = (
        "[bold blue]Available Commands:[/bold blue]\n"
        "  1. Set Password Length        - Define the number of characters for your password.\n"
        "  2. Toggle Uppercase Letters     - Enable/disable uppercase letters.\n"
        "  3. Toggle Lowercase Letters     - Enable/disable lowercase letters.\n"
        "  4. Toggle Digits                - Enable/disable numerical digits.\n"
        "  5. Toggle Punctuation           - Enable/disable punctuation characters.\n"
        "  6. Set Custom Characters        - Add additional characters to the set.\n"
        "  7. Generate New Password        - Create a new password based on current settings.\n"
        "  8. Generate Multiple Passwords  - Generate several passwords at once.\n"
        "  9. Encrypt Generated Password   - Encrypt the last generated password.\n"
        " 10. Decrypt Last Encrypted Password - Decrypt the previously encrypted password.\n"
        " 11. Evaluate Password Strength   - Calculate entropy and rate password strength.\n"
        " 12. Regenerate Encryption Key    - Create a new encryption key for the session.\n"
        " 13. Save Encrypted Password      - Save the encrypted password to a file.\n"
        " 14. Show Current Settings        - Display the current configuration.\n"
        " 15. Help                       - Show this help menu.\n"
        " 16. Exit                       - Quit the application.\n"
    )
    if console:
        console.print(Panel(help_text, title="Help", style="bold blue"))
    else:
        print(help_text)

def exit_program():
    """Exits the application gracefully."""
    print_msg("Exiting the application. Goodbye!", style="bold red")
    sys.exit(0)

# --- Command Mapping ---
def menu_options():
    return {
        "1": set_password_length,
        "2": toggle_uppercase,
        "3": toggle_lowercase,
        "4": toggle_digits,
        "5": toggle_punctuation,
        "6": set_custom_characters,
        "7": generate_new_password,
        "8": generate_multiple_passwords_option,
        "9": encrypt_password_option,
        "10": decrypt_password_option,
        "11": evaluate_strength,
        "12": regenerate_key,
        "13": save_encrypted_to_file,
        "14": show_settings,
        "15": help_menu,
        "16": exit_program
    }

def display_menu():
    """Displays the main menu."""
    menu_items = [
        "1. Set Password Length",
        "2. Toggle Uppercase Letters",
        "3. Toggle Lowercase Letters",
        "4. Toggle Digits",
        "5. Toggle Punctuation",
        "6. Set Custom Characters",
        "7. Generate New Password",
        "8. Generate Multiple Passwords",
        "9. Encrypt Generated Password",
        "10. Decrypt Last Encrypted Password",
        "11. Evaluate Password Strength",
        "12. Regenerate Encryption Key",
        "13. Save Encrypted Password to File",
        "14. Show Current Settings",
        "15. Help",
        "16. Exit"
    ]
    if console:
        panel = Panel("\n".join(menu_items), title="Advanced Password Generator Menu", style="bold green")
        console.print(panel)
    else:
        print("\n" + "\n".join(menu_items))

# --- Individual Command Functions ---
def set_password_length():
    try:
        new_length = int(input("Enter desired password length (e.g., 16): ").strip())
        if new_length <= 0:
            print_msg("[red]Error: Length must be a positive integer.[/red]")
        else:
            settings["length"] = new_length
            print_msg(f"Password length set to {new_length}.", style="bold green")
    except ValueError:
        print_msg("[red]Invalid input. Please enter a number.[/red]")

def toggle_uppercase():
    settings["include_upper"] = not settings["include_upper"]
    state = "enabled" if settings["include_upper"] else "disabled"
    print_msg(f"Uppercase letters are now {state}.", style="bold green")

def toggle_lowercase():
    settings["include_lower"] = not settings["include_lower"]
    state = "enabled" if settings["include_lower"] else "disabled"
    print_msg(f"Lowercase letters are now {state}.", style="bold green")

def toggle_digits():
    settings["include_digits"] = not settings["include_digits"]
    state = "enabled" if settings["include_digits"] else "disabled"
    print_msg(f"Digits are now {state}.", style="bold green")

def toggle_punctuation():
    settings["include_punctuation"] = not settings["include_punctuation"]
    state = "enabled" if settings["include_punctuation"] else "disabled"
    print_msg(f"Punctuation is now {state}.", style="bold green")

def set_custom_characters():
    custom = input("Enter custom characters to include (leave blank to clear): ").strip()
    settings["custom_chars"] = custom
    if custom:
        print_msg(f"Custom characters set to: {custom}", style="bold green")
    else:
        print_msg("Custom characters cleared.", style="bold green")

def generate_new_password():
    global generated_password
    generated_password = generate_password()
    if generated_password:
        print_msg(f"Generated Password: [bold yellow]{generated_password}[/bold yellow]")
    else:
        print_msg("[red]Password generation failed.[/red]")

def generate_multiple_passwords_option():
    try:
        count = int(input("How many passwords would you like to generate? ").strip())
        if count <= 0:
            print_msg("[red]Error: Enter a positive number.[/red]")
        else:
            passwords = generate_multiple_passwords(count)
            print_msg("Generated Passwords:", style="bold green")
            for idx, pwd in enumerate(passwords, start=1):
                print_msg(f"{idx}. {pwd}", style="bold magenta")
    except ValueError:
        print_msg("[red]Invalid input. Please enter a valid number.[/red]")

def encrypt_password_option():
    global last_nonce, last_ciphertext
    if not generated_password:
        print_msg("[red]Error: No password generated yet. Generate a password first.[/red]")
    else:
        last_nonce, last_ciphertext = encrypt_password(generated_password, encryption_key)
        print_msg("Password encrypted successfully.", style="bold green")
        print_msg("Encrypted Password (hex): " + last_ciphertext.hex(), style="bold blue")

def decrypt_password_option():
    if not last_ciphertext or not last_nonce:
        print_msg("[red]Error: No encrypted password available. Please encrypt a password first.[/red]")
    else:
        try:
            decrypted = decrypt_password(last_nonce, last_ciphertext, encryption_key)
            print_msg("Decrypted Password: " + decrypted, style="bold yellow")
        except Exception as e:
            print_msg("Decryption failed: " + str(e), style="red")

def evaluate_strength():
    if not generated_password:
        print_msg("[red]Error: Generate a password first to evaluate its strength.[/red]")
    else:
        entropy = calculate_entropy()
        print_msg(f"Password Entropy: {entropy:.2f} bits", style="bold blue")
        if entropy < 50:
            print_msg("Strength: Weak", style="red")
        elif entropy < 70:
            print_msg("Strength: Moderate", style="yellow")
        else:
            print_msg("Strength: Strong", style="green")

def exit_program():
    print_msg("Exiting the application. Goodbye!", style="bold red")
    sys.exit(0)

# --- Main Loop ---
def main():
    options = menu_options()
    clear_screen()
    welcome_panel()
    pause()
    while True:
        clear_screen()
        display_menu()
        choice = input("\nSelect an option (1-16): ").strip()
        if choice in options:
            clear_screen()
            options[choice]()
        else:
            print_msg("[red]Invalid choice. Type '15' for help or select a valid option.[/red]")
        pause()

if __name__ == "__main__":
    main()
