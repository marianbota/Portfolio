import feedparser
import json
import duckdb
import newspaper
import os

from datetime import datetime
from time import mktime
from textblob import TextBlob


def get_rss_feeds():
    conn = duckdb.connect(database="news/news.db", read_only=False)
    f = open("news/rss_feeds.json")
    RSS_Feeds = json.load(f)

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            title VARCHAR,
            link VARCHAR CONSTRAINT pk_link PRIMARY KEY,
            published TIMESTAMP,
            source VARCHAR,
            content VARCHAR,
            sentiment DOUBLE,
            subjectivity DOUBLE,
        )
    """
    )
    for source, feed in RSS_Feeds.items():

        os.write(f"Processing {source}")
        # print(f"Processing {source}")
        d = feedparser.parse(feed)
        for entry in d.entries:
            os.write(f"--------Processing {entry.title}")
            # print(f"--------Processing {entry.title}")
            try:
                title = entry.title
                link = entry.link
                published = datetime.fromtimestamp(mktime(entry.published_parsed))
                source = source
                conn.execute(
                    """
                    INSERT INTO articles (title, link, published, source)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT DO NOTHING 
                    """,
                    (title, link, published, source),
                )
            except Exception as e:
                os.write(f"Error processing {source}: {e}")
                # print(f"Error processing {source}: {e}")

                continue
    conn.commit()

    f.close()


def add_content(link, content):
    conn = duckdb.connect(database="news/news.db", read_only=False)
    """
    Add content to the article with the given link.
    """
    conn.execute(
        """
        UPDATE articles
        SET content = ?
        WHERE link = ?
        """,
        (content, link),
    )
    conn.commit()


def add_sentiment(link, text):
    conn = duckdb.connect(database="news/news.db", read_only=False)
    """
    Add sentiment to the article with the given link.
    """
    sentiment, subjectivity = get_sentiment_from_text(text)
    conn.execute(
        """
        UPDATE articles
        SET sentiment = ?, subjectivity = ?
        WHERE link = ?
        """,
        (sentiment, subjectivity, link),
    )
    conn.commit()


def get_links():
    conn = duckdb.connect(database="news/news.db", read_only=False)

    """
    Get all links from the articles table.
    """
    links = []
    links = conn.execute(
        """
        SELECT link FROM articles
        WHERE sentiment IS NULL
        """
    ).fetchall()
    for link in links:
        article = newspaper.Article(link[0])
        try:
            article.download()
            article.parse()

            add_content(link[0], article.text)
            add_sentiment(link[0], article.text)
        except:
            os.write(f"Error processing {link[0]}")
            # print(f"Error processing {link[0]}")
            continue
        progressbar(links.index(link), len(links), 30, "■")


def get_sentiment_from_text(text):
    """
    Get sentiment from text using the TextBlob library.
    """

    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment.polarity, sentiment.subjectivity


def clear_database():
    conn = duckdb.connect(database="news/news.db", read_only=False)
    #Delete entries where sentiment is null
    conn.execute(
        """
        DELETE FROM articles
        wHERE SENTIMENT IS NULL
        """
    )
    #delete entries older than 30 days
    conn.execute(
        """
        DELETE FROM articles
        WHERE published < (CURRENT_DATE -30)
        """
    )
    
    conn.commit()


def clear_RSS_feeds():
    conn = duckdb.connect(database="news/news.db", read_only=False)
    feeds = conn.execute(
        """
        SELECT DISTINCT source FROM articles
        """
    ).fetchall()

    f = open("news/rss_feeds.json")
    RSS_Feeds = json.load(f)
    bad_sources = []
    for source in RSS_Feeds.keys():
        if source not in [feed[0] for feed in feeds]:
            bad_sources.append(source)
    for source in bad_sources:
        del RSS_Feeds[source]
    f.close()


def progressbar(current_value, total_value, bar_lengh, progress_char):
    percentage = int(
        (current_value / total_value) * 100
    )  # Percent Completed Calculation
    progress = int(
        (bar_lengh * current_value) / total_value
    )  # Progress Done Calculation
    loadbar = "Progress: [{:{len}}]{}%".format(
        progress * progress_char, percentage, len=bar_lengh
    )  # Progress Bar String
    os.write(loadbar, end="\r")
    # print(loadbar, end="\r")  # Progress Bar Output


if __name__ == "__main__":
    get_rss_feeds()
    get_links()

    clear_database()
    clear_RSS_feeds()

    # # app.run(debug=True)
