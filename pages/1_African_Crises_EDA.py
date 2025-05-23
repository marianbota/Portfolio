import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("data/african_crises.csv")
df["banking_crisis"] = df["banking_crisis"].apply(lambda x: 1 if x == "crisis" else 0)
df2 = df[df["country"].isin(["Angola", "Zimbabwe"])].copy()

adjusted_df = df[["country", "year", "inflation_annual_cpi", "inflation_crises"]].copy()
adjusted_df["inflation_annual_cpi"] = adjusted_df["inflation_annual_cpi"].apply(
    lambda x: x if x < 100 else 100
)
adjusted_df2 = adjusted_df[adjusted_df["country"].isin(["Angola", "Zimbabwe"])].copy()

st.title("Africa Economic, Banking and Systemic Crisis Data ")

# st.sidebar.header("Dataset Information")

pages = [
    "Data Overview",
    "Correlation Heatmap",
    "Inflation Graphs",
    "Adjusted Inflation Graphs",
]
selected_view = st.sidebar.selectbox("Select View", pages)

if selected_view == "Data Overview":
    kaggle_url = "https://www.kaggle.com/datasets/chirin/africa-economic-banking-and-systemic-crisis-data/data"

    st.markdown(
        """
        The project started as a learning exercise for Exploratory Data Analysis (EDA) and data visualization based on the dataset is from [Kaggle](%s) and contains data on the economic, banking and systemic crisis of 13 African countries from 1860 to 2014.
        Going through the different views which can be selected int he left pane it can be seen that simple data visualization techniques can be misleading and the focus of the project has shifted to showcasing how understanding the underlying data and context leads to better insights.
        Below we can see the data overview, including the columns and a few rows of the dataset.
    """
        % kaggle_url
    )
    st.header("Data and Columns overview")
    st.markdown(
        """
    | Column Name  | Description |
    | :------------ | :--------------- | 
    | case | A number which denotes a specific country |
    | cc3 | A three letter country code |
    | country | The name of the country |
    | year | The year of the observation |
    | systemic_crisys | "0" = NO systemic crisis that year and "1" = systemic crisis that year |
    | exch_usd | The exchange rate of the country vs the USD |
    | domestic_debt_in_default | "0" = NO sovereign domestic debt default that year and "1" = sovereign domestic debt default that year |
    | sovereign_external_debt_default | "0" = NO sovereign external debt default that year and "1" = sovereign external debt default that year |
    | gdp_weighted_default | The total debt in default vis-a-vis the GDP |
    | inflation_annual_cpi | The annual CPI Inflation rate |
    | independence |  "0" means "no independence" and "1" means "independence"; |
    | currency_crises | "0" = NO currency crisis that year and "1" = currency crisis that year |
    | inflation_crises | "0" = NO inflation crisis that year and "1" = inflation crisis that year |
    | banking_crises | "0" = NO banking crisis that year and "1" = banking crisis that year |

    """
    )

    st.header("Dataframe ")
    st.write(df.head())


if selected_view == "Correlation Heatmap":
    st.header("Correlation Heatmap")
    st.write("This heatmap shows the correlation between the features in the dataset.")
    fig = plt.figure(figsize=(12, 8))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f")
    st.pyplot(fig)

    st.write(
        """
    The correlation heatmap shows that there is a correlation, as expected, between the following features:  
        - **Exchange Rate** and **Sovereign Debt Default**  
        - **Currency Crisis** and **Inflation Crisis**  
        - **Systemic Crisis** and **Banking Crisis**   
             

    There are also a few expected correlations that are expected but not shown by the heatmap, such as:  
        - **Inflation** and **Inflation Crisis**
                
"""
    )

