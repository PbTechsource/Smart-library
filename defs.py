from ast import pattern
from itertools import count
import re
import json
from turtle import color, title
from matplotlib import table
from matplotlib.font_manager import json_dump
import matplotlib.pyplot as plt
import datetime
from matplotlib.style import available
import requests
from bs4 import BeautifulSoup
import pandas as pd

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
        with open ("users.json","r") as f:
            users = json.load(f)
    except:
        data = {
            "admin":{
                "password": "admin123",
                "role": "admin",
                "logs": []
            }
        } 
        with open("users.json","w") as myfile:
            json.dump(data, myfile, indent=2)




def save_to_json():
    data = {
        "users": users,
        "books": books,
        "inventory": inventory,
        "pinned": list(pinned)
    }
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("📁 Information in {JSON_FILE} saved.")




def log(username, action):
    now = datetime.datetime.now()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username},{action},{now.isoformat()}\n")




def log_info():
    print("Activity records: ")
    try:
        with open(LOG_FILE, "r", encoding="utf-8")as f:
            for line in f:
                print("📝", line.strip())
    except FileExistsError:
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
        json.dump(users, f, indent=2)

    print(f"✅ User registration «{username}» with role «{role}» Successfully completed.")
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
        print(f"{username} entered.")
        return True
    return False


def find_books_with_chapters():
    if not books:
        print("⚠️ The book list is empty.")
        return

    pattern = re.compile(r"\b(?:Chapter|CHAPTER)\s+\d+", re.IGNORECASE)
    found = False
    for title in books:
        if pattern.search(title):
            print(f"✅ Has seasons: {title}")
            found = True
    if not found:
        print("❌ No books with chapter structure were found.")



def suggest_books(style=None):
    print("📚 Book suggestion:")
    if style == "popular":
        lst = sorted(books, key=lambda b: inventory.get(b, 0), reverse=True)[:5]
    elif style == "short":
        lst = sorted(books, key=lambda b: len(b))[:5]
    else:
        lst = books[:5]
    for b in lst:
        print(f"- {b}")



def show_inventory_chart():
    if logged_in_user != "admin":
        print("⚠️ Only the admin can view the chart.")
        return
    
    if not inventory:
        print("📦 The warehouse is empty.")
        return
    titles = list(inventory.keys())
    counts = list(inventory.values())
    plt.figure(figsize=(12, 6))
    plt.bar(titles, counts, color='skyblue')
    plt.xlabel("📚books")
    plt.ylabel("📦 Inventory quantity")
    plt.title("General book inventory chart")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()



def buy_book(book_title, qty=1):
    available = inventory.get(book_title, 0)
    if available >= qty:
        inventory[book_title] -= qty
        save_to_json()
        print(f"✅ shopping with {qty} version of«{book_title}»  Success done.")
    else:
        print("❌ Insufficient stock or book not found.")





def show_inventory():
    if logged_in_user == "admin":
        print("📦 Warehouse inventory:")
        for b in inventory:
            print(f"{b} ➤ {inventory[b]}")
    else:
        print("⚠️ Only admins can see inventory.")

def delete_book(title):
    if title in books:
        books.remove(title)
        inventory.pop(title, None)
        pinned.discard(title)
        save_to_json()
        print(f"❌ books deleted. «{title}»")
    else:
        print("❌ Book not found.")


def pin_book(title):
    if title in books:
        pinned.add(title)
        save_to_json()
        print(f"📌 books pinned. «{title}»")
    else:
        print("❌ The book is not available.")

def filter_books_alpha(start="A", end="Z"):
    lst = sorted([b for b in books if start <= b[0].upper() <= end])
    for b in lst:
        print(f"- {b}")



def export_stats_to_exel():
    df = pd.DataFrame([{"title": b, "inventory": inventory.get(b, 0), "pinned": (b in pinned)} for b in books])
    df.to_excel(EXCEL_FILE, index=False)
    print(f"📁 Excel file named{EXCEL_FILE} created.")



def find_books_with_chapters():
    pattern = re.compile(r"(?:chapteR|CHAPTER)\s+\d+", re.IGNORECASE)
    for title in books:
        if pattern.search(title):
            print(f"✅ Seasonal: {title}")



def load_best_sellers():
    print("⏳ Get a list of books from Wikipedia...")
    url = "https://en.wikipedia.org/wiki/List_of_best-selling_books"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("❌ Error connecting to Wikipedia:", e)
        return
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table", {"class": "wikitable"})
    if not table:
        print("❌ Table not found.")
        return
    rows = table.find_all("tr")[1:]
    for row in rows:
        cols = row.find_all("td")
        if cols:
            title = cols[0].get_text(strip=True)
            if title not in books:
                books.append(title)
                inventory[title] = 5
    save_to_json()
    print("✅ The book list has been loaded.")
