
from pathlib import Path
import pandas as pd

# Folder paths
DATA_FOLDER = Path("Data")
CLEAN_FOLDER = Path("Clean Data")

# Create output folder
CLEAN_FOLDER.mkdir(parents=True, exist_ok=True)

# Numeric columns
NUMERIC_COLUMNS = {
    "Quantity", "Unit_Price", "Shipping_Cost", "Discount",
    "Unit_Cost", "Current_Stock", "Reorder_Level",
    "Record_Count", "Total_Orders", "Total_Sales",
    "Valid_Records_Rate", "Rejected_Records",
    "Missing_Rate", "Duplicate_Rate"
}

# Date columns
DATE_COLUMNS = {
    "Order_Date", "Ship_Date", "Date"
}

# Text columns to standardize
STANDARD_TEXT_COLUMNS = {
    "Product_Name", "Category", "Order_Status",
    "Payment_Method", "Region", "Customer_Segment"
}


def clean_csv(file_path):

    print(f"\nCleaning: {file_path.name}")

    # Read CSV and preserve IDs as strings
    df = pd.read_csv(file_path, dtype="string")

    # 1. String Cleaning
    for col in df.columns:
        df[col] = df[col].str.strip()
        df[col] = df[col].replace("", pd.NA)

    # 2. Data Type Conversion
    for col in NUMERIC_COLUMNS.intersection(df.columns):

        values = (
            df[col]
            .astype("string")
            .str.replace(",", "", regex=False)
            .str.strip()
        )

        df[col] = pd.to_numeric(
            values,
            errors="coerce"
        )

    # 3. Date Cleaning
    for col in DATE_COLUMNS.intersection(df.columns):

        parsed = pd.to_datetime(
            df[col],
            errors="coerce"
        )

        formatted = parsed.dt.strftime(
            "%Y-%m-%d"
        ).astype("string")

        df[col] = formatted.mask(
            parsed.isna(),
            pd.NA
        )

    # 4. Data Standardization
    for col in STANDARD_TEXT_COLUMNS.intersection(df.columns):

        df[col] = (
            df[col]
            .astype("string")
            .str.title()
        )

    # 5. Invalid Values Handling
    non_negative_columns = [
        "Unit_Price",
        "Shipping_Cost",
        "Unit_Cost",
        "Current_Stock",
        "Reorder_Level",
        "Record_Count",
        "Total_Orders",
        "Total_Sales",
        "Rejected_Records"
    ]

    for col in non_negative_columns:

        if col in df.columns:
            df.loc[df[col] < 0, col] = pd.NA

    if "Quantity" in df.columns:
        df.loc[df["Quantity"] <= 0, "Quantity"] = pd.NA

    # 6. Validate Discounts and Rates
    for col in [
        "Discount",
        "Valid_Records_Rate",
        "Missing_Rate",
        "Duplicate_Rate"
    ]:

        if col in df.columns:
            df.loc[
                ~df[col].between(0, 1),
                col
            ] = pd.NA

    # 7. Date Validation
    if {"Order_Date", "Ship_Date"}.issubset(df.columns):

        order_dates = pd.to_datetime(
            df["Order_Date"],
            errors="coerce"
        )

        ship_dates = pd.to_datetime(
            df["Ship_Date"],
            errors="coerce"
        )

        df.loc[
            ship_dates < order_dates,
            "Ship_Date"
        ] = pd.NA

    # 8. Duplicate Removal
    before = len(df)

    df = df.drop_duplicates()

    removed_duplicates = before - len(df)

    # 9. Missing Values Handling
    # Convert columns to object before inserting Unknown
    df = df.astype("object").where(
        df.notna(),
        "Unknown"
    )

    # 10. Save Cleaned CSV
    output_path = CLEAN_FOLDER / file_path.name

    df.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Rows saved: {len(df)}")
    print(f"Duplicates removed: {removed_duplicates}")
    print(f"Saved to: {output_path}")


def main():

    # Check Data folder
    if not DATA_FOLDER.exists():

        print("Error: Data folder not found!")
        print("Make sure Data folder is next to this script.")

        return

    # Get all CSV files
    csv_files = sorted(
        DATA_FOLDER.glob("*.csv")
    )

    if not csv_files:

        print("No CSV files found!")
        return

    print(f"Found {len(csv_files)} CSV file(s).")

    successful = 0
    failed = 0

    # Loop through all CSV files
    for file_path in csv_files:

        try:

            clean_csv(file_path)
            successful += 1

        except Exception as error:

            failed += 1

            print(
                f"Could not clean {file_path.name}: {error}"
            )

    # Final report
    print("\nProcessing Finished!")

    print(f"Successfully cleaned: {successful}")
    print(f"Failed: {failed}")

    print(
        f"Cleaned files folder: {CLEAN_FOLDER.resolve()}"
    )


if __name__ == "__main__":

    main()
