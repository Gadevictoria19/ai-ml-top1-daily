import numpy as np
import pandas as pd
def generate(n_rows:int=1000)->pd.DataFrames:
    np.random.seed(42)
    data={
        'Customer_id': np.random.randint(10000, 99999, size=n_rows),
        'Age':np.random.choice([19,25,35,45,np.nan,52,61],size=n_rows),
        'Join_Date':pd.date_range(start='2023-01-01',periods=n_rows,freq='h'),
        'Transaction_Amount': np.random.uniform(-50, 500, size=n_rows),
        'Region': np.random.choice(['North', 'South', 'East', 'West', None], size=n_rows),
        'Device': np.random.choice(['iOS', 'Android', 'Web'], size=n_rows)

    }
    return pd.DataFrame(data)
def clean_and_process_data(df: pd.DataFrame) -> pd.DataFrame:
    processed_df = df.copy()
    median_age = processed_df['Age'].median()
    processed_df['Age'] = processed_df['Age'].fillna(median_age)
    processed_df['Region'] = processed_df['Region'].fillna('Unknown')
    processed_df['Transaction_Amount'] = processed_df['Transaction_Amount'].clip(lower=0.0)
    
    return processed_df
def merge_regional_tax(df: pd.DataFrame) -> pd.DataFrame:
    """Performs a safe left join with regional reference tax rates."""
    tax_data = pd.DataFrame({
        'Region': ['North', 'South', 'East', 'West'],
        'Tax_Rate': [0.05, 0.07, 0.06, 0.08]
    })
    
    merged_df = pd.merge(df, tax_data, on='Region', how='left')
    merged_df['Tax_Rate'] = merged_df['Tax_Rate'].fillna(0.00)
    return merged_df

if __name__ == "__main__":
    print("🚀 Initializing Pipeline Verification Loop...")
    
    
    raw_df = generate()
    cleaned_df = clean_and_process_data(raw_df)
    final_df = merge_regional_tax(cleaned_df)
    
    
    assert final_df['Age'].isnull().sum() == 0, "Data Integrity Error: Missing ages remain!"
    assert (final_df['Transaction_Amount'] < 0).sum() == 0, "Data Integrity Error: Negative balances found!"
    assert final_df.shape[0] == 1000, "Data Integrity Error: Rows were dropped during processing!"
    
    print("✅ All Pipeline Integrity Checks Passed! Sample output:")
    print(final_df.head(3))