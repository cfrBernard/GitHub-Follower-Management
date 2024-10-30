GO on release page for the app ! 

# GitHub Follower Management Script
This Python script allows you to manage your GitHub subscriptions through a GUI. It can automatically follow users who follow you back, unfollow those who do not, and manage a blacklist of users to ignore.


## Features:
- Follow Back Followers
- Unfollow Non-Followers
- Blacklist Management
- Rate Limit Monitoring


## Quick Download
For the latest `.exe` version, go to [Releases](https://github.com/cfrBernard/GitHub-Follower-Management/releases).


## Prerequisites:
- Python 3.x installed on your machine.
- A personal access token from GitHub with the necessary permissions to manage your subscriptions.


## Installation:
1. Clone this repository or download the script.
  - git clone https://github.com/cfrBernard/GitHub-Follower-Management.git
  - cd GitHub-Follower-Management
2. Install the required libraries. You can install the requests library using pip:
  - pip install requests
   
Note: tkinter comes pre-installed with Python on most systems, but you can check if it's available by trying to import it in a Python shell.


## Configuration:
1. Create a config.txt file in the same directory as the script.
2. Add the following lines to config.txt:
  - GITHUB_TOKEN=your_personal_access_token
  - GITHUB_USERNAME=your_github_username
  - BLACKLIST=user1,user2,user3  # comma-separated list of usernames to ignore
3. Run the script:
  - python github_followback.py
4. The GUI will appear. You can adjust settings as needed.


## Usage:
1. Enter your GitHub username.
2. Select options:
  - Follow Back Followers: Auto-follow back.
  - Unfollow Non-Followers: Unfollow those who don’t follow back.
3. Add users to the blacklist in the text area (one per line).
4. Click Start to process the selected actions.


## API Rate Limits:
Authenticated users: 5000 requests/hour
Unauthenticated users: 60 requests/hour
Example: For 150 followers, 120 following, and actions like following 10 new users and unfollowing 5, only 24 requests are used—well within the authenticated limit.


# License: 
This project is licensed under the MIT License. See the LICENSE file for details.