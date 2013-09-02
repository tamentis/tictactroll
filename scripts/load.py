#!/usr/bin/python

"""
Comment loader.

This script is run by god Cron and loads the last 50 shortest comments to be
thrown at the tictactroll player regularly, for shits and giggles. Mostly
giggles. It's also to avoid blasting the reddit servers with request from
clients.
"""

import time
import urllib
import sqlite3
import simplejson as json


you_words = ("you", "bro", "man", "dude", "brah")
max_length = 64

def read_reddit(url):
    """Expect a query string without the .json, returns a dict."""
    try:
        fp = urllib.urlopen("http://www.reddit.com%s.json" % url)
        data = json.load(fp)
    except:
        data = []
    finally:
        fp.close()
    return data

def is_cool(comment):
    """Tell me if this comment is worthy."""
    data = comment["data"]

    if "body" not in data:
        return False

    body = data["body"].lower()

    if data["ups"] < 5:
        return False

    if "http" in body:
        return False

    if "\n" in body:
        return False

    if len(body) < 8 or len(body) > max_length:
        return False

    if not any([u in body for u in you_words]):
        return False

    return True

def walk_comments(comments):
    """Recurse down an array of comments and yield their body if cool =)"""
    for comment in comments:
        # Deal with the comment itself
        if is_cool(comment):
            yield comment["data"]["body"]

        # Then with the replies (hell yeah recursive generators)
        if "replies" in comment["data"]:
            replies = comment["data"]["replies"]
            if replies:
                for reply in walk_comments(replies["data"]["children"]):
                    yield reply

def generate_comments(articles):
    """Recurse down an array of articles for comments."""
    comment_urls = [a["data"]["permalink"] for a in articles]

    for url in comment_urls:
        time.sleep(2.0)
        comments = read_reddit(url)[-1]["data"]["children"]
        for comment in walk_comments(comments):
            yield comment

def get_clever_lines_from_subreddit():
    articles = read_reddit("/r/wtf/")["data"]["children"]
    return [line for line in generate_comments(articles)]

def refresh_clever_lines():
    conn = sqlite3.connect("tictactroll.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lines (
            ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            line VARCHAR(%d)
        )
        """ % max_length)
    conn.commit()

    # Insert the new lines
    lines = [(l,) for l in get_clever_lines_from_subreddit()]
    cur.executemany("""
        INSERT INTO lines (line) VALUES (?)
        """, lines)
    conn.commit()

    # Crop to 500
    cur.execute("""
        DELETE FROM lines
        WHERE ts < date('now', '-1 day')
        """)
    conn.commit()

    cur.close()
    conn.close()

if __name__ == '__main__':
    refresh_clever_lines()
