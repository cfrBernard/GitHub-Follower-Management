import requests

# Replace with your personal GitHub API token
GITHUB_TOKEN = 'your_github_token'
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_followers(username):
    url = f"https://api.github.com/users/{username}/followers"
    response = requests.get(url, headers=headers)
    return [user['login'] for user in response.json()]

def get_following(username):
    url = f"https://api.github.com/users/{username}/following"
    response = requests.get(url, headers=headers)
    return [user['login'] for user in response.json()]

def follow_user(username_to_follow):
    url = f"https://api.github.com/user/following/{username_to_follow}"
    response = requests.put(url, headers=headers)
    return response.status_code == 204

def unfollow_user(username_to_unfollow):
    url = f"https://api.github.com/user/following/{username_to_unfollow}"
    response = requests.delete(url, headers=headers)
    return response.status_code == 204

# Example of usage
username = "your_username"
followers = set(get_followers(username))
following = set(get_following(username))

# Follow those who follow you
follow_back = True 

if follow_back:
    for user in followers - following:
        follow_user(user)

# Unfollow those who do not follow you
unfollow_non_followers = True 

if unfollow_non_followers:
    for user in following - followers:
        unfollow_user(user)
