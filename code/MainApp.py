import creation as c
import os
import mysql.connector
def insert_tuple_file(table, path,db,cur):
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                data = line.strip().split(';')
                print("\nThe tuple to be added:", data[0])
                query = f"INSERT INTO {table} VALUES {data[0]};"
                cur.execute(query)
            db.commit()
        print("Insertion from file successful!")
    except mysql.connector.Error as err:
        print(f"Insertion failed: {err}")
def insert_tuple(table,fields,db,cur):
    values = []
    for field in fields:
        value = input(f"Enter {field}: ")
        values.append(value)
    ins_values = ""
    for i, value in enumerate(values):
        ins_values += "'"+value+"',"

    ins_values = ins_values[:-1]
    print("\nThe tuple to be added:", "("+ins_values+")")
    try:
        query = f"INSERT INTO {table} VALUES ({ins_values});"
        cur.execute(query)
        db.commit()
        print(f"Insertion into table {table} successful!")
    except mysql.connector.Error as err:
        print(f"Insertion failed: {err}")
def update_tuple(table, search_field, search_value, update_field, update_value,db,cur):
    query = f"UPDATE {table} SET {update_field} = '{update_value}' WHERE {search_field} = '{search_value}'"
    try:
        cur.execute(query)
        db.commit()
        if cur.rowcount > 0:
            print("Update successful!")
        else:
            print("No records found for the provided search criteria.")
    except mysql.connector.Error as err:
        print(f"Failed to update: {err}")
def delete_tuple(table, search_field, search_value,db,cur):
    query = f"DELETE FROM {table} WHERE {search_field} = '{search_value}'"
    try:
        cur.execute(query)
        db.commit()
        if cur.rowcount > 0:
            print("Deletion successful!")
        else:
            print("No records found for the provided search criteria.")
    except mysql.connector.Error as err:
        print(f"Failed to delete: {err}")
def to_table(cur):
    columns = [col[0] for col in cur.description]
    results = cur.fetchall()

    column_widths = [max(len(str(row[i])) for row in results + [columns]) for i in range(len(columns))]

    for i, col in enumerate(columns):
        print(f"{col:{column_widths[i]}}", end="  ")
    print("\n" + "=" * (sum(column_widths) + len(columns) * 2))  # Separator line

    for row in results:
        for i, value in enumerate(row):
            print(f"{value:{column_widths[i]}}", end="  ")
        print()
    print()
