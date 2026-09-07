def tinh_phi_gui_xe(vehicle_type,hours,is_overnight):
    phi_gui = 0
    if hours <= 0:
        raise ValueError("Số giờ gửi phải lớn hơn 0")
    if vehicle_type == "BIKE":
        phi_gui = hours * 5000
    elif vehicle_type == "CAR":
        phi_gui = hours * 20000
    else :
        raise ValueError("Xe không hợp lệ")
    if is_overnight:
        phi_gui = phi_gui + 30000
    return phi_gui
def loc_xe_theo_loai(parking_list, *vehicle_types):
    return[
        vehicle
        for vehicle in parking_list
        if not vehicle_types or vehicle["vehicle_type"] in vehicle_types
    ]
def tinh_tong_doanh_thu_bai_xe(parking_list):
    tong = 0
    for xe in parking_list:
        try:
            phi = tinh_phi_gui_xe(xe["vehicle_type"],xe["hours"],xe["is_overnight"])
            tong += phi
        except ValueError as e:
            print ("Loi so gio / sai loai xe!",e)
            continue
    return tong
parking_logs = [
    {
        "plate": "29A-12345",
        "vehicle_type": "BIKE",
        "hours": 3,
        "is_overnight": False,
    },  # Xe máy 3h -> 15k
    {
        "plate": "30B-67890",
        "vehicle_type": "CAR",
        "hours": 2,
        "is_overnight": True,
    },  # Ô tô 2h (40k) + Qua đêm (30k) -> 70k
    {
        "plate": "51C-99999",
        "vehicle_type": "TRUCK",
        "hours": 5,
        "is_overnight": False,
    },  # Lỗi loại xe TRUCK
    {
        "plate": "43D-11111",
        "vehicle_type": "BIKE",
        "hours": -1,
        "is_overnight": False,
    },  # Lỗi hours <= 0
    {
        "plate": "60E-22222",
        "vehicle_type": "CAR",
        "hours": 1,
        "is_overnight": False,
    },  # Ô tô 1h -> 20k
]

# 1. Test lọc xe theo loại (chỉ lấy Ô tô)
cars = loc_xe_theo_loai(parking_logs, "CAR")
print("Số lượt gửi ô tô:", len(cars))  # Kỳ vọng: 2

# 2. Test tính tổng doanh thu
total_revenue = tinh_tong_doanh_thu_bai_xe(parking_logs)
print(f"Tổng doanh thu bãi xe: {total_revenue:,.0f} VNĐ")
# Kỳ vọng: 15,000 + 70,000 + 20,000 = 105,000 VNĐ (Bỏ qua 2 xe bị lỗi TRUCK và hours < 0)