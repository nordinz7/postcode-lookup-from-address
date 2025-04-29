import pandas as pd
import re
import os
from datetime import datetime


# Load the uploaded CSV file
file_path = "./input.csv"

try:
    print("Step 1: Loading the uploaded CSV file...")
    df = pd.read_csv(file_path)
    print("CSV file loaded successfully.")
except FileNotFoundError:
    print(
        f"ERROR: The file '{file_path}' was not found. Please check the file name and location."
    )
    exit(1)
except Exception as e:
    print(f"ERROR: Could not load the CSV file. Details: {e}")
    exit(1)

# Generate output file name based on input file name and timestamp
base_name = os.path.splitext(os.path.basename(file_path))[0]
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file_path = f"./{base_name}_GENERATED_{timestamp}.csv"

print("\nStep 2: Checking for required address columns...")
required_columns = ["CustomerAdd1", "CustomerAdd2", "CustomerAdd3", "CustomerAdd4"]
missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    print(
        f"ERROR: The following required columns are missing from the CSV: {missing_cols}"
    )
    exit(1)
else:
    print("All required address columns are present.")

# Display the first few rows and column names to understand the structure
print("\nStep 3: Previewing the data (first 5 rows):")
print(df.head())

# Combine all address fields into a single address string
print("\nStep 4: Combining address fields into a single column...")
df["FullAddress"] = (
    df[["CustomerAdd1", "CustomerAdd2", "CustomerAdd3", "CustomerAdd4"]]
    .fillna("")
    .agg(" ".join, axis=1)
)
print("Address fields combined into 'FullAddress'.")

# Extract 5-digit postcode using regex
print("\nStep 5: Extracting 5-digit postcode from the full address...")
df["Postcode"] = df["FullAddress"].apply(lambda x: re.search(r"\b\d{5}\b", x))
df["Postcode"] = df["Postcode"].apply(lambda x: x.group() if x else None)
print("Postcode extraction complete.")

# Lookup City and State from db.csv
print("\nStep 5b: Looking up City and State from postcode database...")
db = pd.read_csv("./db.csv", sep="\t")
db["Postcode"] = db["Postcode"].astype(str)
df["Postcode"] = df["Postcode"].astype(str)
df = df.merge(db, on="Postcode", how="left")
print("City and State lookup complete.")

# Show a sample of the postcode, city, and state
print("\nStep 6: Sample of Postcode, City, and State:")
print(df[["Postcode", "City", "State"]].head(10))

# Save the updated DataFrame to a new CSV file (exclude FullAddress)
print("\nStep 7: Saving the updated data to a new CSV file...")
output_columns = [col for col in df.columns if col != "FullAddress"]
df.to_csv(output_file_path, index=False, columns=output_columns)
print(f"\nSUCCESS: The updated file has been saved as:\n{output_file_path}\n")
print(
    "You can now open this file in Excel or another spreadsheet program to review the results."
)
