def tinh_tien_mon(price,quanity):
    if price <= 0 or quanity <= 0:
        raise ValueError("Giá tiền và số lượng phải lớn hơn 0!")
    return price * quanity
def loc_mon_theo_loai(order_items, *categories):
    return [
        item
        for item in order_items
        if not categories or item["category"] in categories
    ]
def tinh_tong_hoa_don(order_items):
    tong_tien = 0
    for item in order_items:
        try:
            tien = tinh_tien_mon(item["price"],item["quantity"])
            tong_tien += tien
        except (ValueError,TypeError,KeyError) as e:
            print("Co 1 mon bi loi!",e)
            continue
    return tong_tien
# Dữ liệu test
orders = [
    {"name": "Cà phê sữa", "category": "DRINK", "price": 25000, "quantity": 2},
    {"name": "Bánh Tiramisu", "category": "CAKE", "price": 35000, "quantity": 1},
    {
        "name": "Trà đào (Lỗi giá)",
        "category": "DRINK",
        "price": -10000,
        "quantity": 1,
    },  # Món lỗi
    {"name": "Croissant", "category": "CAKE", "price": 20000, "quantity": 3},
]

# 1. Test lọc món theo loại
drinks = loc_mon_theo_loai(orders, "DRINK")
print("Danh sách đồ uống:", [m["name"] for m in drinks])
# Kỳ vọng: ['Cà phê sữa', 'Trà đào (Lỗi giá)']

# 2. Test tính tổng hóa đơn
total_money = tinh_tong_hoa_don(orders)
print(f"Tổng tiền hóa đơn hợp lệ: {total_money:,.0f} VNĐ")
# Kỳ vọng: 25000*2 + 35000*1 + 20000*3 = 145,000 VNĐ (Bỏ qua món Trà đào lỗi)
    