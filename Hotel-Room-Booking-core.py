class OverCapacityError(Exception):
    pass
class NoRoomAvailableError(Exception):
    pass
class InvalidVoucherError(Exception):
    pass
def tinh_tien_dat_phong(room, guests, nights, voucher_code=None, **extra_services):
    if guests > room["max_guests"] or guests <= 0:
        raise OverCapacityError(f"Phòng {room["room_id"]} không đủ chỗ cho số lương khách!")
    if room["available_rooms"] <= 0 or nights <= 0:
        raise NoRoomAvailableError("Không còn phòng !")
    tien_phong = nights * room["nightly_rate"]
    service_pay = 0
    if extra_services.get("breakfast"):
        service_pay += 100000 * guests * nights
    if extra_services.get("laundry_kg"):
        service_pay += 30000 * extra_services["laundry_kg"]
    if extra_services.get("airport_pickup"):
        service_pay += 250000
    discount = 1
    if voucher_code:
        if voucher_code == "HOTEL10":
            discount = 0.9
        elif voucher_code == "HOTEL20":
            discount = 0.8
        else:
            raise InvalidVoucherError("Mã voucher không hợp lệ!")
    room["available_rooms"] -= 1
    return (tien_phong + service_pay) * discount
def loc_phong(room_list, *types, **filters):
    max_rate = filters.get("max_rate",float("inf"))
    has_rooms_only = filters.get("has_rooms_only",False)
    return [
        p
        for p in room_list
        if (not types or p["type"] in types)
        and (not has_rooms_only or p["available_rooms"] > 0)
        and p["nightly_rate"] <= max_rate
    ]
def xu_ly_danh_sach_dat_phong(booking_requests):
    total_revenue = 0
    success_count = 0
    failed_count = 0
    total_nights_booked = 0
    for p in booking_requests:
        try:
            tong = tinh_tien_dat_phong(p["room"],p["guests"],p["nights"],p.get("voucher"),
            breakfast = p.get("breakfast",0),
            laundry_kg = p.get("laundry_kg",0),
            airport_pickup = p.get("airport_pickup",0)
            )
            total_revenue += tong
            success_count += 1
            total_nights_booked += p["nights"]
        except (InvalidVoucherError,NoRoomAvailableError,OverCapacityError) as e:
            print("Lỗi!",e)
            failed_count += 1
    return {
        "total_revenue":total_revenue,
        "success_count":success_count,
        "failed_count":failed_count,
        "total_nights_booked" :total_nights_booked
    }

rooms = [
    {
        "room_id": "R101",
        "type": "Standard",
        "max_guests": 2,
        "available_rooms": 1,
        "nightly_rate": 500000,
    },
    {
        "room_id": "R102",
        "type": "Deluxe",
        "max_guests": 4,
        "available_rooms": 3,
        "nightly_rate": 1000000,
    },
    {
        "room_id": "R103",
        "type": "Suite",
        "max_guests": 5,
        "available_rooms": 0,
        "nightly_rate": 2000000,
    },
]

requests = [
    {
        "room": rooms[0],
        "guests": 2,
        "nights": 2,
        "voucher": "HOTEL10",
        "laundry_kg": 3,
    },
    # Phòng: 2 đêm * 500k = 1tr. Giặt: 3kg * 30k = 90k. Tổng 1.090.000đ -> HOTEL10 (-10%) = 981,000 VNĐ.
    # R101 hết phòng (về 0). Đã đặt 2 đêm.
    {
        "room": rooms[0],
        "guests": 1,
        "nights": 1,
        "voucher": None,
    },
    # Lỗi: R101 đã hết phòng -> NoRoomAvailableError
    {
        "room": rooms[1],
        "guests": 5,
        "nights": 1,
        "voucher": None,
    },
    # Lỗi: 5 khách > max_guests 4 -> OverCapacityError
    {
        "room": rooms[1],
        "guests": 3,
        "nights": 3,
        "voucher": "HOTEL20",
        "breakfast": True,
        "airport_pickup": True,
    },
    # Phòng: 3 đêm * 1tr = 3tr. Sáng: 100k * 3 người * 3 đêm = 900k. Xe: 250k. Tổng 4.150.000đ -> HOTEL20 (-20%) = 3,320,000 VNĐ.
    # R102 còn 2 phòng. Đã đặt 3 đêm.
]

# 1. Test xử lý danh sách đặt phòng
report = xu_ly_danh_sach_dat_phong(requests)
print("Báo cáo doanh thu khách sạn:", report)
# Kỳ vọng: {'total_revenue': 4301000.0, 'total_nights_booked': 5, 'success_count': 2, 'failed_count': 2}

# 2. Test lọc phòng
available_rooms = loc_phong(
    rooms, "Standard", "Deluxe", "Suite", has_rooms_only=True
)
print("Phòng khả dụng:", [r["room_id"] for r in available_rooms])
# Kỳ vọng: ['R102'] (R101 đã bị đặt hết ở đơn 1, R103 vốn có 0 phòng)