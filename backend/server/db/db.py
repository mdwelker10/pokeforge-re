import os
import sqlite3


# Use this method in other classes for transactions
def connect():
  """Gets connection to the database"""
  current_dir = os.path.dirname(os.path.abspath(__file__))
  path = os.path.join(current_dir, 'db-files', 'database.db')
  return sqlite3.connect(path)

def exec(query, data, attribute):
  """Executes a query and returns the cursor, useful for single SELECT and INSERT queries. Do not call with connect
  
  Args:
    query (str): Query to execute
    args (tuple OR List): Arguments to pass to the query. If type is a List executemany is used. If type is a tuple execute is used
    attribute (str): Attribute to return from the cursor. Popular examples are 'rowcount', 'lastrowid', 'fetchall', 'fetchone'
    
  Returns:
    cursor: Cursor object for the query"""
  try:
    con = connect()
    con.row_factory = sqlite3.Row
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
  except Exception as e:
    # Allows testing of db separate from rest of app
    if __name__ != '__main__':
      from server.utils.api_exception import APIException
      raise APIException(500, 'Internal database error')
    else:
      import traceback
      traceback.print_exc()

if __name__ == '__main__':
  x = dict(exec("SELECT * FROM user WHERE username=?", ('user',), 'fetchone'))
  print(x.get('username'))