import os.path
import sqlite3
from key import Key

def createTable(c):    
    c.execute("""CREATE TABLE keys (
                website_key text,
                username text,
                password text
                )""")

def generateKeys():
    #Need to make this an iteration!
    website_key = input('Enter Key Name: ')
    username = input('Enter username used for website: ')
    password = input('Enter password: ')
    
    key_1 = Key(website_key, username, password)
    
    return key_1

def insertKey(key, conn, c):
    with conn:
        c.execute("INSERT INTO keys VALUES (:website_key, :username, :password)", 
                  {'website_key':key.website_key, 'username':key.username, 
                   'password':key.password})
    
def main():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    
    createTable(c)
    key_1 = generateKeys()
    insertKey(key_1, conn, c)
    
    c.execute("SELECT * FROM keys WHERE password='test_pw'")
    
    print(c.fetchone())
    
    conn.commit()
    conn.close()
    
main()   


        
    


