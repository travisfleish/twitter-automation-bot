import openai
import tweepy
import time
import random
from datetime import datetime

# Twitter API Authentication
API_KEY = "your_twitter_api_key"
API_SECRET = "your_twitter_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_SECRET = "your_access_secret"

# Authenticate with Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key"
openai.api_key = OPENAI_API_KEY

# Personalized tweet prompts
TWEET_PROMPTS = [
    "Share an insight on transitioning from real estate to AI.",
    "What was a surprising challenge when learning AI after 15 years in real estate?",
    "Explain how real estate knowledge applies to AI & business automation.",
    "Tweet about a recent AI tool you've experimented with and its potential for automation.",
    "What advice would you give to someone pivoting from a traditional industry into AI?"
]


# Generate tweet using OpenAI
def generate_tweet():
    prompt = random.choice(TWEET_PROMPTS)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system",
                   "content": "You are a professional transitioning from real estate to AI & automation. Provide engaging tweets based on this journey."},
                  {"role": "user", "content": prompt}]
    )
    tweet = response["choices"][0]["message"]["content"].strip()
    return tweet


# Post tweet to Twitter (limited to 2-3 times per week)
def post_tweet():
    tweet = generate_tweet()
    try:
        api.update_status(tweet)
        print(f"Tweet posted: {tweet}")
    except Exception as e:
        print(f"Error posting tweet: {e}")


# Automated engagement: Limited Replies to Stay Within API Limit
def auto_reply():
    search_query = "AI automation OR business automation OR real estate AI"
    tweets = api.search_tweets(q=search_query, count=1, lang='en', result_type='recent')  # Limit replies to 1 per day

    for tweet in tweets:
        try:
            username = tweet.user.screen_name
            tweet_id = tweet.id
            reply_text = generate_tweet()
            api.update_status(status=f"@{username} {reply_text}", in_reply_to_status_id=tweet_id)
            print(f"Replied to @{username}: {reply_text}")
            time.sleep(30)  # Avoid rate limits
        except Exception as e:
            print(f"Error replying: {e}")


# Track follower growth
def track_growth():
    user = api.get_user(screen_name="@RealEstateToAI")
    followers_count = user.followers_count
    print(f"Current followers: {followers_count}")
    return followers_count


# Main loop: Adjusted to post only 2-3 times per week
def main():
    post_days = [1, 4]  # Tweet on Mondays & Thursdays
    while True:
        current_day = datetime.now().weekday()

        if current_day in post_days:
            print("Posting a tweet...")
            post_tweet()

        print("Engaging with Twitter audience...")
        auto_reply()

        print("Tracking follower growth...")
        track_growth()

        print("Sleeping for 24 hours...")
        time.sleep(86400)  # Sleep for 24 hours before checking again


if __name__ == "__main__":
    main()
