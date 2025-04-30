import pandas as pd
import re
from datetime import datetime

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
INPUT_FILE_PATH = "./input.csv"
OUTPUT_FILE_PATH = f"./output_{ts}.csv"
ADDRESS_COLUMNS = ["CustomerAdd1", "CustomerAdd2", "CustomerAdd3", "CustomerAdd4"]
DEFAULT_IF_REQUIRED_NOT_FOUND = "TBA"

# {'billing', 'customs', 'depot', 'forwarder', 'freightForwarder', 'haulier', 'liner', 'oneTimeVendor', 'port', 'shipperConsignee', 'shippingAgent', 'transporter', 'warehouse'}
COMPANY_TYPES = ["shipperConsignee"]

# {'BILLING', 'CONTACT', 'DELIVERY', 'MAILING', 'WAREHOUSE'}
ADDRESS_TYPE = "BILLING"

try:
    print("Step 1: Loading the uploaded CSV file...")
    df = pd.read_csv(INPUT_FILE_PATH)
    print("CSV file loaded successfully.")
except FileNotFoundError:
    print(
        f"ERROR: The file '{INPUT_FILE_PATH}' was not found. Please check the file name and location."
    )
    exit(1)
except Exception as e:
    print(f"ERROR: Could not load the CSV file. Details: {e}")
    exit(1)


print("\nStep 2: Checking for required address columns...")
missing_cols = [col for col in ADDRESS_COLUMNS if col not in df.columns]
if missing_cols:
    print(
        f"ERROR: The following required columns are missing from the CSV: {missing_cols}"
    )
    exit(1)
else:
    print("All required address columns are present.")

print("\nStep 3: Previewing the data (first 5 rows):")
print(df.head())

print("\nStep 4: Combining address fields into a single column...")
df["FullAddress"] = df[ADDRESS_COLUMNS].fillna("").agg(" ".join, axis=1)
print("Address fields combined into 'FullAddress'.")

# Extract 5-digit postcode using regex
print("\nStep 5: Extracting 5-digit postcode from the full address...")


def extract_postcode(address):
    matches = re.findall(r"\b\d{5}\b", address)
    return matches[-1] if matches else None


df["Postcode"] = df["FullAddress"].apply(extract_postcode)
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

# Prepare the final output DataFrame with the required column mapping
print("\nStep 6b: Remapping columns to the required output structure...")


def get_debtor_code(row):
    if pd.notnull(row.get("CustomerDebtorCodeNew")):
        return row["CustomerDebtorCodeNew"]
    elif pd.notnull(row.get("customerDebtorCode")):
        return row["customerDebtorCode"]
    return ""


# Ensure 'CustomerName' is not empty; if empty, set to DEFAULT_IF_REQUIRED_NOT_FOUND
name_filled = (
    df.get("CustomerName", "")
    .fillna("")
    .apply(lambda x: x if str(x).strip() else DEFAULT_IF_REQUIRED_NOT_FOUND)
)

output_df = pd.DataFrame(
    {
        # --- General Info ---
        "no": "",
        "code": df.get("CustomerCode", ""),
        "name": name_filled,
        "description": "",
        "status": "activated",
        "tags": "",
        "overrideDuplicateCode": True,
        "types": COMPANY_TYPES * len(df),
        # --- Country & Currency ---
        "country.name": "Malaysia",
        "country.alpha3": "MYS",
        "currency.code": "MYR",
        "currency.uuid": "",
        # --- Billing/Creditor ---
        "billTo.code": "",
        "billTo.uuid": "",
        "creditorCode": "",
        "creditorTerm": df.get("CustomerTerm", ""),
        # --- Debtor ---
        "debtorCode": df.apply(get_debtor_code, axis=1),
        "debtorTerm": "",
        # --- Tax/Registration ---
        "taxNumber": "",
        "registration": "",
        # --- UUID ---
        "uuid": "",
        # --- Address ---
        "address.name": df.get("CustomerName", DEFAULT_IF_REQUIRED_NOT_FOUND),
        "address.type": ADDRESS_TYPE,
        "address.countryAlpha3": "MYS",
        "address.address1": df.get("CustomerAdd1", "").apply(str),
        "address.address2": df.get("CustomerAdd2", "").apply(str),
        "address.address3": df.get("CustomerAdd3", "").apply(str),
        "address.address4": df.get("CustomerAdd4", "").apply(str),
        "address.city": df.get("City", "").apply(str),
        "address.district": df.get("City", "").apply(str),
        "address.postCode": df.get("Postcode", "").apply(str),
        "address.areaCode": df.get("areaCode", DEFAULT_IF_REQUIRED_NOT_FOUND),
        "address.zone": df.get("zone", DEFAULT_IF_REQUIRED_NOT_FOUND),
        "address.location.type": "",
        "address.location.coordinates": "",
        "address.phone": df.get("CustomerTel", "").apply(str),
        "address.fax": df.get("CustomerFax", "").apply(str),
        "address.tags": ["isDefault"] * len(df),
        "address.status": "activated",
        "address.uuid": "",
        "address.zzz": "",
        # --- Contact ---
        "contact.name": df.get("CustomerContact", ""),
        "contact.email": df.get("CustomerEmail", ""),
        "contact.phone": df.get("CustomerTel", ""),
        "contact.title": "",
        "contact.designation": "",
        "contact.notes": "",
        "contact.status": "activated",
        "contact.uuid": "",
        "contact.zzz": "",
    }
)

print("Column remapping complete. Preview of remapped data:")
print(output_df.head())

# Save the updated DataFrame to a new CSV file (exclude FullAddress)
print("\nStep 7: Saving the updated data to a new CSV file...")
output_columns = [col for col in output_df.columns]
output_df.to_csv(OUTPUT_FILE_PATH, index=False, columns=output_columns)
print(f"\nSUCCESS: The updated file has been saved as:\n{OUTPUT_FILE_PATH}\n")
print(
    "You can now open this file in Excel or another spreadsheet program to review the results."
)
