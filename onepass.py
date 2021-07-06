import os.path
import sqlite3
from key import Key

def menu():
    print("\n***Onepass - Password Manager***\n")
    
    print('(a)dd')
    print('(d)elete')
    print('(v)iew')
    print('(c)opy')
    print('(q)uit')
    
    selected = input("\n>>> ").lower()
    
    return selected
           
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
            
def deleteKey(website_key, conn, c):
     with conn:
         c.execute("DELETE from keys WHERE website_key = :website_key",
                   {'website_key': website_key})
          
def main():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
    # createTable(c)
    selected = menu()
    
    if selected == "a":   
        keys = generateKeys()
        insertKey(keys, conn, c)
    elif selected == "d":
        website_key = input("Enter Key to Delete: ")
        deleteKey(website_key, conn, c)
    elif selected == "c":
        pass
    elif selected == "q":
        pass
    
    # insertKey(keys, conn, c)
    
    # c.execute("SELECT * FROM keys WHERE password='test'")
    
    c.execute("SELECT * FROM keys")
    
    print(c.fetchall())
    
    conn.commit()
    conn.close()
    
main()   


        
    


