import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_verify_data(data_path: str) -> pd.DataFrame:
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"❌ Missing critical dataset! Checked here: {os.path.abspath(data_path)}")
    df = pd.read_csv(data_path)
    print(f"📥 Step 1: Loaded dataset successfully. Shape: {df.shape}")
    return df

def execute_cleaning_layer(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    # Impute numeric columns with column median
    for col in cleaned.select_dtypes(include=[np.number]).columns:
        if cleaned[col].isnull().sum() > 0:
            cleaned[col] = cleaned[col].fillna(cleaned[col].median())
    # Impute text columns with "Unknown"
    for col in cleaned.select_dtypes(exclude=[np.number]).columns:
        if cleaned[col].isnull().sum() > 0:
            cleaned[col] = cleaned[col].fillna("Unknown")
    print("🧹 Step 2: Completed data cleaning layer.")
    return cleaned

def generate_analytical_artifacts(df: pd.DataFrame) -> None:
    os.makedirs("logs", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    
    # Dynamically find columns so no yellow squiggly lines happen
    cat_cols = df.select_dtypes(exclude=[np.number]).columns
    num_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(cat_cols) > 0 and len(num_cols) >= 2:
        group_feature = cat_cols[0]
        metric_1, metric_2 = num_cols[0], num_cols[1]
        
        print(f"📊 Step 3: Extracting metrics grouped by '{group_feature}'...")
        summary_stats = df.groupby(group_feature).agg({
            metric_1: ['mean', 'max'],
            metric_2: ['mean', 'std']
        })
        
        summary_stats.columns = ['_'.join(col).strip() for col in summary_stats.columns]
        summary_stats = summary_stats.reset_index()
        
        with open(os.path.join("logs", "pipeline_summary_report.md"), 'w', encoding='utf-8') as f:
            f.write("# 📊 Automated Pipeline Summary Report\n\n")
            f.write(summary_stats.to_markdown(index=False))
        print("📁 Summary markdown log generated inside 'logs/' folder.")

# 🚀 THIS IS THE ENGINE THAT ACTUALLY RUNS EVERYTHING
if __name__ == "__main__":
    print("🚀 Starting Day 6 Pipeline Run...")
    input_csv = os.path.join("scripts", "housing.csv")
    
    try:
        raw_data = load_and_verify_data(input_csv)
        clean_data = execute_cleaning_layer(raw_data)
        generate_analytical_artifacts(clean_data)
        print("\n🎉 Pipeline execution completed with 100% success!")
    except Exception as e:
        print(f"\n❌ Pipeline crashed due to:\n{e}")