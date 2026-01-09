# GitHub Follower Management Script

[![Version](https://img.shields.io/badge/version-v3.0.0-blue)](https://github.com/cfrBernard/GitHub-Follower-Management/releases)
[![License](https://img.shields.io/github/license/cfrBernard/MaskMapWizard)](./LICENSE.md)

## Features
- **Follow Back Followers**: Automatically follow back users who follow you.
- **Unfollow Non-Followers**: Unfollow users who don't follow you back.
- **Blacklist Management**: Manage a list of users to ignore for follow/unfollow actions.
- **Rate Limit Monitoring**: Track and manage API rate limits to avoid hitting them.

---

## Current Status

GitHub-Follower-Management is currently **CLI-first**.

The previous GUI (v2.x) had critical issues with large accounts and has been deprecated.

> A new GUI may come back in a future version.

---

## 🛠 Setup

### Prerequisites:
- Python 3.x installed on your machine.
- A personal access token from GitHub with the necessary permissions to manage your subscriptions.

### Installation:
1. Clone this repository or download the script:
    ```
    git clone https://github.com/cfrBernard/GitHub-Follower-Management.git
    cd GitHub-Follower-Management
    ```

    > Using a .venv is highly recommended.
   
3. Install the required libraries:
    ```
    pip install requests
    ```

### Configuration
1. Create a `config.txt` file in the same directory as the script.
2. Add the following lines to `config.txt`:
    ```
    GITHUB_TOKEN=your_personal_access_token
    GITHUB_USERNAME=your_github_username
    BLACKLIST=user1,user2,user3  # comma-separated list of usernames to ignore
    ```
3. Run the script:
    ```
    python app.py
    ```
    > The script will perform a dry-run and ask for confirmation before executing any actions.

---

## API Rate Limits
- **Authenticated users**: 5000 requests/hour
- **Unauthenticated users**: 60 requests/hour

> **Example**: For 150 followers, 120 following, and actions like following 10 new users and unfollowing 5, only 24 requests are used—well within the authenticated limit.

---

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE.md) file for details.
