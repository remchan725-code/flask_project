def tinh_gia_ve(price,customer_age,age_limit,is_student):
    if customer_age < age_limit:
        raise ValueError("Khách hàng chưa đủ tuổi xem phim này!")
    if is_student:
        return price * 0.8
    return price
def loc_ve_theo_phim(ticket_list, *movie_names):
    return [
        ticket
        for ticket in ticket_list
        if not movie_names or ticket["movie"] in movie_names
    ]
def tinh_tong_doanh_thu(ticket_list):
    tong_tien = 0
    for ticket in ticket_list:
        try:
            tien = tinh_gia_ve(
                ticket["price"],
                ticket["customer_age"],
                ticket["age_limit"],
                ticket["is_student"]
            )
            tong_tien += tien
        except ValueError as e:
            print("Loi he thong",e)
    return tong_tien
tickets = [
    {
        "movie": "Conan",
        "price": 100000,
        "age_limit": 13,
        "customer_age": 16,
        "is_student": True,
    },  # Đủ tuổi + Sinh viên -> 80k
    {
        "movie": "Deadpool",
        "price": 120000,
        "age_limit": 18,
        "customer_age": 15,
        "is_student": False,
    },  # Lỗi: Chưa đủ 18 tuổi
    {
        "movie": "Conan",
        "price": 100000,
        "age_limit": 13,
        "customer_age": 25,
        "is_student": False,
    },  # Đủ tuổi, không giảm giá -> 100k
    {
        "movie": "Dune",
        "price": 150000,
        "age_limit": 16,
        "customer_age": 20,
        "is_student": True,
    },  # Đủ tuổi + Sinh viên -> 120k
]

# 1. Test lọc vé theo tên phim
conan_tickets = loc_ve_theo_phim(tickets, "Conan")
print("Số vé phim Conan:", len(conan_tickets))  # Kỳ vọng: 2

# 2. Test tính tổng doanh thu
total = tinh_tong_doanh_thu(tickets)
print(f"Tổng doanh thu vé hợp lệ: {total:,.0f} VNĐ")
# Kỳ vọng: 80,000 + 100,000 + 120,000 = 300,000 VNĐ (Bỏ qua vé Deadpool bị lỗi tuổi)