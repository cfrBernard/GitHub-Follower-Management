import requests
import tkinter as tk
from tkinter import messagebox, ttk
import time
import os

class GitHubManager:
    def __init__(self):
        self.requests_made = 0
        self.blacklist = set()
        self.github_token = ""
        self.github_username = ""
        self.headers = {}
        self.load_config()

    def load_config(self):
        """ Load GitHub token, username, and blacklist from config.txt """
        if os.path.exists('config.txt'):
            with open('config.txt', 'r') as file:
                for line in file:
                    if line.startswith("GITHUB_TOKEN="):
                        self.github_token = line.split('=')[1].strip()
                        self.headers = {"Authorization": f"token {self.github_token}"}
                    elif line.startswith("GITHUB_USERNAME="):
                        self.github_username = line.split('=')[1].strip()
                    elif line.startswith("BLACKLIST="):
                        blacklist_users = line.split('=')[1].strip()
                        self.blacklist = set(blacklist_users.split(','))
        else:
            raise FileNotFoundError("Configuration file config.txt not found.")

    def save_blacklist(self):
        """ Save the current blacklist to config.txt """
        with open('config.txt', 'r') as file:
            lines = file.readlines()
        with open('config.txt', 'w') as file:
            for line in lines:
                if line.startswith("BLACKLIST="):
                    file.write(f"BLACKLIST={','.join(self.blacklist)}\n")
                else:
                    file.write(line)

    def api_request(self, url):
        """ Generic API request handler """
        response = requests.get(url, headers=self.headers)
        self.requests_made += 1 
        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code}")
        return response.json()

    def get_followers(self, username):
        return self._get_users(f"https://api.github.com/users/{username}/followers")

    def get_following(self, username):
        return self._get_users(f"https://api.github.com/users/{username}/following")

    def _get_users(self, url):
        """ Retrieve users (followers or following) and apply blacklist """
        users = []
        page = 1
        while True:
            full_url = f"{url}?per_page=100&page={page}"
            try:
                page_users = self.api_request(full_url)
            except Exception as e:
                messagebox.showerror("Error", str(e))
                break

            if not page_users:
                break
            
            users.extend(user['login'] for user in page_users if user['login'] not in self.blacklist)
            page += 1
        return set(users)

    def follow_user(self, username_to_follow):
        return self._manage_following("PUT", username_to_follow)

    def unfollow_user(self, username_to_unfollow):
        return self._manage_following("DELETE", username_to_unfollow)

    def _manage_following(self, method, username):
        """ Manage following/unfollowing users """
        url = f"https://api.github.com/user/following/{username}"
        response = requests.request(method, url, headers=self.headers)
        self.requests_made += 1
        return response.status_code == 204

    def display_rate_limits(self):
        response = requests.get("https://api.github.com/user", headers=self.headers)
        if response.status_code == 200:
            limits = response.headers
            reset_in_seconds = int(limits['X-RateLimit-Reset']) - int(time.time())
            return (limits['X-RateLimit-Limit'], limits['X-RateLimit-Remaining'], reset_in_seconds)
        else:
            raise Exception(f"Rate Limit Error: {response.status_code}")

class App:
    def __init__(self, root):
        self.github_manager = GitHubManager()
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.root.title("GitHub Subscription Manager")
        self.root.geometry("600x600")
        self.root.configure(bg="#f0f0f0")

        frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20)
        frame.pack(pady=10)

        tk.Label(frame, text="GitHub Username:", bg="#ffffff").grid(row=0, column=0, sticky="e")
        self.entry_username = tk.Entry(frame, width=25)
        self.entry_username.insert(0, self.github_manager.github_username)  # Insert username from config
        self.entry_username.grid(row=0, column=1)

        self.var_follow_back = tk.BooleanVar()
        self.var_unfollow_non_followers = tk.BooleanVar()

        tk.Checkbutton(frame, text="Follow Back Followers", variable=self.var_follow_back, bg="#ffffff").grid(row=1, column=0, sticky="w")
        tk.Checkbutton(frame, text="Unfollow Non-Followers", variable=self.var_unfollow_non_followers, bg="#ffffff").grid(row=2, column=0, sticky="w")

        tk.Label(frame, text="Blacklist Usernames (one per line):", bg="#ffffff").grid(row=3, column=0, sticky="e")
        self.blacklist_entry = tk.Text(frame, height=5, width=20)
        self.blacklist_entry.insert(tk.END, "\n".join(self.github_manager.blacklist))  # Load blacklist from config
        self.blacklist_entry.grid(row=3, column=1)

        ttk.Button(frame, text="Update Blacklist", command=self.update_blacklist).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Start", command=self.start_actions).grid(row=5, column=0, columnspan=2, pady=10)

        self.text_output = tk.Text(self.root, height=15, width=70, bg="#f0f0f0", font=("Arial", 10))
        self.text_output.pack(pady=10)

    def start_actions(self):
        self.github_manager.requests_made = 0
        self.text_output.delete(1.0, tk.END)
        username = self.entry_username.get().strip()

        if not username:
            messagebox.showwarning("Warning", "Please enter a username.")
            return

        followers = self.github_manager.get_followers(username)
        following = self.github_manager.get_following(username)

        if self.var_follow_back.get():
            to_follow = followers - following
            for user in to_follow:
                if self.github_manager.follow_user(user):
                    self.text_output.insert(tk.END, f"Followed {user}\n")

        if self.var_unfollow_non_followers.get():
            to_unfollow = following - followers
            for user in to_unfollow:
                if self.github_manager.unfollow_user(user):
                    self.text_output.insert(tk.END, f"Unfollowed {user}\n")

        self.display_rate_limits()

    def display_rate_limits(self):
        try:
            rate_limit, remaining, reset_in_seconds = self.github_manager.display_rate_limits()
            self.text_output.insert(tk.END, f"Total requests made: {self.github_manager.requests_made}\n")
            self.text_output.insert(tk.END, f"Rate Limit: {rate_limit}\nRequests Remaining: {remaining}\n")
            self.text_output.insert(tk.END, f"Rate Limit Reset in: {reset_in_seconds // 60} minutes {reset_in_seconds % 60} seconds\n")
        except Exception as e:
            self.text_output.insert(tk.END, str(e) + "\n")

    def update_blacklist(self):
        users = self.blacklist_entry.get("1.0", tk.END).strip().splitlines()
        self.github_manager.blacklist = {user.strip() for user in users if user.strip()}
        self.github_manager.save_blacklist() 
        messagebox.showinfo("Blacklist Updated", "The blacklist has been updated successfully.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
