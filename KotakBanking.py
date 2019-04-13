import random
import sys
import mysql.connector

__BankName = "Kotak Mahindra Bank"


class Customer:

    def __init__(self, fname, lname,  bal, id):
        self.fname = fname
        self.lname = lname
        self.bal = bal
        self.id = id  

    @staticmethod
    def addUser():
        FName = str(input("Enter Your First Name "))
        LName = str(input("Enter Your Last Name "))
        Balance = input("Enter the Opening Balance ")
        Number = random.randint(1, 3)
        id = LName[0] + FName + str(Number)
        print("Your Account has been created..!! Your Id is:", id)

        return Customer(FName, LName, Balance, id)

    def deposit(self, amount, userId):
        #print(amount)
        TotalBalance = int(self.bal) + amount
        print("Current Balance is: ", self.bal)
        print("Deposit Balance is: ", amount)
        print("Total Balance is:", TotalBalance)
        ObjDbConnect = DbConnect()
        connecton = ObjDbConnect.dbConnect()
        cursor = connecton.cursor()
        cursor.execute(
            "update customer set bal = %s where id = %s", (TotalBalance, userId,))
        sql = "insert into custTransaction(uid, dir, balance, isTransfer, fromUserId) values (%s, %s, %s, %s, %s) "
        values = (userId, "Credit", amount, 0, userId)
        cursor.execute(sql, values)
        connecton.commit()
        return TotalBalance
        
    def withdraw(self, amount, userId):

        if amount > int(self.bal):
            print("Insufficent Balance.............!!")
        else:
            ObjDbConnect = DbConnect()
            connecton = ObjDbConnect.dbConnect()
            cursor = connecton.cursor()
            TotalDeductAmount = int(self.bal) - amount
            print("Total Balance is:", self.bal)
            cursor.execute(
                "update customer set bal = %s where id = %s", (TotalDeductAmount, userId,))
        sql = "insert into custTransaction(uid, dir, balance, isTransfer, fromUserId) values (%s, %s, %s, %s, %s) "
        values = (userId, "Debit", amount, 0, userId)
        cursor.execute(sql, values)
        connecton.commit()
    def checkBalance(self):
        print("Total Balance is :", self.bal)
    def transferBal(self, userData, trfData, amount):
            con = DbConnect()
            if trfData[3] > amount:
                print("Transfer Amount is {}".format(amount)) 
                trfTotal = trfData[3] + amount
                userTotal = userData[3] - amount
                cur = con.dbConnect()
                cursor = cur.cursor()
                cursor.execute("update customer set bal = %s where id = %s",(userTotal, userData[0],))
                print("User Detail has been updated")
                cursor.execute(
                    "update customer set bal = %s where id = %s", (trfTotal,trfData[0],))
                #print("Transfer User Detail has been updated")
                cursor.execute("insert into custTransaction(uid, dir, balance, isTransfer, fromUserId) values ( %s, %s, %s, %s, %s)", (userData[0], "Debit", amount, 1, trfData[0],))
                #print("Insert User transaction detail has been updated")
                cursor.execute("insert into custTransaction(uid, dir, balance, isTransfer, fromUserId) values ( %s, %s, %s, %s, %s)", (trfData[0], "Creadit", amount, 1, userData[0],))
                #print("Insert Transfer User transaction detail has been updated")
                cur.commit()
                print("Total Balance is :", userData[3])
            else:
                print("Insufficient Balance in your Account. Please try Again")
            return trfTotal, userTotal
    def GetTransaction(self, userData):
        con = DbConnect()
        cur =con.dbConnect()
        cursor = cur.cursor()
        data = cursor.execute("select * from custTransaction where uid = %s",(userData[0],))
        print("*" * 7)
        for i in cursor.fetchall():
            print("Transaction Type: {} and Transaction Balance :{}".format(i[1], i[2]))
class DbConnect:

     def dbConnect(self):
            mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="rapidkotak")        
            return mydb

while True:
    print("Please enter your choice")
    userInput = int(input("1. Create Account 2. Login 3. Exit "))
    if userInput == 1:
        cust = Customer.addUser()
        DbConnection = DbConnect()
        con = DbConnection.dbConnect()
        cur = con.cursor()
        sql = "insert into customer(id, fname, lname, bal) values (%s, %s, %s, %s)"
        values = (cust.id, cust.fname, cust.lname, cust.bal)
        cur.execute(sql, values)
        con.commit()
    elif userInput == 2:
        DbConnection = DbConnect()
        con = DbConnection.dbConnect()
        cur = con.cursor()
        userId = input("Please enter the userId ")
        value = cur.execute("select * from customer where id = %s", (userId,))
        data = cur.fetchone()
        if data != None:
                cust = Customer(data[1], data[2], data[3], data[0])
                print("You have successful Login into the account", userId)
                while True:
                    print("1 = Check Balance 2 = Transfer Money 3 = Account Information 4 = Deposit Balance 5 = Widthdraw  6 = Transaction  7 = Exit")
                    userInput = int(input("Please enter your choice "))
                    if userInput == 1:
                        cust.checkBalance()
                    elif userInput == 4:
                        depositAmount =int(input("Please enter the deposit amount "))
                        cust.deposit(depositAmount,userId)
                    elif userInput == 2:
                        usrTransferId = input("Please enter userId for which you want to transfer the amount:  ")
                        value = cur.execute("select * from customer where id = %s", (usrTransferId,))
                        trfData = cur.fetchone()
                        if trfData != None:
                            print("User Id = {} and Last Name = {} would you like to continue".format(trfData[0], trfData[2]))
                            userChoice = int(input("1. Continue 2 Exit "))
                            if userChoice == 1:
                                trfAmount = int(input("Please enter the transfer amount "))
                                cust.transferBal(data,trfData,trfAmount)
                            elif userChoice == 2:
                                sys.exit()
                        else:
                            print("Please enter the correct choice")
                    elif userInput == 5:
                        widthDrawAmount = int(input("Please enter the widthdraw amount "))
                        cust.withdraw(widthDrawAmount, userId)
                    elif userInput == 6:
                        cust.GetTransaction(data)
                    elif userInput == 7:
                        sys.exit()  
        else:
            print("Your account doesn't exist") 

    elif userInput == 3:
        print("Thanks For Banking with Us")
        sys.exit()
    else:
        print("Please enter the correct option")
    
            



