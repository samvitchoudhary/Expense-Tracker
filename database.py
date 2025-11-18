#SQL Stuff
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import hashlib

#initalizes database
def init_database(db_name):
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName(db_name)

    if not database.open():
        return False
    
    # Enable foreign key constraints for SQLite
    query = QSqlQuery()
    query.exec("PRAGMA foreign_keys = ON")
    
    #requests to database
    query = QSqlQuery()

    #Users table
    query.exec("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)
    
    
    #id needs to be unique because no two expenses can be the same
    query.exec("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    date TEXT, 
                    category TEXT,
                    amount REAL, 
                    description TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """)
    
    # Migrate existing expenses table if it doesn't have user_id column
    # Check if user_id column exists
    query.exec("PRAGMA table_info(expenses)")
    has_user_id = False
    while query.next():
        if query.value(1) == "user_id":  # Column name is at index 1
            has_user_id = True
            break
    
    if not has_user_id:
        # Table exists but doesn't have user_id - need to migrate
        # For simplicity, we'll drop and recreate (this will lose old data)
        # In production, you'd want to do a proper migration with data preservation
        query.exec("DROP TABLE IF EXISTS expenses")
        query.exec("""
                    CREATE TABLE expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        date TEXT, 
                        category TEXT,
                        amount REAL, 
                        description TEXT,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                    """)
    
    return True

#hashes password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    query = QSqlQuery()
    query.prepare("""
                    INSERT INTO users (username, password_hash)
                    VALUES (?, ?)
                  """)

    password_hash = hash_password(password)
    query.addBindValue(username)
    query.addBindValue(password_hash)

    if query.exec():
        return True
    return False

#Checks is password is correct, and if it is return the user
def authenticate_user(username, password):
    query = QSqlQuery()
    query.prepare("SELECT id, password_hash FROM users WHERE username = ?")
    query.addBindValue(username)

    if query.exec() and query.next():
        stored_hash = query.value(1)
        provided_hash = hash_password(password)

        if stored_hash == provided_hash:
            return query.value(0)
        
    return None

#Checks if username already exists
def user_exists(username):
    query = QSqlQuery()
    query.prepare("SELECT COUNT(*) FROM users WHERE username = ?")
    query.addBindValue(username)

    if query.exec() and query.next():
        return query.value(0) > 0
    return False

#update table visually
def get_expenses(user_id):
    #request to database - filters by user_id
    query = QSqlQuery()
    query.exec("PRAGMA foreign_keys = ON")
    query.prepare("SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC")
    query.addBindValue(int(user_id))  # Ensure user_id is an integer
    #gets added to table widget
    expenses = []
    #will loop until there is still expenses
    if query.exec():
        while query.next():
            #appending new list because each new list represents a row in the database
            #6 because id, user_id, date, category, amount, and description from query.exec in init_database
            row = [query.value(i) for i in range(6)]
            expenses.append(row)
    return expenses

def add_expenses(user_id, date, category, amount, description):
    query = QSqlQuery()
    # Enable foreign keys for this query (required for each connection)
    query.exec("PRAGMA foreign_keys = ON")
    
    query.prepare("""
                  INSERT INTO expenses (user_id, date, category, amount, description)
                  VALUES (?, ?, ?, ?, ?)
                  """)
    
    query.addBindValue(int(user_id))  # Ensure user_id is an integer
    query.addBindValue(date)
    query.addBindValue(category)
    query.addBindValue(float(amount))  # Ensure amount is a float
    query.addBindValue(description)

    #runs the query
    result = query.exec()
    if not result:
        # Print error for debugging
        print(f"SQL Error: {query.lastError().text()}")
    return result

def remove_expenses(expense_id, user_id):
    query = QSqlQuery()
    query.exec("PRAGMA foreign_keys = ON")
    query.prepare("DELETE FROM expenses WHERE id = ? AND user_id = ?")
    query.addBindValue(int(expense_id))
    query.addBindValue(int(user_id))  # Ensure user_id is an integer
    return query.exec()