class OutOfStockError(Exception):
    pass
class Product:
    @property
    def stock(self):
        return self.__stock
    def __init__(self,product_id,name,price,stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.__stock = stock
    def import_stock(self,amount):
        if amount <= 0:
            raise ValueError("Amount must greater than 0")
        self.__stock += amount
        return self.__stock
    def export_stock(self,amount):
        if amount <= 0:
            raise ValueError("It can not be 0")
        if amount > self.stock :
            raise OutOfStockError ("Not enough product in WareHouse")
        self.stock -= amount
        return self.stock
    def __str__(self):
        return f"Mã SP: {self.product_id} |Tên SP: {self.name} |Giá: {self.price} |Tồn kho: {self.stock}"
class WareHouse:
    def __init__(self):
        self.products = []
    def add_product(self,name,price,stock,product_id):
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        if stock < 0:
            raise ValueError("Stock must be greater than or equal to 0")
        for product in self.products:
            if product.product_id == product_id:
                raise ValueError (f"Product ID already exits!")
        new_product = Product(product_id,name,price,stock)
        self.products.append(new_product)
    def get_low_stock_product(self,threshold):
        
        return[p for p in self.products if p.stock <= threshold]
    def auto_import(self):
        low_stock = self.get_low_stock_product(5)
        for sp in low_stock:
            sp.import_stock(20)
    def __len__(self):
        return len(self.products)
wh = WareHouse()
wh.add_product("Áo phông", 100, 3, "P001")
wh.add_product("Quần Jean", 200, 20, "P002")
wh.add_product("Mũ lưỡi trai", 50, 4, "P003")
for p in wh.products:
    print(p)
print("Tổng số sản phẩm:", len(wh))

wh.auto_import()
for p in wh.products:
    print(p)