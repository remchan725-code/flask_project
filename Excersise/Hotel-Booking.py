class RoomUnavailableError(Exception):
    pass
class InvalidPromoError(Exception):
    pass
def tinh_tien_dat_phong(room,nights,promo_code = None):

    if room["is_available"] == False or nights <= 0:
        raise RoomUnavailableError("Phong khong kha dung hoac so dem khong hop le")
    discount = 1
    if promo_code:
        if promo_code == "SUMMER10":
            discount = 0.9
        elif promo_code == "VIP20":
            discount = 0.8
        else:
            raise InvalidPromoError("Ma giam gia khong hop le")
        return room["price_per_night"] * nights * discount

def loc_phong(room_list,*types,**filters):
    min_price = filters.get("min_amount", 0) 
    max_price = filters.get("max_amount", float("inf"))
    return [
        p 
        for p in room_list
        if not types or p["type"] in types
        and min_price <= p["price_per_night"] <= max_price
    ]

def thong_ke_dat_phong(booking_list):
    total_revenue = 0
    success_count = 0
    failed_count = 0
    for room in booking_list:
        try:
            total = tinh_tien_dat_phong(room["room"],room["nights"],room.get("promo_code"))
            total_revenue += total
            success_count += 1
        except(RoomUnavailableError,InvalidPromoError) as e:
            print(e)
            failed_count += 1
        return {
            "total_revenue" : total_revenue,
            "success_count" : success_count,
            "failed_count" : failed_count
        }
# Danh sách phòng trong khách sạn
rooms = [
    {
        "room_id": "R101",
        "type": "VIP",
        "price_per_night": 1000000,
        "is_available": True,
    },
    {
        "room_id": "R102",
        "type": "DELUXE",
        "price_per_night": 600000,
        "is_available": True,
    },
    {
        "room_id": "R103",
        "type": "STANDARD",
        "price_per_night": 300000,
        "is_available": False,
    },  # Đã có người ở
]

# Danh sách lượt khách đặt phòng
bookings = [
    {
        "room": rooms[0],
        "nights": 2,
        "promo_code": "SUMMER10",
    },  # Thành công: R101 (2 triệu - 10%) -> 1.8M. R101 đổi sang is_available = False
    {
        "room": rooms[0],
        "nights": 1,
        "promo_code": None,
    },  # Lỗi: R101 vừa bị đặt ở bước trên -> RoomUnavailableError
    {
        "room": rooms[1],
        "nights": 3,
        "promo_code": "TEST99",
    },  # Lỗi: Promo code sai -> InvalidPromoError
    {
        "room": rooms[1],
        "nights": 1,
        "promo_code": "VIP20",
    },  # Thành công: R102 (600k - 20%) -> 480k
]

# 1. Test lọc phòng
available_vip = loc_phong(rooms, "VIP", "DELUXE", min_price=500000)
print(
    "Các phòng VIP/Deluxe giá từ 500k:", [r["room_id"] for r in available_vip]
)
# Kỳ vọng: ['R101', 'R102']

# 2. Test thống kê đặt phòng
report = thong_ke_dat_phong(bookings)
print("Báo cáo đặt phòng:", report)
# Kỳ vọng: {'total_revenue': 2280000.0, 'success_count': 2, 'failed_count': 2}