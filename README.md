# Data Scraping & Cleaning Project

## About the Project

I created this project to practice two important tasks in data work:
collecting data from a website and cleaning CSV files using Python.

The project is divided into two main parts: - **Scrapping:** I scrape
book information from the Books to Scrape website and save the collected
data in a CSV file. - **Cleaning:** I use Python to clean multiple CSV
files automatically and save the cleaned versions in a separate folder.

## Project Structure

``` text
Project/
│
├── Scrapping/
│   ├── Scrapping.py
│   └── books.csv
│
└── Cleaning/
    ├── clean_all_csv_files.py
    ├── Data/
    │   ├── customers_master.csv
    │   ├── new_daily_batch.csv
    │   ├── orders.csv
    │   ├── previous_days_summary.csv
    │   └── products_master.csv
    │
    └── Clean Data/
        ├── customers_master.csv
        ├── new_daily_batch.csv
        ├── orders.csv
        ├── previous_days_summary.csv
        └── products_master.csv
```

## 1. Web Scraping

**Folder:** `Scrapping/`\
**Script:** `Scrapping.py`\
**Source website:** [Books to Scrape](https://books.toscrape.com/)

In this part, I built a Python script to collect book data from the
Books to Scrape website. The website contains multiple pages, so the
script goes through the paginated catalog, extracts the available book
information, and stores the results in `books.csv`.

The data collected includes: - Book title - Price - Availability -
Rating - Product page URL

### Libraries used

-   **Requests:** to send HTTP requests and get the website pages.
-   **BeautifulSoup:** to read and parse the HTML content and extract
    book information.
-   **Pandas:** to organize the extracted data and save it as a CSV
    file.

## 2. Data Cleaning

**Folder:** `Cleaning/`\
**Script:** `clean_all_csv_files.py`

In this part, I created one reusable script to process all CSV files
inside the `Data/` folder instead of cleaning each file separately.

The script checks for CSV files in `Cleaning/Data/`, applies the
cleaning steps, and saves each result in `Cleaning/Clean Data/` using
the original filename. The original input files stay in the `Data/`
folder.

### CSV files

The cleaning script is set up to process these five files:

-   `customers_master.csv`
-   `new_daily_batch.csv`
-   `orders.csv`
-   `previous_days_summary.csv`
-   `products_master.csv`

### Cleaning steps

The script performs the following operations, according to the rules
configured in the code:

1.  **Read CSV files:** Finds and reads all CSV files directly inside
    the `Data/` folder.
2.  **Clean text values:** Removes unnecessary spaces from text values.
3.  **Handle empty cells:** Treats empty cells as missing values.
4.  **Convert numeric columns:** Converts the configured numeric columns
    to numeric values. Values that cannot be converted are treated as
    missing.
5.  **Format dates:** Converts the configured date columns to
    `YYYY-MM-DD`.
6.  **Standardize categories:** Applies consistent title case to the
    selected categorical columns.
7.  **Validate data:** Checks configured rules, such as non-negative
    values, valid rate ranges, and ensuring that the shipping date is
    not earlier than the order date.
8.  **Remove exact duplicates:** Removes rows that are identical across
    all columns.
9.  **Fill missing or invalid values:** Replaces remaining missing
    values with `Unknown`.
10. **Save cleaned files:** Exports each cleaned file to the
    `Clean Data/` folder with its original filename.

### Notes about the cleaning process

-   Duplicate removal is based on the complete row. Two rows are removed
    as duplicates only when all their column values match.
-   Rows are not removed just because they have some similar values.
-   The script does not currently perform automatic statistical outlier
    detection.
-   The cleaning and validation rules are configured in the Python
    script and may need adjustment if the dataset columns or business
    rules change.
-   The script scans the files directly inside `Data/`; it does not scan
    nested folders.
-   Since missing values are replaced with `Unknown`, some output
    columns may contain text values even if they originally contained
    numbers.

## 3. Requirements

I used Python and the following libraries:

``` bash
python -m pip install requests beautifulsoup4 pandas
```

## 4. How to Run the Project

### Run the scraping script

Open a terminal inside the `Scrapping/` folder and run:

``` bash
python Scrapping.py
```

The script saves the scraped book data in `books.csv`.

### Run the cleaning script

1.  Put the original CSV files inside `Cleaning/Data/`.
2.  Open a terminal inside the `Cleaning/` folder.
3.  Run:

``` bash
python clean_all_csv_files.py
```

4.  The cleaned CSV files will be saved in `Cleaning/Clean Data/`.

## 5. Technologies

-   Python
-   Requests
-   BeautifulSoup
-   Pandas
-   CSV

## What I Practiced

Through this project, I practiced: - Sending HTTP requests and scraping
data from a website. - Parsing HTML pages and extracting structured
information. - Working with multiple CSV files using Pandas. - Handling
missing and invalid values. - Converting data types and formatting
dates. - Applying basic data validation rules. - Detecting and removing
exact duplicate rows. - Automating a repeatable data-cleaning workflow.

## Final Goal

My goal with this project was to build practical experience with data
collection and data preparation. These are important steps before moving
on to data analysis and machine learning.
