class InvalidAcountError(Exception):
    pass
class InsufficientBalanceError(Exception):
    pass
def chuyen_tien(sender,receiver,amount,fee = 100):
    if sender["is_active"] == False or receiver["is_active"] == False:
        raise InvalidAcountError("Tai khoan bi khoa hoac khong hop le")
    total_deduct = amount + fee
    if sender["balance"] < total_deduct or amount < 0:
        raise InsufficientBalanceError("So du khong du thuc hien giao dich")
    sender["balance"] = sender["balance"] - total_deduct
    receiver["balance"] = receiver["balance"] + amount
    return amount
def loc_giao_dich(transaction_list, *types, **filters):
    min_price = filters.get("min_amount", 0) 
    max_price = filters.get("max_amount", float("inf"))
    return [
        p
        for p in transaction_list
        if not types or p["transaction"] in transaction_list
        and min_amount <= p["amount"] <= max_price
    ]
def xu_ly_hang_cho_giao_dich(transfer_queue):
    total_transferred = 0
    success_count = 0
    failed_count = 0
    for p in transfer_queue:
        try:
            fee = p.get("fee",1000)
            tong = chuyen_tien(p["sender"],p["receiver"],p["amount"])
            total_transferred += tong
            success_count += 1
        except (InvalidAcountError,InsufficientBalanceError) as e:
            print("Loi giao dich!",e)
            failed_count += 1
    return {
        "total_transferred" : total_transferred,
        "success_count": success_count,
        "failed_count": failed_count
    }
    
# Danh sách tài khoản
acc1 = {"acc_id": "A01", "owner": "An", "balance": 500000, "is_active": True}
acc2 = {"acc_id": "A02", "owner": "Bình", "balance": 100000, "is_active": True}
acc3 = {"acc_id": "A03", "owner": "Cường", "balance": 50000, "is_active": False}

# Danh sách hàng chờ chuyển tiền
queue = [
    {"sender": acc1, "receiver": acc2, "amount": 100000},  # Thành công: An -> Bình 100k
    {
        "sender": acc1,
        "receiver": acc3,
        "amount": 50000,
    },  # Lỗi: acc3 bị khóa (InvalidAccountError)
    {
        "sender": acc2,
        "receiver": acc1,
        "amount": 300000,
    },  # Lỗi: Bình chỉ có 200k (100k cũ + 100k vừa nhận) không đủ chuyển 300k (InsufficientBalanceError)
    {"sender": acc1, "receiver": acc2, "amount": 50000},  # Thành công: An -> Bình 50k
]

# Run test
report = xu_ly_hang_cho_giao_dich(queue)
print("Báo cáo giao dịch:", report)
# Kỳ vọng: {'total_transferred': 150000, 'success_count': 2, 'failed_count': 2}