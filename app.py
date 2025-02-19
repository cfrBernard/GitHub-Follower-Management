import requests
import time
import json

def read_config(file_path):
    config = {}
    with open(file_path, "r") as file:
        for line in file:
            key, value = line.strip().split("=")
            config[key] = value.split(",") if key == "BLACKLIST" else value
    return config

config = read_config("config.txt")

GITHUB_TOKEN = config["GITHUB_TOKEN"]
GITHUB_USERNAME = config["GITHUB_USERNAME"]
BLACKLIST = set(config["BLACKLIST"])
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def check_rate_limit():
    url = "https://api.github.com/rate_limit"
    response = requests.get(url, headers=HEADERS)
    rate_limit_data = response.json()
    remaining = rate_limit_data['resources']['core']['remaining']
    reset = rate_limit_data['resources']['core']['reset']
    return remaining, reset

def api_request(url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS)
            remaining = response.headers.get('X-RateLimit-Remaining')
            reset = response.headers.get('X-RateLimit-Reset')
            
            if remaining is not None and int(remaining) < 10:
                print(f"⚠️ API rate limit approaching: {remaining} requests left. Reset in {reset} seconds.")
                return None

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
    """ Retrieves the full list of followers or following with pagination handling. """
    url = f"https://api.github.com/users/{username}/{action}?per_page=100"
    users = []

    while url:
        print(f"🔄 Retrieving {url}...")
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"⚠️ API Error {response.status_code}: {response.text}")
            break

        page_data = response.json()
        users.extend(user['login'] for user in page_data if user['login'] not in BLACKLIST)
        print(f"📄 Page retrieved: {len(page_data)} users")
        
        # Check if the 'Link' header contains a next page
        if 'Link' in response.headers:
            links = response.headers['Link'].split(',')
            next_url = None
            for link in links:
                if 'rel=\"next\"' in link:
                    next_url = link[link.find('<')+1:link.find('>')]
                    break
            url = next_url
        else:
            url = None

    return set(users)

def dry_run(followers, following):
    to_follow = followers - following - BLACKLIST
    to_unfollow = following - followers - BLACKLIST

    print("\n🔄 Planned actions:")
    print(f"👥 Users to follow: {len(to_follow)}")
    print(f"👥 Users to unfollow: {len(to_unfollow)}")

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

if __name__ == "__main__":
    config = read_config("config.txt")
    GITHUB_TOKEN = config["GITHUB_TOKEN"]
    GITHUB_USERNAME = config["GITHUB_USERNAME"]
    BLACKLIST = set(config["BLACKLIST"])
    HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

    print(f"🔄 Retrieving followers and following for {GITHUB_USERNAME}...\n")

    followers = get_users_list(GITHUB_USERNAME, "followers")
    following = get_users_list(GITHUB_USERNAME, "following")

    if followers is None or following is None:
        print("🚨 Error retrieving data. Please try again later.")
    else:
        print("\n📊 Summary of retrieved data:")
        print(f"👥 Followers: {len(followers)}")
        print(f"➡️ Following: {len(following)}")
        # Dry run
        dry_run(followers, following)
        # Save results in a JSON file for debugging
        with open("github_users_data.json", "w") as f:
            json.dump({"followers": list(followers), "following": list(following)}, f, indent=4)
        print("\n✅ Data saved in github_users_data.json")

        # Display remaining API requests at the end of the run
        remaining_requests, reset_time = check_rate_limit()
        print(f"🔄 Remaining API requests: {remaining_requests}")
        print(f"🔄 Resetting requests in {reset_time} seconds")
