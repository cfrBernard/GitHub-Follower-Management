import requests
import time

def read_config(file_path):
    """Reads configuration from a specified file and returns it as a dictionary."""
    config = {}
    with open(file_path, "r") as file:
        for line in file:
            key, value = line.strip().split("=")
            # Split blacklist values by comma
            config[key] = value.split(",") if key == "BLACKLIST" else value
    return config

# Read configuration values
config = read_config("config.txt")
GITHUB_TOKEN = config["GITHUB_TOKEN"]
GITHUB_USERNAME = config["GITHUB_USERNAME"]
BLACKLIST = set(config["BLACKLIST"])
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# Flags for enabling follow/unfollow actions
enable_follow = True
enable_unfollow = True

def check_rate_limit():
    """Checks the current rate limit status of the GitHub API."""
    url = "https://api.github.com/rate_limit"
    response = requests.get(url, headers=HEADERS)
    rate_limit_data = response.json()
    remaining = rate_limit_data['resources']['core']['remaining']
    reset = rate_limit_data['resources']['core']['reset']
    return remaining, reset

def api_request(url, retries=3, delay=5):
    """Makes a request to the specified URL with retry logic."""
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS)
            remaining = response.headers.get('X-RateLimit-Remaining')
            reset = response.headers.get('X-RateLimit-Reset')
            
            # Warn if rate limit is low
            if remaining is not None and int(remaining) < 100:
                print(f"⚠️ API rate limit approaching: {remaining} requests left. Reset in {reset} seconds.")
                return None

            # Return JSON response if successful
            if response.status_code == 200:
                return response.json()
            else:
                print(f"⚠️ API Error {response.status_code}: {response.text}")
        except requests.RequestException as e:
            print(f"❌ Connection error: {e}")

        print(f"⏳ Retrying ({attempt+1}/{retries}) in {delay} seconds...")
        time.sleep(delay)
    
    print("🚨 Failure after multiple attempts. Stopping process.")
    return None

def get_users_list(username, action):
    """Retrieves the full list of followers or following with pagination handling."""
    url = f"https://api.github.com/users/{username}/{action}?per_page=100"
    users = []

    while url:
        print(f"🔄 Retrieving {url}...")
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"⚠️ API Error {response.status_code}: {response.text}")
            break

        page_data = response.json()
        # Filter out blacklisted users
        users.extend(user['login'] for user in page_data if user['login'] not in BLACKLIST)
        print(f"📄 Page retrieved: {len(page_data)} users")
        
        # Check for next page
        if 'Link' in response.headers:
            links = response.headers['Link'].split(',')
            next_url = None
            for link in links:
                if 'rel=\"next\"' in link:
                    next_url = link[link.find('<') + 1:link.find('>')]
                    break
            url = next_url
        else:
            url = None

    return set(users)

def dry_run(followers, following):
    """Plans follow/unfollow actions and prompts for confirmation."""
    global enable_follow, enable_unfollow  

    to_follow = followers - following - BLACKLIST
    to_unfollow = following - followers - BLACKLIST

    print("\n🔄 Planned actions:")
    if enable_follow:
        print(f"👥 Users to follow: {len(to_follow)}")
    if enable_unfollow:
        print(f"👥 Users to unfollow: {len(to_unfollow)}")

    if not enable_follow and not enable_unfollow:
        print("✅ No actions to perform.")
        return True

    while True:
        choice = input("\n⚡ Do you want to continue? (y/n) ").strip().lower()
        if choice == "y":
            print("✅ Starting actions...")
            return True
        elif choice == "n":
            print("❌ Operation canceled.")
            exit(0)
        else:
            print("⚠️ Invalid input. Type 'y' to continue or 'n' to cancel.")

def follow_user(username, retries=3, delay=5):
    """Follows a specified user, with retry logic on failure."""
    url = f"https://api.github.com/user/following/{username}"
    
    for attempt in range(retries):
        response = requests.put(url, headers=HEADERS)
        
        if response.status_code == 204:
            print(f"✅ Followed {username}")
            return True
        else:
            print(f"⚠️ Failed to follow {username}: {response.status_code} - {response.text}")

        if attempt < retries - 1:
            print(f"⏳ Retrying in {delay} seconds... ({attempt+1}/{retries})")
            time.sleep(delay)
    
    print(f"❌ Could not follow {username} after {retries} attempts.")
    return False

