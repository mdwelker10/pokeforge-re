import sqlite3

from flask import current_app


# Use this method in other classes for transactions
def connect():
  """Gets connection to the database"""
  # return sqlite3.connect('db-files/database.db')
  return sqlite3.connect(current_app.config['DATABASE_FILE'])

def exec(query, data, attribute):
  """Executes a query and returns the cursor, useful for single SELECT and INSERT queries. Do not call with connect
  
  Args:
    query (str): Query to execute
    args (tuple OR List): Arguments to pass to the query. If type is a List executemany is used. If type is a tuple execute is used
    attribute (str): Attribute to return from the cursor. Popular examples are 'rowcount', 'lastrowid', 'fetchall', 'fetchone'
    
  Returns:
    cursor: Cursor object for the query"""
  con = connect()
  cur = con.cursor()
  if type(data) == list:
    cur.executemany(query, data)
  else:
    cur.execute(query, data)
  con.commit()
  
  # Get the chosen attribute, whether it be a function, int or otherwise
  attr = getattr(cur, attribute)
  # Call function if it is callable (meaning it is a function)
  ret = attr() if callable(attr) else attr
  con.close()
  return ret

if __name__ == '__main__':
  print(exec("SELECT * FROM category", (), "fetchone")) # Test the exec method