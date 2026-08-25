class FullBusError(Exception):
    pass
class OverweightLuggageError(Exception):
    pass
class InvalidVoucherError(Exception):
    pass
def tinh_tien_dat_ve_xe(trip, passenger, seats, luggage_kg=0, voucher_code=None, **options):
    phi_bao_hiem = 0
    phi_hanh_ly = 0
    if trip["booked"] + seats > trip["capacity"] or seats <= 0:
        raise FullBusError("Đã kín chỗ ngồi!")
    if luggage_kg > 30:
        raise OverweightLuggageError("Hành lý quá số cân cho phép!")
    tien_ve = seats * trip["base_price"]
    if passenger.get("is_student") == True:
        tien_ve = tien_ve * 0.9
    free_weight = seats * 5
    if luggage_kg > free_weight :
        phi_hanh_ly = (luggage_kg - free_weight) * 10000
    if options.get("has_insurance") == True:
        phi_bao_hiem = seats * 20000
    tien_ve_sau = tien_ve + phi_bao_hiem + phi_hanh_ly
    if voucher_code:
        if voucher_code == "SUMMER10":
            tien_ve_sau *= 0.9
        elif voucher_code == "BUS20":
            tien_ve_sau *= 0.8
        else:
            raise InvalidVoucherError("Voucher không hợp lệ!")
    trip["booked"] += seats
    return tien_ve_sau
def loc_chuyen_xe(trip_list, *routes, **filters):
    max_price = filters.get("max_price",float("inf"))
    available_seats_only = filters.get("available_seats_only",False)
    return [
        p
        for p in trip_list
        if (not routes or p["route"] in routes)
        and (not available_seats_only or p["capacity"] - p["booked"] > 0)
        and p["base_price"] <= max_price
    ]
def xu_ly_danh_sach_dat_ve(booking_requests):
    total_revenue = 0
    success_count = 0
    failed_count = 0
    total_seats_sold = 0
    for p in booking_requests:
        try:
            seats = p["seats"]
            passenger = p["passenger"]
            trip = p["trip"]
            luggage_kg = p["luggage_kg"]
            voucher = p.get("voucher")
            options = {
                k : v
                for k,v in p.items()
                if k not in ["trip","seats","passenger","luggage_kg","voucher"]
            }
            tong = tinh_tien_dat_ve_xe(trip,passenger,seats,luggage_kg,voucher,**options)
            total_revenue += tong
            success_count += 1 
            total_seats_sold += p["seats"]
        except (OverweightLuggageError,FullBusError,InvalidVoucherError) as e:
            print("Lỗi!",e)
            failed_count += 1
    return {
        "total_revenue": total_revenue,
        "total_seats_sold" : total_seats_sold,
        "success_count": success_count,
        "failed_count": failed_count,
    }
trips = [
    {
        "trip_id": "BUS01",
        "route": "Hà Nội - Sapa",
        "capacity": 30,
        "booked": 28,
        "base_price": 300000,
    },
    {
        "trip_id": "BUS02",
        "route": "Hà Nội - Hải Phòng",
        "capacity": 20,
        "booked": 20,
        "base_price": 200000,
    },
    {
        "trip_id": "BUS03",
        "route": "Hà Nội - Quảng Ninh",
        "capacity": 15,
        "booked": 5,
        "base_price": 250000,
    },
]

passengers = [
    {"name": "Nam", "is_student": True},
    {"name": "Hoa", "is_student": False},
]

booking_requests = [
    {
        "trip": trips[0],
        "passenger": passengers[0],
        "seats": 2,
        "luggage_kg": 15,
        "voucher": "SUMMER10",
        "has_insurance": True,
    },
    # Vé 2 ghế * 300k = 600k. HS/SV (-10%) -> 540k.
    # Hành lý miễn phí 10kg -> Dư 5kg * 10k = 50k. Bảo hiểm: 2 ghế * 20k = 40k.
    # Tổng trước voucher: 630k. SUMMER10 (-10%) -> 567.000 VNĐ. BUS01 đầy (30/30).
    {
        "trip": trips[1],
        "passenger": passengers[1],
        "seats": 1,
        "luggage_kg": 0,
        "voucher": None,
    },
    # Lỗi: BUS02 đã hết chỗ (20/20) -> FullBusError
    {
        "trip": trips[2],
        "passenger": passengers[1],
        "seats": 2,
        "luggage_kg": 35,
        "voucher": None,
    },
    # Lỗi: Hành lý 35kg > 30kg -> OverweightLuggageError
    {
        "trip": trips[2],
        "passenger": passengers[1],
        "seats": 1,
        "luggage_kg": 8,
        "voucher": None,
        "has_insurance": False,
    },
    # Vé 1 ghế * 250k = 250k. Hành lý dư 3kg * 10k = 30k. Tổng = 280.000 VNĐ.
]

# 1. Test xử lý danh sách
report = xu_ly_danh_sach_dat_ve(booking_requests)
print("Báo cáo nhà xe:", report)
# Kỳ vọng: {'total_revenue': 847000.0, 'total_seats_sold': 3, 'success_count': 2, 'failed_count': 2}

# 2. Test lọc chuyến xe
available_trips = loc_chuyen_xe(
    trips, "Hà Nội - Sapa", "Hà Nội - Quảng Ninh", available_seats_only=True
)
print("Chuyến xe khả dụng:", [t["trip_id"] for t in available_trips])
# Kỳ vọng: ['BUS03'] (BUS01 đã hết ghế sau đơn 1)