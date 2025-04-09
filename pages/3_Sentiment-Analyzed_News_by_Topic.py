import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import duckdb


st.title("Sentiment-Analyzed News by Topic")

# st.sidebar.header("Sentiment-Analyzed News by Topic")

pages = [
    "News Sources Overview",
    "Filter by Topic",
    "Update News",
]
selected_view = st.sidebar.selectbox("Select View", pages)

if selected_view == "News Sources Overview":
    conn = duckdb.connect(database="news/news.db", read_only=False)
    st.markdown(
        """
    This is a streamlit app to showcase an approach to analyze topics as they are covered by different news sources.
    To update the news articles, click on the "Update News" button in the sidebar.
    """
    )

    st.markdown(
        """
    In this page an overview of the news sources is provided including a comparison of how subjective or objective the news sources are, or if they are left or right leaning in a political sense.
    A Trend over time of the overall sentiment of all the news sources is also provided.
    """
    )

    # Select statement to get the average sentiment  grouped by source
    query = """
    SELECT source, AVG(sentiment) as sentiment, AVG(subjectivity) as subjectivity
    FROM articles
    GROUP BY source
    ORDER BY sentiment DESC
    """
    df = conn.execute(query).fetchdf()
    df["sentiment"] = df["sentiment"].round(2)
    df["subjectivity"] = df["subjectivity"].round(2)

    st.header("Average Sentiment score by source")
    st.markdown(
        """
    The average sentiment score of the news sources is shown below. The sentiment score is a value between -1 and 1, where -1 is very negative, 0 is neutral and 1 is very positive.
    """
    )

    # Create a bar plot of the average sentiment by source
    fig, ax = plt.subplots()
    sns.barplot(x="sentiment", y="source", data=df, ax=ax)
    ax.set_title("Average Sentiment by Source")
    ax.set_xlabel("Average Sentiment")
    ax.set_ylabel("Source")
    st.pyplot(fig)

    # Create a bar plot of the average subjectivity by source
    st.header("Average Subjectivity score by source")
    st.markdown(
        """
    The average subjectivity score of the news sources is shown below. The subjectivity score is a value between 0 and 1, where 0 is very objective and 1 is very subjective.
    """
    )
    fig, ax = plt.subplots()
    sns.barplot(
        x="subjectivity",
        y="source",
        data=df,
        ax=ax,
        order=df.sort_values("subjectivity")["source"],
    )
    ax.set_title("Average Subjectivity by Source")
    ax.set_xlabel("Average Subjectivity")
    ax.set_ylabel("Source")
    st.pyplot(fig)

    # Select statement to get the average sentiment grouped by date
    query = """
    SELECT published as date, AVG(sentiment) as sentiment
    FROM articles
    GROUP BY date
    ORDER BY date
    """
    df = conn.execute(query).fetchdf()
    df["date"] = pd.to_datetime(df["date"])
    df["date"] = df["date"].dt.date
    df["sentiment"] = df["sentiment"].round(2)
    st.header("Average Sentiment score over time")
    st.markdown(
        """
        The average sentiment score of the news sources over time is shown below. The sentiment score is a value between -1 and 1, where -1 is very negative, 0 is neutral and 1 is very positive.
        """
    )
    # Create a line plot of the average sentiment over time
    fig, ax = plt.subplots()
    sns.lineplot(x="date", y="sentiment", data=df, ax=ax)
    ax.set_title("Average Sentiment over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Average Sentiment")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    conn.close()

if selected_view == "Filter by Topic":
    conn = duckdb.connect(database="news/news.db", read_only=False)
    st.markdown(
        """
    This page allows you to filter the news articles by a keyword. You can enter a keyword  and select from a dropdown menu if you want to search in the title or content of the article.
    """
    )

    # Text input for keyword
    keyword = st.text_input("Enter a keyword to search for")
    # Dropdown menu for title or content
    search_in = st.selectbox("Search in", ["title", "content"])
    # Button to search
    if st.button("Search"):
        if keyword:
            # Select statement to get the articles that contain the keyword in the title or content
            query = f"""
            SELECT * FROM articles
            WHERE LOWER({search_in}) LIKE LOWER('%{keyword}%')
            """
            df = conn.execute(query).fetchdf()
            if df.empty:
                st.write("No articles found")
            else:
                st.write(f"Found {len(df)} articles")
                # Display the articles in a table
                st.dataframe(
                    df[
                        [
                            "title",
                            "link",
                            "published",
                            "source",
                            "sentiment",
                            "subjectivity",
                        ]
                    ],
                    column_config={"link": st.column_config.LinkColumn()},
                )
                # Create a bar plot of the sentiment of the articles
                fig, ax = plt.subplots()
                sns.barplot(x="sentiment", y="source", data=df, ax=ax)
                ax.set_title("Sentiment by Source")
                ax.set_xlabel("Sentiment")
                ax.set_ylabel("Source")
                st.pyplot(fig)
                # Create a bar plot of the subjectivity of the articles
                fig, ax = plt.subplots()
                sns.barplot(x="subjectivity", y="source", data=df, ax=ax)
                ax.set_title("Subjectivity by Source")
                ax.set_xlabel("Subjectivity")
                ax.set_ylabel("Source")
                st.pyplot(fig)
                # Create a line plot of the sentiment over time
                df["published"] = pd.to_datetime(df["published"])
                df["published"] = df["published"].dt.date
                fig, ax = plt.subplots()
                sns.lineplot(x="published", y="sentiment", data=df, ax=ax)
                ax.set_title("Sentiment over Time")
                ax.set_xlabel("Date")
                ax.set_ylabel("Sentiment")
                plt.xticks(rotation=45)
                st.pyplot(fig)

        else:
            st.write("Please enter a keyword to search for")


if selected_view == "Update News":
    from news.news_backend import (
        get_rss_feeds,
        get_links,
        get_sentiment_from_text,
        clear_database,
        clear_RSS_feeds,
        progressbar,
        add_content,
        add_sentiment,
    )

    st.markdown(
        """
    You can update the news articles by clicking the button below. This will fetch the latest news articles from the predefined RSS feeds and store them in the database.\
    
    **Caution:**

    This takes a long time, more than 5 minutes to run so I recommend exploring the rest of the project first as the results can be skewed while the update is running.
    """
    )

    # Button to run the news/news_backend.py script
    if st.button("Update news"):
        st.write("Updating articles from RSS feeds...")
        get_rss_feeds()
        st.write("Finished updating articles from RSS feeds")
        st.write("Updating sentiment of articles...")
        get_links()
        st.write("Finished updating sentiment of articles")
        st.write("Clearing database")
        clear_database()
        st.write("Finished clearing database")
        st.write("Clearing RSS feeds")
        clear_RSS_feeds()
        st.write("Finished clearing RSS feeds")
        # Run the script
