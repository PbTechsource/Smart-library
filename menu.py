import json
from defs import (add_book, buy_book, create_json_file, delete_book,
                  export_stats_to_exel, find_books_with_chapters,
                  load_best_sellers, load_data, log_info, login, logout,
                  pin_book, register_user, show_inventory_chart, show_inventory_chart,
                  suggest_books)


def menu_start():
    while True:
        print("\n== Welcome to Smart Library ==")
        print("1 - Admin")
        print("2 - User register/login")
        print("3 - Exit")
        choice = input("Your choice: ").strip()
        if choice in ["1", "2", "3"]:
            return int(choice)
        print("❌ Invalid input. Please enter 1, 2, or 3.")


def menu_admin():
    while True:
        print("\n== Admin Menu ==")
        print("1 - Add a book")
        print("2 - Delete a book")
        print("3 - View registered users")
        print("4 - View logs")
        print("5 - View book inventory chart")
        print("6 - Pin a book")
        print("7 - Save books to Excel")
        print("0 - Back")
        choice = input("Your choice: ").strip()
        if choice in [str(i) for i in range(8)]:
            return int(choice)
        print("❌ Invalid input. Please enter a number from 0 to 7.")


def menu_user():
    while True:
        print("\n📘 User Menu")
        print("1 - Book recommendations")
        print("2 - Buy a book")
        print("3 - Display books with chapters")
        print("4 - Save the status of books in an Excel file")
        print("5 - Show pinned books")
        print("0 - Back")
        choice = input("Your choice: ").strip()
        if choice in ["0", "1", "2", "3", "4", "5"]:
            return int(choice)
        print("❌ Invalid input. Please enter a number between 0 and 5.")


def menu_authentication():
    while True:
        print("\n🔐 Authentication Menu")
        print("1 - Register")
        print("2 - Login")
        print("3 - Logout")
        print("0 - Back")
        choice = input("Your choice: ").strip()
        if choice in ["0", "1", "2", "3"]:
            return int(choice)
        print("❌ Invalid input. Please enter 0 to 3.")


if __name__ == "__main__":
    create_json_file()
    load_data()
    load_best_sellers()

    while True:
        start_choice = menu_start()

        if start_choice == 3:
            print("👋 The program has ended.")
            break

        elif start_choice == 1:  # Admin
            username = input("👤 Admin username: ")
            password = input("🔐 Admin password: ")

            if login(username, password):
                try:
                    with open("users.json", "r", encoding="utf-8") as f:
                        users = json.load(f)
                except FileNotFoundError:
                    users = {}

                if users.get(username, {}).get("role") == "admin":
                    while True:
                        admin_choice = menu_admin()

                        if admin_choice == 0:
                            break

                        elif admin_choice == 1:  
                            title = input("📖 Book title: ")
                            try:
                                qty = int(input("📦 Quantity: "))
                            except ValueError:
                                print("❌ Invalid quantity.")
                                continue
                            add_book(title, qty)

                        elif admin_choice == 2:  
                            delete_book(input("📖 Name of the book to delete: "))

                        elif admin_choice == 3:  
                            print("👥 Registered users:")
                            for u in users:
                                print("-", u)

                        elif admin_choice == 4:  
                            log_info()

                        elif admin_choice == 5:  
                            show_inventory_chart()

                        elif admin_choice == 6:  
                            pin_book(input("📖 Book title to pin: "))

                        elif admin_choice == 7:  
                            export_stats_to_exel()
                else:
                    print("❌ You do not have admin access.")
            else:
                print("❌ Login failed.")

        elif start_choice == 2:  
            while True:
                auth_choice = menu_authentication()

                if auth_choice == 0:
                    break

                elif auth_choice == 1:  
                    u = input("🆕 Username: ")
                    p = input("🔑 Password: ")
                    
                    while True:
                        r = input("👤 Role (admin/user): ").strip().lower()
                        if r in ["admin", "user"]:
                            break
                        print("❌ Invalid role. Please enter 'admin' or 'user'.")
                    
                    register_user(u, p, r)
                elif auth_choice == 2:  
                    u = input("👤 Username: ")
                    p = input("🔐 Password: ")

                    if login(u, p):
                        try:
                            with open("users.json", "r", encoding="utf-8") as f:
                                users = json.load(f)
                        except FileNotFoundError:
                            users = {}

                        if users.get(u, {}).get("role") == "admin":
                            print("⚠️ You are admin. Please use the admin menu.")
                        else:
                            while True:
                                user_choice = menu_user()

                                if user_choice == 0:
                                    break

                                elif user_choice == 1:  
                                    suggest_books()

                                elif user_choice == 2:  # Buy book
                                    title = input("📖 Book title: ")
                                    try:
                                        qty = int(input("📦 Quantity: "))
                                    except ValueError:
                                        print("❌ Invalid quantity.")
                                        continue
                                    buy_book(title, qty)

                                elif user_choice == 3:  
                                    find_books_with_chapters()

                                elif user_choice == 4: 
                                    export_stats_to_exel()

                                elif user_choice == 5:  
                                    try:
                                        with open("library.json", "r", encoding="utf-8") as f:
                                            data = json.load(f)
                                        pinned = data.get("pinned", [])
                                        if pinned:
                                            print("📌 Pinned books:")
                                            for book in pinned:
                                                print("-", book)
                                        else:
                                            print("⚠️ No pinned books found.")
                                    except FileNotFoundError:
                                        print("❌ No data file found.")
                    else:
                        print("❌ Login failed.")

                elif auth_choice == 3:  
                    logout()