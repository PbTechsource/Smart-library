import json
from random import choice
from matplotlib.font_manager import json_load
from defs import buy_book, create_json_file, delete_book, export_stats_to_exel, find_books_with_chapters, load_best_sellers, log_info, login, pin_book, register_user, show_inventory, show_inventory_chart, suggest_books


def menu_start():
    while True:
        print("\n == Welcome to Smart Library ==")
        print("1 - Admin")
        print("2 - user register/login")
        print("3 - exit")
        choice = input("your choice: ").strip()
        if choice in ["1","2","3"]:
            return int(choice)
        print("invalid input. please enter 1,2, or 3.")




def menu_admin():
    while True:
        print("\n == admin menu ==")
        print("1 - add a book")
        print("2 - delete a book")
        print("3 - view registered users")
        print("4 - view logs")
        print("5 - View book inventory chart")
        print("6 - Send broadcast message")
        print("7 - Filter books by quantity")
        print("8 - Pin a book")
        print("9 - Save books to Excel")
        print("10 - Show all user tickets")
        print("0 - Back")
        choice = input("Your choice: ").strip()
        if choice in [str(i) for i in range(11)]:
            return int(choice)
        print("❌ Invalid input. Please enter a number from 0 to 10.")



def menu_user():
    while True:
        print("\n📘 User Menu")
        print("1 - Book recommendations")
        print("2 - Buy a book")
        print("3 - Display books with chapters")
        print("4 - Save the status of books in an Excel file")
        print("5 - Show pinned books")
        print("0 - return")
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
    with open("users.json", "r") as f:
        users = json.load(f)
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}
    load_best_sellers()
    while True:
        start_choice = menu_start()
        if start_choice == 0:
            print("👋 The program has ended.")
            break
        elif start_choice == 1:
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
                    show_inventory()
                elif admin_choice == 2:
                    delete_book(input("Name of the book to delete: "))
                elif admin_choice == 3:
                    print("👥 Registered users: ")
                    for u in users:
                        print("-", u)
                elif admin_choice == 4:
                    log_info()
                elif admin_choice == 5:
                    show_inventory_chart()
                elif admin_choice == 6:
                    pin_book(input("Book title for Pin: "))
                elif admin_choice == 7:
                    export_stats_to_exel()
        else:
            print("❌ You do not have admin access.")
    else:
        print("❌ ورود ناموفق.")
    if start_choice == 2:
        while True:
            auth_choice = menu_authentication()
            if auth_choice == 0:
                break
            elif auth_choice == 1:
                u = input("🆕 Username: ")
                p = input("🔑 Password: ")
                r = input("👤 نقش کاربر (admin یا user): ").strip().lower()
                if r not in ["admin", "user"]:
                    print("❌ نقش وارد شده معتبر نیست. مقدار پیش‌فرض 'user' در نظر گرفته می‌شود.")
                    r = "user"
                register_user(u, p, role=r)
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
                        print("⚠️ شما ادمین هستید. لطفاً از مسیر منوی ادمین وارد شوید.")
                else:
                    while True:
                        user_choice = menu_user()
                        if user_choice == 0:
                            break
                        elif user_choice == 1:
                            suggest_books()
                        elif user_choice == 2:
                            title = input("📖 Book title: ")
                            qty = int(input("📦 Quantity: "))
                            buy_book(title, qty)
                        elif user_choice == 3:
                            find_books_with_chapters()
                        elif user_choice == 4:
                            for b in books:
                                print("-", b)
        while True:
            auth_choice = menu_authentication()
            if auth_choice == 0:
                break
            elif auth_choice == 1:
                u = input("🆕 Username: ")
                p = input("🔑 Password: ")
                r = input("👤 User role (admin or user): ").strip().lower
                if r not in ["admin", "user"]:
                    print("❌ The entered role is not valid. The default value 'user' is assumed.")
                    r = "user"
                register_user(u, p, role=r)
                try:
                    with open("users.json", "r", encoding="utf-8") as f:
                        users = json.load(f)
                    users[u]["role"] = "user"
                    with open("users.json", "w", encoding="utf-8") as f:
                        json.dump(users, f, indent=2)
                except:
                    print("⚠️ Error saving user role.")