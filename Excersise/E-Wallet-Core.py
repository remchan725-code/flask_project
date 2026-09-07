class InsufficientBalanceError(Exception): #tong hop cac loi 
    pass
class Wallet:
    def __init__(self,wallet_id,inittial_balance = 0):
        self.wallet_id = wallet_id
        self.__balance = inittial_balance #__balance la private, khong the doi tu ben ngoai
        self.history = [] # list de luu lich su giao dich
    @property
    def balance(self):
        return self.__balance
    def deposit(self,amount):
        if amount <= 0:
            raise ValueError("Deposit money have to greater than 0")
        self.__balance += amount
        self.history.append(("Deposit",amount))
    def withdraw(self,amount):
        if amount <= 0:
            raise ValueError("Withdraw money have to greater than 0")
        if amount > self.__balance: #luong rut ra > so du tai khoan => goi ve InsufficientBalanceError
            raise InsufficientBalanceError("Not have enough money")
        self.__balance -= amount
        self.history.append(("Withdraw",amount))
    def get_history(self,*action_types):
        history_call = 0
        return [tx for tx in self.history if tx[history_call] in action_types]
    def __str__(self):
        return f"Ví {self.wallet_id} | Số dư : {self.balance} | Số lần giao dịch : {len(self.history)} "

wallet1 = Wallet("W001", 500)
wallet1.deposit(1000)
wallet1.deposit(1000)
wallet1.deposit(1000)
wallet1.withdraw(2000)
print(wallet1.wallet_id)
print(wallet1.balance)
print(wallet1.get_history("Deposit","Withdraw"))
print(wallet1)
