class InsufficientBalanceError(Exception):
    pass
class DailyLimitExceededError(Exception):
    pass
class InvalidAccountError(Exception):
    pass
def xu_ly_chuyen_tien(wallet, amount, recipient_id, transfer_type= "internal", **options):
    if not recipient_id.startswith("WAL_") or recipient_id == wallet["id"]:
        raise InvalidAccountError("recipient_id không hợp lệ")
    if amount <= 0 or (wallet["daily_transferred"] + amount) > 20000000:
        raise InsufficientBalanceError("Vượt quá hạn mức!")
    if options.get("is_priority") == True :
        phi = 0
    else:
        fees = {"internal": 0, "interbank": 5000, "fast_247": 10000}
        phi = fees.get(transfer_type, 0)
    tong_tru = amount + phi
    if wallet["balance"] < tong_tru:
        raise InsufficientBalanceError("Không đủ số dư!")
    wallet["balance"] -= tong_tru
    wallet["daily_transferred"] += amount
    return amount,phi
def loc_lich_su(history_list, *types, **filters):
    min_amount = filters.get("min_amount",0)
    status_success_only = filters.get("status_success_only",False)
    return [
        p
        for p in history_list
        if (not types or p["type"] in types)
        and (not status_success_only or p["status"] == "success")
        and p["amount"] > min_amount
    ]
def xu_ly_danh_sach_giao_dich(wallet, transaction_requests):
    total_transferred = 0
    total_fee = 0
    success_count = 0
    failed_count = 0
    for p in transaction_requests:
        try:
            recipient_id = p["recipient_id"]
            amount = p["amount"]
            transfer_type = p.get("transfer_type","internal")

            options = {
                k : v
                for k,v in p.items()
                if k not in ["recipient_id", "amount", "transfer_type"]
            }
            amt,fee = xu_ly_chuyen_tien(wallet,amount,recipient_id,**options)
            total_transferred += amt
            total_fee += fee
            success_count += 1
        except (InsufficientBalanceError,DailyLimitExceededError,InvalidAccountError) as e:
            print("Lỗi!",e)
            failed_count += 1
    return {
        "total_transferred": total_transferred,
        "total_fee": total_fee,
        "success_count": success_count,
        "failed_count": failed_count,
    }
if __name__ == "__main__":
    wallet = {"id": "WAL_001", "balance": 5000000, "daily_transferred": 15000000}

    requests = [
        {
            "recipient_id": "WAL_002",
            "amount": 3000000,
            "transfer_type": "interbank",
        },
        {
            "recipient_id": "WAL_003",
            "amount": 3000000,
            "transfer_type": "internal",
        },
        {
            "recipient_id": "WAL_003",
            "amount": 2000000,
            "transfer_type": "fast_247",
        },
        {
            "recipient_id": "WAL_004",
            "amount": 1000000,
            "transfer_type": "fast_247",
            "is_priority": True,
        },
    ]

    report = xu_ly_danh_sach_giao_dich(wallet, requests)
    print("Báo cáo giao dịch ví:", report)

    history = [
        {"type": "transfer", "amount": 500000, "status": "success"},
        {"type": "topup", "amount": 1000000, "status": "success"},
        {"type": "transfer", "amount": 200000, "status": "failed"},
    ]
    filtered = loc_lich_su(
        history, "transfer", min_amount=300000, status_success_only=True
    )
    print("Lịch sử thỏa điều kiện:", filtered)