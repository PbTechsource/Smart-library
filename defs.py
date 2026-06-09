import re
import json
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

LOG_FILE = "log.txt"
EXCEL_FILE = "stats.xlsx"
JSON_FILE = "library.json"

books = []
inventory = {}
pinned = set()
users = {}
logged_in_user = None



def create_json_file():
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {
            "admin": {
                "password": "admin123",
                "role": "admin",
                "logs": []
            }
        }
        with open("users.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print("✅ users.json created with default admin.")




def load_data():
    global books, inventory, pinned, users
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            books = data.get("books", [])
            inventory = data.get("inventory", {})
            pinned = set(data.get("pinned", []))
        print("✅ Data loaded from library.json")
    except FileNotFoundError:
        print("⚠️ No existing data found, starting fresh.")
    except json.JSONDecodeError:
        print("⚠️ library.json is corrupted, starting fresh.")



def save_to_json():
    data = {
        "books": books,
        "inventory": inventory,
        "pinned": list(pinned)
    }
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"📁 Information saved in {JSON_FILE}.")



def log(username, action):
    now = datetime.datetime.now()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username},{action},{now.isoformat()}\n")


def log_info():
    print("📋 Activity records:")
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            print("⚠️ Log file is empty.")
            return
        for line in lines:
            print("📝", line.strip())
    except FileNotFoundError:
        print("❌ Log file not found.")




def register_user(username, password, role="user"):
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}

    if username in users:
        print("⚠️ This username is already registered.")
        return False

    users[username] = {
        "password": password,
        "logs": [],
        "role": role
    }

    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

    print(f"✅ User '{username}' registered successfully with role '{role}'.")
    return True


def login(username, password):
    global logged_in_user, users
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}

    if username in users and users[username]["password"] == password:
        logged_in_user = username
        log(username, "login")
        print(f"✅ '{username}' logged in successfully.")
        return True

    print("❌ Incorrect username or password.")
    return False


def logout():
    global logged_in_user
    if logged_in_user:
        print(f"👋 '{logged_in_user}' logged out successfully.")
        log(logged_in_user, "logout")
        logged_in_user = None
    else:
        print("⚠️ No user is currently logged in.")




def add_book(title, qty=1):
    global books, inventory

    if not title.strip():
        print("❌ Book title cannot be empty.")
        return

    if title in books:
        inventory[title] += qty
        print(f"✅ '{title}' already exists. Inventory updated to {inventory[title]}.")
    else:
        books.append(title)
        inventory[title] = qty
        print(f"✅ Book '{title}' added with {qty} copies.")

    save_to_json()


def delete_book(title):
    if title in books:
        books.remove(title)
        inventory.pop(title, None)
        pinned.discard(title)
        save_to_json()
        print(f"🗑️ Book '{title}' deleted.")
    else:
        print("❌ Book not found.")


def pin_book(title):
    if title in books:
        pinned.add(title)
        save_to_json()
        print(f"📌 Book '{title}' pinned.")
    else:
        print("❌ The book is not available.")


def show_inventory():
    if not inventory:
        print("📦 Inventory is empty.")
        return
    print("📦 Warehouse inventory:")
    for b, qty in inventory.items():
        print(f"  {b} ➤ {qty}")


def buy_book(book_title, qty=1):
    available = inventory.get(book_title, 0)
    if available >= qty:
        inventory[book_title] -= qty
        save_to_json()
        print(f"✅ Successfully purchased {qty} copy of '{book_title}'.")
    else:
        print("❌ Insufficient stock or book not found.")



def suggest_books(style=None):
    if not books:
        print("⚠️ No books available.")
        return
    print("📚 Book suggestions:")
    if style == "popular":
        lst = sorted(books, key=lambda b: inventory.get(b, 0), reverse=True)[:5]
    elif style == "short":
        lst = sorted(books, key=lambda b: len(b))[:5]
    else:
        lst = books[:5]
    for b in lst:
        print(f"  - {b}")




