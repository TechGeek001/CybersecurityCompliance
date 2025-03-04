import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pointbiserialr
import seaborn as sns


FILE_PATH = "Employee_Survey_Results.xlsx"

def visualize_point_biserial(df):
    # Calculate point-biserial correlations for each continuous variable
    point_biserial_results = {}
    for col in ['strong_passwords', 'team_expectation', 'phishing_confidence', 'training_hours']:
        corr, p_value = pointbiserialr(df['clicked_suspicious_link'], df[col])
        point_biserial_results[col] = {'Correlation': corr, 'p-value': p_value}

    # Extract correlation coefficients for visualization
    correlations = [result['Correlation'] for result in point_biserial_results.values()]
    variables = list(point_biserial_results.keys())

    # Box Plots for Each Continuous Variable (split by binary outcome)
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    sns.boxplot(x='clicked_suspicious_link', y='strong_passwords', data=df, ax=axes[0, 0], palette='coolwarm', legend=False)
    axes[0, 0].set_title('Strong Passwords vs Clicked Link')
    sns.boxplot(x='clicked_suspicious_link', y='team_expectation', data=df, ax=axes[0, 1], palette='coolwarm', legend=False)
    axes[0, 1].set_title('Team Expectation vs Clicked Link')
    sns.boxplot(x='clicked_suspicious_link', y='phishing_confidence', data=df, ax=axes[1, 0], palette='coolwarm', legend=False)
    axes[1, 0].set_title('Phishing Confidence vs Clicked Link')
    sns.boxplot(x='clicked_suspicious_link', y='training_hours', data=df, ax=axes[1, 1], palette='coolwarm', legend=False)
    axes[1, 1].set_title('Training Hours vs Clicked Link')
    plt.tight_layout()
    plt.show()

def analyze_correlations(df):
    """
    Analyzes correlations in the provided DataFrame and prints results in a formatted way.
    
    Args:
        df (pd.DataFrame): Preprocessed DataFrame with columns:
            - 'strong_passwords'
            - 'team_expectation'
            - 'phishing_confidence'
            - 'clicked_suspicious_link' (bool)
            - 'training_hours'
    """
    # Descriptive statistics for continuous variables
    total = len(df)
    num_passed = df['passed_phishing_test'].sum()
    descriptive_stats = df[['strong_passwords', 'team_expectation', 'phishing_confidence', 'training_hours']].describe()

    # Percentage of Yes/No for the binary column
    clicked_counts = df['clicked_suspicious_link'].value_counts(normalize=True) * 100

    # Point-biserial correlations for binary column against continuous variables
    point_biserial_results = {}
    for col in ['strong_passwords', 'team_expectation', 'phishing_confidence', 'training_hours']:
        corr, p_value = pointbiserialr(df['clicked_suspicious_link'], df[col])
        point_biserial_results[col] = {'Correlation': corr, 'p-value': p_value}

    # Print results in a formatted way
    print(
        "Employee Survey Results (Point-Biserial):\n"
        "\n"
        "   Strong Passwords:\n"
        f"      Point-Biserial r-value:{point_biserial_results['strong_passwords']['Correlation']:.2f}\n"
        f"      p-value:               {point_biserial_results['strong_passwords']['p-value']:.3e}\n"
        "\n"
        "   Team Expectation:\n"
        f"      Point-Biserial r-value:{point_biserial_results['team_expectation']['Correlation']:.2f}\n"
        f"      p-value:               {point_biserial_results['team_expectation']['p-value']:.3e}\n"
        "\n"
        "   Phishing Confidence:\n"
        f"      Point-Biserial r-value:{point_biserial_results['phishing_confidence']['Correlation']:.2f}\n"
        f"      p-value:               {point_biserial_results['phishing_confidence']['p-value']:.3e}\n"
        "\n"
        "   Training Hours:\n"
        f"      Point-Biserial r-value:{point_biserial_results['training_hours']['Correlation']:.2f}\n"
        f"      p-value:               {point_biserial_results['training_hours']['p-value']:.3e}\n"
    )

