class OutOfStockError(Exception):
    pass
class InvalidVoucherError(Exception):
    pass
def thanh_toan_don_hang(product,quantity,distance_km,voucher = None):
    tien_hang = product["price"] * quantity
    ship_fee = 15000
    if quantity <= 0 or quantity > product["stock"]:
        raise OutOfStockError(f"So luong san pham {product["name"]} trong kho khong du")
    if distance_km > 6 :
        ship_fee = 15000 + 5000 * (distance_km - 5)
    discount = 1
    if voucher :
        if voucher == "FREESHIP":
            if tien_hang >= 300000:
                ship_fee = 0
            else:
                raise InvalidVoucherError(f"Don hang {product["product_id"]} khong du dieu kien de duoc free ship")
        elif voucher == "SALE10":
            discount = 0.9
        else:
            raise InvalidVoucherError("Ma voucher khong ton tai")
    product["stock"] -= quantity
    return (tien_hang * discount) + ship_fee
def loc_san_pham(product_list, *categories, **filters):
    min_price = filters.get("min_price",0)
    max_price = filters.get("max_price",float("inf"))
    in_stock_only = filters.get("in_stock_only",False)
    return [
        p
        for p in product_list
        if not categories or p["category"] in categories
        and min_price <= p["price"] <= max_price
        and (not in_stock_only or p["stock"] > 0)
    ]
def xu_ly_gio_hang(order_list):
    total_revenue = 0
    success_count = 0
    failed_count = 0
    for p in order_list:
        try:
            tong = thanh_toan_don_hang(p["product"],p["quantity"],p["distance_km"],p.get("voucher"))
            total_revenue += tong
            success_count += 1
        except(OutOfStockError,InvalidVoucherError) as e:
            print("Loi!",e)
            failed_count += 1
    return {
        "total_revenue" : total_revenue,
        "success_count" : success_count,
        "failed_count" : failed_count
    }
products = [
    {
        "product_id": "P01",
        "name": "Áo Thun",
        "category": "Thời trang",
        "price": 150000,
        "stock": 5,
    },
    {
        "product_id": "P02",
        "name": "Tai Nghe",
        "category": "Điện tử",
        "price": 500000,
        "stock": 2,
    },
    {
        "product_id": "P03",
        "name": "Chuột Máy Tính",
        "category": "Điện tử",
        "price": 200000,
        "stock": 0,
    },  # Hết hàng
]

orders = [
    {
        "product": products[0],
        "quantity": 3,
        "distance_km": 7,
        "voucher": "FREESHIP",
    },
    # Tiền 450k >= 300k -> Được FREESHIP. Ship_fee = 0. Tổng = 450k. P01 còn 2 cái.
    {
        "product": products[0],
        "quantity": 3,
        "distance_km": 2,
        "voucher": None,
    },
    # Lỗi: P01 chỉ còn 2 cái mà đặt 3 cái -> OutOfStockError
    {
        "product": products[1],
        "quantity": 1,
        "distance_km": 3,
        "voucher": "FREESHIP",
    },
    # Tiền 500k >= 300k -> Được FREESHIP. Ship_fee = 0. Tổng = 500k. P02 còn 1 cái.
    {
        "product": products[0],
        "quantity": 1,
        "distance_km": 4,
        "voucher": "FREESHIP",
    },
    # Lỗi: Tiền 150k < 300k mà đòi xài FREESHIP -> InvalidVoucherError
]

# 1. Test lọc sản phẩm Điện tử còn hàng
available_tech = loc_san_pham(products, "Điện tử", in_stock_only=True)
print("Sản phẩm Điện tử còn hàng:", [p["name"] for p in available_tech])
# Kỳ vọng: ['Tai Nghe']

# 2. Test xử lý giỏ hàng
report = xu_ly_gio_hang(orders)
print("Báo cáo giỏ hàng:", report)
# Kỳ vọng: {'total_revenue': 950000.0, 'success_count': 2, 'failed_count': 2}
    