from ..config import env_vars
import requests

TEST_DATE = "2011-08-01"


def test_request():
    global TEST_DATE

    base_url = f"https://api.twitter.com/2/users/133110529/tweets?max_results=100&start_time={TEST_DATE}T00:00:00Z&end_time={TEST_DATE}T23:59:59Z&tweet.fields=created_at&exclude=retweets"

    authorization = env_vars["authorization"]

    headers = {
        "Authorization": f"Bearer {authorization}"
    }

    response = requests.get(f"{base_url}", headers=headers)

    tweet_list = response.json()

    assert tweet_list["meta"]["result_count"] > 0