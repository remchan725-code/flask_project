class OutOfStockError(Exception):
    pass
class WeightLimitExceededError(Exception):
    pass
class InvalidCouponError(Exception):
    pass
def tinh_tong_don_hang(product, quantity, coupon=None, **options):
    if quantity <= 0 or quantity > product["stock"]:
        raise OutOfStockError("Không đủ hàng trong kho!")

    weight = quantity * product["weight_kg"]
    if weight > 20:
        raise WeightLimitExceededError("Hàng quá số cân nặng cho phép!")

    # 1. Tiền hàng & Giảm giá tiền hàng
    tien_hang = quantity * product["price"]
    tien_hang_sau_giam = tien_hang

    if coupon == "SALE10":
        tien_hang_sau_giam = tien_hang * 0.9
    elif coupon and coupon != "FREESHIP":
        raise InvalidCouponError("Mã giảm giá không tồn tại!")

    # 2. Phí ship (Gốc 30k + Express 25k + Quá cân 10k/kg)
    ship_fee = 30000
    if options.get("express_shipping"):
        ship_fee += 25000
    if weight > 5:
        ship_fee += (weight - 5) * 10000

    # Giảm ship nếu có FREESHIP
    if coupon == "FREESHIP":
        ship_fee = max(0, ship_fee - 30000)

    # 3. VAT chỉ tính trên tiền hàng sau giảm
    vat_rate = options.get("vat_rate", 0.1)
    tien_vat = tien_hang_sau_giam * vat_rate

    # 4. Trừ kho và trả về tổng
    product["stock"] -= quantity
    return tien_hang_sau_giam + tien_vat + ship_fee
    
def loc_san_pham(product_list, *categories, **filters):
    max_price = filters.get("max_price",float("inf"))
    in_stock_only = filters.get("in_stock_only",False)
    return [
        p
        for p in product_list
        if (not categories or p["category"] in categories)
        and (not in_stock_only or p["stock"] > 0)
        and p["price"] <= max_price
    ]
def xu_ly_danh_sach_don_hang(order_requests):
    total_revenue = 0
    success_count = 0
    failed_count = 0
    total_items_sold = 0
    for p in order_requests:
        try:
            tong = tinh_tong_don_hang(p["product"],p["quantity"],p.get("coupon"))
            total_revenue += tong
            success_count += 1
            total_items_sold += p["quantity"]
        except (InvalidCouponError,WeightLimitExceededError,OutOfStockError) as e:
            print("Lỗi!",e)
            failed_count += 1
    return {
        "total_revenue": total_revenue,
        "success_count": success_count,
        "failed_count": failed_count,
        "total_items_sold" : total_items_sold
    }
products = [
    {
        "sku": "P01",
        "name": "Áo Sơ Mi",
        "category": "Thời trang",
        "stock": 10,
        "price": 200000,
        "weight_kg": 0.3,
    },
    {
        "sku": "P02",
        "name": "Nồi Cơm Điện",
        "category": "Gia dụng",
        "stock": 2,
        "price": 1000000,
        "weight_kg": 6.0,
    },
    {
        "sku": "P03",
        "name": "Tạ Đơn 25kg",
        "category": "Thể thao",
        "stock": 5,
        "price": 500000,
        "weight_kg": 25.0,
    },
]

order_requests = [
    {
        "product": products[0],
        "quantity": 2,
        "coupon": "SALE10",
        "express_shipping": True,
        "vat_rate": 0.1,
    },
    # Tiền hàng: 400k -10% = 360k. VAT 10% = 36k. Ship: 30k + 25k (express) = 55k. Tổng = 451,000 VNĐ. P01 còn 8.
    {
        "product": products[1],
        "quantity": 1,
        "coupon": "FREESHIP",
        "vat_rate": 0.08,
    },
    # Nặng 6kg (>5kg thừa 1kg -> +10k ship). Ship: 30k + 10k = 40k. FREESHIP giảm 30k -> ship còn 10k.
    # Tiền hàng: 1tr. VAT 8% = 80k. Tổng = 1,090,000 VNĐ. P02 còn 1.
    {
        "product": products[1],
        "quantity": 5,
        "coupon": None,
    },
    # Lỗi: Mua 5 cái > stock 1 -> OutOfStockError
    {
        "product": products[2],
        "quantity": 1,
        "coupon": None,
    },
    # Lỗi: Nặng 25kg > 20kg -> WeightLimitExceededError
]

# 1. Test xử lý danh sách
report = xu_ly_danh_sach_don_hang(order_requests)
print("Báo cáo doanh thu checkout:", report)
# Kỳ vọng: {'total_revenue': 1541000.0, 'total_items_sold': 3, 'success_count': 2, 'failed_count': 2}

# 2. Test lọc sản phẩm
available_prods = loc_san_pham(
    products, "Thời trang", "Gia dụng", in_stock_only=True, max_price=500000
)
print("Sản phẩm khả dụng:", [p["name"] for p in available_prods])
# Kỳ vọng: ['Áo Sơ Mi']