import os
import requests
import datetime
import sqlalchemy as db
from dotenv import load_dotenv

load_dotenv(".env")

authorization = os.getenv("AUTHORIZATION")
database_url = os.getenv("DATABASE_URL")

yesterday = (datetime.datetime.today() -
             datetime.timedelta(days=1)).strftime("%Y-%m-%d")

headers = {
    "Authorization": f"Bearer {authorization}"
}
base_url = f"https://api.twitter.com/2/users/133110529/tweets?max_results=10&start_time={yesterday}T12:00:00Z&end_time={yesterday}T23:59:59Z&tweet.fields=created_at"


def main():
    all_tweets = []
    total_iterations = 1

    def get_tweets(pagination_token=None):
        global base_url
        if pagination_token != None:
            new_url = base_url + "&pagination_token=" + pagination_token
        else:
            new_url = base_url

        response = requests.get(
            f"{new_url}", headers=headers)

        tweet_list = response.json()

        if tweet_list["meta"]["result_count"] == 0:
            print("No tweets")
            return True

        all_tweets.extend(tweet_list["data"])

        if "next_token" in tweet_list["meta"]:
            nonlocal total_iterations
            total_iterations += 1
            print("Getting next result set: ", total_iterations)
            return get_tweets(tweet_list["meta"]["next_token"])

        return True

    get_tweets()

    if len(all_tweets) == 0:
        return True

    engine = db.create_engine(
        f"postgresql://{database_url}", echo=True)

    conn = engine.connect()

    for tweet in all_tweets:
        text = "INSERT INTO tweets (id, text, created_at) VALUES (:id, :text, :created_at)"
        q = db.text(text)

        result = conn.execute(
            q, id=tweet["id"], text=tweet["text"], created_at=tweet["created_at"])

        print(result)

    conn.close()


if __name__ == "__main__":
    main()
