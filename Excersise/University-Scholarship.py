class InvalidScoreError(Exception):
    pass
class DisqualifiedError(Exception):
    pass
def tinh_tien_hoc_bong(gpa,training_score,is_warning):
    tien = 0
    if gpa <= 0 or gpa > 4:
        raise InvalidScoreError
    if gpa <= 3.2 or is_warning == True:
        raise DisqualifiedError
    if gpa >= 3.6 and training_score >= 90:
        print("Xuat xac")
        tien = tien + 5000000
    elif gpa >= 3.2 and training_score >= 80:
        print("Gioi")
        tien = tien + 3000000
    else:
        raise DisqualifiedError
    return tien
def loc_sinh_vien(student_list, *majors, **filters):
    min_gpa = filters.get("min_gpa",0) 
    max_gpa = filters.get("max_gpa",4.0 )
    return[
        p
        for p in student_list
        if not majors or p["major"] in majors
        and min_gpa <= p["gpa"] <= max_gpa
    ]
def thong_ke_trao_hoc_bong(student_list):
    total_fund = 0
    awarded_count = 0
    disqualified_count = 0
    for s in student_list:
        try:
            tong = tinh_tien_hoc_bong(s["gpa"],s["training_score"],s["is_warning"])
            total_fund += tong
            print(f"Sinh vien {s["name"]} voi hoc luc du dieu kien de nhan hoc bong\n")
            awarded_count += 1
        except (InvalidScoreError,DisqualifiedError) as e:
            print(f"Sinh vien {s["name"]} khong du dieu kien nhan hoc bong\n",e)
            disqualified_count += 1
    return {
        "total_fund" : total_fund,
        "awarded_count" : awarded_count,
        "disqualified_count" : disqualified_count
    }
students = [
    {
        "student_id": "SV01",
        "name": "An",
        "major": "CNTT",
        "gpa": 3.8,
        "training_score": 95,
        "is_warning": False,
    },  # Xuất sắc -> 5 triệu
    {
        "student_id": "SV02",
        "name": "Bình",
        "major": "CNTT",
        "gpa": 3.4,
        "training_score": 85,
        "is_warning": False,
    },  # Giỏi -> 3 triệu
    {
        "student_id": "SV03",
        "name": "Cường",
        "major": "KTPM",
        "gpa": 3.7,
        "training_score": 90,
        "is_warning": True,
    },  # Lỗi: Bị cảnh cáo học tập (DisqualifiedError)
    {
        "student_id": "SV04",
        "name": "Dũng",
        "major": "CNTT",
        "gpa": 4.5,
        "training_score": 80,
        "is_warning": False,
    },  # Lỗi: GPA > 4.0 (InvalidScoreError)
    {
        "student_id": "SV05",
        "name": "Giang",
        "major": "KHMT",
        "gpa": 2.8,
        "training_score": 70,
        "is_warning": False,
    },  # Không đủ mức nhận HB -> 0k
]

# 1. Test lọc sinh viên ngành CNTT có GPA từ 3.0 đến 4.0
filtered = loc_sinh_vien(students, "CNTT", min_gpa=3.0, max_gpa=4.0)
print("Sinh viên CNTT GPA khá/giỏi:", [s["name"] for s in filtered])
# Kỳ vọng: ['An', 'Bình']

# 2. Test thống kê trao học bổng
report = thong_ke_trao_hoc_bong(students)
print("Báo cáo học bổng:", report)
# Kỳ vọng: {'total_fund': 8000000, 'awarded_count': 2, 'disqualified_count': 2}