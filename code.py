# ==========================================
# This project analyzes global tech layoffs from the year 2020 to 2025 and shows the below analysis
#1. Identify monthly layoff trends
#2. Find companies with highest layoffs
#3. Determine most impacted industries and where tech stands in it.
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("Current Working Directory:", os.getcwd())

sns.set_style("whitegrid")

# ======================
# Create Output Folder
# ======================
output_dir = "Output"
os.makedirs(output_dir, exist_ok=True)

# ======================
# Step 1: Load Dataset
# ======================
input_file = r"https://raw.githubusercontent.com/gsaipriyank/tech_layoffs_til_2025/refs/heads/main/tech_layoffs_til_2025.csv"
df = pd.read_csv(input_file)

print("Dataset Loaded Successfully")
print(df.head())

# ======================
# Step 2: Data Cleaning
# ======================

# Remove rows with missing values in important columns
df = df.dropna(subset=["Company", "Date_layoffs", "Laid_Off"])

# Convert date column
df["Date_layoffs"] = pd.to_datetime(df["Date_layoffs"])

# Extract Month & Year
df["Month"] = df["Date_layoffs"].dt.month
df["Year"] = df["Date_layoffs"].dt.year

# Standardize text
df["Company"] = df["Company"].str.strip().str.title()
df["Industry"] = df["Industry"].str.strip().str.title()

# ======================
# Step 3: Monthly Total Layoffs
# ======================

monthly = df.groupby(["Year", "Month"])["Laid_Off"].sum().reset_index()

plt.figure(figsize=(10,5))
sns.lineplot(data=monthly, x="Month", y="Laid_Off", hue="Year", marker="o")
plt.title("Monthly Total Employees Laid Off")
plt.xlabel("Month")
plt.ylabel("Total Employees Laid Off")
plt.xticks(range(1,13))
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "monthly_total_layoffs.png"))
plt.close()

# ======================
# Step 4: Top 10 Companies by Total Layoffs
# ======================

top_companies = df.groupby("Company")["Laid_Off"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,5))
top_companies.plot(kind="bar")
plt.title("Top 10 Companies by Total Layoffs")
plt.xlabel("Company")
plt.ylabel("Total Employees Laid Off")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "top_10_companies_total_layoffs.png"))
plt.close()

# ======================
# Step 5: Industry-wise Total Layoffs
# ======================

industry_totals = df.groupby("Industry")["Laid_Off"].sum().sort_values(ascending=False)

plt.figure(figsize=(10,6))
industry_totals.head(15).plot(kind="barh")
plt.title("Top 15 Industries by Total Layoffs")
plt.xlabel("Total Employees Laid Off")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "industry_total_layoffs.png"))
plt.close()

# ======================
# Step 6: Export Excel Summary
# ======================

monthly.to_excel(os.path.join(output_dir, "monthly_summary.xlsx"), index=False)
top_companies.to_excel(os.path.join(output_dir, "top_companies_summary.xlsx"))
industry_totals.to_excel(os.path.join(output_dir, "industry_summary.xlsx"))

print("\nAll charts and summary files generated successfully!")
print("Current Working Directory:", os.getcwd())
print("Check the 'Output' folder inside your project directory.")