def admin_consol(db,cur):
    while(True):
        print("ADMIN MENU")
        print("1. Initialize database\n2. Add users\n3. Edit users\n4. Block users\n5. Enter a SQL Query to MUSEUM database\n6. Logout")
        selection = input("Type either 1, 2, 3, 4, 5 or 6: ")
        if selection in ['1']:
            while(True):
                print("\nDATABASE INITIALIZATION\n")
                print("WARNING! Re-initializing the database results in all users being deleted.\nThis could affect your account! Do you wish to continue? (Y/N)")
                yes = input()
                if(yes in ['y'] or yes in ['Y']):
                    path = input("Provide the path of the sql file you wish to populate the MUSEUM database with:\n->")
                    if(c.initialize_db(path) == True):
                        try:
                            print("Database initialized please login again")
                            username= input("Username: ")
                            password= input("Password: ")
                            db = mysql.connector.connect(
                                host="localhost",
                                port=3306,
                                user=username,
                                password= password
                            )
                            cur = db.cursor()
                            cur.execute("SELECT current_role();")
                            role = cur.fetchone()[0]
                            if not ("db_admin" in role or "read_access" in role or "data_access" in role):
                                print("You deleted your account...")
                                return
                        except:
                            exit(1)
                        break
                    else:
                        print("Not a valid path. Please try again\n")
                        continue
                else:
                    break
            continue
        elif selection in ['2']:
            print("\nUSER CREATION\n")
            username = ''
            password = ''
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            print("Enter role\n1. Admin\n2. Data Entry\n3. Guest")
            role = input("Type either 1, 2 or 3: ")
            if role in ['1']:
                role = "db_admin"
            elif role in ['2']:
                role = "data_access"
            elif role in ['3']:
                role = "read_access"
            else:
                print("Invalid input. Please try again.\n")
                continue    
            try:
                cur.execute(f"DROP USER IF EXISTS {username}@localhost;")
                db.commit()
                cur.execute(f"CREATE USER {username}@localhost IDENTIFIED WITH mysql_native_password BY '{password}';")
                db.commit()
                cur.execute(f"GRANT {role}@localhost TO {username}@localhost;")
                db.commit()
                cur.execute(f"SET DEFAULT ROLE {role}@localhost TO {username}@localhost;")
                db.commit()
                print("Account created successfully with role:",role.upper()+"!\n")
                continue
            except mysql.connector.Error as err:
                print(f"Error creating account, Please try again.\nERROR:{err}\n")
                continue
        elif selection in ['3']:
            print("\nEDIT USERS\n")
            username = ''
            username = input("Enter the username of user you wish to edit: ")
            print("Change role to\n1. Admin\n2. Data Entry\n3. Guest")
            role = input("Type either 1, 2 or 3: ")
            if role in ['1']:
                role = "db_admin"
            elif role in ['2']:
                role = "data_access"
            elif role in ['3']:
                role = "read_access"
            else:
                print("Invalid input. Please try again.\n")
                continue    
            try:
                cur.execute(f"GRANT {role}@localhost TO {username}@localhost")
                db.commit()
                cur.execute(f"SET DEFAULT ROLE {role}@localhost TO {username}@localhost;")
                db.commit()
                print(username,"changed successfully to role:",role.upper()+"!\n")
                continue
            except mysql.connector.Error as err:
                print(f"Error editing account, Please try again.\nERROR:{err}\n")
                continue
        elif selection in ['4']:
            print("\nBLOCK USERS\n")
            username = ''
            username = input("Enter the username of user you wish to block: ")
            try:
                cur.execute(f"GRANT blocked@localhost TO {username}@localhost;")
                db.commit()
                cur.execute(f"SET DEFAULT ROLE blocked@localhost TO {username}@localhost;")
                db.commit()
                print(username,"blocked successfully!\n")
                continue
            except mysql.connector.Error as err:
                print(f"Error blocking account, Please try again.\nERROR:{err}\n")
                continue
        elif selection in ['5']: 
            print("\nSQL QUERY\n")
            query = input("Please enter an SQL query you wish to commit to the database: \n-> ")
            try:
                queries = query.split(";")  # Split multiple queries by semicolon
                cur.execute("USE MUSEUM;")
                for single_query in queries:
                    if single_query.strip():  # Check if the query is not empty
                        cur.execute(single_query)
                db.commit()
                print("Queries committed successfully!\n")
                continue
            except mysql.connector.Error as err:
                print(f"Error committing query, Please try again.\nERROR: {err}\n")
                continue
        elif selection in ['6']:
            print("Logging out...\n")
            break
        else:
            print("Invalid input. Please try again.\n")
            continue
