import mysql.connector
def initialize_db(path):
    db = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            #password should be the password to your root on MySQL
            password= "")  
    cur = db.cursor()
    try:
        fd = open(path, 'r')
    except:
        print("path is incorrect")
        return False
    sqlFile = fd.read()
    fd.close()  
    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        try:
            if command.strip() != "":
                cur.execute(command)
                print(command)
        except:
            print("ERROR: Command skipped", command)
            
    print("Done!")
    return True
    

