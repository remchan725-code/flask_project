class Coupon:
    def caLculate_discount(self,total_amount):
        raise NotImplementedError #chua duoc thuc hien o lop Cha

class Percent_Coupon(Coupon):
    def __init__(self,percent,max_discount):
        self.percent = percent
        self.max_discount = max_discount
    def calculate_discount(self,total_amount):
        discount = total_amount * self.percent/100 #discount = 300 * 10/100 = 30 if 30 < max_discount => ap dung
        return min(discount,self.max_discount) #neu discount > max_discount thi ap dung max_discount

class Fixed_Coupon(Coupon):#Giam gia truc tiep
    def __init__(self,amount):
        self.amount = amount
    def calculate_discount (self,total_amount):
        return min(self.amount,total_amount)

class Order:
    def __init__(self):
        self.items = []
        self.coupon = None

    def add_item(self,name,price,quanity):
        if price <= 0:
            raise ValueError ("Price must be greater than 0")
        if quanity <= 0:
            raise ValueError("Quanity must be greater than 0")
        self.items.append({
            "Name" : name,
            "Price": price,
            "Quanity" : quanity 
        })
    @property
    def subtotal(self):# tinh gia goc
            return sum (item["Price"] * item["Quanity"] for item in self.items)

    def apply_coupon(self,coupon):
            self.coupon = coupon

    @property
    def final_total(self):
        if self.coupon:
            discount = self.coupon.calculate_discount(self.subtotal)
        else:
            discount = 0
        return max(0,self.subtotal - discount)
            
    def __str__(self):
        return (
            f"Don hang bao gom {len(self)} mon",
            f"Tien goc : {self.subtotal} VND ",
            f"Thuc tra : {self.final_total} VND"
            )
    def __len__(self):
        return sum (item["Quanity"] for item in self.items)
order1 = Order()
order1.add_item("Quần Jean",300,2)
order1.add_item("Áo phông",200,3)
print(order1.items)

coupon = Percent_Coupon(10,100)
print("Subtotal:", order1.subtotal)
print("Discount:", coupon.calculate_discount(order1.subtotal))
order1.apply_coupon(coupon)
print("Final total:", order1.final_total)



