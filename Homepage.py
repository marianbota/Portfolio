import streamlit as st


st.set_page_config(page_title="Data Science Portfolio", page_icon=":necktie:")

st.sidebar.success("Select a page to view")

st.title("Welcome to My Data Science Portfolio")

st.markdown(
    """
This space showcases a selection of data science projects I've undertaken, demonstrating my skills in data exploration, analysis, and insight generation. Below, you'll find a brief overview of each project. Feel free to delve deeper into each one by selecting the sections from the left pane."""
)

st.header("Project 1: Unveiling the Dynamics of African Crises: A Case Study in Data Visualization Interpretation")
st.markdown(
    """
This project delves into the complexities of African crises, with a particular focus on understanding the relationship between inflation and events specifically marked as "inflation crises." 
Beyond simply visualizing the data, ***this project serves as a compelling case study demonstrating how initial data visualizations can sometimes be misleading and underscores the critical importance of understanding the underlying data and context*** to derive accurate insights.
""")

with st.expander("Project Breakdown & Key Findings:"):
    st.markdown(
        """

    **Data Overview:** This initial stage involved a thorough examination of the dataset, providing context on its sources, the range of information it contains, and clear descriptions of the variables under analysis. This foundational understanding is crucial for interpreting subsequent visualizations effectively.

    **Correlation Analysis:** Utilizing correlation heatmaps, I investigated the linear relationships between various factors, with a specific focus on the correlation between the general inflation rate and the occurrence of designated "inflation crisis" events. The initial heatmap revealed only a seemingly weak correlation between these two variables, a result that, on the surface, might lead to a premature conclusion.
                
    **Inflation Trends and Crisis Events:** To visualize the evolution of inflation, I created time-series graphs displaying the inflation rate per year for several African countries. Crucially, these graphs also highlight the specific years where "inflation crisis" events were recorded, allowing for a direct visual assessment of their co-occurrence. Separate graphs were generated for two selected countries that initially exhibited a particularly low apparent correlation. These visualizations further emphasized the initial observation of a less-than-obvious relationship.

    **The Impact of Extreme Inflation:** Adjusted Analysis: A key insight emerged from recognizing the presence of extremely high inflation rates in certain periods. These extreme values were obscuring the underlying relationship. To address this, I implemented an adjusted inflation rate (capped at 100%). The "Adjusted Inflation Graphs" page showcases how this adjustment reveals a significantly stronger and more evident correlation between inflation spikes and the documented "inflation crisis" events. This highlights a crucial lesson: visualizations alone can be deceptive if the underlying data characteristics are not properly understood and accounted for.
    
    **Key Insight:**

    This project powerfully illustrates how data visualization, while a valuable tool, can be misleading if interpreted without a deep understanding of the data's nuances. The initial visualizations suggested a weak link between inflation rate and inflation crises. However, by recognizing the impact of extreme inflation values and adjusting the data accordingly, a much clearer and more meaningful correlation was revealed. This underscores the importance of critical thinking, domain knowledge, and further analysis beyond initial visualizations to extract accurate and insightful conclusions from data.
    
    **Limitations:**

    The dataset used in this project is limited to only 13 African countries, which may not provide a comprehensive view of Economic situation in the entire African continent let alone at a global scale.
    The Dataset is also limited to the time period 1860 to 2014 so it does not reflect the current economic situation in Africa. The focus of the project is on the correlation between inflation and inflation crises and does not tackle the full complexity of the economic situation in Africa.
    """
    )
