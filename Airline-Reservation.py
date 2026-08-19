class SeatUnavailableError(Exception):
    pass
class OverBaggageWeightError(Exception):
    pass
class InvalidPromoCodeError(Exception):
    pass
def dat_ve_may_bay(flight,baggage_kg,promo_code = None):
    phi_hanh_ly = 0
    limited_kg = 7
    if flight["available_seats"] <= 0:
        raise SeatUnavailableError(f"Het vi tri ngoi tren {flight["flight_code"]}")
    if baggage_kg > 30 :
        raise OverBaggageWeightError
    if 7 < baggage_kg <= 30: 
        phi_hanh_ly = 50000 *(baggage_kg - limited_kg)
    discount = 1
    if promo_code:
        if promo_code == "FLY10":
            discount = 0.9
        elif promo_code == "FLY20":
            discount = 0.8
        else:
            raise InvalidPromoCodeError
    flight["available_seats"] -= 1
    return (flight["base_price"] + phi_hanh_ly) * discount

def loc_chuyen_bay(flight_list, *destinations, **filters):
    min_price = filters.get("min_price",0)
    max_price = filters.get("max_price",float("inf"))
    has_seats_only = filters.get("has_seats_only", False)
    return [
        f
        for f in flight_list
        if not destinations or f["destination"] in destinations
        and min_price <= f["base_price"] <= max_price
        and (not has_seats_only or f["available_seats"] > 0)
    ]

def xu_ly_danh_sach_dat_ve(booking_requests):
    total_revenue = 0
    success_count = 0
    failed_count = 0
    for b in booking_requests:
        try:
            tong = dat_ve_may_bay(b["flight"],b["baggage_kg"],b.get("promo_code"))
            total_revenue += tong
            success_count += 1
        except (SeatUnavailableError,OverBaggageWeightError,InvalidPromoCodeError) as e:
            print(e)
            failed_count += 1
    return {
        "total_revenue" : total_revenue,
        "success_count" : success_count,
        "failed_count" : failed_count
    }
flights = [
    {
        "flight_code": "VN101",
        "destination": "HAN",
        "base_price": 1000000,
        "available_seats": 1,
    },
    {
        "flight_code": "VJ202",
        "destination": "SGN",
        "base_price": 800000,
        "available_seats": 5,
    },
    {
        "flight_code": "QH303",
        "destination": "DAD",
        "base_price": 1500000,
        "available_seats": 0,
    },  # Hết ghế
]

bookings = [
    {
        "flight": flights[0],
        "baggage_kg": 10,
        "promo_code": "FLY10",
    },  # Hợp lệ: 10kg (dư 3kg = 150k). Tổng gốc 1.15M - 10% = 1,035,000 VNĐ. VN101 hết ghế (chuyển sang 0)
    {
        "flight": flights[0],
        "baggage_kg": 5,
        "promo_code": None,
    },  # Lỗi: VN101 đã hết ghế do đơn trên vừa đặt (SeatUnavailableError)
    {
        "flight": flights[1],
        "baggage_kg": 35,
        "promo_code": None,
    },  # Lỗi: Hành lý 35kg > 30kg (OverBaggageWeightError)
    {
        "flight": flights[1],
        "baggage_kg": 7,
        "promo_code": "FLY20",
    },  # Hợp lệ: 7kg (miễn phí). 800k - 20% = 640,000 VNĐ
]

# 1. Test lọc chuyến bay đến SGN/HAN còn ghế trống
available_flights = loc_chuyen_bay(
    flights, "HAN", "SGN", has_seats_only=True, max_price=1200000
)
print("Chuyến bay khả dụng:", [f["flight_code"] for f in available_flights])
# Kỳ vọng: ['VJ202'] (VN101 đã hết ghế sau khi chạy, QH303 đã 0 ghế từ đầu)

# 2. Test xử lý danh sách đặt vé
report = xu_ly_danh_sach_dat_ve(bookings)
print("Báo cáo đặt vé máy bay:", report)
# Kỳ vọng: {'total_revenue': 1675000.0, 'success_count': 2, 'failed_count': 2}