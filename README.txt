# GitHub Follower Management Script 

This Python script allows you to manage your GitHub subscriptions through a graphical user interface (GUI). It can automatically follow users who follow you back, unfollow those who do not, and manage a blacklist of users to ignore.

### Features:
- **Follow Back Followers**: Automatically follow users who follow you.
- **Unfollow Non-Followers**: Unfollow users who do not follow you back.
- **Blacklist Management**: Load and save a list of users to ignore during operations.
- **Rate Limit Monitoring**: Displays API usage and remaining requests.

### Prerequisites:
- Python 3.x installed on your machine.
- A personal access token from GitHub with the necessary permissions to manage your subscriptions.

### Installation:
1. Clone this repository or download the script.
2. Install the `requests` library and `tkinter` if you haven't already. You can install the requests library using pip:

   ```bash
   pip install requests


### Configuration:
1. Open the Python script in a text editor.
2. Replace GITHUB_TOKEN with your personal GitHub access token.
3. Run the script: python your_script.py
4. Set the GitHub username for which you want to manage subscriptions in the GUI.
5. Use the GUI to enable or disable features.


### Warning:
- Make sure not to abuse GitHub's API requests. Respect the rate limits to avoid being blocked. 
- Use this script at your own risk. Always check your subscriptions before performing bulk actions.


# License:
This project is licensed under the MIT License. See the docs/LICENSE file for details.


* GitHub API Rate Limits:
All authenticated GitHub accounts are allowed 5000 requests per hour to access the GitHub API. Unauthenticated users (i.e., those who have not provided an authentication token) have a much lower limit of 60 requests per hour.

Example Request Calculation
Let's imagine you have:

150 followers
120 people you are following
10 new followers to follow
5 people you are following who no longer follow you
The total number of requests would be as follows:

5 requests to retrieve followers (get_followers) (150 / 30).
4 requests to retrieve following (get_following) (120 / 30).
10 requests to follow new followers.
5 requests to unfollow certain people.
Total: 24 requests

This script operates well within the 5000 requests per hour limit for authenticated users.