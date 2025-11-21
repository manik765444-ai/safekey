# main.py

import getpass
import hashlib
import os
import pickle
from typing import Dict, List

class PasswordManager:
    """
    A simple password manager CLI.
    
    Attributes:
        password_file (str): The file where passwords are stored.
        master_password (str): The master password to access the password manager.
    """

    def __init__(self, password_file: str = "passwords.dat"):
        """
        Initializes the password manager.
        
        Args:
            password_file (str, optional): The file where passwords are stored. Defaults to "passwords.dat".
        """
        self.password_file = password_file
        self.master_password = None
        self.passwords: Dict[str, str] = self.load_passwords()

    def load_passwords(self) -> Dict[str, str]:
        """
        Loads the passwords from the password file.
        
        Returns:
            Dict[str, str]: A dictionary of usernames and passwords.
        """
        if os.path.exists(self.password_file):
            with open(self.password_file, "rb") as f:
                return pickle.load(f)
        else:
            return {}

    def save_passwords(self) -> None:
        """
        Saves the passwords to the password file.
        """
        with open(self.password_file, "wb") as f:
            pickle.dump(self.passwords, f)

    def set_master_password(self) -> None:
        """
        Sets the master password.
        """
        self.master_password = getpass.getpass("Enter master password: ")
        self.master_password = hashlib.sha256(self.master_password.encode()).hexdigest()

    def check_master_password(self) -> bool:
        """
        Checks if the master password is correct.
        
        Returns:
            bool: True if the master password is correct, False otherwise.
        """
        password = getpass.getpass("Enter master password: ")
        password = hashlib.sha256(password.encode()).hexdigest()
        return password == self.master_password

    def add_password(self) -> None:
        """
        Adds a new password.
        """
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        self.passwords[username] = password
        self.save_passwords()

    def delete_password(self) -> None:
        """
        Deletes a password.
        """
        username = input("Enter username: ")
        if username in self.passwords:
            del self.passwords[username]
            self.save_passwords()
        else:
            print("Username not found.")

    def list_passwords(self) -> None:
        """
        Lists all passwords.
        """
        for username, password in self.passwords.items():
            print(f"{username}: {password}")

    def get_password(self) -> None:
        """
        Gets a password.
        """
        username = input("Enter username: ")
        if username in self.passwords:
            print(self.passwords[username])
        else:
            print("Username not found.")


def main() -> None:
    """
    The main function.
    """
    try:
        manager = PasswordManager()
        if not manager.master_password:
            manager.set_master_password()
        if not manager.check_master_password():
            print("Incorrect master password.")
            return
        while True:
            print("\n1. Add password")
            print("2. Delete password")
            print("3. List passwords")
            print("4. Get password")
            print("5. Quit")
            choice = input("Enter choice: ")
            if choice == "1":
                manager.add_password()
            elif choice == "2":
                manager.delete_password()
            elif choice == "3":
                manager.list_passwords()
            elif choice == "4":
                manager.get_password()
            elif choice == "5":
                break
            else:
                print("Invalid choice.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()