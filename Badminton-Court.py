class CourtUnavailableError(Exception):
    pass
class InvalidBookingHoursError(Exception):
    pass
class InvalidVoucherError(Exception):
    pass
def tinh_tien_dat_san(court, hours, voucher_code=None, **options):
    if not court["is_available"] :
        raise CourtUnavailableError("Hết sân để thuê!")
    if hours <= 0 or hours > 6:
        raise InvalidBookingHoursError("Thời gian không hợp lệ")
    tien_goc = hours * court["hourly_rate"]
    if options.get("is_peak_hour") == True:
        tien_goc *= 1.25
    racket_count = options.get("racket_rental",0)
    racket_rental = racket_count * hours * 20000
    tien_tong = tien_goc + racket_rental
    if voucher_code:
        if voucher_code == "BADMINTON10":
            tien_tong *= 0.9
        elif voucher_code == "SPORT20":
            tien_tong *= 0.8
        else:
            raise InvalidVoucherError("Mã giảm giá không khả dụng")
    court["is_available"] = False
    return tien_tong 
def loc_san_cau_long(court_list, *names, **filters):
    max_rate = filters.get("max_rate",float("inf"))
    available_only = filters.get("available_only",False)
    return [
        p
        for p in court_list
        if (not names or p["name"] in names)
        and (not available_only or p["is_available"] == True)
        and max_rate >= p["hourly_rate"]
    ]
def xu_ly_danh_sach_dat_san(booking_requests):
    total_revenue = 0
    success_count = 0
    failed_count = 0
    total_hours_booked = 0
    for p in booking_requests:
        try:
            court = p["court"]
            hours = p["hours"]
            voucher = p.get("voucher")
            options = {
                k : v
                for k,v in p.items()
                if k not in ["court","hours","voucher"]
            }
            tong = tinh_tien_dat_san(court,hours,voucher,**options)
            total_revenue += tong
            success_count += 1
            total_hours_booked += p["hours"]
        except (InvalidBookingHoursError,InvalidVoucherError,CourtUnavailableError) as e:
            print ("Lỗi!",e)
            failed_count += 1
    return {
        "total_revenue": total_revenue,
        "total_hours_booked": total_hours_booked,
        "success_count": success_count,
        "failed_count": failed_count,
    }
courts = [
    {
        "court_id": "C01",
        "name": "Sân 1",
        "hourly_rate": 80000,
        "is_available": True,
    },
    {
        "court_id": "C02",
        "name": "Sân 2",
        "hourly_rate": 120000,
        "is_available": False,
    },
    {
        "court_id": "C03",
        "name": "Sân VIP",
        "hourly_rate": 100000,
        "is_available": True,
    },
]

booking_requests = [
    {
        "court": courts[0],
        "hours": 2,
        "is_peak_hour": True,
        "racket_rental": 2,
        "voucher": "BADMINTON10",
    },
    # Tiền sân: 2h * 80k * 1.25 (cao điểm) = 200k. Thuê 2 vợt * 2h * 20k = 80k. Tổng: 280k.
    # BADMINTON10 (-10%) -> 252.000 VNĐ. Sân 1 chuyển is_available = False.
    {
        "court": courts[1],
        "hours": 2,
        "is_peak_hour": False,
        "voucher": None,
    },
    # Lỗi: C02 đang không sẵn sàng -> CourtUnavailableError
    {
        "court": courts[2],
        "hours": 8,
        "voucher": None,
    },
    # Lỗi: 8h > 6h tối đa -> InvalidBookingHoursError
    {
        "court": courts[2],
        "hours": 3,
        "is_peak_hour": False,
        "racket_rental": 0,
        "voucher": "SPORT20",
    },
    # Tiền sân: 3h * 100k = 300k. SPORT20 (-20%) -> 240.000 VNĐ. Sân VIP chuyển is_available = False.
]

# 1. Test xử lý danh sách
report = xu_ly_danh_sach_dat_san(booking_requests)
print("Báo cáo sân cầu lông:", report)
# Kỳ vọng: {'total_revenue': 492000.0, 'total_hours_booked': 5, 'success_count': 2, 'failed_count': 2}

# 2. Test lọc sân
available_courts = loc_san_cau_long(courts, available_only=True)
print("Sân trống khả dụng:", [c["name"] for c in available_courts])
# Kỳ vọng: [] (Do C01 và C03 đã bị đặt ở đơn 1 và 4, C02 bận từ đầu)