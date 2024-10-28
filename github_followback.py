import requests

# Replace with your personal GitHub API token
GITHUB_TOKEN = 'your_github_token'
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_followers(username):
    followers = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/followers?per_page=100&page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            page_followers = response.json()
            if not page_followers:
                break
            followers.extend(user['login'] for user in page_followers)
            page += 1
    return followers

def get_following(username):
    following = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/following?per_page=100&page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            page_following = response.json()
            if not page_following:
                break
            following.extend(user['login'] for user in page_following)
            page += 1
    return following

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
follow_back = False

if follow_back:
    for user in followers - following:
        if follow_user(user):
            print(f"Followed {user}")

# Unfollow those who do not follow you
unfollow_non_followers = True

if unfollow_non_followers:
    for user in following - followers:
        if unfollow_user(user):
            print(f"Unfollowed {user}")


# Retrieve and display rate limit info
response = requests.get(f'https://api.github.com/user', headers=headers)  
if response.status_code == 200:
    
    print("Status Code:", response.status_code) 

    print("Rate Limit:", response.headers['X-RateLimit-Limit'])    
    print("Requests Remaining:", response.headers['X-RateLimit-Remaining']) 
    print("Rate Limit Reset:", response.headers['X-RateLimit-Reset'])     
else:
    print("Failed to retrieve rate limit information. Status Code:", response.status_code)
    print("Response:", response.json())  