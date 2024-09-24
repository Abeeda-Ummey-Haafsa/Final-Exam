class Bank:
    def __init__(self, bankName, totalBalance, totalLoan) -> None:
        self.bankName = bankName
        self.__totalBalance = totalBalance
        self.__totalLoan = totalLoan
        self.accountLists = []
        self.accountSerialNo = 24101
        self.loanStatus = False
        self.isBankrupt = False

    def getTotalBalance(self):
        return self.__totalBalance
    
    def getTotalLoan(self):
        return f'Current Loan in {self.bankName}: {self.__totalLoan}'
    
    def setTotalBalance(self, value, action):
        if action == "D":
            self.__totalBalance += value
        else:
            self.__totalBalance -= value

    def setTotalLoan(self, value):
        self.__totalLoan += value

    def settingAccountNo(self, user):
        user.accountNo = self.accountSerialNo
        self.accountSerialNo +=1
        self.accountLists.append(user)

    def showUsers(self):
        print("NAME\tBALANCE\tACCOUNT TYPE\tLOAN")
        for user in self.accountLists:
            print(f'{user.name}\t{user.balance}\t{user.accountType}\t\t{user.loanBalance}')

    def deletingAccount(self, actNo):
        trace = False
        for account in self.accountLists:
            if account.accountNo == actNo:
                self.accountLists.remove(account)
                print(f'Account No. {actNo} has been removed successfully.')
                trace = True
                break
        if trace == False:
            print(f'Account No. {actNo} does not exist.')

    def offLoan(self):
        if self.loanStatus == False:
            self.loanStatus=True
        
    def onLoan(self):
        if self.loanStatus == True:
            self.loanStatus=False

    def controlOfLoanFeature(self):
        if self.__totalBalance <= 50000:
            self.offLoan()
            return True
        else:
            self.onLoan()
            return False

    def checkIsBankrupt(self):
        if self.__totalLoan*2 >= self.__totalBalance:
            self.isBankrupt=True
            return True
        else:
            self.isBankrupt=False
            return False

class Person:
    def __init__(self, name, email, address) -> None:
        self.name = name
        self.email = email
        self.address = address

class User(Person):
    def __init__(self, name, email, address, accountType) -> None:
        super().__init__(name, email, address)
        self.accountType = accountType
        self.balance = 0
        self.loanBalance = 0
        self.accountNo = 0
        self.min_withdraw = 500
        self.max_withdraw = 50000
        self.loanTracker = 0
        self.transactionHistory = []

    def depositBalance(self, amount, bank):
        if amount > 100:
            self.balance += amount
            #self.loanBalance += amount
            print(f'{amount} has been deposited to account no. {self.accountNo}')
            self.transactionHistory.append(f'Deposited Amount: {amount}')
            bank.setTotalBalance(amount, "D")
            
        else:
            print("Insufficient Balance")

    def withdrawBalance(self, amount, bank):

        #elif self.balance == amount and self.balance >= bank.getTotalBalance()/2:
        if bank.checkIsBankrupt() == True:
            print("The Bank is Bankrupt")
            print("\t\t\t ! ! ! TRANSACTION FAILED ! ! ! ")
        elif amount>=self.min_withdraw and amount<=self.max_withdraw: 
            if amount>=self.balance:
                print("Withdrawal amount exceeded")
                print("\t\t\t ! ! ! TRANSACTION FAILED ! ! ! ")
            else: #
                self.balance -= amount
                print(f'Here is your {amount} taka')
                print(f'Remaining Balance: {self.balance}')
                self.transactionHistory.append(f'Withdrawed Amount: {amount}')
                bank.setTotalBalance(amount, "W")
            # else:
            #     print("Insufficient Balance In Your Account For Withdrawal")
            #     print("\t\t\t ! ! ! TRANSACTION FAILED ! ! ! ")
        
        else:
            print(f'Amount Must Between {self.min_withdraw} and {self.max_withdraw}')

    
    def checkAvailableBalance(self):
        print(f'Available Balance in Account No. {self.accountNo}: {self.balance}')

    def checkTransactionHistory(self):
        if len(self.transactionHistory) > 0:
            print("\t\t\t- - - TRANSACTION HISTORY - - - ")
            for transaction in self.transactionHistory:
                print(transaction)
        else:
            print("No Transaction Has Occurred Yet")

    def transferBalance(self, amount, receiverAccountNo, bank):
        if self.balance<amount:
            print("Insufficient balance for transfer.")
            return
        receiverAct = None
        for account in bank.accountLists:
            if account.accountNo == receiverAccountNo:
                receiverAct = account
                break
        if receiverAct is None:
            print("Account does not exist.")
            return
        self.balance -= amount
        receiverAct.balance += amount
        self.transactionHistory.append(f'Transferred {amount} to Account No. {receiverAccountNo}')
        receiverAct.transactionHistory.append(f'Received {amount} from Account No. {self.accountNo}')
        print(f'Transfer of {amount} taka to Account No. {receiverAccountNo} successful.')


    def takeLoan(self, amount, bank):
        if bank.controlOfLoanFeature() == False:
            if self.accountType == "Savings" and self.loanTracker >= 2:
                print("Limit Exceeded ! ! !")
            else:
                if bank.getTotalBalance()-amount>=50000 :
                    self.balance += amount
                    self.loanBalance += amount
                    print(f'Here is your loan {amount} taka')
                    print(f'Current Balance: {self.balance}')
                    self.transactionHistory.append(f'Loan Taken: {amount}')
                    bank.setTotalLoan(amount)
                    bank.setTotalBalance(amount, "W")
                    self.loanTracker+=1
                    bank.controlOfLoanFeature()
                else:
                    print("Loan feature is not available at the moment")
                    print("\t\t\t ! ! ! TRANSACTION FAILED ! ! ! ")
        else:
            # if bank.controlOfLoanFeature() == False:
            #     self.balance += amount
            #     print(f'Here is your loan {amount} taka')
            #     print(f'Current Balance: {self.balance}')
            #     self.transactionHistory.append(f'Loan Taken: {amount}')
            #     bank.setTotalLoan(amount)
            #     self.loanTracker+=1
            # else:
            #     print("Loan feature is not available at the moment")
            #     print("\t\t\t ! ! ! PROCCESS FAILED ! ! ! ")

            print("Loan Feature is turned off at the moment")
            print("\t\t\t ! ! ! TRANSACTION FAILED ! ! ! ")
