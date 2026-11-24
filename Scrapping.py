import requests
from bs4 import BeautifulSoup
import pandas as pd 
from urllib.parse import urljoin

# Website URL
url = "https://books.toscrape.com/"

# Store all books
all_books = []

# Loop through all pages
while url:

    print("Scraping:", url)

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Get all books on current page
        books = soup.find_all("article", class_="product_pod")

        for book in books:

            title = book.h3.a.get("title", "Unknown")

            price_tag = book.find("p", class_="price_color")
            price = price_tag.text.strip() if price_tag else "Unknown"

            availability_tag = book.find(
                "p", class_="instock availability"
            )
            availability = (
                availability_tag.text.strip()
                if availability_tag else "Unknown"
            )

            rating_class = book.p.get("class", [])
            rating = (
                rating_class[1]
                if len(rating_class) > 1 else "Unknown"
            )

            # Replace missing or empty values
            all_books.append({
                "Title": title or "Unknown",
                "Price": price or "Unknown",
                "Availability": availability or "Unknown",
                "Rating": rating or "Unknown"
            })

        # Find next page
        next_button = soup.find("li", class_="next")

        if next_button and next_button.a:
            next_page = next_button.a.get("href")
            url = urljoin(url, next_page)
        else:
            url = None

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        break

# Create DataFrame
df = pd.DataFrame(all_books)

# Replace all missing values with Unknown
df = df.fillna("Unknown")

# Save data to CSV
df.to_csv(
    "books.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nScraping Completed!")
print("Total Books:", len(df))
print("File saved as books.csv")

print(df.head())
