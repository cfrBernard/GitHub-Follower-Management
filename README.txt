# GitHub Follower Management Script

This Python script allows you to manage your GitHub subscriptions. It can automatically follow users who follow you back and unfollow those who do not.

### Prerequisites

- Python 3.x installed on your machine.
- A personal access token from GitHub with the necessary permissions to manage your subscriptions.


### Installation

1. Clone this repository or download the script.
2. Install the `requests` library if you haven't already. You can install it using pip:

   ```bash
   pip install requests


### Configuration

1. Open the Python script in a text editor.
2. Replace GITHUB_TOKEN with your personal GitHub access token:
3. Set the GitHub username for which you want to manage subscriptions:
4. Use the following variables to enable or disable features:
   
   follow_back = True    # Follow users who follow you
   unfollow_non_followers = True   # Unfollow users who do not follow you

To execute both actions, set both to True.

5. Run the script: python your_script.py


### Warning

- Make sure not to abuse GitHub's API requests. Respect the rate limits to avoid being blocked.
- Use this script at your own risk. Always check your subscriptions before performing bulk actions.


# License

This project is licensed under the MIT License. See the docs/LICENSE file for details.