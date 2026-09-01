from abc import ABC, abstractmethod
class InsufficientBalanceError(Exception):
    pass
class InvalidVoucher(Exception):
    pass
class Ride(ABC):
    def __init__(self,distance,promo_code = None):
        self.distance = distance
        self.promo_code = promo_code
    @abstractmethod
    def calculate_fare(self):
        pass
    @staticmethod
    def validate_promo(code):
        if code == "SAVE10":
            return 0.9  
        elif code == "SAVE20":
            return 0.8  
        else:
            raise InvalidVoucher("Voucher khong hop le!")
    @classmethod
    def from_dict(cls,data):
        return cls ( distance=data["distance"],promo_code=data.get("promo_code"))
    def __str__(self):
        return f"[{self.__class__.__name__}] - Quãng đường: {self.distance} km"
class StandardRide(Ride):
    def calculate_fare(self):
        discount = self.validate_promo(self.promo_code)
        base_fare = self.distance * 10000 + 15000
        return base_fare * discount
class VIPRide(Ride):
    def __init__(self,distance,promo_code = None, wifi_fee = 20000):
        super().__init__(distance,promo_code)
        self.wifi_fee = wifi_fee
    def calculate_fare(self):
        discount = self.validate_promo(self.promo_code)
        base_fare = self.distance * 18000 + 30000 + self.wifi_fee
        return base_fare * discount
class Customer:
    def __init__(self,name, balance = 0):
        self.name = name
        self.__balance = balance
    @property
    def balance(self):
        return self.__balance
    def pay(self,amount):
        if self.__balance < amount:
            raise InsufficientBalanceError("Số dư không đủ để thanh toán!")
        else:
            self.__balance -= amount
def xu_ly_danh_sach_chuyen_xe(customer, rides):
    total_spent = 0
    success_count = 0
    failed_count = 0
    for p in rides:
        try:
            fare = p.calculate_fare()
            customer.pay(fare)
            total_spent += fare
            success_count += 1
        except (InsufficientBalanceError,InvalidVoucher) as e:
            print("LỖI! ",e)
            failed_count += 1
    return {
        "total_spent": total_spent,
        "success_count": success_count,
        "failed_count": failed_count
    }
# 1. Khởi tạo khách hàng có 100.000 VNĐ
user = Customer(name="Hoàng", balance=100000)

# 2. Khởi tạo danh sách chuyến xe từ dict bằng @classmethod
ride_data = [
    {
        "type": "standard",
        "distance": 3,
        "promo_code": "SAVE10",
    },  # Giá: (3*10k + 15k)*0.9 = 40.500đ. Còn dư 59.500đ.
    {
        "type": "vip",
        "distance": 2,
        "promo_code": None,
    },  # Giá: (2*18k + 30k + 20k)*1.0 = 86.000đ > 59.500đ -> Lỗi InsufficientBalanceError!
]

rides = [
    StandardRide.from_dict(r) if r["type"] == "standard" else VIPRide.from_dict(r)
    for r in ride_data
]

# 3. Thử nghiệm Dunder Method __str__
for r in rides:
    print(r)
# Kỳ vọng in ra:
# StandardRide - Quãng đường: 3 km
# VIPRide - Quãng đường: 2 km

# 4. Xử lý thanh toán hàng loạt
report = xu_ly_danh_sach_chuyen_xe(user, rides)
print("Báo cáo chuyến xe:", report)
# Kỳ vọng: {'total_spent': 40500.0, 'success_count': 1, 'failed_count': 1}
print("Số dư còn lại của khách:", user.balance)
# Kỳ vọng: 59500.0