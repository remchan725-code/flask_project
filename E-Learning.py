class CourseFullError(Exception):
    pass
class PrerequisiteMissingError(Exception):
    pass
class InvalidVoucherError(Exception):
    pass
def tinh_hoc_phi_dang_ky(course, student, voucher_code=None, **options):
    if course["enrolled"] >= course["max_students"]:
        raise CourseFullError("Lớp đã đủ sĩ số!")
    if not all(p in student["completed_courses"] for p in course["prerequisites"]): #kiểm tra xem các phần tử trong pre... có nằm trong completed_course k 
        raise PrerequisiteMissingError(f"Không đủ điều kiện tiên quyết để học môn {course['name']} !")
    tuition = course["tuition"]
    after = tuition
    if student.get("is_vip") == True:
        after = tuition * 0.85
    if voucher_code:
        if voucher_code == "STUDENT10":
            after = after * 0.9
        elif voucher_code == "STUDENT20":
            after = after * 0.8
        else:
            raise InvalidVoucherError("Voucher không hợp lệ!")
    installment_months = options.get("installment_months",1)
    pay_per_months = None
    if installment_months > 1:
        pay_per_months = after / installment_months
    course["enrolled"] += 1
    return (after,pay_per_months)
def loc_khoa_hoc(course_list, *categories, **filters):
    max_tuition = filters.get("max_tuition",float("inf"))
    available_only = filters.get("available_only",False)
    return [
        p
        for p in course_list
        if (not categories or p["category"] in categories)
        and (not available_only or p["enrolled"] < p["max_students"])
        and p["tuition"] <= max_tuition
    ]
def xu_ly_danh_sach_dang_ky(registration_requests):
    total_revenue = 0
    total_enrolled_students = 0
    success_count = 0
    failed_count = 0
    for p in registration_requests:
        try:
            course = p["course"]
            student = p["student"]
            voucher = p.get("voucher")
            options = {
                k : v
                for k,v in p.items()
                if k not in ["course","student","voucher"]
            }
            tong_tien,_ = tinh_hoc_phi_dang_ky(course,student,voucher,**options)
            total_revenue += tong_tien
            total_enrolled_students += 1
            success_count += 1
        except (CourseFullError,PrerequisiteMissingError,InvalidVoucherError) as e:
            print("Lỗi đăng ký:", e)
            failed_count += 1
    return {
        "total_revenue": total_revenue,
        "total_enrolled_students": total_enrolled_students,
        "success_count": success_count,
        "failed_count": failed_count,
    }
courses = [
    {
        "id": "PY101",
        "name": "Python Cơ Bản",
        "max_students": 30,
        "enrolled": 29,
        "tuition": 2000000,
        "prerequisites": ["CS100"],
    },
    {
        "id": "AI202",
        "name": "Trí Tuệ Nhân Tạo",
        "max_students": 10,
        "enrolled": 10,
        "tuition": 4000000,
        "prerequisites": [],
    },
    {
        "id": "ADV303",
        "name": "Python Nâng Cao",
        "max_students": 20,
        "enrolled": 5,
        "tuition": 3000000,
        "prerequisites": ["PY101"],
    },
]

students = [
    {
        "id": "SV01",
        "name": "An",
        "completed_courses": ["CS100"],
        "is_vip": True,
    },
    {
        "id": "SV02",
        "name": "Bình",
        "completed_courses": [],
        "is_vip": False,
    },
]

registration_requests = [
    {
        "course": courses[0],
        "student": students[0],
        "voucher": "STUDENT10",
        "installment_months": 3,
    },
    # Học phí gốc: 2.000.000đ. VIP (-15%) -> 1.700.000đ. STUDENT10 (-10%) -> 1.530.000đ.
    # Trả góp 3 tháng -> 510.000đ/tháng. Khóa PY101 tăng enrolled lên 30.
    {
        "course": courses[1],
        "student": students[0],
        "voucher": None,
        "installment_months": 1,
    },
    # Lỗi: Lớp AI202 đã đầy (enrolled 10 == max 10) -> CourseFullError
    {
        "course": courses[2],
        "student": students[1],
        "voucher": "WELCOME20",
        "installment_months": 1,
    },
    # Lỗi: Bình chưa hoàn thành môn tiên quyết "PY101" -> PrerequisiteMissingError
    {
        "course": courses[0],
        "student": students[1],
        "voucher": "BADVOUCHER",
        "installment_months": 1,
    },
    # Lỗi: Mã giảm giá sai -> InvalidVoucherError
]

# 1. Test xử lý danh sách đăng ký
report = xu_ly_danh_sach_dang_ky(registration_requests)
print("Báo cáo hệ thống học tập:", report)
# Kỳ vọng: {'total_revenue': 1530000.0, 'total_enrolled_students': 1, 'success_count': 1, 'failed_count': 3}

# 2. Test lọc khóa học
available_courses = loc_khoa_hoc(courses, max_tuition=3500000, available_only=True)
print("Khóa học phù hợp:", [c["name"] for c in available_courses])
# Kỳ vọng: ['Python Nâng Cao'] (PY101 đã đầy chỗ ở đơn 1, AI202 đã đầy từ đầu)