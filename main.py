import json

print("📚 WELCOME TO LIBRARY MANAGEMENT SYSTEM")
USER_FILE = "users.json"
BOOKS_FILE = "books.json"

logged_in_user = None

def register():
    try:
        with open(USER_FILE, "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    username = input("Enter new username: ")
    password = input("Enter new password: ")

    if username in users:
        print(" Username already exists!")
        return

    users[username] = password
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)

    print("User registered successfully!")

# Function to login
def login():
    global logged_in_user
    if logged_in_user is not None:
        print("user is already logged in")
    try:
        with open(USER_FILE, "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username in users and users[username] == password:
        logged_in_user = username
        print(f"Welcome, {username}!")
    else:
        print(" Invalid username or password")

# Function to search books
def search_book(query):
    try:
        with open(BOOKS_FILE, "r") as file:
            books = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("📁 No books available!")
        return

    results = [book for book in books if query.lower() in book["title"].lower() or query.lower() in book["author"].lower()]
    
    if results:
        print("🔍 Search Results:")
        for i, book in enumerate(results, start=1):
            print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - Copies: {book['copies']}, Available: {book['available']}")
    else:
        print(" No books found matching your search!")

# Function to borrow a book
def borrow_book(query):
    if not logged_in_user:
        print("You must log in first!")
        return

    try:
        with open(BOOKS_FILE, "r") as file:
            books = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(" No books available!")
        return

    for book in books:
        if query.lower() in book["title"].lower() or query.lower() in book["author"].lower():
            if book["available"] > 0:
                book["available"] -= 1
                book.setdefault("borrowers", []).append(logged_in_user)

                with open(BOOKS_FILE, "w") as file:
                    json.dump(books, file, indent=4)

                print(f" {book['title']} borrowed successfully!")
                return
            else:
                print(f" {book['title']} is not available!")
                return

    print(" Book not found!")

# Function to check book availability
def check_availability(query):
    try:
        with open(BOOKS_FILE, "r") as file:
            books = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("📁 No books available!")
        return

    for book in books:
        if query.lower() in book["title"].lower() or query.lower() in book["author"].lower():
            if book["available"] > 0:
                print(f" {book['title']} is available with {book['available']} copies left.")
            else:
                print(f" {book['title']} is fully occupied! Borrowers: {', '.join(book.get('borrowers', []))}")
            return

    print(" Book not found!")

# Main Menu Loop
while True:
    if logged_in_user is not None:
        print(f"\n\t\t\t\t\tWelcome, {logged_in_user}!")

    print("\n Choose an option:")
    print("1) Login")
    print("2) Register")
    print("3) Search Book")
    print("4) Borrow Book")
    print("5) Check Availability")
    print("6) Exit")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print(" Please enter a valid number!")
        continue

    if choice == 1:
        login()
    elif choice == 2:
        register()
    elif choice == 3:
        search_query = input("Enter book title or author: ")
        search_book(search_query)
    elif choice == 4:
        borrow_query = input("Enter book title or author: ")
        borrow_book(borrow_query)
    elif choice == 5:
        check_query = input("Enter book title or author: ")
        check_availability(check_query)
    elif choice == 6:
        print(" Exiting Library System. Goodbye!")
        break
    else:
        print(" Invalid choice! Try again.")
