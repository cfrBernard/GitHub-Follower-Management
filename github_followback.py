import requests  # Importing the requests library to handle HTTP requests
import tkinter as tk  # Importing the tkinter library for the GUI
from tkinter import ttk  # Importing ttk module for themed widgets
import time  # Importing time for managing time-related functions
import os  # Importing os for file path operations

class GitHubManager:
    def __init__(self):
        """Initialize the GitHubManager class and load configuration."""
        self.requests_made = 0  # Counter for API requests made
        self.blacklist = set()  # Set of usernames to be ignored
        self.github_token = ""  # GitHub token for authentication
        self.github_username = ""  # GitHub username for API calls
        self.headers = {}  # HTTP headers for API requests
        self.load_config()  # Load configuration from file
        self.validate_token()  # Validate the GitHub token

    def load_config(self):
        """Load GitHub token, username, and blacklist from config.txt."""
        if os.path.exists('config.txt'):  # Check if the config file exists
            with open('config.txt', 'r') as file:  # Open the file for reading
                for line in file:
                    line = line.strip()  # Remove leading and trailing whitespace
                    if "=" in line:  # Ensure the line is a key-value pair
                        key, value = line.split('=', 1)  # Split into key and value
                        if key == "GITHUB_TOKEN":
                            self.github_token = value.strip()  # Set GitHub token
                            self.headers = {"Authorization": f"token {self.github_token}"}  # Set headers
                        elif key == "GITHUB_USERNAME":
                            self.github_username = value.strip()  # Set GitHub username
                        elif key == "BLACKLIST":
                            self.blacklist = set(value.strip().split(','))  # Load blacklist from config

    def validate_token(self):
        """Validate the GitHub token by making a simple API request."""
        if self.github_token:  # Check if the token is set
            response = requests.get("https://api.github.com/user", headers=self.headers)  # Make a request to GitHub API
            if response.status_code != 200:  # Check if the response is not OK
                self.github_token = ""  # Reset token if invalid
                return "Invalid token."  # Return an error message
        return None  # Return None if the token is valid

    def save_config(self):
        """Save the current configuration (token, username, and blacklist) to config.txt."""
        with open('config.txt', 'w') as file:  # Open the file for writing
            file.write(f"GITHUB_TOKEN={self.github_token}\n")  # Write token
            file.write(f"GITHUB_USERNAME={self.github_username}\n")  # Write username
            file.write(f"BLACKLIST={','.join(self.blacklist)}\n")  # Write blacklist

    def api_request(self, url):
        """Generic API request handler."""
        if not self.github_token:  # Check if the token is provided
            return {"error": "No token provided."}  # Return an error message
        try:
            response = requests.get(url, headers=self.headers)  # Make the API request
            self.requests_made += 1  # Increment request counter
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()  # Return the JSON response
        except requests.RequestException as e:  # Handle any request exceptions
            return {"error": f"API Error: {str(e)}"}  # Return the error message

    def get_users(self, username, action):
        """Retrieve users (followers or following) and apply blacklist."""
        url = f"https://api.github.com/users/{username}/{action}"  # Construct the API URL
        users = []  # Initialize a list to store usernames
        page = 1  # Start from the first page
        
        while True:
            full_url = f"{url}?per_page=100&page={page}"  # URL for paginated requests
            page_users = self.api_request(full_url)  # Get users from API

            if "error" in page_users:  # Check for errors
                break

            if not page_users:  # If no more users, exit the loop
                break

            # Add users to the list if they are not in the blacklist
            users.extend(user['login'] for user in page_users if user['login'] not in self.blacklist)
            page += 1  # Move to the next page
            
        return set(users)  # Return a set of usernames to avoid duplicates

    def follow_user(self, username_to_follow):
        """Follow a user."""
        return self._manage_following("PUT", username_to_follow)  # Call the private method to follow

    def unfollow_user(self, username_to_unfollow):
        """Unfollow a user."""
        return self._manage_following("DELETE", username_to_unfollow)  # Call the private method to unfollow

    def _manage_following(self, method, username):
        """Manage following/unfollowing users."""
        url = f"https://api.github.com/user/following/{username}"  # Construct the API URL
        response = requests.request(method, url, headers=self.headers)  # Make the request (PUT/DELETE)
        self.requests_made += 1  # Increment request counter
        return response.status_code == 204  # Return True if the action was successful

    def display_rate_limits(self):
        """Display the current rate limits."""
        response = requests.get("https://api.github.com/user", headers=self.headers)  # Make a request to check rate limits
        if response.status_code == 200:  # If the response is OK
            limits = response.headers  # Get response headers
            reset_in_seconds = int(limits['X-RateLimit-Reset']) - int(time.time())  # Calculate time until reset
            return (limits['X-RateLimit-Limit'], limits['X-RateLimit-Remaining'], reset_in_seconds)  # Return limits and reset time
        else:
            raise Exception(f"Rate Limit Error: {response.status_code}")  # Raise an error for failed request

