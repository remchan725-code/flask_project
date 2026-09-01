from abc import ABC,abstractmethod
class InsufficientBalanceError(Exception):
    pass
class InvalidVoucherError(Exception):
    pass
class MovieTicket(ABC):
    def __init__(self,seat_count,voucher_code = None):
        self.seat_count = seat_count
        self.voucher_code = voucher_code
    @abstractmethod
    def calculate_total(self):
        pass
    @staticmethod
    def validate_voucher(code):
        if code == "CINEMA10":
            return 0.9
        elif code == "CINEMA20":
            return 0.8
        elif not code:
            return 1
        else: 
            raise InvalidVoucherError("Voucher khong kha dung!")
    @classmethod
    def from_dict(cls,data):
        return cls (seat_count=data["seat_count"],voucher_code=data.get("voucher_code"))
    def __str__(self):
        return f"[{self.__class__.__name__} So luong: {self.seat_count}]"
class StandardTicket(MovieTicket):
    def calculate_total(self):
        discount = self.validate_voucher(self.voucher_code)
        tien_ve = self.seat_count * 80000
        tong_tien = tien_ve * discount
        return tong_tien
class VIP3DTicket(MovieTicket):
    def __init__(self,seat_count,voucher_code = None,glass_fee = 20000):
        super().__init__(seat_count,voucher_code)
        self.glass_fee = glass_fee
    def calculate_total(self):
        discount = self.validate_voucher(self.voucher_code)
        tien_ve = self.seat_count *(140000 + self.glass_fee)
        tong_tien = tien_ve * discount
        return tong_tien
class Customer():
    def __init__(self,name,balance):
        self.name = name
        self.__balance = balance
    @property
    def balance(self):
        return self.__balance
    def pay(self,amount):
        if self.__balance < amount:
            raise InsufficientBalanceError("So du khong du!")
        self.__balance -= amount
def xu_ly_danh_sach_dat_ve(customer, tickets):
    total_spent = 0
    succes_count = 0
    failed_count = 0
    for p in tickets:
        try:
            tong = p.calculate_total()
            customer.pay(tong)
            total_spent += tong
            succes_count += 1
        except (InsufficientBalanceError,InvalidVoucherError) as e:
            print("Loi!",e)
            failed_count += 1
    return {
        "total_spent" : total_spent,
        "success_count": succes_count,
        "failed_count" : failed_count
    }
# 1. Khởi tạo khách hàng có 500.000 VNĐ trong tài khoản
user = Customer(name="Minh", balance=500000)

# 2. Khởi tạo dữ liệu vé xem phim
ticket_data = [
    {
        "type": "standard",
        "seat_count": 2,
        "voucher_code": "CINEMA10",
    },  # Giá: (2 * 80k) * 0.9 = 144.000đ. Dư 356.000đ.
    {
        "type": "vip3d",
        "seat_count": 2,
        "voucher_code": "CINEMA20",
    },  # Giá: (2 * (140k + 20k)) * 0.8 = 256.000đ. Dư 100.000đ.
    {
        "type": "standard",
        "seat_count": 2,
        "voucher_code": None,
    },  # Giá: (2 * 80k) = 160.000đ > 100.000đ -> Lỗi InsufficientBalanceError!
]

tickets = [
    StandardTicket.from_dict(t)
    if t["type"] == "standard"
    else VIP3DTicket.from_dict(t)
    for t in ticket_data
]

# 3. Test __str__
for t in tickets:
    print(t)
# Kỳ vọng:
# StandardTicket - Số lượng: 2 ghế
# VIP3DTicket - Số lượng: 2 ghế
# StandardTicket - Số lượng: 2 ghế

# 4. Thanh toán danh sách đặt vé
report = xu_ly_danh_sach_dat_ve(user, tickets)
print("Báo cáo đặt vé:", report)
# Kỳ vọng: {'total_spent': 400000.0, 'success_count': 2, 'failed_count': 1}
print("Số dư tài khoản còn lại:", user.balance)
# Kỳ vọng: 100000.0