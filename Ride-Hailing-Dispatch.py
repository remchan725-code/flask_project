class NoDriverError(Exception):
    pass
class CapacityExceededError(Exception):
    pass
class InvalidPromotionError(Exception):
    pass
def tinh_cuoc_chuyen_xe(rides, distance_km, passengers, is_peak_hour=False, promo_code=None):
    tong = 0
    he_so_peak_hour = 1
    if rides["drivers_available"] <= 0 or distance_km > 50 :
        raise NoDriverError("Không có tài xế nào nhận cuốc của bạn!")
    if passengers > rides["capacity"] :
        raise CapacityExceededError("Số lượng khách vượt quá chỗ ngồi của xe!") 
    gia = 20000
    if distance_km > 2 :
        gia += (distance_km - 2) * rides["per_km_rate"]
    if is_peak_hour == True:
       he_so_peak_hour = 1.5
    discount = 1
    if promo_code:
        if promo_code == "GRAB10":
            discount = 0.9
        elif promo_code == "GRAB20":
            discount = 0.8
        else:
            raise InvalidPromotionError(f"Mã khuyến mãi {promo_code} không tồn tại")
    rides["drivers_available"] -= 1
    tong = (gia * he_so_peak_hour ) * discount
    return tong

def xu_ly_danh_sach_cuoc_xe(ride_requests):
    total_revenue = 0
    success_count = 0
    failed_count = 0
    distance_km_serve = 0
    for p in ride_requests:
        try :
            tong = tinh_cuoc_chuyen_xe(p["ride"],p["distance_km"],p["passengers"],p["is_peak_hour"],p.get("promo_code"))
            total_revenue += tong
            success_count += 1
            distance_km_serve += p["distance_km"]
        except (NoDriverError,CapacityExceededError,InvalidPromotionError) as e:
            print("Loi!",e)
            failed_count += 1
    return {
        "total_revenue" : total_revenue,
        "success_count" : success_count,
        "failed_count" : failed_count,
        "distance_km_serve":distance_km_serve
    }
def loc_chuyen_xe(ride_list, *types, **filters):
    max_rate = filters.get("max_rate",float("inf"))
    has_driver_only = filters.get("has_driver_only",False)
    return [
        p
        for p in ride_list
        if (not types or p["type"] in types)
        and p["per_km_rate"] <= max_rate
        and (not has_driver_only or p["drivers_available"] > 0)
    ]    
rides = [
    {
        "ride_id": "R01",
        "type": "Car4",
        "capacity": 4,
        "drivers_available": 1,
        "per_km_rate": 10000,
    },
    {
        "ride_id": "R02",
        "type": "Car7",
        "capacity": 7,
        "drivers_available": 2,
        "per_km_rate": 15000,
    },
    {
        "ride_id": "R03",
        "type": "Bike",
        "capacity": 1,
        "drivers_available": 0,
        "per_km_rate": 5000,
    },  # Hết xe
]

requests = [
    {
        "ride": rides[0],
        "distance_km": 10,
        "passengers": 3,
        "is_peak_hour": True,
        "promo_code": "GRAB10",
    },
    # 2km đầu: 20k, 8km sau: 80k -> Cước 100k. Peak x1.5 = 150k. GRAB10 giảm 10% -> 135,000 VNĐ.
    # rides[0] hết driver (về 0). Phục vụ 10km.
    {
        "ride": rides[0],
        "distance_km": 5,
        "passengers": 1,
        "is_peak_hour": False,
        "promo_code": None,
    },
    # Lỗi: rides[0] đã hết driver do đơn trên vừa đặt -> NoDriverError
    {
        "ride": rides[1],
        "distance_km": 12,
        "passengers": 8,
        "is_peak_hour": False,
        "promo_code": None,
    },
    # Lỗi: 8 người > capacity 7 người -> CapacityExceededError
    {
        "ride": rides[1],
        "distance_km": 6,
        "passengers": 5,
        "is_peak_hour": False,
        "promo_code": "GRAB20",
    },
    # 2km đầu: 20k, 4km sau: 60k -> Cước 80k. Không peak. GRAB20 giảm 20% -> 64,000 VNĐ.
    # rides[1] còn 1 driver. Phục vụ 6km.
]
# 2. Test xử lý danh sách cuốc xe
report = xu_ly_danh_sach_cuoc_xe(requests)
# Kỳ vọng: {'total_revenue': 199000.0, 'total_km_served': 16, 'success_count': 2, 'failed_count': 2}

# 1. Test lọc chuyến xe
available_cars = loc_chuyen_xe(rides,"Car4","Car7", has_driver_only=True)
print("Các loại xe khả dụng:", [r["type"] for r in available_cars])
# Kỳ vọng: ['Car7'] (Do Car4 đã hết tài xế sau khi chạy danh sách)
print("Báo cáo cuốc xe:", report)

        