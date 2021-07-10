import sqlite3
import pyperclip
from key import Key

def checkTableExistence(c):
    """Checks if keys table exists in database.
    Returns boolean true/false stored in tableExistence"""
    
    #Query ALL tables in database
    #List of tables stored in tableList
    c.execute("SELECT name FROM sqlite_master")
    tableList = c.fetchall()
    
    if tableList == []:
        tableExistence = False
    else:
        tableExistence = True
        
    return tableExistence
        
def viewKeys(c):
    """Returns a list of all Key IDs in database"""
    
    c.execute("SELECT website_key FROM keys")
    website_keyList = c.fetchall()
    
    return website_keyList
    
def menu(tableExistence, c):
    """Displays menu for user.
    User options dependent on tableExistence.
    Returns option selected by user
    which should be in ['a', 'd', 'c', 'u', 'q']"""
    
    print("\nOnePass - Password Manager")
    
    #if keys table does not exist
    #User only has option to add new key or quit
    #No key list shown because no keys
    if tableExistence == False:
        selected = input("\n(a)dd or (q)uit? >>> ").lower()
    
    #Else call viewKeys()
    #Print each Key ID on its own line for easy user view
    #When keys already exist in db, user has more options
    else:
        website_keyList = viewKeys(c)
        
        for website_key in website_keyList:
            print("|-- " + website_key[0])
        
        selected = input('\n(a)dd, (d)elete, (c)opy, (u)pdate, or (q)uit? >>> ').lower()
    
    return selected
           
def createTable(c): 
    """Create keys table in SQLite database.""" 
      
    c.execute("""CREATE TABLE keys (
                website_key text primary key,
                password text
                )""")

def generateKeys():
    """Return a list of key objects."""
    
    #Try converting user input to integer
    #Throw error and exit if user enters string that can't be converted
    try:
        numKeys = int(input('Enter number of keys to be added: '))
    except ValueError:
        print("Invalid command: integer value expected")
        exit()

    #Append key objects to empty key list in for-loop
    #After iteration, return keys list
    keys = []
    for i in range(0, numKeys):             
        website_key = input('\nKey ID: ')
        password = input('Password: ')
    
        key = Key(website_key, password)
        
        keys.append(key)
    
    return keys

def insertKey(keys, conn, c):
    """Try to insert all keys to database.
    Throw error if a key ID already exists in database."""
    
    for key in keys:
        with conn:
            try:
                c.execute("INSERT INTO keys VALUES (:website_key, :password)", 
                    {'website_key':key.website_key, 'password':key.password})
            except sqlite3.IntegrityError:
                print("Key cannot be added because <" + key.website_key + "> already exists!")  
            
def deleteKey(website_key, conn, c):
    """Delete key from database.
    This function will delete keys table
    if no rows left in table after deletion"""
    
    #Query Key ID before deletion to provide
    #feedback to user if key does not exist
    with conn:
        c.execute("SELECT website_key FROM keys WHERE website_key = :website_key",
                  {'website_key': website_key}) 
        toBeDeleted = c.fetchone()
        
        if toBeDeleted == None:
            print("Error: Key ID does not exist")
        
        #If Query ID does exist then delete from database and
        #provide user confirmation it was deleted    
        else: 
            c.execute("DELETE from keys WHERE website_key = :website_key", 
                      {'website_key': website_key})
            print("Key ID <" + website_key + "> deleted from database.")
            
            #After deletion query all rows in keys table
            c.execute("SELECT * FROM keys")
            rowNum = len(c.fetchall())
            
            #If no rows in table, then delete table
            if rowNum == 0:
                c.execute("DROP table keys")
            else:
                pass
         
def copyKey(website_key, conn, c):
    """Copy key password to user's clipboard.
    pyperclip module used for easy copy functionality"""
    
    with conn:
        c.execute("SELECT password FROM keys WHERE website_key = :website_key",
                  {'website_key': website_key})
        
        password = c.fetchone()
        
        #Try to copy password to clipboard
        #Throw error if Key ID does not exist in db
        try:
            pyperclip.copy(password[0])
            print("Password has been copied to your clipboard!")
        except TypeError:
            print("Error: Key ID does not exist")
            
def updateKey(website_key, conn, c):
    """Change password for a Key ID in database"""
    
    with conn:
        #Query db for website_key input by user
        c.execute("SELECT website_key FROM keys WHERE website_key = :website_key",
                  {'website_key': website_key})
         
        toBeUpdated = c.fetchone()
        
        #Throw error if Key ID entered by user doesn't exist
        #Else prompt user to enter new password
        if toBeUpdated == None:
            print("Error: Key ID does not exist")
        else:
            password = input("New password: ")
    
            #Update Key ID password
            with conn:
                c.execute("UPDATE keys SET password = :password WHERE website_key = :website_key",
                          {'password': password, 'website_key': website_key})
            
            #Provide user confirmation that password was updated
            print("Password for <" + website_key + "> has been updated!")
          
def runCommand(tableExistence, selected, conn, c):
    """"Call a function dependent on user input at menu.
    User selection should be in ['a', 'd', 'c', 'u', 'q']
    Some options are invalid depending on tableExistence."""
    
    #Add new key to db
    #Create table if it doesn't already exist
    #Call generateKeys() and insertKey()
    if selected == "a":
        if tableExistence == False:
            createTable(c)   
        keys = generateKeys()
        insertKey(keys, conn, c)
    
    #Delete key from database 
    #Invalid command if keys table does not exist
    #User-entered Key ID passed to deleteKey()   
    elif selected == "d":
        if tableExistence == False:
            print("Invalid command")
        else:
            website_key = input("Enter Key ID to delete: ")
            print()
            deleteKey(website_key, conn, c)
    
    #Copy Key ID's password to clipboard
    #Invalid command if keys table doesn't exist
    #User-entered Key ID passed to copyKey()     
    elif selected == "c":
        if tableExistence == False:
            print("Invalid command")
        else:
            website_key = input("Enter Key ID to copy password: ")
            print()
            copyKey(website_key, conn, c)
    
    #Change password for user-entered Key ID
    #Invalid command if keys table doesn't exist
    #User-entered Key ID passed to updateKey()        
    elif selected == "u":
        if tableExistence == False:
            print("Invalid command")
        else:
            website_key = input("Enter Key ID to update password: ")
            print()
            updateKey(website_key, conn, c)
    
    #Call no functions if user enters q for quit
    elif selected == "q":
        pass
    
    #Anything else entered by user is invalid command     
    else:
        print("Invalid command")
        exit()
    
def main():
    """Establish connection with database and
    present user with menu to manage passwords. 
    User has the option to add new passwords, 
    delete existing passwords, copy passwords to clipboard,
    and change passwords.
    
    Any changes made to database are committed and
    conection closed before program end."""
    
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
    tableExistence = checkTableExistence(c)

    selected = menu(tableExistence, c)
    
    runCommand(tableExistence, selected, conn, c)
    
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    main()   

        
    


