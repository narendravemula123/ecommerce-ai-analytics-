

import pandas as pd
import datetime
from openai import OpenAI

client = OpenAI()   # ✅ no key here

# Load data
def load_data():
    return pd.read_csv("Data/sales_data.csv")

# Process data
def process_data(df):
    df["revenue"] = df["price"] * df["units_sold"]
    return df

# Generate KPIs
def generate_kpis(df):
    total_revenue = df["revenue"].sum()

    # Top product
    top_product = df.loc[df["revenue"].idxmax()]

    # Category revenue
    category_revenue = df.groupby("category")["revenue"].sum()
    best_category = category_revenue.idxmax()

    # Average Order Value
    avg_order_value = df["revenue"].mean()

    # Top 3 products
    top_3_products = df.sort_values(by="revenue", ascending=False).head(3)

    # Category contribution %
    category_percentage = (category_revenue / total_revenue) * 100

    return (
        total_revenue,
        top_product,
        category_revenue,
        best_category,
        avg_order_value,
        top_3_products,
        category_percentage
    )
def generate_ai_description(product_name, category):
    return f"{product_name} is a premium product in the {category} category, designed with quality, durability, and customer satisfaction in mind. Ideal for everyday use and optimized for modern e-commerce standards."




# Save report
def save_report(df, category_revenue):
    output_file = "Output/report.xlsx"
    with pd.ExcelWriter(output_file, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, sheet_name="Raw Data", index=False)
        category_revenue.to_excel(writer, sheet_name="Category Revenue")

# Main workflow
def main():
    print("Starting pipeline...")

    df = load_data()
    df = process_data(df)

    (total_revenue, top_product, category_revenue, best_category,
     avg_order_value, top_3_products, category_percentage) = generate_kpis(df)

    # 🔥 CLEAN ANALYTICS OUTPUT
    print("\n========== E-COMMERCE ANALYTICS REPORT ==========")

    print(f"\nTotal Revenue: {total_revenue}")

    print("\nTop Product:")
    print(top_product)

    print("\nCategory Revenue:")
    print(category_revenue)

    print(f"\nBest Category: {best_category}")

    print(f"\nAverage Order Value: {avg_order_value}")

    print("\nTop 3 Products:")
    print(top_3_products)

    print("\nCategory Contribution (%):")
    print(category_percentage)

    print("\n===============================================")

    # Save report
    save_report(df, category_revenue)

    print("\nReport saved successfully")
    print("Executed at:", datetime.datetime.now())

    # 🔥 AI OUTPUT (PROPERLY INDENTED)
    print("\n========== AI GENERATED DESCRIPTIONS ==========")

    for _, row in df.head(3).iterrows():
        desc = generate_ai_description(row["product_name"], row["category"])
        print(f"\n{row['product_name']}:\n{desc}")

    print("\n===============================================")


if __name__ == "__main__":
    main()