import os.path
import sqlite3
import pyperclip
from key import Key

def checkTableExistence(c):
    c.execute("SELECT name FROM sqlite_master")
    tableList = c.fetchall()
    
    if tableList == []:
        tableExistence = False
    else:
        tableExistence = True
        
    return tableExistence
        
def viewKeys(c):
    c.execute("SELECT website_key FROM keys")
    website_keyList = c.fetchall()
    
    return website_keyList
    
def menu(tableExistence, c):
    print("\nOnePass - Password Manager")
    
    if tableExistence == False:
        selected = input("\n(a)dd or (q)uit? >>> ").lower()
    
    else:
        website_keyList = viewKeys(c)
        
        for website_key in website_keyList:
            print("|-- " + website_key[0])
        
        selected = input('\n(a)dd, (d)elete, (c)opy, or (q)uit? >>> ').lower()
    
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
         
def copyKey(website_key, conn, c):
    with conn:
        c.execute("SELECT password FROM keys WHERE website_key = :website_key",
                  {'website_key': website_key})
        
        password = c.fetchone()
        pyperclip.copy(password[0])
        
        print("Password has been copied to your clipboard")
          
def runCommand(tableExistence, selected, conn, c):
    
    if selected == "a":
        if tableExistence == False:
            createTable(c)   
        keys = generateKeys()
        insertKey(keys, conn, c)
        
    elif selected == "d":
        if tableExistence == False:
            print("Invalid Command")
        else:
            website_key = input("Enter Key to Delete: ")
            deleteKey(website_key, conn, c)
        
    elif selected == "c":
        if tableExistence == False:
            print("Invalid Command")
        else:
            website_key = input("Enter Key to Copy Password: ")
            copyKey(website_key, conn, c)
    
    elif selected == "q":
        pass
        
    else:
        print("Invalid Command")
        exit()
    
def main():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
    tableExistence = checkTableExistence(c)

    selected = menu(tableExistence, c)
    
    runCommand(tableExistence, selected, conn, c)
    
    conn.commit()
    conn.close()
    
main()   


        
    