def data_entry(db,cur):
    while(True):
        table_list = ['ARTIST','ART_OBJECT','PAINTING','SCULPTURE_STATUE','OTHER','COLLECTION','PERMANENT_COLLECTION','BORROWED_COLLECTION','EXHIBITION','EXHIBITION_HAS']
        field_list = [
                                ["Name", "Date_born", "Date_died", "Country_of_origin", "Epoch", "Main_style", "Description"],
                                ["Id_no","Artist_name", "Year", "Title", "Description", "Origin", "Epoch"],
                                ["Art_id", "Paint_type", "Drawn_on", "Style"],
                                ["Art_id", "Material", "Height", "Weight", "Style"],
                                ["Art_id", "Type", "Style"],
                                ["Name", "Type", "Description", "Address", "Phone", "Contact_person"],
                                ["Art_id", "Date_acquired", "Status", "Cost"],
                                ["Art_id", "Collection_name", "Date_borrowed", "Date_returned"],
                                ["Name", "Start_date", "End_date"],
                                ["Exhibition_name", "Art_id"],
                             ]
        print("DATA ENTRY MENU")
        print("1. Lookup Information\n2. Insert tuple to table\n3. Update tuple\n4. Delete tuple\n5. Logout")
        selection = input("Type either 1, 2, 3, 4 or 5: ")
        if selection in ['1']:
            while(True):
                print("\n1. Lookup Tables\n2. Lookup ART_OBJECTS by field values")
                lookup = input("Type 1 or 2: ")
                if lookup in ['1']:
                    print("\nLOOKUP TABLES\n")
                    print("Please select what Tables you wish to lookup\n")
                    print("1. ARTIST\n2. ART_OBJECT\n3. PAINTING\n4. SCULPTURE_STATUE\n5. OTHER\n6. COLLECTION\n7. PERMANENT_COLLECTION\n8. BORROWED_COLLECTION\n9. EXHIBITION\n10. EXHIBITION_HAS\n11. <-")
                    table = input("Type either 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 or 11: ")
                    print()
                    cur.execute("USE MUSEUM;")
                    if table in ['1']:
                        try:
                            print("NOTE: ARTIST description is too long, it is exempt from this query")
                            print("ARTIST TABLE\n")
                            query = "SELECT Name, Date_born, Date_died, Country_of_origin, Epoch, Main_style FROM ARTIST"
                            cur.execute(query)
                            to_table(cur)
                            break
                        except: 
                            print(f"Error looking up table. Please try again.\n")
                            continue
                    elif table in ['2']:
                        try:  
                            print("ART_OBJECT TABLE\n")
                            print("NOTE: ART_OBJECT description is too long, it is exempt from this query")
                            query = "SELECT Id_no, Artist_name, Year,Title, Origin, Epoch FROM ART_OBJECT;"
                            cur.execute(query)
                            to_table(cur)
                            break
                        except: 
                            print(f"Error looking up table. Please try again.\n")
                            continue
                        
                    elif table in ['3']:
                        try:
                            print("PAINTING TABLE\n")
                            query = "SELECT * FROM PAINTING"
                            cur.execute(query)
                            to_table(cur)
                            break
                        except: 
                            print(f"Error looking up table. Please try again.\n")
                            continue
                    elif table in ['4']:
                        try:
                            print("SCULPTURE_STATUE TABLE\n")
                            query = "SELECT * FROM SCULPTURE_STATUE"
                            cur.execute(query)
                            to_table(cur)
                            break
                        except: 
                            print(f"Error looking up table. Please try again.\n")
                            continue
                    elif table in ['5']:
                        try:
                            print("OTHER TABLE\n")
                            query = "SELECT * FROM OTHER"
                            cur.execute(query)
                            to_table(cur)
                            break
                        except: 
                            print(f"Error looking up table. Please try again.\n")
                            continue
                    elif table in ['6']:
                        try:
                            print("COLLECTION TABLE\n")
                            print("NOTE: COLLECTION description is too long, it is exempt from this query")
                            query = "SELECT Name, Type, Address, Phone, Contact_person FROM COLLECTION"
                            cur.execute(query)
                            to_table(cur)
                            break
                        except: 
                            print(f"Error looking up table. Please try again.\n")
                            continue
                    elif table in ['7']:
                        try:
                            print("PERMANENT_COLLECTION TABLE\n")
                            query = "SELECT * FROM PERMANENT_COLLECTION"
                            cur.execute(query)
                            to_table(cur)
                            break
                        except: 
                            print(f"Error looking up table. Please try again.\n")
                            continue
                    elif table in ['8']:
                        try:
                            print("BORROWED_COLLECTION TABLE\n")
                            query = "SELECT * FROM BORROWED_COLLECTION"
                            cur.execute(query)
                            to_table(cur)
                            break
                        except: 
                            print(f"Error looking up table. Please try again.\n")
                            continue
                    elif table in ['9']:
                        try:
                            print("EXHIBITION TABLE\n")
                            query = "SELECT * FROM EXHIBITION"
                            cur.execute(query)
                            to_table(cur)
                            break
                        except: 
                            print(f"Error looking up table. Please try again.\n")
                            continue
                    elif table in ['10']:
                        try:
                            print("EXHIBITION_HAS TABLE\n")
                            query = "SELECT * FROM EXHIBITION_HAS"
                            cur.execute(query)
                            to_table(cur)
                            break
                        except: 
                            print(f"Error looking up table. Please try again.\n")
                            continue
                    elif table in ['11']:
                        break
                elif lookup in ['2']:
                    print("\nLOOKUP ART_OBJECTS\n")
                    cur.execute("USE MUSEUM;")
                    print("NOTE: ART_OBJECT descriptions too long, it is exempt from this query")
                    print("Search ART_OBJECT by...\n1. Artist_name\n2. Year\n3. Origin\n4. Epoch\n5. <-")
                    search_by = input("Type 1, 2, 3, 4 or 5: ")
                    print()
                    if search_by in ['1']:
                        search = input("Enter Artist_name: ")
                        query = f"SELECT Id_no, Artist_name, Year,Title, Origin, Epoch FROM ART_OBJECT WHERE Artist_name ='{search}'"
                        cur.execute(query)
                        to_table(cur)
                        break
                    elif search_by in ['2']:
                        search = input("Enter Year: ")
                        query = f"SELECT Id_no, Artist_name, Year,Title, Origin, Epoch FROM ART_OBJECT WHERE Year ='{search}'"
                        cur.execute(query)
                        to_table(cur)
                        break
                    elif search_by in ['3']:
                        search = input("Enter Origin: ")
                        query = f"SELECT Id_no, Artist_name, Year,Title, Origin, Epoch FROM ART_OBJECT WHERE Origin ='{search}'"
                        cur.execute(query)
                        to_table(cur)
                        break
                    elif search_by in ['4']:
                        search = input("Enter Epoch: ")
                        query = f"SELECT Id_no, Artist_name, Year,Title, Origin, Epoch FROM ART_OBJECT WHERE Epoch ='{search}'"
                        cur.execute(query)
                        to_table(cur)
                        break
                    elif search_by in ['5']:
                        break
                    else: 
                        print(f"Error looking up ART_OBJECT. Please try again.\n")
                        continue
        elif selection in ['2']:
            while(True):
                print("\nINSERT TUPLES\n")
                print("Please select what Tables you wish to insert a tuple into\n")
                print("TABLE LIST:\nARTIST\nART_OBJECT\nPAINTING\nSCULPTURE_STATUE\nOTHER\nCOLLECTION\nPERMANENT_COLLECTION\nBORROWED_COLLECTION\nEXHIBITION\nEXHIBITION_HAS\n1. <-")
                table = input("Type out the table you wish to insert a tuple into or type 1 to go back to menu\n->")
                table = table.upper()
                print()
                if table in table_list:
                    print("Insert tuple by...\n1. File\n2. Prompts")
                    selection = input("Type either 1 or 2: ")
                    cur.execute("USE MUSEUM;")
                    if selection in ['1']:
                        try:
                            path = input("Enter the path of the tuple file\n->")
                            insert_tuple_file(table,path,db,cur)
                        except:
                            print("Invalid input. Please try again")
                            continue
                    elif selection in ['2']:
                        try:
                            insert_tuple(table,field_list[table_list.index(table)],db,cur)
                        except:
                            print("Invalid input. Please try again")
                            continue
                    else:
                        print("Invalid input. Please try again.\n")
                        continue
                elif table in ['1']:
                    break
                else:
                    print("Invalid input. Please make sure to type out the name of the table fully.\n")
                    continue
        elif selection in ['3']:
            while(True):
                cur.execute("USE MUSEUM;")
                print("\nUPDATE TUPLES\n")
                print("Please select which Table you wish to update a tuple for\n")
                print("TABLE LIST:\nARTIST\nART_OBJECT\nPAINTING\nSCULPTURE_STATUE\nOTHER\nCOLLECTION\nPERMANENT_COLLECTION\nBORROWED_COLLECTION\nEXHIBITION\nEXHIBITION_HAS\n1. <-")
                table = input("Type out the table you wish to update a tuple into or type 1 to go back to menu\n->")
                table = table.upper()
                print()
                if table in table_list:
                    try:
                        print("List of field values for",table)
                        for value in field_list[table_list.index(table)]:
                            print(value)
                        search_field = input("Please type out the field to search tuple by (CASE-SENSITVE)\n->")
                        if search_field in field_list[table_list.index(table)]:
                            search_value = input("Please type out the value of the field to search tuple by (CASE-SENSITVE)\n->")
                            update_field = input("Please type out the field you would like to update (CASE-SENSITVE)\n->")
                            if update_field in field_list[table_list.index(table)]:
                                 update_value = input("Please type out the value of the field you would like to update\n->")
                                 update_tuple(table,search_field,search_value,update_field,update_value,db,cur)
                            else:
                                print("Invalid input. Please try again.")
                                continue 
                        else:
                            print("Invalid input. Please try again.")
                            continue
                    except: 
                        print("Invalid input. Please try again.")
                        continue
                elif table in ['1']:
                    break
                else:
                    print("Invalid input. Please try again.")
                    continue
        elif selection in ['4']:
             while(True):
                cur.execute("USE MUSEUM;")
                print("\nDELETE TUPLES\n")
                print("Please select which Table you wish to delete a tuple for\n")
                print("TABLE LIST:\nARTIST\nART_OBJECT\nPAINTING\nSCULPTURE_STATUE\nOTHER\nCOLLECTION\nPERMANENT_COLLECTION\nBORROWED_COLLECTION\nEXHIBITION\nEXHIBITION_HAS\n1. <-")
                table = input("Type out the table you wish to delete a tuple for or type 1 to go back to menu\n->")
                table = table.upper()
                print()
                if table in table_list:
                    try:
                        print("List of field values for",table)
                        for value in field_list[table_list.index(table)]:
                            print(value)
                        search_field = input("Please type out the field to search tuple by (CASE-SENSITVE)\n->")
                        if search_field in field_list[table_list.index(table)]:
                            search_value = input("Please type out the value of the field to search tuple by (CASE-SENSITVE)\n->")
                            delete_tuple(table,search_field,search_value,db,cur)
                        else:
                            print("Invalid input. Please try again.")
                            continue
                    except: 
                        print("Invalid input. Please try again.")
                        continue
                elif table in ['1']:
                    break
                else:
                    print("Invalid input. Please try again.")
                    continue
        elif selection in ['5']:
            print("Logging out...\n")
            break
        else:
            print("Invalid input. Please try again.\n")
            continue
