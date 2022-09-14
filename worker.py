import datetime
import logging
import requests
import psycopg2
from twilio.rest import Client
from config import env_vars

yesterday = (datetime.datetime.today() -
             datetime.timedelta(days=1)).strftime("%Y-%m-%d")


def main():
    print("Job running...")

    all_tweets = []
    total_iterations = 1
    tweets_added = 0
    global yesterday

    def get_tweets(pagination_token=None):

        base_url = f"https://api.twitter.com/2/users/133110529/tweets?max_results=100&start_time={yesterday}T00:00:00Z&end_time={yesterday}T23:59:59Z&tweet.fields=created_at&exclude=retweets"

        authorization = env_vars["authorization"]

        headers = {
            "Authorization": f"Bearer {authorization}"
        }

        if pagination_token != None:
            base_url = base_url + "&pagination_token=" + pagination_token

        response = requests.get(
            f"{base_url}", headers=headers)

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
        print("Database not connected: ", error)

    finally:
        client = Client(env_vars["twilio_sid"], env_vars["twilio_token"])
        body = ""

        if conn:
            cursor.close()
            conn.close()
            print("Connection closed.")

            if tweets_added > 0:
                url = f"https://dbclassic.herokuapp.com/tweet?date={yesterday}"
                body = f"Total tweets added: {tweets_added}. So money: {url}"
            else:
                body = "No tweets added. So steamed."
        else:
            body = "Error connecting to DB. Kinda concerning?"

        client.messages.create(
            to=env_vars["twilio_to"],
            from_=env_vars["twilio_from"],
            body=body)


if __name__ == "__main__":
    main()
