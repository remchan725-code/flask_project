from abc import ABC, abstractmethod
class InsufficientBalanceError(Exception):
    pass
class InvalidVoucher(Exception):
    pass
class FoodOrder(ABC):
    def __init__(self,quantity,voucher_code = None):
        self.quantity = quantity
        self.voucher_code = voucher_code
    @abstractmethod
    def calculate_total(self):
        pass
    @staticmethod
    def validate_voucher(code):
        if code == "FOOD10":
            return 0.9
        elif code == "FOOD20":
            return 0.8
        else:
            raise InvalidVoucher("Voucher khong hop le!")
    @classmethod
    def from_dict(cls,data):
        return cls (quantity=data["quantity"],voucher_code=data.get("voucher_code"))
    def __str__(self):
        return f"[{self.__class__.__name__}] - Số lượng : {self.quantity}"
class SingleFood(FoodOrder):
    def calculate_total(self):
        discount = self.validate_voucher(self.voucher_code) 
        base_price = self.quantity * 40000
        ship_fee = 15000
        total = (base_price + ship_fee) * discount
        return total
class ComboFood(FoodOrder):
    def __init__(self,quantity,voucher_code = None,side_drink_fee = 10000):
        super().__init__(quantity,voucher_code)
        self.side_drink_fee = side_drink_fee
    def calculate_total(self):
        discount = self.validate_voucher(self.voucher_code) 
        base_price = self.quantity * (70000 + self.side_drink_fee)
        ship_fee = 15000
        total = (base_price + ship_fee) * discount
        return total
class Customer():
    def __init__(self,name = "",balance = 0):
        self.name = name
        self.__balance = balance
    @property
    def balance(self):
        return self.__balance
    def pay(self,amount):
        if self.__balance < amount:
            raise InsufficientBalanceError("Số dư không đủ!")
        self.__balance -= amount
def xu_ly_danh_sach_don_hang(customer, orders):
    total_spent = 0
    succes_count = 0
    failed_count = 0
    for p in orders:
        try:
            total = p.calculate_total()
            customer.pay(total)
            total_spent += total
            succes_count += 1
        except(InsufficientBalanceError,InvalidVoucher) as e:
            print("Lỗi!",e)
            failed_count += 1
    return {
        "total_spent" : total_spent,
        "success_count": succes_count,
        "failed_count" : failed_count
    }
# 1. Khởi tạo khách hàng có 200.000 VNĐ trong ví
user = Customer(name="Linh", balance=200000)

# 2. Khởi tạo dữ liệu các đơn đặt đồ ăn
order_data = [
    {
        "type": "single",
        "quantity": 2,
        "voucher_code": "FOOD10",
    },  # Giá: (2*40k + 15k) * 0.9 = 85.500đ. Dư 114.500đ.
    {
        "type": "combo",
        "quantity": 1,
        "voucher_code": "FOOD20",
    },  # Giá: (1*(70k + 10k) + 15k) * 0.8 = 76.000đ. Dư 38.500đ.
    {
        "type": "single",
        "quantity": 3,
        "voucher_code": None,
    },  # Giá: (3*40k + 15k) = 135.000đ > 38.500đ -> Lỗi InsufficientBalanceError!
]

orders = [
    SingleFood.from_dict(o) if o["type"] == "single" else ComboFood.from_dict(o)
    for o in order_data
]

# 3. Test __str__
for o in orders:
    print(o)
# Kỳ vọng:
# SingleFood - Số lượng: 2 phần
# ComboFood - Số lượng: 1 phần
# SingleFood - Số lượng: 3 phần

# 4. Thanh toán danh sách đơn hàng
report = xu_ly_danh_sach_don_hang(user, orders)
print("Báo cáo đơn hàng:", report)
# Kỳ vọng: {'total_spent': 161500.0, 'success_count': 2, 'failed_count': 1}
print("Số dư ví ShopeePay còn lại:", user.balance)
# Kỳ vọng: 38500.0


        