def unfollow_user(username, retries=3, delay=5):
    """Unfollows a specified user, with retry logic on failure."""
    url = f"https://api.github.com/user/following/{username}"
    
    for attempt in range(retries):
        response = requests.delete(url, headers=HEADERS)
        
        if response.status_code == 204:
            print(f"✅ Unfollowed {username}")
            return True
        else:
            print(f"⚠️ Failed to unfollow {username}: {response.status_code} - {response.text}")

        if attempt < retries - 1:
            print(f"⏳ Retrying in {delay} seconds... ({attempt+1}/{retries})")
            time.sleep(delay)
    
    print(f"❌ Could not unfollow {username} after {retries} attempts.")
    return False

def process_follow_unfollow(followers, following, x=100):
    """Processes follow/unfollow actions based on user lists and API limits."""
    global enable_follow, enable_unfollow 

    to_follow = followers - following - BLACKLIST
    to_unfollow = following - followers - BLACKLIST

    remaining_requests, _ = check_rate_limit()

    # Calculate maximum actions
    max_allowed_actions = (remaining_requests - x) // 3

    if max_allowed_actions <= 0:
        print("⚠️ Not enough API requests available. Please try again later.")
        return

    print(f"🔄 API Requests Left: {remaining_requests} | Max Allowed Actions: {max_allowed_actions}")

    actions_done = 0

    # Follow users if enabled
    if enable_follow and to_follow:
        max_follow = min(len(to_follow), max_allowed_actions - actions_done)
        
        # Adjust follow count based on remaining requests
        if (remaining_requests - max_follow * 3) < x:
            max_follow = (remaining_requests - x) // 3  

        print(f"🚀 Starting follow process ({max_follow} users)...")

        for user in list(to_follow)[:max_follow]:
            if follow_user(user):
                actions_done += 1
            else:
                print(f"⚠️ Failed to follow {user}, moving to the next.")
            if actions_done >= max_allowed_actions:
                print("⚠️ API limit reached, stopping follow process.")
                break

    # Unfollow users if enabled
    if enable_unfollow and to_unfollow:
        max_unfollow = min(len(to_unfollow), max_allowed_actions - actions_done)

        # Adjust unfollow count based on remaining requests
        if (remaining_requests - max_unfollow * 3) < x:
            max_unfollow = (remaining_requests - x) // 3  

        print(f"🚀 Starting unfollow process ({max_unfollow} users)...")

        for user in list(to_unfollow)[:max_unfollow]:
            if unfollow_user(user):
                actions_done += 1
            else:
                print(f"⚠️ Failed to unfollow {user}, moving to the next.")
            if actions_done >= max_allowed_actions:
                print("⚠️ API limit reached, stopping unfollow process.")
                break

    print(f"✅ Completed {actions_done} actions.")

if __name__ == "__main__":
    # Read configuration again in main
    config = read_config("config.txt")
    GITHUB_TOKEN = config["GITHUB_TOKEN"]
    GITHUB_USERNAME = config["GITHUB_USERNAME"]
    BLACKLIST = set(config["BLACKLIST"])
    HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

    print(f"🔄 Retrieving followers and following for {GITHUB_USERNAME}...\n")

    # Retrieve followers and following lists
    followers = get_users_list(GITHUB_USERNAME, "followers")
    following = get_users_list(GITHUB_USERNAME, "following")
    
    # Check for errors in retrieval
    if followers is None or following is None:
        print("🚨 Error retrieving data. Please try again later.")
    else:
        print("\n📊 Summary of retrieved data:")
        print(f"👥 Followers: {len(followers)}")
        print(f"➡️ Following: {len(following)}")

        # Dry Run before executing actions
        if dry_run(followers, following):
            process_follow_unfollow(followers, following)

        # Display remaining API requests at the end of the run
        remaining_requests, reset_time = check_rate_limit()
        print(f"🔄 Remaining API requests: {remaining_requests}")
        print(f"🔄 Resetting requests in {reset_time} seconds")
