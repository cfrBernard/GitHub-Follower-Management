---

## ⚠️ Important Notice // (01/31/2025) 

Please be aware that all versions of this tool currently suffer from a major bug affecting accounts with thousands of followers or following.

If this is your case, do not use the tool for now — pagination and large user list handling are unstable and may lead to incorrect result

> A fix is in progress. Thank you for your patience!

## Progress Update // (02/15–02/19/2025)

A new CLI script (app.py) is available in the dev branch.
It refactors and improves core logic for data collection, and is significantly more robust.

### Key CLI Features:

- Error detection with process halt
- API rate-limit awareness
- Dry-run mode with confirmation prompts
- Automatic follow/unfollow
- Stats display (followers/following, API remaining)
- Blacklist support

> GUI development is planned but not started yet.

---

# GitHub Follower Management Script

[**Download the latest version here**](https://github.com/cfrBernard/GitHub-Follower-Management/releases)

![Version](https://img.shields.io/badge/version-v2.2.0-blue)
![License](https://img.shields.io/github/license/cfrBernard/MaskMapWizard)

## Features:
- **Follow Back Followers**: Automatically follow back users who follow you.
- **Unfollow Non-Followers**: Unfollow users who don't follow you back.
- **Blacklist Management**: Manage a list of users to ignore for follow/unfollow actions.
- **Rate Limit Monitoring**: Track and manage API rate limits to avoid hitting them.

> ⚠️ The GUI is still based on the older code and shares the known bug with large accounts.

---

## 🛠 Recommended (Dev/CLI):

If you’re comfortable with the command line, use the new CLI version from the dev branch:

### Prerequisites:
- Python 3.x installed on your machine.
- A personal access token from GitHub with the necessary permissions to manage your subscriptions.

### Installation:
1. Clone this repository or download the script:
    ```bash
    git clone https://github.com/cfrBernard/GitHub-Follower-Management.git
    cd GitHub-Follower-Management
    git checkout dev
    ```

    > **Note**: Using a .venv is highly recommended.
   
3. Install the required libraries:
    ```bash
    pip install requests
    ```

### Configuration:
1. Create a `config.txt` file in the same directory as the script.
2. Add the following lines to `config.txt`:
    ```text
    GITHUB_TOKEN=your_personal_access_token
    GITHUB_USERNAME=your_github_username
    BLACKLIST=user1,user2,user3  # comma-separated list of usernames to ignore
    ```
3. Run the script:
    ```bash
    python app.py
    ```
    > The script will perform a dry-run and ask for confirmation before executing any actions.

---

## API Rate Limits:
- **Authenticated users**: 5000 requests/hour
- **Unauthenticated users**: 60 requests/hour

> **Example**: For 150 followers, 120 following, and actions like following 10 new users and unfollowing 5, only 24 requests are used—well within the authenticated limit.

---

## License: 
This project is licensed under the MIT License. See the [LICENSE](./LICENSE.md) file for details.

---

> **Note**: A MacOS version will be released in the future. Maybe..