if selected_view == "Inflation Graphs":
    st.header("Inflation Graphs")
    st.write("Below we can see the plots for the inflation rate for each country. Included are the inflation crises marked in the dataset.")
    sns.set_style("whitegrid")
    fig, axes = plt.subplots(ncols=4, nrows=4, figsize=(12, 9))
    axes = axes.flatten()
    for i, ax in zip(df["country"].unique(), axes):
        sns.lineplot(
            x="year",
            y="inflation_annual_cpi",
            data=df[df["country"] == i],
            ax=ax,
            color="blue",
        )
        ax.set_xlabel("Year")
        ax.set_ylabel("Inflation Rate")
        ax.set_title("{}".format(i))
        inflation = df[(df["country"] == i) & (df["inflation_crises"] == 1)][
            "year"
        ].unique()
        for i in inflation:
            ax.axvline(x=i, color="red", linestyle="--", linewidth=0.9)
    fig.subplots_adjust(top=0.95)
    for i in range(13, 16):
        fig.delaxes(axes[i])
    plt.tight_layout()
    st.pyplot(fig)

    st.write(
        """
             Angola and Zimbabwe seem to not have their inflation rate correlated with the inflation crisis marked in the dataset.

             On closer inspection both graphs have a very high peak of >4000% and >20.000.000% respectively. This skews the y axis and could be the cause of why the graph is not showing a correlation.

             Below we can see these two countries in a separate graph.
"""
    )

    fig2, axes = plt.subplots(ncols=1, nrows=2, figsize=(12, 9))
    axes = axes.flatten()
    for i, ax in zip(df2["country"].unique(), axes):
        sns.lineplot(
            x="year",
            y="inflation_annual_cpi",
            data=df2[df2["country"] == i],
            ax=ax,
            color="blue",
        )
        ax.set_xlabel("Year")
        ax.set_ylabel("Inflation Rate")
        ax.set_title("{}".format(i))
        inflation = df2[(df2["country"] == i) & (df2["inflation_crises"] == 1)][
            "year"
        ].unique()
        for i in inflation:
            ax.axvline(x=i, color="red", linestyle="--", linewidth=0.9)
    fig2.subplots_adjust(top=0.95)
    # for i in range(13, 16):
    #     fig2.delaxes(axes2[i])
    plt.tight_layout()
    st.pyplot(fig2)

if selected_view == "Adjusted Inflation Graphs":
    st.header("Adjusted Inflation Graphs")
    st.write(
        """
             We can check if using a capped inflation rate at 100 will show a correlation between the inflation rate and the inflation crisis.
            """
    )

    sns.set_style("whitegrid")
    fig2, axes = plt.subplots(ncols=1, nrows=2, figsize=(12, 9))
    axes = axes.flatten()
    for i, ax in zip(adjusted_df2["country"].unique(), axes):
        sns.lineplot(
            x="year",
            y="inflation_annual_cpi",
            data=adjusted_df2[adjusted_df2["country"] == i],
            ax=ax,
            color="blue",
        )
        ax.set_xlabel("Year")
        ax.set_ylabel("Inflation Rate")
        ax.set_title("{}".format(i))
        inflation = adjusted_df2[
            (adjusted_df2["country"] == i) & (adjusted_df2["inflation_crises"] == 1)
        ]["year"].unique()
        for i in inflation:
            ax.axvline(x=i, color="red", linestyle="--", linewidth=0.9)
    fig2.subplots_adjust(top=0.95)
    # for i in range(13, 16):
    #     fig2.delaxes(axes2[i])
    plt.tight_layout()
    st.pyplot(fig2)

    st.write(
        """
             These plots have the inflation capped at 100 and the correlation between the inflation rate and the inflation crisis is more visible.

             Below we can also see the correlation heatmap for the adjusted data, and this also shows a much higher correlation between inflation rate and inflation crisis.
            """
    )
    fig = plt.figure(figsize=(12, 8))
    sns.heatmap(
        adjusted_df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f"
    )
    st.pyplot(fig)

    st.write(
        """
             For reference the graphs for all countries are included below:
            """
    )

    fig, axes = plt.subplots(ncols=4, nrows=4, figsize=(28, 22), dpi=60)
    axes = axes.flatten()
    for i, ax in zip(adjusted_df["country"].unique(), axes):
        sns.lineplot(
            x="year",
            y="inflation_annual_cpi",
            data=adjusted_df[adjusted_df["country"] == i],
            ax=ax,
            color="blue",
        )
        ax.set_xlabel("Year")
        ax.set_ylabel("Inflation Rate")
        ax.set_title("{}".format(i))
        inflation = adjusted_df[
            (adjusted_df["country"] == i) & (adjusted_df["inflation_crises"] == 1)
        ]["year"].unique()
        for i in inflation:
            ax.axvline(x=i, color="red", linestyle="--", linewidth=0.9)
    fig.subplots_adjust(top=0.95)
    for i in range(13, 16):
        fig.delaxes(axes[i])
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown(
        """
    **Key Insight:**

    This project powerfully illustrates how data visualization, while a valuable tool, can be misleading if interpreted without a deep understanding of the data's nuances. The initial visualizations suggested a weak link between inflation rate and inflation crises. However, by recognizing the impact of extreme inflation values and adjusting the data accordingly, a much clearer and more meaningful correlation was revealed. This underscores the importance of critical thinking, domain knowledge, and further analysis beyond initial visualizations to extract accurate and insightful conclusions from data.
    
    **Limitations:**
    
    The dataset used in this project is limited to only 13 African countries, which may not provide a comprehensive view of Economic situation in the entire African continent let alone at a global scale.
    The Dataset is also limited to the time period 1860 to 2014 so it does not reflect the current economic situation in Africa. The focus of the project is on the correlation between inflation and inflation crises and does not tackle the full complexity of the economic situation in Africa.
    """
    )