def find_books_with_chapters():
    if not books:
        print("⚠️ The book list is empty.")
        return

    pattern = re.compile(r"\b(?:Chapter|Vol|Volume|Part)\s+\d+", re.IGNORECASE)
    found = False

    for title in books:
        if pattern.search(title):
            print(f"✅ Has chapters: {title}")
            found = True

    if not found:
        print("❌ No books with chapter structure were found.")
        print(f"  (Total books loaded: {len(books)})")




def show_inventory_chart():
    global inventory

    if not inventory:
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                inventory = data.get("inventory", {})
        except FileNotFoundError:
            print("❌ No data found.")
            return

    if not inventory:
        print("⚠️ Inventory is empty.")
        return

    titles = list(inventory.keys())
    counts = list(inventory.values())
    short_titles = [t[:20] + "..." if len(t) > 20 else t for t in titles]

    plt.figure(figsize=(14, 7))
    bars = plt.bar(short_titles, counts, color='skyblue', edgecolor='navy', linewidth=0.5)

    for bar, count in zip(bars, counts):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            str(count),
            ha='center', va='bottom', fontsize=8
        )

    plt.xlabel("📚 Books", fontsize=12)
    plt.ylabel("📦 Quantity", fontsize=12)
    plt.title("📊 Book Inventory Chart", fontsize=14)
    plt.xticks(rotation=75, ha='right', fontsize=7)
    plt.tight_layout()
    plt.show()




def export_stats_to_exel():
    global books, inventory, pinned

    if not books:
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                books = data.get("books", [])
                inventory = data.get("inventory", {})
                pinned = set(data.get("pinned", []))
        except FileNotFoundError:
            print("❌ library.json not found.")
            return

    if not books:
        print("⚠️ No books to export.")
        return

    df = pd.DataFrame([
        {
            "title": b,
            "inventory": inventory.get(b, 0),
            "pinned": (b in pinned)
        }
        for b in books
    ])

    try:
        df.to_excel(EXCEL_FILE, index=False)
        print(f"📁 Excel file '{EXCEL_FILE}' created successfully.")
    except Exception as e:
        print(f"❌ Error saving Excel file: {e}")




def load_best_sellers():
    global books, inventory
    print("⏳ Getting book list from Wikipedia...")

    url = "https://en.wikipedia.org/wiki/List_of_best-selling_books"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    try:
        session = requests.Session()
        resp = session.get(url, headers=headers, timeout=15)

        if resp.status_code == 403:
            print("⚠️ Wikipedia blocked the request. Using backup list...")
            _load_backup_books()
            return

        resp.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        print("⚠️ Using backup list instead...")
        _load_backup_books()
        return

    try:
        soup = BeautifulSoup(resp.text, "html.parser")
        tables = soup.find_all("table", {"class": "wikitable"})

        if not tables:
            print("⚠️ Table not found. Using backup list...")
            _load_backup_books()
            return

        count = 0
        for table in tables:
            rows = table.find_all("tr")[1:]
            for row in rows:
                cols = row.find_all("td")
                if cols:
                    title = cols[0].get_text(strip=True)
                    if title and title not in books:
                        books.append(title)
                        inventory[title] = 5
                        count += 1

        if count == 0:
            print("⚠️ No books found. Using backup list...")
            _load_backup_books()
            return

        save_to_json()
        print(f"✅ {count} books loaded successfully.")

    except Exception as e:
        print(f"❌ Parse error: {e}")
        _load_backup_books()


def _load_backup_books():
    global books, inventory

    backup = [
        "Don Quixote", "A Tale of Two Cities", "The Lord of the Rings",
        "The Little Prince", "Harry Potter and the Philosopher's Stone",
        "And Then There Were None", "Dream of the Red Chamber",
        "The Hobbit", "The Da Vinci Code", "The Alchemist",
        "Twilight", "Gone with the Wind", "1984",
        "To Kill a Mockingbird", "The Catcher in the Rye",
        "Brave New World", "Animal Farm", "The Great Gatsby",
        "Pride and Prejudice", "The Hunger Games"
    ]

    count = 0
    for title in backup:
        if title not in books:
            books.append(title)
            inventory[title] = 5
            count += 1

    save_to_json()
    print(f"✅ {count} books loaded from backup list.")