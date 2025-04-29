# Address Lookup Automation

This project processes address data from CSV files, extracts postcodes, and looks up city/state information using a postcode database. It is designed for batch processing and can be replicated easily by IT or other users.

## Project Structure

- `app.py`: Main Python script for processing input CSV files.
- `db.csv`: Postcode-to-city/state mapping database (tab-separated).
- `input.csv` and `input_GENERATED_*.csv`: Input address data files (comma-separated).
- `requirements.txt`: Python dependencies.

## Prerequisites

- Python 3.8 or newer
- pip (Python package manager)

## Setup Instructions

1. **Clone the repository**
   ```sh
   git clone <your-remote-repo-url>
   cd addr-lookup
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Prepare input files**
   - Place your input CSV files in the project directory (e.g., `input.csv`).
   - Ensure `db.csv` (postcode database) is present in the same directory.

4. **Run the script**
   ```sh
   python app.py
   ```
   - The script will process the input file, extract postcodes, look up city/state, and save the output as a new CSV file.

## File Descriptions

- **app.py**: Reads input CSV, combines address fields, extracts 5-digit postcodes using regex, merges with `db.csv` for city/state lookup, and writes the result to a new CSV.
- **db.csv**: Tab-separated file mapping postcodes to city and state.
- **input.csv**: Example input file with address data. You can use your own files with the same format.
- **input_GENERATED_*.csv**: Example generated input files.
- **requirements.txt**: Lists required Python packages.

## Example Usage

```sh
python app.py
```

## Pushing to Remote Repository

1. Initialize git (if not already):
   ```sh
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-remote-repo-url>
   git push -u origin main
   ```

## Notes
- Input and output CSVs are ignored in `.gitignore` to avoid pushing large or sensitive data.
- For any issues, check that your input files match the expected format and that all dependencies are installed.
