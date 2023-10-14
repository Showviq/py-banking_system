class BankAccount:
    def __init__(self, name, email, pin, address, account_type, id):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.account_number = self.generate_account_number(id)
        self.pin = pin
        self.balance = 0
        self.loan_limit = 2
        self.loan_taken = 0
        self.transaction_history = []

    def generate_account_number(self, id):
        return f'{id:06d}'

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited ${amount}")
            return f"${amount} deposited successfully."
        else:
            return "Invalid deposit amount."

    def withdraw(self, amount):
        if amount > 0:
            if amount <= self.balance:

                self.balance -= amount
                self.transaction_history.append(f"Withdrew ${amount}")
                return f"${amount} withdrawn successfully."
            else:
                return "Withdrawal amount exceeded."
        else:
            return "Invalid withdrawal amount."

    def check_balance(self):
        return f"Available balance: ${self.balance}"

    def check_transaction_history(self):
        return self.transaction_history

    def take_loan(self, amount):
        if self.loan_limit > 0:
            if amount > 0:
                self.loan_limit -= 1
                self.loan_taken += amount
                self.balance += amount
                self.transaction_history.append(f"Loan of ${amount} taken.")
                return f"Loan of ${amount} taken successfully."
            else:
                return "Invalid loan amount."
        else:
            return "You have reached your maximum loan limit."

    def transfer(self, other_account, amount):
        if amount > 0:
            if amount <= self.balance:
                self.balance -= amount
                other_account.balance += amount
                self.transaction_history.append(f"Transferred ${amount} to Account {other_account.account_number}")
                other_account.transaction_history.append(f"Received ${amount} from Account {self.account_number}")
                return f"${amount} transferred successfully to Account {other_account.account_number}."
            else:
                return "Insufficient funds for the transfer."
        else:
            return "Invalid transfer amount."


class Admin:
    def __init__(self):
        self.account_created = 0
        self.user_accounts = []




    def create_account(self, name, email, pin, address, account_type):
        account = BankAccount(name, email, pin, address, account_type, self.account_created)
        self.user_accounts.append(account)
        self.account_created += 1
        return account

    def delete_account(self, account):
        if account in self.user_accounts:
            self.user_accounts.remove(account)
            return "Account deleted successfully."
        else:
            return "Account not found."

    def list_accounts(self):
        return [account.account_number for account in self.user_accounts]

    def total_bank_balance(self):
        total_balance = sum(account.balance for account in self.user_accounts)
        return f"Total Bank Balance: ${total_balance}"

    def total_loan_amount(self):
        total_loan = sum(account.loan_taken for account in self.user_accounts)
        return f"Total Loan Amount: ${total_loan}"

    def toggle_loan_feature(self, enabled):
        BankAccount.loan_limit = 2 if enabled else 0
        return f"Loan feature {'enabled' if enabled else 'disabled'}."

    def withdraw_bankrupt(self, amount):
        check_balance = sum(account.balance for account in self.user_accounts) - sum(account.loan_taken for account in self.user_accounts) - amount

        return True if check_balance < 0 else False


def main():
    admin = Admin()

    while True:
        print("\nWelcome to the Banking System")
        print("1. User Login")
        print("2. Admin Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nUser Login")
            account_number = input("Enter your account number: ")
            account = None
            for user_account in admin.user_accounts:
                if user_account.account_number == account_number:
                    account = user_account

            if account:
                pin = input("Enter your PIN: ")
                if pin != account.pin:
                  print("WRONG PIN")
                  continue
                while True:
                    print("\nUser Menu")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Transaction History")
                    print("5. Take Loan")
                    print("6. Transfer Money")
                    print("7. Logout")
                    user_choice = input("Enter your choice: ")
                    if user_choice == "1":
                        amount = float(input("Enter the amount to deposit: "))
                        print(account.deposit(amount))
                    elif user_choice == "2":
                        amount = float(input("Enter the amount to withdraw: "))
                        if admin.withdraw_bankrupt(amount):
                          print("The bank is bankrupt.")
                        else:
                          print(account.withdraw(amount))
                    elif user_choice == "3":
                        print(account.check_balance())
                    elif user_choice == "4":
                        print(account.check_transaction_history())
                    elif user_choice == "5":
                        amount = float(input("Enter the loan amount: "))
                        if admin.withdraw_bankrupt(amount):
                          print("The bank is bankrupt.")
                        else:
                          print(account.take_loan(amount))
                    elif user_choice == "6":
                        other_account_number = input("Enter the account number to transfer to: ")
                        other_account = None
                        for user_account in admin.user_accounts:
                            if user_account.account_number == other_account_number:
                                other_account = user_account
                                break
                        if other_account:
                            amount = float(input("Enter the amount to transfer: "))
                            print(account.transfer(other_account, amount))
                        else:
                            print("Account does not exist.")
                    elif user_choice == "7":
                        break
            else:
                print("Account not found.")

        elif choice == "2":
            print("\nAdmin Login")
            admin_password = input("Enter the admin password: ")
            if admin_password == "Admin123":
                while True:
                    print("\nAdmin Menu")
                    print("1. Create Account")
                    print("2. Delete Account")
                    print("3. List Accounts")
                    print("4. Total Bank Balance")
                    print("5. Total Loan Amount")
                    print("6. Toggle Loan Feature")
                    print("7. Logout")
                    admin_choice = input("Enter your choice: ")
                    if admin_choice == "1":
                        name = input("Enter user's name: ")
                        email = input("Enter user's email: ")
                        pin = input("Enter user's PIN: ")
                        address = input("Enter user's address: ")
                        account_type = input("Enter account type (Savings/Current): ")
                        account = admin.create_account(name, email, pin, address, account_type)
                        print(f"Account created successfully. Account Number: {account.account_number}")
                    elif admin_choice == "2":
                        account_number = input("Enter the account number to delete: ")
                        account = None
                        for user_account in admin.user_accounts:
                            if user_account.account_number == account_number:
                                account = user_account
                                break
                        if account:
                            print(admin.delete_account(account))
                        else:
                            print("Account not found.")
                    elif admin_choice == "3":
                        print("List of User Accounts:")
                        accounts = admin.list_accounts()
                        for account_number in accounts:
                            print(account_number)
                    elif admin_choice == "4":
                        print(admin.total_bank_balance())
                    elif admin_choice == "5":
                        print(admin.total_loan_amount())
                    elif admin_choice == "6":
                        enable_loan = input("Enable or disable loan feature (Y/N): ")
                        enabled = enable_loan.lower() == "Y"
                        print(admin.toggle_loan_feature(enabled))
                    elif admin_choice == "7":
                        break
            else:
                print("Invalid admin password.")

        elif choice == "3":
            print("Exiting the Banking System. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()