st.header("Project 2: Predicting Employee Attrition: Leveraging Classification Models")
st.markdown(
    """
Predicting employee attrition is the focus of this project, utilizing a synthetic dataset where individual features show limited correlation with employee turnover. Simple analyses of single features against attrition provide little insight. To address this, machine learning classification models – a Decision Tree and a Random Forest – are employed. These methods can analyze all features simultaneously to uncover complex patterns and offer a more effective approach to understanding the drivers of employee attrition.
"""
)
with st.expander("Project Breakdown & Key Findings:"):
    st.markdown(
        """

        **Initial Data Exploration:** My initial exploration included visualizing the relationship between attrition and individual features, such as Age, Monthly Income and Overtime. As demonstrated in these graphs, drawing clear conclusions from simple bivariate visualizations can be challenging, especially in datasets with complex interactions between multiple variables.
        
        **Decision Tree Classifier for Attrition Prediction:** To gain deeper insights, I implemented a Decision Tree Classifier. This model learns hierarchical decision rules from the data to predict the likelihood of attrition. The resulting tree structure provides a visual representation of the key factors and their thresholds that contribute to an attrition prediction.
        
        **Random Forest Classifier and Feature Importance:** Building upon the Decision Tree approach, I employed a Random Forest Classifier. This ensemble method combines multiple decision trees to improve prediction accuracy and robustness. A significant advantage of the Random Forest is its ability to calculate feature importance scores. These scores provide a valuable ranking of which employee attributes (e.g., salary, tenure, job role) have the most significant influence on the likelihood of attrition. This allows for a more data-driven understanding of the drivers behind employee turnover.

        **Key Insight:**

        This project highlights the power of classification models in understanding complex relationships within datasets. While initial exploratory visualizations might not reveal clear patterns, machine learning algorithms like Decision Trees and Random Forests can effectively identify the features that significantly influence the target variable (in this case, attrition). Furthermore, the feature importance scores provided by the Random Forest Classifier offer actionable insights into the key factors driving employee turnover, enabling businesses to focus their retention strategies effectively.
        
        **Limitations:**

        The dataset used in this project is synthetic, which means it may not accurately represent real-world employee behavior and attrition patterns. While the models can provide insights into feature importance, the conclusions drawn from this dataset may not be generalizable to actual employee populations. Additionally, the project does not explore the potential impact of external factors (e.g., economic conditions, industry trends) on employee attrition, which could further enhance the analysis.
        
        """
    )

st.header("Project 3: News Sentiment Analysis from RSS Feeds")
st.markdown("""This project explores the dynamic landscape of news sentiment by building a system to collect articles from various RSS feeds, store them in a database, and perform real-time sentiment analysis. The goal was to understand the overall public sentiment expressed by different news sources and how that sentiment evolves over time, as well as the ability to analyze sentiment around specific topics.
""")
with st.expander("Project Breakdown & Key Findings:"):
    st.markdown(
        """
**News Source Sentiment Overview:** The first page presents visualizations showing the average sentiment and subjectivity scores for each news source, providing a comparative overview of their general tone. Additionally, the project tracks the evolution of sentiment over time, allowing for the identification of trends and shifts in public opinion as reflected by the news.

**Keyword-Based Sentiment Filtering and Analysis:** To enable more targeted analysis, a filtering mechanism was implemented. Users can input a specific keyword, and the system will retrieve all relevant news articles containing that keyword from the database. For this filtered subset of articles, a detailed breakdown of sentiment and subjectivity is provided, offering insights into the specific sentiment surrounding the chosen topic across different news sources. This feature allows for a deeper understanding of public perception on particular events or subjects.

**Key Insight:**

This project demonstrates the power of natural language processing techniques. The project shows that it's possible to gain valuable insights into the prevailing sentiment expressed by various news outlets, track sentiment trends over time, and perform focused analysis on specific topics of interest. This type of analysis has applications in various fields, including market research, public relations, and understanding societal responses to current events.

**Limitations:**

The project has a limited list of news source which are openly available. The list doesn't not include a lot of news outlets that are behind a paywall or require a subscription. The sentiment analysis is based on a pre-trained model, which may not capture the nuances of specific news articles or the context in which they are written. The project does not account for potential biases in the news sources, which could affect the overall sentiment analysis.
Due to the nature of the project as a showcase of the approach the data is kept for the last 30 days and the articles are update manually in the last sub-page entitled "Update News". This can lead to the dataset being out of date, but further development and fine tuning is out of the scope of this project.     
            
            """
    )