def guest_view(db,cur):
    while(True):
        cur = db.cursor()
        cur.execute("USE MUSEUM;")
        print("\nGUEST BROWSE\n")
        print("Welcome to the Museum!\nLet's browse through what the museum has to offer\nAt a surface level...\n1. ARTIST -the creators of the many pieces found in the museum!\n2. ART_OBJECTS -All of the art pieces our museum has to offer!\n3. COLLECTION -Collections found in the museum that dont belong to us\n4. EXHIBITION -Exhibitions found in our museum that host a variety of art pieces!\n<- 5. Logout")
        selection = input("Please type 1, 2, 3, 4 or 5: ")
        if selection in ['1']:
            while(True):
                print("\nARTIST")
                print("ARTIST TABLE\n")
                print("NOTE: ARTIST description is too long, it is exempt from this query")
                query = "SELECT Name, Date_born, Date_died, Country_of_origin, Epoch, Main_style FROM ARTIST"
                cur.execute(query)
                to_table(cur)
                choice = input("<-1. Back ")
                if choice in ['1']:
                    break
                else:
                    print("Invalid input. Please try again.")
                    continue
        elif selection in ['2']:
            while(True):
                print("\nART_OBJECT")
                print("Theres a variety of ART_OBJECTs our museum has to offer!\n1. Show all ART_OBJECTs\n2. Show PAINTINGs only (type of ART_OBJECT)\n3. Show SCULPTURE_STATUEs only (type of ART_OBJECT)\n4. Show OTHERs only (type of ART_OBJECT)\n5. Show BORROWED_COLLECTION only (ART_OBJECTS from borrowed collection)\n6. Show PERMANENT_COLLECTION only (ART_OBJECTS from permanent collection)\n7. <- Back")
                choice = input("Please type 1, 2, 3, 4, 5, 6 or 7: ")
                if choice in ['1']:
                    print("ART_OBJECT TABLE\n")
                    print("NOTE: ART_OBJECT description is too long, it is exempt from this query")
                    query = "SELECT Id_no, Artist_name, Year,Title, Origin, Epoch FROM ART_OBJECT;"
                    cur.execute(query)
                    to_table(cur)
                    continue
                elif choice in ['2']:
                    print("PAINTING TABLE\n")
                    query = "SELECT * FROM PAINTING"
                    cur.execute(query)
                    to_table(cur)
                    print()
                    print("PAINTING and it's correlating ART_OBJECT TABLE\n")
                    query = "SELECT Id_no, Artist_name, Year,Title, Origin, Epoch FROM ART_OBJECT AS a RIGHT JOIN PAINTING as e ON e.Art_id = a.Id_no;"
                    cur.execute(query)
                    to_table(cur)
                    continue
                elif choice in ['3']:
                    print("SCULPTURE_STATUE TABLE\n")
                    query = "SELECT * FROM SCULPTURE_STATUE"
                    cur.execute(query)
                    to_table(cur)
                    print()
                    print("SCULPTURE_STATUE and it's correlating ART_OBJECT TABLE\n")
                    query = "SELECT Id_no, Artist_name, Year,Title, Origin, Epoch FROM ART_OBJECT AS a RIGHT JOIN SCULPTURE_STATUE as e ON e.Art_id = a.Id_no;"
                    cur.execute(query)
                    to_table(cur)
                    continue
                elif choice in ['4']:
                    print("OTHER TABLE\n")
                    query = "SELECT * FROM OTHER"
                    cur.execute(query)
                    to_table(cur)
                    print()
                    print("OTHER and it's correlating ART_OBJECT TABLE\n")
                    query = "SELECT Id_no, Artist_name, Year,Title, Origin, Epoch FROM ART_OBJECT AS a RIGHT JOIN OTHER as e ON e.Art_id = a.Id_no;"
                    cur.execute(query)
                    to_table(cur)
                    continue
                elif choice in ['5']:
                    print("BORROWED_COLLECTION TABLE\n")
                    query = "SELECT * FROM BORROWED_COLLECTION"
                    cur.execute(query)
                    to_table(cur)
                    print()
                    print("BORROWED_COLLECTION and it's correlating ART_OBJECT TABLE\n")
                    query = "SELECT Id_no, Artist_name, Year,Title, Origin, Epoch FROM ART_OBJECT AS a RIGHT JOIN BORROWED_COLLECTION as e ON e.Art_id = a.Id_no;"
                    cur.execute(query)
                    to_table(cur)
                    continue
                elif choice in ['6']:
                    print("PERMANENT_COLLECTION TABLE\n")
                    query = "SELECT * FROM PERMANENT_COLLECTION"
                    cur.execute(query)
                    to_table(cur)
                    print()
                    print("PERMANENT_COLLECTION and it's correlating ART_OBJECT TABLE\n")
                    query = "SELECT Id_no, Artist_name, Year,Title, Origin, Epoch FROM ART_OBJECT AS a RIGHT JOIN PERMANENT_COLLECTION as e ON e.Art_id = a.Id_no;"
                    cur.execute(query)
                    to_table(cur)
                    continue
                elif choice in ['7']:
                    break
                else:
                    print("Invalid input. Please try again.")
                    continue
        elif selection in ['3']:
            while(True):
                print("\nCOLLECTION")
                print("COLLECTION is a table keeping track of who and what we borrowed!\n1. Show all COLLECTION\n2. Show BORROWED_COLLECTION (Table of the borrowed collections from COLLECTION)\n3. <- Back")
                choice = input("Please type 1, 2 or 3: ")
                if choice in ['1']:
                    print("COLLECTION TABLE\n")
                    print("NOTE: COLLECTION description is too long, it is exempt from this query")
                    query = "SELECT Name, Type, Address, Phone, Contact_person FROM COLLECTION"
                    cur.execute(query)
                    to_table(cur)
                    continue
                elif choice in ['2']:
                    print("BORROWED_COLLECTION TABLE\n")
                    query = "SELECT * FROM BORROWED_COLLECTION"
                    cur.execute(query)
                    to_table(cur)
                    print()
                    print("BORROWED_COLLECTION and it's correlating ART_OBJECT TABLE\n")
                    query = "SELECT Id_no, Artist_name, Year,Title, Origin, Epoch FROM ART_OBJECT AS a LEFT JOIN BORROWED_COLLECTION as e ON e.Art_id = a.Id_no;"
                    cur.execute(query)
                    to_table(cur)
                    continue
                elif choice in ['3']:
                    break
                else:
                    print("Invalid input. Please try again.")
                    continue
        elif selection in ['4']:
            while(True):
                print("\nEXHIBITION")
                print("EXHIBITION is a table of all the exhibitions our museum has to offer!\n1. Show all EXHIBITION\n2. Show EXHIBITION_HAS (Table of what each exhbiit has in store and the exhbit they belong to)\n3. <- Back")
                choice = input("Please type 1, 2, or 3: ")
                if choice in ['1']:
                    print("EXHIBITION TABLE\n")
                    query = "SELECT * FROM EXHIBITION"
                    cur.execute(query)
                    to_table(cur)
                    continue
                elif choice in ['2']:
                    print("EXHIBITION_HAS TABLE\n")
                    query = "SELECT * FROM EXHIBITION_HAS"
                    cur.execute(query)
                    to_table(cur)
                    print()
                    print("EXHIBITION_HAS and it's correlating ART_OBJECT TABLE\n")
                    query = "SELECT Id_no, Artist_name, Year,Title, Origin, Epoch FROM ART_OBJECT AS a LEFT JOIN EXHIBITION_HAS as e ON e.Art_id = a.Id_no;"
                    cur.execute(query)
                    to_table(cur)
                    continue
                elif choice in ['3']:
                    break
                else:
                    print("Invalid input. Please try again.")
                    continue     
        elif selection in ['5']:
            print()
            break                      
