import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

# Retrieve Book Details: Title, Price, Rating, Availability
books_data = []

for page in range(1, 6): # Scrape first 3 pages
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"

    print(f"Scraping page {page}...")

    response = requests.get(url)
    response.raise_for_status() # check if the request was successful

    print(response.status_code)

    #print(response.text[:1000])

    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')

    print(soup.title.text)
    print(len(books)) # per page 20 books

    #book_1 = books[0]

    #print(book_1)

    for book in books:
        #title = book.h3.attrs['title']
        title = book.h3.a.attrs['title']
        price = book.find('p', class_ = 'price_color').text
        rating = book.p.attrs['class'][1]
        availability = book.find('p', class_ = 'instock availability').text.strip()
        # -------------------------
        # Category
        # -------------------------
            category = soup.select_one("ul.breadcrumb li:nth-of-type(1)")

        books_data.append({
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability
        })

df_books_data = pd.DataFrame(books_data)

print("No.of Books Scraped", df_books_data.shape[0]) # Total number of books scraped
#print(df_books_data.head())

# Convert Price: from GBP to INR

df_books_data["price"] = df_books_data["price"].str.replace("Â", "", regex=False)  # Remove any unwanted characters
df_books_data["price"] = df_books_data["price"].str.replace("£", "", regex=False)

df_books_data["price_inr"] = df_books_data["price"].astype(float) * 100  # Assuming 1 GBP = 100 INRi

# Convert Rating: from string to numeric
rating_map = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}
df_books_data['rating_numeric'] = df_books_data['rating'].map(rating_map)

print(df_books_data[['title', 'price_inr', 'rating_numeric', 'availability']].head(50))
print(df_books_data.shape[0])

conn = sqlite3.connect('books_data.db')
df_books_data.to_sql('books', conn, if_exists='replace', index=False)

print("Data saved to SQLite database 'books_data.db' in table 'books'.")
print(f"Books table created successfully with ({len(books)}) records.")

query = "SELECT * FROM books"
df_sql = pd.read_sql(query, conn)
print(df_sql)

conn.close()






