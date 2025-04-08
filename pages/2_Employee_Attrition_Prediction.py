import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.patches as mpatches


df = pd.read_csv("data/Employee-Attrition.xls")
df.drop(
    ["EmployeeCount", "EmployeeNumber", "Over18", "StandardHours"],
    axis="columns",
    inplace=True,
)

categorical_col = []
for column in df.columns:
    if df[column].dtype == object and len(df[column].unique()) <= 50:
        categorical_col.append(column)

df["Attrition"] = df.Attrition.astype("category").cat.codes

st.title("Employee Attrition Prediction")

# st.sidebar.header("Dataset Information")


pages = [
    "Data Overview",
    "Decision Tree Classifier",
    "Random Forest Classifier",
]

selected_view = st.sidebar.selectbox("Select View", pages)

if selected_view == "Data Overview":
    kaggle_url = "https://www.kaggle.com/datasets/uniabhi/ibm-hr-analytics-employee-attrition-performance/data"
    notebook_url = "https://www.kaggle.com/code/marianbota/predicting-employee-attrition"

    st.markdown(
        """
    This project is based on the dataset from [Kaggle](%s) that contains a synthetic data created by IBM data scientists.
    Going through the views that can be selected in the left pane we will see that simple data visualizations as the ones presented below do not provide powerful insights into what causes employee attrition.
    As a note the three graphs below are for the percentage of attrition by age, monthly income and overtime which have been identified as we will see later on as being the three most important factors for employee attrition.
    The full notebook can be found [here](%s).
    """
        % (kaggle_url, notebook_url)
    )

    attrition = df[df["Attrition"] == 1].groupby("Age")["Attrition"].count().reset_index()
    total = df.groupby("Age")["Attrition"].count().reset_index()
    attrition["percent_attrition"] = [
        i / j * 100 for i, j in zip(attrition["Attrition"], total["Attrition"])
    ]
    # Create graph of attrition percentage by age
    fig = plt.figure()
    sns.barplot(
        x="Age",
        y="percent_attrition",
        data=attrition,
        color="darkblue",
    )
    plt.ylim(0, 115)
    plt.ylabel("Attrition Percentage")
    plt.xlabel("Age")
    plt.title("Attrition Percentage by Age")
    plt.tick_params(labelsize=7)
    st.pyplot(fig)

    # Create copy df with 10 MonthlyIncome buckets and attrition percentage for each bucket
    bins = pd.IntervalIndex.from_tuples([(0, 2900), (2900, 4800), (4800, 6700), (6700, 8600), (8600, 10500), (10500, 12400), (12400, 14300), (14300, 16200), (16200, 18100), (18100, 20000)])
    income_bins = pd.cut(
        df["MonthlyIncome"], 
        bins, 
        include_lowest=True, 
        ordered=True
    )

    df["MonthlyIncomeBracket"] = income_bins

    attrition = (
        df[df["Attrition"] == 1]
        .groupby("MonthlyIncomeBracket", observed=False)["Attrition"]
        .count()
        .reset_index()
    )
    total = df.groupby("MonthlyIncomeBracket")["Attrition"].count().reset_index()
    attrition["percent_attrition"] = [
        i / j * 100 for i, j in zip(attrition["Attrition"], total["Attrition"])
    ]

    # Create graph of attrition percentage by MonthlyIncome
    fig = plt.figure()
    sns.barplot(
        x="MonthlyIncomeBracket",
        y="percent_attrition",
        data=attrition,
        color="darkblue",
    )
    plt.ylim(0, 115)
    plt.ylabel("Attrition Percentage")
    plt.xlabel("Monthly Income")
    plt.title("Attrition Percentage by Monthly Income")
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    st.pyplot(fig)

    # Create barplot of attrition percentage by OverTime
    attrition = (
        df[df["Attrition"] == 1]
        .groupby("OverTime")["Attrition"]
        .count()
        .reset_index()
    )
    total = df.groupby("OverTime")["Attrition"].count().reset_index()
    attrition["percent_attrition"] = [
        i / j * 100 for i, j in zip(attrition["Attrition"], total["Attrition"])
    ]
    # Create graph of attrition percentage by OverTime
    fig = plt.figure()
    sns.barplot(
        x="OverTime",
        y="percent_attrition",
        data=attrition,
        color="darkblue",
    )
    plt.ylim(0, 115)
    plt.ylabel("Attrition Percentage")
    plt.xlabel("OverTime")
    plt.title("Attrition Percentage by OverTime")
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    st.pyplot(fig)

    st.markdown("""
    As we can see from the graph there is some correlation between age and attrition, however it would be hard to use any single feature to predict attrition.
                For such a dataset, a decision tree classifier or a random forest classifier would be a better choice.
    """)


