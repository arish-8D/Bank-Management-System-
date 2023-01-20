import mysql.connector as sql
import tabulate as tbl

try:
    pwd = input("Enter the password of your mysql server: ")
    connector = sql.connect(host ="localhost", user ="root", password = pwd)
except Exception:
    print('Wrong password, exiting program...')
    exit()

cursor = connector.cursor()


def create_db_table():
    cursor.execute(f"create database bank_management")
    cursor.execute(f'use bank_management')
    cursor.execute("create table bank_details("
                   "Name varchar(255) NOT NULL,"
                   "Account_Number bigint PRIMARY KEY,"
                   "Account_Type char(7) NOT NULL,"
                   "Account_Balance int NOT NULl,"
                   "Address varchar(255) NOT NULL,"
                   "Gender char(1) NOT NULL,"
                   "DOB date NOT NULL,"
                   "Aadhar_Number bigint NOT NULL,"
                   "Phone_Number bigint NOT NULL)")


    print("\nDatabase and table are successfully created...\n")


try:
    create_db_table()
    cursor.execute(f"desc bank_details")
    data = cursor.fetchall()
    table = tbl.tabulate(data, headers = ['Field', 'Type', 'Null', 'Key', 'Default', 'Extra'])
    print(table)

except Exception:
    print("\nThe database and table already exist.")
    
finally:
    input("\nPress Enter to exit.")
