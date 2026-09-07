class OutOfStockError(Exception):
    pass
class InvalidVoucher(Exception):
    pass
def xu_ly_don_hang(product,quantity,voucher = None):
    if quantity <= 0 or quantity > product["stock"]:
        raise OutOfStockError("Kho khong du hang!")
    discount = 1
    if voucher == "SALE10":
        discount = 0.9
    elif voucher == "SALE20":
        discount = 0.8
    else:
        raise InvalidVoucher("Ma giam gia khong hop le")
    return product["price"] * quantity * discount
def loc_san_pham(product_list, *categories, **filters):
    min_price = filters.get("min_price",0)
    max_price = filters.get("max_price",float("inf"))
    return [
        p
        for p in product_list
        if (not categories or p["category"] in categories)#co/khong chon danh muc catogories
        and min_price <= p["price"] <= max_price #loc gia nguoi dung chon
    ]
def thong_ke_don_hang(order_list):
    total_revenue = 0
    failed_count = 0
    for order in order_list:
        try:
            price = xu_ly_don_hang(order["product"],order["quantity"],order.get("voucher"))
            total_revenue += price
        except (OutOfStockError,InvalidVoucher) as e:
            failed_count += 1
    return {"Total revenue ": total_revenue, "Failed_count":failed_count}
# Danh sách sản phẩm trong kho
products = [
    {
        "id": "P01",
        "name": "Áo thun",
        "category": "THOI_TRANG",
        "price": 100000,
        "stock": 10,
    },
    {
        "id": "P02",
        "name": "Tai nghe",
        "category": "DIEN_TU",
        "price": 500000,
        "stock": 2,
    },
    {
        "id": "P03",
        "name": "Sạc dự phòng",
        "category": "DIEN_TU",
        "price": 300000,
        "stock": 5,
    },
]

# Danh sách đơn hàng cần xử lý
orders = [
    {
        "product": products[0],
        "quantity": 2,
        "voucher": "SALE10",
    },  # Áo thun (200k giảm 10%) -> 180k
    {
        "product": products[1],
        "quantity": 5,
        "voucher": None,
    },  # Lỗi: Mua 5 cái mà kho chỉ có 2 (OutOfStockError)
    {
        "product": products[2],
        "quantity": 1,
        "voucher": "HAPPY100",
    },  # Lỗi: Voucher không tồn tại (InvalidVoucherError)
    {
        "product": products[2],
        "quantity": 2,
        "voucher": "SALE20",
    },  # Sạc (600k giảm 20%) -> 480k
]

# 1. Test lọc sản phẩm linh hoạt với *args và **kwargs
filtered_p = loc_san_pham(
    products, "DIEN_TU", min_price=200000, max_price=400000
)
print("Sản phẩm điện tử giá từ 200k - 400k:", [p["name"] for p in filtered_p])
# Kỳ vọng: ['Sạc dự phòng']

# 2. Test thống kê đơn hàng
report = thong_ke_don_hang(orders)
print("Báo cáo đơn hàng:", report)
# Kỳ vọng: {'total_revenue': 660000.0, 'failed_count': 2}