if selected_view == "Decision Tree Classifier":
    kaggle_url = "https://www.kaggle.com/datasets/uniabhi/ibm-hr-analytics-employee-attrition-performance/data"
    notebook_url = (
        "https://www.kaggle.com/code/marianbota/predicting-employee-attrition"
    )

    st.markdown(
        """
    The Decision Tree Classifier is a supervised learning algorithm that is used for classification problems.
    It works by splitting the data into subsets based on the value of the features.
    The decision tree is built by recursively splitting the data into subsets based on the value of the features.
    As can be seen in the [notebook](%s) the dataset is split into training and testing sets. The accuracy on the test set is 77.78 and this can be improved up to 86.78 using GridSearchCV. 
    """
        % (notebook_url)
    )

    st.text(
        """
            Test Result:
        ================================================
        Accuracy Score: 87.30%
        _______________________________________________

    """
    )
    st.markdown(
        """
        CLASSIFICATION REPORT:
        |    |    0     |     1 | accuracy  | macro avg | weighted avg
        |-------|------------|---------|-----------|-----------|----------------|
        precision  |  0.891304 |  0.592593 | 0.873016  |  0.741948  |    0.849986
        recall     |  0.971053 |  0.262295 | 0.873016  |  0.616674  |    0.873016
        f1-score   |  0.929471 |  0.363636 | 0.873016  |  0.646554  |    0.851204
        support    |380.000000 | 61.000000 | 0.873016  |441.000000  |  441.000000
    """
    )
    st.text(
        """
        _______________________________________________
        Confusion Matrix: 
        [[369  11]
        [ 45  16]]
        ================================================
        \n\n
        \n\n
    """
    )

    st.subheader("The resulting decision tree can be seen in the diagram below:")
    st.image("data/Decision_tree.png", caption="Decision Tree Classifier")


if selected_view == "Random Forest Classifier":
    kaggle_url = "https://www.kaggle.com/datasets/uniabhi/ibm-hr-analytics-employee-attrition-performance/data"
    notebook_url = (
        "https://www.kaggle.com/code/marianbota/predicting-employee-attrition"
    )

    st.markdown(
        """
    The Decision Tree Classifier has a few drawbacks such as overfitting and being sensitive to noise.
    The Random Forest Classifier is an ensemble method that uses multiple decision trees to make predictions.
    Some of the advantages typically associated with Random Forest Classifier are:
    - It is less prone to overfitting compared to a single decision tree.
    - It can better handle datasets with high dimensionality.
    - It usually has higher accuracy because the ensemble approach reduces the impact of individual tree errors and biases.
    - I can be more robust to outliers and noise in the data.
    As can be seen in the [notebook](%s) the accuracy on the test set does not improve significantly compared to the Decision Tree Classifier in this case.
    """
        % (notebook_url)
    )

    st.text(
        """
            Test Result:
        ================================================
        Accuracy Score: 86.17%
        _______________________________________________

    """
    )
    st.markdown(
        """
        CLASSIFICATION REPORT:
        |    |    0     |     1 | accuracy  | macro avg | weighted avg
        |-------|------------|---------|-----------|-----------|----------------|
        precision |   0.871795  | 0.500000 | 0.861678 |   0.685897   |   0.820367
        recall    |   0.984211  | 0.098361 | 0.861678 |   0.541286   |   0.861678
        f1-score  |   0.924598  | 0.164384 | 0.861678 |   0.544491   |   0.819444
        support   | 380.000000  |61.000000 | 0.861678 |  441.000000  |  441.000000
    """
    )
    st.text(
        """
        _______________________________________________
        Confusion Matrix: 
        [[374   6]
        [ 55   6]]
        ================================================
        \n\n
        \n\n
    """
    )

    st.subheader("The resulting feature importance scores are plotted below:")
    st.image("data/feature_comparison.png", caption="Feature Importance Score")

    st.markdown(
        """
                Conclusion: The two classifier algorithms have been very helpful in understanding the factors that influence employee attrition.
                The accuracy of the models can be helpful in predicting employee attrition, however the models are not perfect and should be used with caution.
                A very important aspect of the analysis is understanding feature importance scores as these could be the basis for future HR policies that could be implemented to reduce attrition.
    
                **Limitations:**
                The dataset used in this project is synthetic, which means it may not accurately represent real-world employee behavior and attrition patterns. While the models can provide insights into feature importance, the conclusions drawn from this dataset may not be generalizable to actual employee populations. Additionally, the project does not explore the potential impact of external factors (e.g., economic conditions, industry trends) on employee attrition, which could further enhance the analysis.
        
                """
    )
