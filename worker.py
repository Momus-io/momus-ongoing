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


def main():
    response = requests.get(
        f"https://api.twitter.com/2/users/133110529/tweets?max_results=100&start_time={yesterday}T12:00:00Z&end_time={yesterday}T23:59:59Z&tweet.fields=created_at", headers=headers)

    tweet_list = response.json()

    engine = db.create_engine(
        f"postgresql://{database_url}", echo=True)

    conn = engine.connect()
    for tweet in tweet_list["data"]:
        text = "INSERT INTO tweets (id, text, created_at) VALUES (:id, :text, :created_at)"
        q = db.text(text)
        result = conn.execute(
            q, id=tweet["id"], text=tweet["text"], created_at=tweet["created_at"])

        print(result)

    conn.close()


if __name__ == "__main__":
    main()
