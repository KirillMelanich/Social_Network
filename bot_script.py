import requests
from faker import Faker
import random
from config import CONFIG

fake = Faker()


def register_user():
    register_url = f"{CONFIG['BASE_URL']}/user/register/"
    user_data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "password": "12345",  # You can generate a random password if needed
    }

    response = requests.post(register_url, data=user_data)
    if response.status_code == 201:
        print(f"User registered successfully: {user_data['email']}")
        return user_data
    else:
        print(f"Failed to register user: {user_data['email']}")
        print(f"Error: {response.json() if response.text else 'No response body'}")
        return None


def get_access_token(email, password):
    token_url = f"{CONFIG['BASE_URL']}/user/token/"
    token_data = {
        "email": email,
        "password": password,
    }

    response = requests.post(token_url, data=token_data)
    if response.status_code == 200:
        access_token = response.json().get("access")
        print(f"Access token received successfully for user: {email}")
        return access_token
    else:
        print(f"Failed to get access token for user: {email}")
        print(f"Error: {response.json() if response.text else 'No response body'}")
        return None


def create_post(access_token):
    post_url = f"{CONFIG['BASE_URL']}/tweetogram/posts/"
    headers = {"Authorization": f"Bearer {access_token}"}
    post_data = {
        "content": fake.text(),
    }

    response = requests.post(post_url, headers=headers, data=post_data)
    if response.status_code == 201:
        print(f"Post created successfully")
        return response.json()["id"]
    else:
        print(f"Failed to create post")
        print(f"Error: {response.json() if response.text else 'No response body'}")
        return None


def like_post(access_token, post_id):
    like_url = f"{CONFIG['BASE_URL']}/tweetogram/posts/{post_id}/like/"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.post(like_url, headers=headers)
    if response.status_code == 200:
        print(f"Post liked successfully")
    else:
        print(f"Failed to like post")
        print(f"Error: {response.json() if response.text else 'No response body'}")


def main():
    for _ in range(CONFIG["number_of_users"]):
        user_data = register_user()
        if user_data:
            access_token = get_access_token(user_data["email"], user_data["password"])

            for _ in range(random.randint(1, CONFIG["max_posts_per_user"])):
                post_id = create_post(access_token)

                # Likelihood of liking a post can be adjusted based on your requirements
                if random.random() < 0.5:
                    for _ in range(random.randint(1, CONFIG["max_likes_per_user"])):
                        like_post(access_token, post_id)


if __name__ == "__main__":
    main()
