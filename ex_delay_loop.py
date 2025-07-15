
import requests
import time
import random

headers = {
    "User-Agent": "Instagram 123.0.0.21.114 Android",
    "Cookie": "sessionid=71445303940%3AEEM3jLRrDnEisv%3A23%3AAYcjXMfR5Iq-GC2CGARSaoB6hOYvaOxmJKYpoa2e_A; csrftoken=RCclLE1ZY6mh7bXAhR8LOobGrsJ6YW3e; ds_user_id=71445303940"
}

user_id = "225411328"
extracted = set()
round_count = 0

try:
    while True:
        round_count += 1
        print(f"[ROUND {round_count}] Requesting followers...")

        url = f"https://i.instagram.com/api/v1/friendships/{user_id}/followers/?count=50"
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            print(f"[ERROR] Status {res.status_code}")
            break

        data = res.json()
        users = data.get("users", [])
        print(f"[INFO] Received {len(users)} users.")

        new_users = 0
        for user in users:
            username = user["username"]
            if username not in extracted:
                extracted.add(username)
                new_users += 1

        print(f"[INFO] New extracted this round: {new_users}")
        with open("followers.txt", "w", encoding="utf-8") as f:
            for u in sorted(extracted):
                f.write(u + "\n")

        print(f"[TOTAL SAVED] {len(extracted)} usernames so far.")

        wait_minutes = random.randint(3, 5)
        print(f"[WAIT] Waiting {wait_minutes} minutes before next round...")
        time.sleep(wait_minutes * 60)

except Exception as e:
    print("[FATAL ERROR]", str(e))
