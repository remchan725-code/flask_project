class AgeLimitError(Exception):
    pass
class SeatUnavailableError(Exception):
    pass
class InvalidVoucherError(Exception):
    pass
def tinh_tien_dat_ve(movie, age, seats, voucher_code=None, **combos):
    if age < movie["age_rating"]:
        raise AgeLimitError(f"Người xem chưa đủ tuổi để xem bộ phim {movie["title"]}!")
    if seats > movie["available_seats"] or seats <= 0:
        raise SeatUnavailableError("Không đủ ghế trống!")
    tien_ve = seats * movie["ticket_price"]
    gia_combo = {"popcorn":60000,"soda":30000,"combo_family":120000}
    tinh_combo = 0
    for item,quantity in combos.items():
        tinh_combo += gia_combo.get(item,0) * quantity
    discount = 1
    if voucher_code:
        if voucher_code == "CINEMA10":
            discount = 0.9
        elif voucher_code == "CINEMA20":
            discount = 0.8
        else:
            raise InvalidVoucherError("Voucher không hợp lệ!")
    movie["available_seats"] -= seats
    return (tinh_combo + tien_ve) * discount
def loc_phim(movie_list, *genres, **filters):
    max_price = filters.get("max_price",float("inf"))
    has_seats_only = filters.get("has_seats_only",False)
    return [
        p
        for p in movie_list
        if (not genres or p["genre"] in genres)
        and (not has_seats_only or p["available_seats"] > 0)
        and p["ticket_price"] <= max_price
    ]
def xu_ly_danh_sach_dat_ve(booking_requests):
    total_revenue = 0
    success_count = 0
    failed_count = 0
    total_tickets_sold = 0
    for p in booking_requests:
        try:
            tong = tinh_tien_dat_ve(p["movie"],p["age"],p["seats"],p.get("voucher"),
            popcorn=p.get("popcorn", 0),
            soda=p.get("soda", 0),
            combo_family=p.get("combo_family", 0),)
            total_revenue += tong
            success_count += 1
            total_tickets_sold += p["seats"]
        except (InvalidVoucherError,SeatUnavailableError,AgeLimitError) as e:
            print("Lỗi!",e)
            failed_count += 1
    return {
        "total_revenue": total_revenue,
        "success_count": success_count,
        "failed_count": failed_count,
        "total_tickets_sold": total_tickets_sold,
    }
movies = [
    {
        "title": "Lật Mặt 8",
        "genre": "Hành động",
        "age_rating": 16,
        "available_seats": 3,
        "ticket_price": 90000,
    },
    {
        "title": "Con Cám",
        "genre": "Kinh dị",
        "age_rating": 18,
        "available_seats": 20,
        "ticket_price": 110000,
    },
    {
        "title": "Doraemon",
        "genre": "Hoạt hình",
        "age_rating": 0,
        "available_seats": 0,
        "ticket_price": 70000,
    },  # Hết ghế
]

requests = [
    {
        "movie": movies[0],
        "age": 20,
        "seats": 2,
        "voucher": "CINEMA10",
        "popcorn": 1,
        "soda": 1,
    },
    # Vé: 2 * 90k = 180k. Combo: 60k + 30k = 90k. Tổng: 270k. CINEMA10 (-10%) -> 243,000 VNĐ.
    # movies[0] còn 1 ghế.
    {
        "movie": movies[0],
        "age": 22,
        "seats": 2,
        "voucher": None,
    },
    # Lỗi: movies[0] chỉ còn 1 ghế mà đòi đặt 2 -> SeatUnavailableError
    {
        "movie": movies[1],
        "age": 15,
        "seats": 1,
        "voucher": None,
    },
    # Lỗi: 15 tuổi đòi xem phim 18+ -> AgeLimitError
    {
        "movie": movies[1],
        "age": 19,
        "seats": 3,
        "voucher": "CINEMA20",
        "combo_family": 1,
    },
    # Vé: 3 * 110k = 330k. Combo family: 120k. Tổng: 450k. CINEMA20 (-20%) -> 360,000 VNĐ.
    # movies[1] còn 17 ghế.
]
available_movies = loc_phim(movies, "Hành động", "Kinh dị", has_seats_only=True)
print("Phim khả dụng:", [m["title"] for m in available_movies])

# 1. Test xử lý danh sách đặt vé
report = xu_ly_danh_sach_dat_ve(requests)
print("Báo cáo doanh thu rạp:", report)
# Kỳ vọng: {'total_revenue': 603000.0, 'total_tickets_sold': 5, 'success_count': 2, 'failed_count': 2}

# 2. Test lọc phim

# Kỳ vọng: ['Lật Mặt 8', 'Con Cám'] (Doraemon hết ghế nên bị loại)