class Admin(Person):
    def __init__(self, name, email, address) -> None:
        super().__init__(name, email, address)
    
    def creatingAccount(self, user, bank):
        bank.settingAccountNo(user)

    def deleteAccount(self, actNo, bank):
        bank.deletingAccount(actNo)

    def viewAllAvailableUsers(self, bank):
        bank.showUsers()

    def checkTheTotalAvailableBankBalance(self, bank):
        print(f'Current Available Balance: {bank.getTotalBalance()}')

    def checkTotalBankLoanAmount(self, bank):
        print(bank.getTotalLoan())

    def controlOfLoanFeatureAdmin(self, bank):
        if bank.controlOfLoanFeature() == True:
            print("Loan feature is turned off")
        else:
            print("Loan feature is turned on")


abcBank = Bank("ABC Bank", 100000, 40000)
admin = Admin("Alex", "alex@gmail.com", "Banani, Dhaka")
userRahim = User("Rahim", "rahim@gmail.com", "Uttara", "Savings")
userKarim = User("Karim", "karim@gmail.com", "Badda", "Current")
abcBank.settingAccountNo(userKarim)
abcBank.settingAccountNo(userRahim)




def userMain(user, bank):
    print("\t\t\t - - - Welcome To ",bank.bankName," - - -")
    while True:
        print("1. Deposit Balance")
        print("2. Withdraw Balance")
        print("3. Check Available Balance")
        print("4. View Transaction History")
        print("5. Transfer Balance")
        print("6. Take Loan")
        print("7. Logout")
        choose = int(input("Select an option: "))

        if choose == 1:
            amount = int(input("Enter the amount to deposit: "))
            user.depositBalance(amount, bank)

        elif choose == 2: 
            amount = int(input("Enter the amount to withdraw: "))
            user.withdrawBalance(amount, bank)

        elif choose == 3: 
            user.checkAvailableBalance()

        elif choose == 4: 
            user.checkTransactionHistory()

        elif choose == 5: 
            amount =int(input("Enter the amount to transfer: "))
            revAct = int(input("Enter the receiver's account no: "))
            user.transferBalance(amount, revAct, bank)

        elif choose == 6: 
            amount =int(input("Enter the amount of loan: "))
            user.takeLoan(amount, bank)
        else :
            print("Logged out successfully !!!")
            break

def adminMain(admin, bank):
    print("\t\t\t - - - Welcome To ",bank.bankName," - - -")
    while True:
        print()
        print("1. Create an account")
        print("2. Delete User's Account")
        print("3. See All User Account")
        print("4. Check The Total Available of the Bank")
        print("5. Check the total loan amount")
        print("6. On/Off the loan feature of the bank")
        print("7. Logout")
        j = int(input("Select an option: "))

        if j == 1:
            name = input("1. Enter Your Name: ")
            email = input("2. Enter Your Email: ")
            address = input("3. Enter Your Address: ")
            actType =input("Enter account type: ")
            newUser = User(name, email, address, actType)
            admin.creatingAccount(newUser, bank)

        elif j == 2:
            delAct =int(input("Enter the deleting account no: "))
            admin.deleteAccount(delAct, bank)

        elif j == 3:
            admin.viewAllAvailableUsers(bank)

        elif j == 4:
            admin.checkTheTotalAvailableBankBalance(bank)

        elif j == 5:
            admin.checkTotalBankLoanAmount(bank)

        elif j == 6:
            admin.controlOfLoanFeatureAdmin(bank)
        else:
            print("Logged out successfully !!!")
            break



while True:
    print("Select an option - ")
    print("1. Create an account")
    print("2. Login")
    print("3. EXIT")
    op = int(input("Enter Option: "))
    if op == 1:
        name = input("1. Enter Your Name: ")
        email = input("2. Enter Your Email: ")
        address = input("3. Enter Your Address: ")
        print("What type of account you want to open?")
        print("1. Savings Account")
        print("2. Current Account")
        # Here the main difference between accounts is in the limitation of loan
        # Savings account user can only take loan 2 times
        # For Current account, there's no limitation
        actType = int(input("What type of account you want to open? "))
        if actType == 1:
            user = User(name, email, address, "Savings")
        else:
            user = User(name, email, address, "Current")
        admin.creatingAccount(user, abcBank)
        userMain(user, abcBank)

    elif op == 2:
        print("Are you an -")
        print("1. User")
        print("2. Admin")
        i = int(input("Select an option: "))
        if i == 1:
            checker=False
            actNo =int(input("Enter Account No: "))
            for account in abcBank.accountLists:
                if account.accountNo==actNo:
                    checker=True
                    userMain(account, abcBank)
                    break
            if checker==False:
                print(actNo, "does not exist")
        else:
            adminMain(admin, abcBank)
    
    else: 
        break