def calculate_basic_stats(df):
    total = len(df)
    num_passed = df['passed_phishing_test'].sum()
    stats = (
        "Employee Survey Results:\n"
        "\n"
        "   Phishing Test Results:\n"
        f"      Passed:                {num_passed} ({round((num_passed / total) * 100, 2)}%)\n"
        "\n"
        "   Strong Passwords:\n"
        f"      Mean:                  {df['strong_passwords'].mean()}\n"
        f"      Median:                {df['strong_passwords'].median()}\n"
        f"      Correlation (r-value): {df['strong_passwords'].corr(df['passed_phishing_test']).round(2)}\n"
        "   Team Expectation:\n"
        f"      Mean:                  {df['team_expectation'].mean()}\n"
        f"      Median:                {df['team_expectation'].median()}\n"
        f"      Correlation (r-value): {df['team_expectation'].corr(df['passed_phishing_test']).round(2)}\n"
        "   Phishing Confidence:\n"
        f"      Mean:                  {df['phishing_confidence'].mean()}\n"
        f"      Median:                {df['phishing_confidence'].median()}\n"
        f"      Correlation (r-value): {df['phishing_confidence'].corr(df['passed_phishing_test']).round(2)}\n"
        "   Training Hours:\n"
        f"      Mean:                  {df['training_hours'].mean()}\n"
        f"      Median:                {df['training_hours'].median()}\n"
        f"      Correlation (r-value): {df['training_hours'].corr(df['passed_phishing_test']).round(2)}\n"
    )
    print(stats)


def group_by_results(df):
    # Group by "Clicked Suspicious Link (Yes/No)" and compute means
    group_means = df.groupby('clicked_suspicious_link')[
        ['strong_passwords', 'team_expectation', 
        'phishing_confidence', 'training_hours']
    ].mean()
    print(group_means)


def visualize_relationships(df):
    # List of metrics to analyze
    metrics = ['strong_passwords', 'team_expectation', 'phishing_confidence', 'training_hours']
    
    # Correlation Matrix Heatmap for the Numeric Features
    corr = df[metrics].corr()
    plt.figure(figsize=(6,5))
    heatmap = plt.imshow(corr, cmap='coolwarm', interpolation='none', aspect='auto')
    plt.colorbar(heatmap)
    plt.xticks(range(len(corr)), corr.columns, rotation=45)
    plt.yticks(range(len(corr)), corr.index)
    plt.title('Correlation Matrix')
    # Annotate the heatmap with correlation values
    for (i, j), val in np.ndenumerate(corr):
        plt.text(j, i, f"{val:.2f}", ha='center', va='center', 
                 color='white' if abs(val) > 0.5 else 'black')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    df = pd.read_excel(FILE_PATH)
    # Rename the columns to make them more Pythonic (and easier to type)
    df.rename(
        columns={
            "Employee ID": "employee_id",
            "Strong Passwords (1-5)": "strong_passwords",
            "Team Expectation (1-5)": "team_expectation",
            "Phishing Confidence (1-5)": "phishing_confidence",
            "Clicked Suspicious Link (Yes/No)": "clicked_suspicious_link",
            "Training Hours (0-10)": "training_hours",
        },
        inplace=True
    )
    # Create the "passed_phishing_test" column; a boolean
    # Invert the result so that "Yes" is False and "No" is True
    df["clicked_suspicious_link"] = df["clicked_suspicious_link"].replace({"Yes": True, "No": False})
    df["passed_phishing_test"] = df["clicked_suspicious_link"] != True
    # Show the basic statistics
    calculate_basic_stats(df)
    #Show stats for point-biserial correlations
    analyze_correlations(df)
    # Show the group means
    group_by_results(df)
    # Visualize the relationships
    visualize_relationships(df)
    #Point biserial based visualizations
    visualize_point_biserial(df)