class App:
    def __init__(self, root):
        """Initialize the App class and set up the user interface."""
        self.github_manager = GitHubManager()  # Create an instance of GitHubManager
        self.root = root  # Save the root window reference
        self.setup_ui()  # Set up the user interface

    def setup_ui(self):
        """Set up the user interface."""
        self.root.title("GitHub Follower Management")  # Set the window title
        self.root.geometry("412x500")  # Set the window size
        self.root.configure(bg="#e0e0e0")  # Set the background color

        # Frame for user input
        frame_user = tk.Frame(self.root, bg="#e0e0e0", padx=20, pady=0)  # Create a frame
        frame_user.pack(pady=0)  # Add the frame to the window

        # Create input fields for GitHub username and token
        tk.Label(frame_user, text="GitHub Username:", bg="#e0e0e0").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_username = tk.Entry(frame_user, width=25)  # Entry for username
        self.entry_username.insert(0, self.github_manager.github_username)  # Pre-fill with saved username
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_user, text="GitHub Token:", bg="#e0e0e0").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_token = tk.Entry(frame_user, width=25, show="*")  # Entry for token
        self.entry_token.insert(0, self.github_manager.github_token)  # Pre-fill with saved token
        self.entry_token.grid(row=1, column=1, padx=5, pady=5)

        # Boolean variables for checkboxes
        self.var_follow_back = tk.BooleanVar()  # Follow back followers checkbox
        self.var_unfollow_non_followers = tk.BooleanVar()  # Unfollow non-followers checkbox

        # Create checkboxes for following/unfollowing options
        tk.Checkbutton(frame_user, text="Follow Back Followers", variable=self.var_follow_back, bg="#e0e0e0").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(frame_user, text="Unfollow Non-Followers", variable=self.var_unfollow_non_followers, bg="#e0e0e0").grid(row=3, column=0, sticky="w", padx=5, pady=5)

        # Create a text area for blacklist usernames
        tk.Label(frame_user, text="Blacklist Usernames (one per line):", bg="#e0e0e0").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.blacklist_entry = tk.Text(frame_user, height=5, width=20)  # Text area for blacklist
        self.blacklist_entry.insert(tk.END, "\n".join(self.github_manager.blacklist))  # Pre-fill with saved blacklist
        self.blacklist_entry.grid(row=4, column=1, padx=5, pady=5)

        # Create buttons for saving configuration and starting actions
        ttk.Button(frame_user, text="Save", command=self.update_config).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(frame_user, text="Start", command=self.start_actions).grid(row=6, column=0, columnspan=2, pady=10)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=412, mode="determinate")  # Progress bar for actions
        self.progress.pack(pady=0)  # Add progress bar to the window

        # Output area for messages
        self.text_output = tk.Text(self.root, height=15, width=58, bg="#e0e0e0", font=("Arial", 10))  # Text area for output
        self.scrollbar = tk.Scrollbar(self.root, command=self.text_output.yview)  # Scrollbar for output area
        self.text_output.config(yscrollcommand=self.scrollbar.set)  # Link scrollbar to text area
        
        self.text_output.pack(pady=0)  # Add text output area to the window

    def start_actions(self):
        """Start following and unfollowing actions based on user input."""
        self.github_manager.requests_made = 0  # Reset request counter
        self.text_output.delete(1.0, tk.END)  # Clear previous output
        username = self.entry_username.get().strip()  # Get username from entry
        token = self.entry_token.get().strip()  # Get token from entry

        self.github_manager.github_username = username  # Update manager with new username
        self.github_manager.github_token = token  # Update manager with new token

        if token:  # If token is provided
            self.github_manager.headers = {"Authorization": f"token {token}"}  # Set authorization header
            token_error = self.github_manager.validate_token()  # Validate the token
            if token_error:  # If token validation fails
                self.text_output.insert(tk.END, f"Error: {token_error}\n")  # Display error
                return
        else:
            self.text_output.insert(tk.END, "Error: No token provided.\n")  # Display error if no token
            return 

        if not username:  # Check if username is provided
            self.text_output.insert(tk.END, "Error: Please enter a username.\n")  # Display error if no username
            return

        # Retrieve followers and following lists
        followers_response = self.github_manager.get_users(username, "followers")
        if "error" in followers_response:  # Handle error in followers retrieval
            self.text_output.insert(tk.END, f"Error: {followers_response['error']}\n")
            return

        following_response = self.github_manager.get_users(username, "following")
        if "error" in following_response:  # Handle error in following retrieval
            self.text_output.insert(tk.END, f"Error: {following_response['error']}\n")
            return

        total_users = 0  # Initialize counter for total actions
        if self.var_follow_back.get():  # If follow back option is selected
            to_follow = followers_response - following_response  # Determine users to follow
            total_users += len(to_follow)  # Count total users to follow

        if self.var_unfollow_non_followers.get():  # If unfollow non-followers option is selected
            to_unfollow = following_response - followers_response  # Determine users to unfollow
            total_users += len(to_unfollow)  # Count total users to unfollow

        self.progress["maximum"] = total_users  # Set maximum for progress bar
        self.progress["value"] = 0  # Reset progress bar value

        if self.var_follow_back.get():  # Follow back users if option is selected
            to_follow = followers_response - following_response  # Get users to follow back
            for user in to_follow:  # Iterate over each user
                if self.github_manager.follow_user(user):  # Follow user
                    self.text_output.insert(tk.END, f"Followed {user}\n")  # Output success message
                    self.progress["value"] += 1  # Update progress bar
                    self.root.update_idletasks()  # Update UI

        if self.var_unfollow_non_followers.get():  # Unfollow users if option is selected
            to_unfollow = following_response - followers_response  # Get users to unfollow
            for user in to_unfollow:  # Iterate over each user
                if self.github_manager.unfollow_user(user):  # Unfollow user
                    self.text_output.insert(tk.END, f"Unfollowed {user}\n")  # Output success message
                    self.progress["value"] += 1  # Update progress bar
                    self.root.update_idletasks()  # Update UI

        self.display_rate_limits()  # Display rate limits after actions

    def display_rate_limits(self):
        """Display the current rate limits after actions are performed."""
        try:
            rate_limit, remaining, reset_in_seconds = self.github_manager.display_rate_limits()  # Get rate limits

            output = (
                f"Total requests made: {self.github_manager.requests_made} | "
                f"Rate Limit: {rate_limit} | "
                f"Requests Remaining: {remaining} | "
                f"Rate Limit Reset in: {reset_in_seconds // 60} minutes {reset_in_seconds % 60} seconds\n"
            )  # Format output string

            self.text_output.insert(tk.END, output)  # Display rate limit information
        except Exception as e:  # Handle any exceptions
            self.text_output.insert(tk.END, str(e) + "\n")  # Display error message

    def update_config(self):
        """Update the configuration based on user input and save to config.txt."""
        users = self.blacklist_entry.get("1.0", tk.END).strip().splitlines()  # Get blacklist from text area
        self.github_manager.blacklist = {user.strip() for user in users if user.strip()}  # Update blacklist
        self.github_manager.github_username = self.entry_username.get().strip()  # Update username
        self.github_manager.github_token = self.entry_token.get().strip()  # Update token
        self.github_manager.save_config()  # Save updated configuration
        self.text_output.insert(tk.END, "Configuration has been updated successfully.\n")  # Display success message

if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    app = App(root)  # Create an instance of the App class
    root.mainloop()  # Start the GUI event loop
