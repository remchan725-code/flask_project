class AgeRestrictionError(Exception):
    pass
class PTScheduleFullError(Exception):
    pass
class InvalidVipCodeError(Exception):
    pass
def dang_ky_goi_tap(package, member_age, pt_sessions=0, vip_code=None):
    if member_age < package["min_age"]:
        raise AgeRestrictionError(f"Người dùng không đủ tuổi để tập gói {package["name"]}")
    if pt_sessions > package["pt_slots"]:
        raise PTScheduleFullError(f"Huấn luyện viên đã hết lịch trống cho số buổi yêu cầu")
    phi_pt = pt_sessions * 200000
    discount = 1
    if vip_code:
        if vip_code == "VIP10":
            discount = 0.9
        elif vip_code == "VIP20":
            discount = 0.8
        else:
            raise InvalidVipCodeError(f"Mã {vip_code} không tồn tại")
    package["pt_slots"] -= pt_sessions
    return (package["base_price"] + phi_pt ) * discount
def loc_goi_tap(package_list, *categories, **filters):
    min_price = filters.get("min_price",0)
    max_price = filters.get("max_price",float("inf"))
    has_pt_only = filters.get("has_pt_only",False)
    return [
        p
        for p in package_list
        if not categories or p["category"] in categories
        and max_price <= p["base_price"] <= max_price
        and ( not has_pt_only or p["pt_slot"] > 0 )
    ]
def xu_ly_danh_sach_dang_ky(registration_list):
    total_revenue = 0
    success_count = 0
    failed_count = 0
    for p in registration_list:
        try:
            tong = dang_ky_goi_tap(p["package"],p["member_age"],p["pt_sessions"],p.get("vip_code"))
            total_revenue += tong
            success_count += 1
        except(InvalidVipCodeError,PTScheduleFullError,AgeRestrictionError) as e:
            print("LỖI!",e)
            failed_count += 1
    return {
        "total_revenue" : total_revenue,
        "success_count" : success_count,
        "failed_count" : failed_count
    }
packages = [
    {
        "package_id": "G01",
        "name": "Gym Pro",
        "category": "Gym",
        "base_price": 500000,
        "min_age": 16,
        "pt_slots": 2,
    },
    {
        "package_id": "Y01",
        "name": "Yoga Basic",
        "category": "Yoga",
        "base_price": 400000,
        "min_age": 12,
        "pt_slots": 0,
    },
    {
        "package_id": "Z01",
        "name": "Zumba Dance",
        "category": "Zumba",
        "base_price": 600000,
        "min_age": 15,
        "pt_slots": 5,
    },
]

registrations = [
    {
        "package": packages[0],
        "member_age": 18,
        "pt_sessions": 2,
        "vip_code": "VIP10",
    },
    # Hợp lệ: 500k + (2*200k) = 900k. VIP10 giảm 10% = 810,000 VNĐ. G01 hết slots PT (về 0).
    {
        "package": packages[0],
        "member_age": 20,
        "pt_sessions": 1,
        "vip_code": None,
    },
    # Lỗi: G01 đã hết slots PT do đơn trên vừa đăng ký (PTScheduleFullError)
    {
        "package": packages[2],
        "member_age": 13,
        "pt_sessions": 1,
        "vip_code": None,
    },
    # Lỗi: 13 tuổi < min_age 15 (AgeRestrictionError)
    {
        "package": packages[1],
        "member_age": 25,
        "pt_sessions": 0,
        "vip_code": "VIP20",
    },
    # Hợp lệ: 400k + 0 = 400k. VIP20 giảm 20% = 320,000 VNĐ.
]

# 1. Test lọc gói tập Gym/Yoga có hỗ trợ PT
available_pt = loc_goi_tap(packages, "Gym", "Yoga", has_pt_only=True)
print("Gói tập có PT:", [p["name"] for p in available_pt])
# Kỳ vọng: [] (Vì G01 đã về 0 slots PT sau khi chạy, Y01 vốn có 0 slots)

# 2. Test xử lý danh sách đăng ký
report = xu_ly_danh_sach_dang_ky(registrations)
print("Báo cáo đăng ký:", report)
# Kỳ vọng: {'total_revenue': 1130000.0, 'success_count': 2, 'failed_count': 2}