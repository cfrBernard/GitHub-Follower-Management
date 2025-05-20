---

## ⚠️ Important Notice // (01/31/2025) 

Please be aware that all versions of this tool currently have a **major issue** that affects users with several thousand followers/following.

If your account has **thousands of followers or following**, **I strongly advise against using this tool at the moment**. There are known issues with pagination and the handling of large user lists, which may result in incomplete or incorrect data being processed.

> **I am actively working on fixing this issue**, and a more stable version will be available soon. Thank you for your patience and understanding!

## Progress Update // (02/15/2025)

I have made progress on the refactoring and created a test script (`app.py` in the `dev` branch) that focuses solely on data collection. The script is highly robust, and everything appears to be functioning correctly. The next step is to rebuild the application around this script.

## Progress Update // (02/19/2025)

### Features Implemented (app.py):

1. Error Checking and Halt on Failure: Stops the process if data retrieval fails.
2. Request Security: Monitors API limits and halts requests when approaching limits.
3. Dry Run Mode: Displays planned actions without executing them, with user confirmation.
4. Automatic Follow/Unfollow: Enables or disables follow/unfollow actions.
5. Statistics Display: Shows follower/following stats and remaining requests.
6. Blacklist Management: Allows management of a blacklist to ignore certain users.

- GUI Development: Planned as the next major step, focusing on user interface and experience.

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

---

## 🛠 Development Setup

### Prerequisites:
- Python 3.x installed on your machine.
- A personal access token from GitHub with the necessary permissions to manage your subscriptions.

### Installation:
1. Clone this repository or download the script:
    ```bash
    git clone https://github.com/cfrBernard/GitHub-Follower-Management.git
    cd GitHub-Follower-Management
    ```
2. Install the required libraries:
    ```bash
    pip install requests
    ```
   **Note**: `tkinter` comes pre-installed with Python on most systems, but you can check if it's available by trying to import it in a Python shell.

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
    python github_followback.py
    ```
4. The GUI will appear, and you can adjust settings as needed.

## Usage:
1. Enter your GitHub username and token in the provided fields.
2. Enter any usernames you want to ignore in the designated text area. Each username should be on a new line.
3. After entering or changing any settings, click the **Update Config** button to save the changes.
4. After configuring your settings, click the **Start** button.
    - The application will display output messages in the text area, informing you about the actions taken and requests limit.

## API Rate Limits:
- **Authenticated users**: 5000 requests/hour
- **Unauthenticated users**: 60 requests/hour

> **Example**: For 150 followers, 120 following, and actions like following 10 new users and unfollowing 5, only 24 requests are used—well within the authenticated limit.

---

## License: 
This project is licensed under the MIT License. See the [LICENSE](./LICENSE.md) file for details.

---

> **Note**: A MacOS version will be released in the future. Maybe..
