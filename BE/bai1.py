def detect_spam_requests(request_logs, **thresholds):
    #1.Lấy cấu hình ngưỡng cho phép
    max_failed_attemps = thresholds.get("max_failed_attemps",2) #dùng .get() để hệ thống k sập nếu ng dùng k truyền tham số vào max_failed_attemps
    failed_counts = {} #đếm số lần nhập sai
    total_valid_requests = 0
    #2.Duyệt dữ liệu, làm sạch và thống kê lỗi
    for req in request_logs:
        ip = req.get("ip")
        if not ip:
            continue
    #kiểm tra status_code an toàn bằng try và except
        try:
            status_code = int(req.get("status_code"))
        except (ValueError,TypeError): #chặn dữ liệu rác
            continue
        total_valid_requests += 1

    #Mã lỗi HTTP thường từ 400 trở lên
        if status_code >= 400:
            failed_counts[ip] = failed_counts.get(ip,0) + 1
    
    #3.lọc IP bằng set comprehesion
    blacklisted_ips = {
        ip
        for ip,count in failed_counts.items()
        if count >= max_failed_attemps
    }
    return {
            "total_valid_requests": total_valid_requests,
            "blacklisted_ips": blacklisted_ips,
            "failed_stats": failed_counts,
        }
requests = [
    {"ip": "10.0.0.1", "action": "LOGIN", "status_code": "200"},
    {"ip": "10.0.0.2", "action": "PAYMENT", "status_code": "500"},  # Lỗi 1
    {"ip": "10.0.0.1", "action": "LOGIN", "status_code": "401"},  # Lỗi 1
    {"ip": "10.0.0.1", "action": "LOGIN", "status_code": "401"},  # Lỗi 2 -> Đạt ngưỡng 2
    {"ip": "10.0.0.3", "action": "API_CALL", "status_code": "INVALID_CODE"},  # Rác -> Bỏ qua
]

# Chạy với ngưỡng mặc định (2 lần lỗi là khóa)
result = detect_spam_requests(requests, max_failed_attempts=2)
print(result)