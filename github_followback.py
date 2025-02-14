import requests  
import tkinter as tk  
from tkinter import ttk  
import time 
import os 

class GitHubManager:
    def __init__(self):
        """Initialize the GitHubManager class and load configuration."""
        self.requests_made = 0  
        self.blacklist = set() 
        self.github_token = ""  
        self.github_username = ""  
        self.headers = {}  
        self.load_config()  
        self.validate_token()  

    def load_config(self):
        """Load GitHub token, username, and blacklist from config.txt."""
        if os.path.exists('config.txt'): 
            with open('config.txt', 'r') as file:  
                for line in file:
                    line = line.strip()  
                    if "=" in line:  
                        key, value = line.split('=', 1)  
                        if key == "GITHUB_TOKEN":
                            self.github_token = value.strip()  
                            self.headers = {"Authorization": f"token {self.github_token}"} 
                        elif key == "GITHUB_USERNAME":
                            self.github_username = value.strip() 
                        elif key == "BLACKLIST":
                            self.blacklist = set(value.strip().split(','))  

    def validate_token(self):
        """Validate the GitHub token by making a simple API request."""
        if self.github_token: 
            response = requests.get("https://api.github.com/user", headers=self.headers) 
            if response.status_code != 200: 
                self.github_token = ""  
                return "Invalid token." 
        return None 

    def save_config(self):
        """Save the current configuration (token, username, and blacklist) to config.txt."""
        with open('config.txt', 'w') as file: 
            file.write(f"GITHUB_TOKEN={self.github_token}\n")  
            file.write(f"GITHUB_USERNAME={self.github_username}\n") 
            file.write(f"BLACKLIST={','.join(self.blacklist)}\n") 

    def api_request(self, url):
        """Generic API request handler."""
        if not self.github_token:
            return {"error": "No token provided."}  
        try:
            response = requests.get(url, headers=self.headers) 
            self.requests_made += 1 
            response.raise_for_status() 
            return response.json()  
        except requests.RequestException as e:  
            return {"error": f"API Error: {str(e)}"}  

    def get_users(self, username, action):
        """Retrieve users (followers or following) and apply blacklist."""
        url = f"https://api.github.com/users/{username}/{action}" 
        users = []  
        page = 1  
        
        while True:
            full_url = f"{url}?per_page=100&page={page}"  
            page_users = self.api_request(full_url) 

            if "error" in page_users: 
                break

            if not page_users: 
                break

            
            users.extend(user['login'] for user in page_users if user['login'] not in self.blacklist)
            page += 1 
            
        return set(users)  

    def follow_user(self, username_to_follow):
        """Follow a user."""
        return self._manage_following("PUT", username_to_follow)  

    def unfollow_user(self, username_to_unfollow):
        """Unfollow a user."""
        return self._manage_following("DELETE", username_to_unfollow) 

    def _manage_following(self, method, username):
        """Manage following/unfollowing users."""
        url = f"https://api.github.com/user/following/{username}"  
        response = requests.request(method, url, headers=self.headers) 
        self.requests_made += 1 
        return response.status_code == 204 

    def display_rate_limits(self):
        """Display the current rate limits."""
        response = requests.get("https://api.github.com/user", headers=self.headers)
        if response.status_code == 200: 
            limits = response.headers 
            reset_in_seconds = int(limits['X-RateLimit-Reset']) - int(time.time()) 
            return (limits['X-RateLimit-Limit'], limits['X-RateLimit-Remaining'], reset_in_seconds)
        else:
            raise Exception(f"Rate Limit Error: {response.status_code}")  

