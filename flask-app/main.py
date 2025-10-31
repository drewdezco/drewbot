import pandas as pd
import numpy as np
import random

def setup_environment():
    """
    Import necessary libraries and return them.

    Returns:
    tuple: A tuple containing the imported `pandas`, `numpy`, and `random` modules.

    This function serves to modularize the code by importing and returning the essential
    libraries required in the script.
    """
    import pandas as pd
    import numpy as np
    import random
    return pd, np, random

def set_random_seed(seed=42):
    """
    Set the random seed for the random and numpy libraries to ensure reproducibility.

    Parameters:
    seed (int): The seed value to use for initialization. Default is 42.

    This function sets the seed for Python's built-in random library
    and NumPy's random number generator. Using the same seed across runs
    guarantees that you get the same sequence of random numbers, which is
    particularly beneficial during development and testing to ensure consistent
    behavior and output.
    """
    random.seed(seed)
    np.random.seed(seed)

def create_dataframe():
    """
    Create a DataFrame with business-related columns and random data.

    Returns:
    DataFrame: A pandas DataFrame with synthetic data for analysis.

    The generated DataFrame contains columns like `Revenue`, `Expenses`, `Profit`, etc.,
    with random values suitable for simulating a business data analysis scenario.
    """
    columns = ['Business_ID', 'Revenue', 'Expenses', 'Profit', 
               'Number_of_Employees', 'Customer_Satisfaction', 
               'Market_Share', 'Growth_Rate', 'Industry_Ranking']
    data = pd.DataFrame({
        'Business_ID': range(1, 126),
        'Revenue': np.random.randint(10000, 1000000, size=125),
        'Expenses': np.random.randint(5000, 500000, size=125),
        'Profit': np.random.randint(0, 500000, size=125),
        'Number_of_Employees': np.random.randint(10, 1000, size=125),
        'Customer_Satisfaction': np.random.rand(125) * 100,
        'Market_Share': np.random.rand(125) * 100,
        'Growth_Rate': np.random.rand(125) * 10,
        'Industry_Ranking': np.random.randint(1, 100, size=125)
    })
    return data

def introduce_missing_data(data, fraction=0.1):
    """
    Introduce missing values into a DataFrame.

    Parameters:
    data (DataFrame): The DataFrame to modify.
    fraction (float): The fraction of data to be replaced with NaN values. Default is 0.1.

    Iterates through the columns and randomly assigns NaN values in them based on the specified fraction
    to simulate real-world scenarios where data may be incomplete.
    """
    for col in data.columns[1:]:
        data.loc[data.sample(frac=fraction).index, col] = np.nan

def analyze_data(data):
    """
    Provide a summary analysis of the data.

    Parameters:
    data (DataFrame): The DataFrame to analyze.

    Returns:
    tuple: A tuple containing a DataFrame summary and metrics.

    Generates descriptive statistics and additional metrics like count of missing values, mean, and median
    for the DataFrame, helping to understand the dataset in practical scenarios.
    """
    data_summary = data.describe()
    missing_values_count = data.isnull().sum()
    metrics = pd.DataFrame({
        'Mean': data.mean(),
        'Median': data.median(),
        'Missing_Values_Count': missing_values_count
    })
    return data_summary, metrics

def main():
    """
    Execute the main workflow for data simulation and analysis.

    This function sets up the environment, seeds random number generators,
    creates and modifies a DataFrame with synthetic data, introduces missing data,
    and performs data analysis, printing the results.
    """
    print("Running test script...")
    setup_environment()
    set_random_seed()
    data = create_dataframe()
    introduce_missing_data(data)
    data_summary, metrics = analyze_data(data)
    print(data_summary)
    print(metrics)

main()