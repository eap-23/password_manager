import os.path
import sqlite3
from key import Key

def createTable(c):    
    c.execute("""CREATE TABLE keys (
                website_key text primary key,
                username text,
                password text
                )""")

def generateKeys():
    #Need to make this an iteration!
    numKeys = int(input('Enter Number of Keys: '))
    print()
    keys = []
    
    for i in range(0, numKeys):             
        website_key = input('Enter Key Name: ')
        username = input('Enter username used for website: ')
        password = input('Enter password: ')
        print()
    
        key = Key(website_key, username, password)
        
        keys.append(key)
    
    return keys

def insertKey(keys, conn, c):
    for key in keys:
        with conn:
            c.execute("INSERT INTO keys VALUES (:website_key, :username, :password)", 
                  {'website_key':key.website_key, 'username':key.username, 
                   'password':key.password})
    
def main():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    
    createTable(c)
    keys = generateKeys()
    insertKey(keys, conn, c)
    
    c.execute("SELECT * FROM keys WHERE password='test_pw'")
    
    print(c.fetchall())
    
    conn.commit()
    conn.close()
    
main()   


        
    


