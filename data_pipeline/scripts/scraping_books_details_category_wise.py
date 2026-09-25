import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import sqlite3

url = "https://books.toscrape.com"

response = requests.get(url)
response.raise_for_status() # check if the request was successful

print(response.status_code)

print(response.text[:150])

# ---------------------------------------------------------
# Task-1: Scrape all books listed across at-least 
#         3 different book categories. For each book 
#         capture: title, price (as listed, in GBP), 
#         star_rating (as text, e.g. "Three"), availability 
#         (as listed text), and category.
# ---------------------------------------------------------
# Find all products page
base_url = "https://books.toscrape.com"

# --------------------------------------------------
# STEP 1: Get the All Products page
# --------------------------------------------------
response = requests.get(base_url)
response.raise_for_status()  # check if the request was successful
soup = BeautifulSoup(response.text, "html.parser")

# --------------------------------------------------
# STEP 2: Find all subcategory links under Books
# --------------------------------------------------
category_links = {}
categories = []

# Find the Books section in the sidebar
#category_link = soup.select_one("ul.nav-list li a")
books_section = soup.select_one("div.side_categories ul.nav-list > li > ul")

# Get all subcategory links under Books
for link in books_section.find_all("a"):
    subcategory_name = link.get_text(strip=True)
    subbcategory_url = urljoin(base_url, link['href'])
    category_links[subcategory_name] = subbcategory_url

    category_id = link['href'].split("_")[-1].split("/")[0]

    categories.append({"category_id": category_id, "category_name": subcategory_name})

print("All Categories in Books Section:- ")
for key, value in categories: 
    print(key, "->", value)

# Display available categories
#print("Available Categories:")
#print(category_links.keys())

# --------------------------------------------------
# STEP 3: Select 3 categories
# --------------------------------------------------
selected_categories = ["Travel", "Historical Fiction", "Mystery", 'Sequential Art']

# --------------------------------------------------
# STEP 4: Scrape books from the 4 categories
# --------------------------------------------------
all_books = []

for category in selected_categories:
    url = category_links[category]
    response = requests.get(url)
    response.raise_for_status()  # check if the request was successful

    category_soup = BeautifulSoup(response.text, "html.parser")

    # Find all books on currecnt page
    books = category_soup.find_all("article", class_="product_pod")

    
    for book in books:
        book_link = book.find("h3").find("a")
    
        book_url = book_link["href"]
        book_id = int(
        book_url.rsplit("_", 1)[1].split("/")[0]
        )
        title = book.h3.a.attrs.get('title')
        price = book.find("p", class_='price_color').text.strip()
        rating = book.p.attrs.get('class')[1]
        availability = book.find("p", class_='instock availability').text.strip()

        all_books.append({
            "book_id": book_id,
            "category_name": subcategory_name,
            "title": title,
            "category_id": category_id,
            "rating": rating,
            "availability": availability,
            "price": price,
        })

        # Find Next page
        # ------------------------------------------
        next_button = category_soup.select_one(
            "li.next a"
        )
        if next_button:
            next_url = next_button["href"]
            url = urljoin(
                url,
                next_url
            )
        else:
            # No more pages
            url = None

# --------------------------------------------------
# STEP 5: Create DataFrame
# --------------------------------------------------
df_books = pd.DataFrame(all_books)
df_category = pd.DataFrame(categories)
print(f"books dataset columns:- {df_category.columns}")
print(f"books dataset columns:- {df_books.columns}")

# --------------------------------------------------
# STEP 6: Display results
# --------------------------------------------------
print("\nScraping completed!")
print("Total books:", len(df_books))
print("Total categories:", len(df_category))
#print("\nBooks by category:")
#print(df_books["category_name"].value_counts())
#print("\nFirst 60 records:")
#print(df_books.head(60))

# --------------------------------------------------------------------------
# Task-2: Clean the scraped fields into proper types:
#         - Strip the currency symbol from price and convert it 
#           to a float column price_gbp. 
#         - Convert the text star - rating (One…Five) into an integer column 
#           rating (1–5).
#         - Parse the availability text into a boolean column 
#           in_stock. 
#         - If any field fails to parse for a given row 
#           (e.g., unexpected text), handle it with the median-imputation 
#           approach for numeric fields or drop the row (state and justify 
#           your choice) — do not leave the pipeline crashing on messy rows.
# ----------------------------------------------------------------------------
# Parse availability text into a boolean column: in_stock
df_books['in_stock'] = (
    df_books['availability']
    .str.strip()
    .str.lower()
    .eq('in stock')
)

print(f"Columns in books dataset after conversion of col: 'availability' to bool type:- {df_books.columns}")

#print(df_books[['availability', 'in_stock']].head(20))
#print(df_books['in_stock'].dtype)

# drop column 'availability - parsed as 'in_stock' - bool type
df_books.drop(columns='availability', inplace=True)

# Remove any unwanted characters
df_books["price_inr"] = df_books["price"].str.replace("Â£", "", regex=False)

# Rename column: 'price' as 'price_gbp'
df_books["price_gbp"] = df_books["price"].round(3)

# --------------------------------------------------------------------------
# Task-3: Convert price_gbp to a price_inr column using the project's fixed 
#         baseline conversion rate: 1 GBP = 105.50 INR
# ---------------------------------------------------------------------------

