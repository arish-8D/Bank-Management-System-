import mysql.connector as sql
import tabulate as tbl

connector = sql.connect(host="localhost", user="root", passwd="qwerty", database="bank_management", autocommit=True)
cursor = connector.cursor(buffered=True)


table_headers = ['Name', 'Account Number', 'Account Type', 'Account Balance', 'Address', 'Gender', 'DOB', 'Aadhar Number', 'Phone Number']


def check_for_acc(account_no):
    """A function to check if any account with the inputted account number exists or not"""
    cursor.execute(f"select account_number from bank_details")
    data = cursor.fetchall()
    accounts = []
    for i in data:
        accounts.append(i[0])

    if account_no in accounts:
        found = True
    else:
        found = False

    return found


def more_options():
    more = input("\nWant to do more operations? (y/n): ").lower()
    if more == 'y':
        ask_choices()
    elif more == 'n':
        connector.close()
        print("Okay, Have a nice day!!!")
    else:
        print("Enter y/n")
        more_options()


def add_account():
    try:
        name = input("\nEnter your full name: ").upper()
        gender = input("Enter you gender (M/F): ").upper()
        dob = input("Enter your date of birth (YYYY-MM-DD): ")
        aadhar = int(input("Enter your aadhar card number: "))
        address = input("Enter your residential address: ").upper()
        phone = int(input("Enter your phone number: "))
        acc_type = input("Enter the type of account you want to open (Savings/Current): ").upper()
        money_added = int(input("Amount of money added while opening account: "))

    except ValueError:
        print("\nYou entered something invalid... Try again!!!")
        add_account()

    cursor.execute(f"select max(Account_Number) from bank_details")
    max_acc = cursor.fetchall()[0][0]

    if max_acc is None:
        new_acc = 1234567890
    else:
        new_acc = max_acc + 1
    try:
        cursor.execute(
            f"""insert into bank_details values(
            '{name}',
             {new_acc},
            '{acc_type}',
             {money_added},
            '{address}',
            '{gender}',
            '{dob}',
             {aadhar},
             {phone})""")
        print(f"\nAccount added successfully!!\nYour account number is: {new_acc}")
    except Exception:
        print("Something went wrong...")

    more_options()


def view_user_profile():
    acc_no = int(input("\nEnter the account number: "))

    if check_for_acc(acc_no):
        cursor.execute(f"select * from bank_details where account_number = {acc_no}")
        data = cursor.fetchall()

        acc_details = tbl.tabulate(data, headers = table_headers)
        print()
        print(acc_details)

    else:
        print(f"Account with account number {acc_no}  does not exist.")

    more_options()


def view_all():
    cursor.execute(f"select * from bank_details")
    data = cursor.fetchall()

    table = tbl.tabulate(data, headers = table_headers)
    print()
    print(table)

    more_options()


def deposit_money():
    acc_no = int(input("\nEnter you account number: "))
    if check_for_acc(acc_no):
        cursor.execute(f'select account_balance from bank_details where account_number = {acc_no}')
        bal = cursor.fetchone()[0]
        print(f"\nYour current bank balance is {bal}")
        amount = int(input("\nEnter the amount to be added: "))

        cursor.execute(f"update bank_details set account_balance = {bal + amount} where account_number = {acc_no}")
        cursor.execute(f'select account_balance from bank_details where account_number = {acc_no}')
        new_bal = cursor.fetchone()[0]

        print(f"\n₹{amount} added successfully...\nCurrent account balance is ₹{new_bal}.")
    else:
        print(f"\nAccount with account number {acc_no}  does not exist.")

    more_options()


def withdraw_money():
    acc_no = int(input("\nEnter your account number: "))
    if check_for_acc(acc_no):

        cursor.execute(f'select account_balance from bank_details where account_number = {acc_no}')
        bal = cursor.fetchone()[0]
        print(f"Your current bank balance is {bal}")

        amount = int(input("\nEnter the amount to be withdrawn: "))
        cursor.execute(f"select account_balance from bank_details where account_number = {acc_no}")

        if amount > bal:
            print("\nInsufficient Balance.")
        else:
            cursor.execute(f"update bank_details set account_balance = {bal-amount} where account_number = {acc_no}")
            cursor.execute(f"select account_balance from bank_details where account_number = {acc_no}")
            new_bal = cursor.fetchone()[0]
            print(f"\nTransaction successful, new account balance is ₹{new_bal}")

    else:
        print(f"\nAccount with account number {acc_no} does not exist.")

    more_options()


def update_account_info():
    acc_no = int(input("\nEnter the account number of the account you want to update: "))

    if check_for_acc(acc_no):

        choice = int(input("""Enter what you want to update: 
                         1. Name
                         2. Gender
                         3. DOB
                         4. Aadhar Number
                         5. Address
                         6. Phone Number
                         --> """))
        if choice == 1:
            name = input("\nEnter the corrected name: ")
            cursor.execute(f"update bank_details set Name = '{name}' where account_number = {acc_no}")
            print("Updated successfully...")
        elif choice == 2:
            gender = input("\nEnter the corrected gender (M/F): ")
            cursor.execute(f"update bank_details set gender = '{gender}' where account_number = {acc_no}")
            print("Updated successfully...")
        elif choice == 3:
            dob = input("\nEnter the corrected DOB (YYYY-MM-DD): ")
            cursor.execute(f"update bank_details set DOB = '{dob}' where account_number = {acc_no}")
            print("Updated successfully...")
        elif choice == 4:
            ad_no = int(input("\nEnter the corrected aadhar number: "))
            cursor.execute(f"update bank_details set Aadhar_Number = {ad_no} where account_number = {acc_no}")
            print("Updated successfully...")
        elif choice == 5:
            address = input("\nEnter the corrected address: ")
            cursor.execute(f"update bank_details set Address = '{address}' where account_number = {acc_no}")
            print("Updated successfully...")
        elif choice == 6:
            phone = int(input("\nEnter the corrected phone number: "))
            cursor.execute(f"update bank_details set Phone_Number = {phone} where account_number = {acc_no}")
            print("Updated successfully...")

    more_options()


def close_account():
    acc_no = int(input("\nEnter the account number of the account to be closed: "))

    if check_for_acc(acc_no):
        confirmation = input("Are you sure you want to close this account? (y/n): ")

        if confirmation == 'y':
            cursor.execute(f"delete from bank_details where Account_Number = {acc_no}")
            print(f"\nAccount with account number {acc_no} has been closed.\n")

        elif confirmation == 'n':
            print("\nThe command for closing the account has been cancelled.")

        else:
            print("\nYou can only enter either y or n...\nTry again")
            close_account()
    else:
        print(f"\nAccount with account number {acc_no} does not exist.")

    more_options()



def ask_choices():
    print('''
    1. Add an account
    2. Check account Details of a Specific Account Holder
    3. Check Account Details of all Account Holders
    4. Deposit Money
    5. Withdraw Money
    6. Modify Account Details
    7. Close Account
    ''')
    try:
        choice = int(input("Please choose from the above options.\n(only a number)\n--> "))
    except ValueError:
        print("Please enter a valid number... Try Again!!\n")
        ask_choices()

    if choice == 1:
        add_account()
    elif choice == 2:
        view_user_profile()
    elif choice == 3:
        view_all()
    elif choice == 4:
        deposit_money()
    elif choice == 5:
        withdraw_money()
    elif choice == 6:
        update_account_info()
    elif choice == 7:
        close_account()
    else:
        print("You have to enter a number between 1 and 7")
        ask_choices()


ask_choices()
connector.close()