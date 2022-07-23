import datetime
import logging
import requests
import psycopg2
from twilio.rest import Client
from config import env_vars


def main():
    print("Job running...")

    yesterday = (datetime.datetime.today() -
                 datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    authorization = env_vars["authorization"]

    headers = {
        "Authorization": f"Bearer {authorization}"
    }

    base_url = f"https://api.twitter.com/2/users/133110529/tweets?max_results=100&start_time={yesterday}T00:00:00Z&end_time={yesterday}T23:59:59Z&tweet.fields=created_at&exclude=retweets"

    all_tweets = []
    total_iterations = 1
    tweets_added = 0

    def get_tweets(pagination_token=None):
        if pagination_token != None:
            new_url = base_url + "&pagination_token=" + pagination_token
        else:
            new_url = base_url

        response = requests.get(
            f"{new_url}", headers=headers)

        response.raise_for_status()

        tweet_list = response.json()

        if tweet_list["meta"]["result_count"] == 0:
            print("Job finished: No tweets.")
            return True

        all_tweets.extend(tweet_list["data"])

        if "next_token" in tweet_list["meta"]:
            nonlocal total_iterations
            total_iterations += 1
            print("Getting next result set: ", total_iterations)
            return get_tweets(tweet_list["meta"]["next_token"])

        return True

    get_tweets()

    try:
        conn = psycopg2.connect(dbname=env_vars["db_name"], user=env_vars["db_user"],
                                password=env_vars["db_pass"], host=env_vars["db_host"], port=env_vars["db_port"])

        cursor = conn.cursor()

        for tweet in all_tweets:
            id, text, created_at = tweet["id"], tweet["text"], tweet["created_at"]
            select_query = "SELECT * FROM tweets WHERE id = %s"
            cursor.execute(select_query, (id,))
            result = cursor.fetchone()

            if result == None:
                tweets_added += 1
                insert_query = "INSERT INTO tweets (id, text, created_at) VALUES (%s, %s, %s)"
                cursor.execute(
                    insert_query, (id, text, created_at,))
                conn.commit()
                print(f"Tweet ID {id} added to database.")
            else:
                print(f"Tweet ID {id} already exists in database.")

    except psycopg2.OperationalError as error:
        print("Database not connected.", error)

    finally:
        client = Client(env_vars["twilio_sid"], env_vars["twilio_token"])
        body = ""

        if conn:
            cursor.close()
            conn.close()
            print("Connection closed.")

            if len(all_tweets) > 0:
                body = f"Total tweets added: {tweets_added}."
            else:
                body = "No tweets added."
        else:
            body = "Error connecting to DB."

        client.messages.create(
            to=env_vars["twilio_to"],
            from_=env_vars["twilio_from"],
            body=body)


if __name__ == "__main__":
    main()
