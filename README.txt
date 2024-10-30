GO on release page for the app ! 

# GitHub Follower Management Script
This Python script allows you to manage your GitHub subscriptions through a GUI. It can automatically follow users who follow you back, unfollow those who do not, and manage a blacklist of users to ignore.

## Features:
- Follow Back Followers
- Unfollow Non-Followers
- Blacklist Management
- Rate Limit Monitoring

## Prerequisites:
- Python 3.x installed on your machine.
- A personal access token from GitHub with the necessary permissions to manage your subscriptions.


## Installation:
1. Clone this repository or download the script.
   ```bash
   git clone https://github.com/cfrBernard/GitHub-Follower-Management.git
   cd GitHub-Follower-Management

2. Install the required libraries. You can install the requests library using pip:
   ```bash
   pip install requests
   
   Note: tkinter comes pre-installed with Python on most systems, but you can check if it's available by trying to import it in a Python shell.


## Configuration:
1. Create a config.txt file in the same directory as the script.

2. Add the following lines to config.txt:
   GITHUB_TOKEN=your_personal_access_token
   GITHUB_USERNAME=your_github_username
   BLACKLIST=user1,user2,user3  # comma-separated list of usernames to ignore

3. Run the script:
   ```bash
   python github_followback.py

4. The GUI will appear. You can adjust settings as needed.


## Usage:
1. Enter your GitHub username in the GUI.

2. Enable or disable features:
   - Follow Back Followers: Check this box to automatically follow back users who follow you.
   - Unfollow Non-Followers: Check this box to unfollow users who do not follow you back.

3. Manage the blacklist by entering usernames in the designated text area (one per line).

4. Click the Start button to begin processing.


## Warning:
- Respect GitHub's API Rate Limits: Make sure not to abuse GitHub's API requests. You are allowed 5000 requests per hour if authenticated.
- Use at Your Own Risk: Always review your subscriptions before performing bulk actions.


## GitHub API Rate Limits
- Authenticated accounts: 5000 requests per hour.
- Unauthenticated users: 60 requests per hour.

### Example Request Calculation
For instance, with:

- 150 followers
- 120 following
- 10 new followers to follow
- 5 who don't follow back

You will make approximately:

- 5 requests for followers
- 4 requests for following
- 10 requests to follow new followers
- 5 requests to unfollow

**Total**: 24 requests (well within the limit for authenticated users).

*Note: Rate limit information will be displayed in the GUI.*


# License
This project is licensed under the MIT License. See the LICENSE file for details.