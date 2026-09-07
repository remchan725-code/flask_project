def tinh_phi_giao_hang(distance,is_rush_hour):
    phi_ship = 0
    if distance <= 0:
        raise ValueError("Khoang cach giao hang phai lon hon 0")
    if distance <= 2:
        phi_ship = 15000
    if distance > 2:
       phi_ship = 15000 + (distance - 2) * 5000
    if is_rush_hour == True:
        phi_ship = phi_ship * 1.2
    return phi_ship
def loc_don_theo_trang_thai(order_list, *statuses):
    return [
        order
        for order in order_list
        if not statuses or order["status"] in statuses
    ]
def tinh_tong_phi_ship(order_list):
    tong_phi = 0
    for order in order_list:
        try:
            total = tinh_phi_giao_hang(order["distance"],order["is_rush_hour"])
            tong_phi += total
        except ValueError as e:
            print("Don bi loi!")
            continue 
    return tong_phi
orders = [
    {
        "order_id": "D01",
        "distance": 1.5,
        "is_rush_hour": False,
        "status": "COMPLETED",
    },  # 1.5 km -> 15k
    {
        "order_id": "D02",
        "distance": 4.0,
        "is_rush_hour": True,
        "status": "COMPLETED",
    },  # 4 km (15k + 2*5k = 25k) * 1.2 -> 30k
    {
        "order_id": "D03",
        "distance": -2.0,
        "is_rush_hour": False,
        "status": "COMPLETED",
    },  # Lỗi distance <= 0 -> Bỏ qua
    {
        "order_id": "D04",
        "distance": 5.0,
        "is_rush_hour": False,
        "status": "CANCELLED",
    },  # 5 km (15k + 3*5k = 30k)
]

# 1. Test lọc đơn theo trạng thái
completed_orders = loc_don_theo_trang_thai(orders, "COMPLETED")
print("Số đơn đã hoàn thành:", len(completed_orders))  # Kỳ vọng: 3

# 2. Test tính tổng tiền ship các đơn hợp lệ
total_ship = tinh_tong_phi_ship(orders)
print(f"Tổng phí ship tính được: {total_ship:,.0f} VNĐ")
# Kỳ vọng: 15,000 + 30,000 + 30,000 = 75,000 VNĐ (Bỏ qua D03 bị lỗi distance)