df_books["price_inr"] = ((df_books["price_inr"].astype(float)) * 105.50).round(3)  # Assuming 1 GBP = 105.50 INR

# Drop 'price' column - not needed
df_books.drop(columns='price', inplace=True)

# Convert Rating: from text to integer
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

df_books["rating"] = df_books["rating"].map(rating_map)

print(df_books[['book_id', 'category_id', 'title', 'rating', 'in_stock', 'price_gbp', 'price_inr']].head(60))

def to_store_in_db(df_books, df_category):
    # ---------------------------------------------------------------------------
    # Task-4: Store the cleaned data into a SQLite database with two tables:
    #         - books: with columns title, price_inr, rating, in_stock, category
    #         - categories: with columns category_id, category_name
    # ---------------------------------------------------------------------------
    # Create SQLite database connection
    conn = sqlite3.connect("books_data.db")

    books = df_books.to_sql("books", conn, if_exists="replace", index=False)
    categories = df_category.to_sql("categories", conn, if_exists="replace", index=False)

    print("Data stored in SQLite database 'books_data.db' successfully!")
    print("Database tables: 'books' and 'categories' created.")
    print("Total records inserted into 'books' table: ", len(df_books))
    print("Total records inserted into 'categories' table: ", len(df_category))

    print(f"\n Columns in books dataset:- {df_books.columns.to_list()}")
    print(f"\n Columns in categories dataset:- {df_category.columns.to_list()}")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
            FROM sqlite_master
            WHERE type='table'
    """)
    
    print(cursor.fetchall())
    
    cursor.execute(""" 
        PRAGMA table_info(CATEGORIES)
    """)
    
    columns = cursor.fetchall()

    print("CATEGORIES table data:- ")
    for column in columns:
        print(column)
    
    cursor.execute(""" 
        PRAGMA table_info(BOOKS)
    """)
    
    columns = cursor.fetchall()

    print("BOOKS table data:- ")
    for column in columns:
        print(column)
    
    #------------------------------------------------------------------------------------------------
    # Task-5: Using Python's sqlite3 (or pandas.DataFrame.to_sql), insert your cleaned, converted 
    # data into this schema. Then write and execute at least 5 SQL queries against the database that 
    # collectively demonstrate: SELECT/WHERE, ORDER BY, LIMIT, DISTINCT, and (IN or BETWEEN) — plus at 
    # least one JOIN between your two tables 
    # (e.g., "list the 10 highest-rated books per category"). Save each query string and its output.
    #-------------------------------------------------------------------------------------------------
    '''
    cursor.execute("""
        CREATE TABLE CATEGORIES_NEW (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE BOOKS_NEW (
            book_id INTEGER PRIMARY KEY,
            category_id INTEGER,
            title TEXT,
            rating INTEGER,
            in_stock BOOL,
            price_gbp REAL,
            price_inr REAL,
            FOREIGN KEY (category_id) REFERENCES CATEGORIES_NEW(category_id)
        )
    """)

    cursor.execute("""
        INSERT INTO CATEGORIES_NEW
            (category_id, category_name)
        SELECT
            category_id, category_name
        FROM CATEGORIES
    """)
    
    cursor.execute("""
            INSERT INTO BOOKS_NEW
                (book_id, category_id, title, rating, in_stock, price_gbp, price_inr)
            SELECT
                book_id, category_id, title, rating, in_stock, price_gbp, price_inr
            FROM BOOKS
        """)
    '''
    # To fetch CATEGORIES_NEW table data
    cursor.execute("""
        SELECT * FROM CATEGORIES_NEW
    """)
    rows = cursor.fetchall()

    print("CATEGORIES_NEW table data")
    for row in rows:
        print(row)

    # To fetch BOOKS_NEW table data
    cursor.execute("""
        SELECT * FROM BOOKS_NEW
    """)
    rows = cursor.fetchall()
    
    print("BOOKS_NEW table data")
    for row in rows:
        print(row)

    # Fetch category wise books data
    cursor.execute("""
        SELECT c.category_id, c.category_name, b.book_id, b.title, b.rating, b.in_stock, b.price_inr
        FROM CATEGORIES_NEW AS c INNER JOIN BOOKS_NEW AS b on c.category_id = b.category_id 
    """)
    rows = cursor.fetchall()

    print("category wise books data - INNERJOIN Query Resultset:-")
    for row in rows:
        print(row)
    
    conn.commit()

    '''
    cursor.execute("""
        DROP TABLE CATEGORIES
    """)
    '''

    #----------------------------------------------------------------------------------------------
    # Task.6: Read back at least two of the above query results into pandas DataFrames using 
    # pd.read_sql(...), and separately reproduce the join-query's result using pd.merge(...) directly 
    # on your in-memory DataFrames (no SQL) — show that both approaches produce equivalent output.
    #------------------------------------------------------------------------------------------------
    df_category_new = pd.read_sql("SELECT * FROM CATEGORIES_NEW", conn)
    df_books_new = pd.read_sql("SELECT * FROM BOOKS_NEW", conn)

    print("CATEGORIES_NEW and BOOKS_NEW table data stored back to DataFrame Successfully")
    print("Data from CATEGORIES_NEW table:")
    print(df_category_new)

    print("Data from BOOKS_NEW table:")
    print(df_books_new)

    # Inner Join
    pd.merge(df_category_new, df_books_new, on='category_id', how='inner')
to_store_in_db(df_books, df_category)