class App:
    def __init__(self, root):
        """Initialize the App class and set up the user interface."""
        self.github_manager = GitHubManager() 
        self.root = root 
        self.setup_ui()  

    def setup_ui(self):
        """Set up the user interface."""
        self.root.title("GitHub Follower Management")  
        self.root.geometry("412x500") 
        self.root.configure(bg="#e0e0e0")  

        
        frame_user = tk.Frame(self.root, bg="#e0e0e0", padx=20, pady=0) 
        frame_user.pack(pady=0) 

        
        tk.Label(frame_user, text="GitHub Username:", bg="#e0e0e0").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_username = tk.Entry(frame_user, width=25) 
        self.entry_username.insert(0, self.github_manager.github_username)  
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_user, text="GitHub Token:", bg="#e0e0e0").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_token = tk.Entry(frame_user, width=25, show="*") 
        self.entry_token.insert(0, self.github_manager.github_token)  
        self.entry_token.grid(row=1, column=1, padx=5, pady=5)

        
        self.var_follow_back = tk.BooleanVar()  
        self.var_unfollow_non_followers = tk.BooleanVar()  

        
        tk.Checkbutton(frame_user, text="Follow Back Followers", variable=self.var_follow_back, bg="#e0e0e0").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(frame_user, text="Unfollow Non-Followers", variable=self.var_unfollow_non_followers, bg="#e0e0e0").grid(row=3, column=0, sticky="w", padx=5, pady=5)

        
        tk.Label(frame_user, text="Blacklist Usernames (one per line):", bg="#e0e0e0").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.blacklist_entry = tk.Text(frame_user, height=5, width=20) 
        self.blacklist_entry.insert(tk.END, "\n".join(self.github_manager.blacklist))
        self.blacklist_entry.grid(row=4, column=1, padx=5, pady=5)

        
        ttk.Button(frame_user, text="Save", command=self.update_config).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(frame_user, text="Start", command=self.start_actions).grid(row=6, column=0, columnspan=2, pady=10)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=412, mode="determinate")  
        self.progress.pack(pady=0)

        # Output area for messages
        self.text_output = tk.Text(self.root, height=15, width=58, bg="#e0e0e0", font=("Arial", 10)) 
        self.scrollbar = tk.Scrollbar(self.root, command=self.text_output.yview)  
        self.text_output.config(yscrollcommand=self.scrollbar.set)  
        
        self.text_output.pack(pady=0) 

    def start_actions(self):
        """Start following and unfollowing actions based on user input."""
        self.github_manager.requests_made = 0 
        self.text_output.delete(1.0, tk.END)  
        username = self.entry_username.get().strip()  
        token = self.entry_token.get().strip()

        self.github_manager.github_username = username 
        self.github_manager.github_token = token 

        if token: 
            self.github_manager.headers = {"Authorization": f"token {token}"} 
            token_error = self.github_manager.validate_token()  
            if token_error: 
                self.text_output.insert(tk.END, f"Error: {token_error}\n") 
                return
        else:
            self.text_output.insert(tk.END, "Error: No token provided.\n")  
            return 

        if not username: 
            self.text_output.insert(tk.END, "Error: Please enter a username.\n") 
            return

        
        followers_response = self.github_manager.get_users(username, "followers")
        if "error" in followers_response: 
            self.text_output.insert(tk.END, f"Error: {followers_response['error']}\n")
            return

        following_response = self.github_manager.get_users(username, "following")
        if "error" in following_response:  
            self.text_output.insert(tk.END, f"Error: {following_response['error']}\n")
            return

        total_users = 0 
        if self.var_follow_back.get(): 
            to_follow = followers_response - following_response  
            total_users += len(to_follow) 

        if self.var_unfollow_non_followers.get():  
            to_unfollow = following_response - followers_response  
            total_users += len(to_unfollow)  

        self.progress["maximum"] = total_users  
        self.progress["value"] = 0 

        if self.var_follow_back.get(): 
            to_follow = followers_response - following_response 
            for user in to_follow:  
                if self.github_manager.follow_user(user):  
                    self.text_output.insert(tk.END, f"Followed {user}\n") 
                    self.progress["value"] += 1 
                    self.root.update_idletasks() 

        if self.var_unfollow_non_followers.get():  
            to_unfollow = following_response - followers_response  
            for user in to_unfollow:  
                if self.github_manager.unfollow_user(user): 
                    self.text_output.insert(tk.END, f"Unfollowed {user}\n") 
                    self.progress["value"] += 1 
                    self.root.update_idletasks() 

        self.display_rate_limits() 

    def display_rate_limits(self):
        """Display the current rate limits after actions are performed."""
        try:
            rate_limit, remaining, reset_in_seconds = self.github_manager.display_rate_limits() 

            output = (
                f"Total requests made: {self.github_manager.requests_made} | "
                f"Rate Limit: {rate_limit} | "
                f"Requests Remaining: {remaining} | "
                f"Rate Limit Reset in: {reset_in_seconds // 60} minutes {reset_in_seconds % 60} seconds\n"
            )  

            self.text_output.insert(tk.END, output) 
        except Exception as e: 
            self.text_output.insert(tk.END, str(e) + "\n")  

    def update_config(self):
        """Update the configuration based on user input and save to config.txt."""
        users = self.blacklist_entry.get("1.0", tk.END).strip().splitlines() 
        self.github_manager.blacklist = {user.strip() for user in users if user.strip()}  
        self.github_manager.github_username = self.entry_username.get().strip()  
        self.github_manager.github_token = self.entry_token.get().strip() 
        self.github_manager.save_config()
        self.text_output.insert(tk.END, "Configuration has been updated successfully.\n") 

if __name__ == "__main__":
    root = tk.Tk() 
    app = App(root)  
    root.mainloop()  
