import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


FILE_PATH = "Employee_Survey_Results.xlsx"

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
    # Show the group means
    group_by_results(df)
    # Visualize the relationships
    visualize_relationships(df)