if __name__ == "__main__":
    while(True):
        
        print("Welcome to the Arts Museum Database:")
        print("1. Login\n2. Continue as Guest\n3. Initialize datbase with root\n4. Exit")
        selection = input("Type 1, 2, 3 or 4: ")
        if selection in ['1']:
            try:
                username = ''
                password = ''
                username= input("\nUsername: ")
                password= input("Password: ")
                
                db = mysql.connector.connect(
                host="localhost",
                port=3306,
                user=username,
                password= password)
                cur = db.cursor()
                cur.execute("SELECT current_role();")
                role = cur.fetchone()[0]
                print("\nLogging in with", role.upper(), "permissions...")
                if "db_admin" in role:
                    admin_consol(db,cur)
                elif"data_access" in role:
                    data_entry(db,cur)
                elif "read_access" in role:
                    guest_view(db,cur)
                elif "blocked" in role:
                    print("Unfortunately, you have been blocked from the database...\n")
                else: 
                    print("Login failed!\n")
                continue  
            except:
                 print("INVALID: Returning to Main Menu...\n")
                 continue
            
        elif selection in ['2']:
            username = ''
            password = ''
            username="guest"
            passcode=None
            db = mysql.connector.connect(
                host="localhost",
                port=3306,
                user=username,
                password= password)
            cur = db.cursor
            role = "read_access"
            print("Logging in with", role.upper(), "permissions...")
            guest_view(db,cur)
            continue
        elif selection in ['3']:
            current_dir = os.path.dirname(__file__) 
            print("Enter path of the SQL creation script")
            path = input("->")
            c.initialize_db(path)
        elif selection in ['4']:
            print("Terminating program...")
            exit(1)
        else:
            print("Invalid input. Please try again.\n")
            continue
   

