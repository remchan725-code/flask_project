class InvalidTransactionError(Exception):
    pass
def clean_transaction(raw_tx:dict) -> tuple:
    status = "OK"
    VALID_CATEGORIES = {"FOOD", "SHOPPING", "BILL", "TRANSFER"}
    if id or amount not in raw_tx:
        raise InvalidTransactionError("Giao dich khong hop le")
    
    tx_id = raw_tx["ID"]
    amount = raw_tx["Amount"]

    if amount <= 0:
        raise InvalidTransactionError("Amount phai lon hon 0")
    category = raw_tx.get("Category","Others")
    if category not in VALID_CATEGORIES:
        category = "Others"
    return (tx_id, category, amount, status)

def filter_transactions(cleaned_list,*categories,**filter):
        min_amount = filters.get("min_amount",0)
        status_filter = filters.get("status",None)
        return[
            tx #tra ve tx
            for tx in cleaned_list #voi moi tx trong cleaned_list
            if (not categories or tx[1] in categories) #neu khong phai categories hoac tx[1] trong categories 
            and tx[2] >= min_amount
            and (status_filter is None or tx[3] == status_filter)
        ]