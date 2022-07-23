# Tweet Getter for DB Classic API

## Current Functionality:
- clock.py runs at midnight central time, kicking off the worker.py script
- worker.py queries Twitter's API for Karl's tweets from the previous day, starting
- Script paginates over the list of returned tweets in the off chance there's over 100 in a single response
- If any tweets are found, we sanity check that they weren't already in the DB by running a SELECT statement on the tweet ID
- If it's not in the DB already, it's inserted into the DB
- Text notification is sent via Twilio's API confirming the job has finished

## To Do:
- DB backups
- Proper logging