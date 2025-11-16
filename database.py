#SQL Stuff
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

#initalizes database
def init_database(db_name):
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName(db_name)

    if not database.open():
        return False
    
    #requests to database
    query = QSqlQuery()
    
    #id needs to be unique because no two expenses can be the same
    query.exec("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT, 
                    category TEXT,
                    amount REAL, 
                    description TEXT
                )
                """)
    
    return True

#update table visually
def get_expenses():
    #request to database
    query = QSqlQuery("SELECT * FROM expenses ORDER BY date DESC")
    #gets added to table widget
    expenses = []
    #will loop until there is still expenses
    while query.next():
        #appending new list because each new list represents a row in the database
        #5 because id, date, category, amount, and description from query.exec in init_database
        row = [query.value(i) for i in range(5)]
        expenses.append(row)
    return expenses

def add_expenses(date, category, amount, description):
    query = QSqlQuery()
    query.prepare("""
                  INSERT INTO expenses (date, category, amount, description)
                  VALUES (?, ?, ?, ?)
                  """)
    
    query.addBindValue(date)
    query.addBindValue(category)
    query.addBindValue(amount)
    query.addBindValue(description)

    #runs the query
    return query.exec()

def remove_expenses(expense_id):
    query = QSqlQuery()
    query.prepare("DELETE FROM expenses WHERE id = ?")
    query.addBindValue(expense_id)
    return query.exec()