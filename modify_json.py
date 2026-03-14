import json

file_path = r"d:\NTU\CNTT\NCKH\Code\StudentDataStandardization\student_input_standard.json"

with open(file_path, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

# 1. Update labels
for spec in data["controlled_values"]["specialization_codes"]:
    if spec["code"] == "CNPM":
        spec["label"] = "Công nghệ phần mềm"
    elif spec["code"] == "HTTT":
        spec["label"] = "Hệ thống thông tin"
    elif spec["code"] == "TTMMT":
        spec["label"] = "Truyền thông và mạng máy tính"

# 2. Update learning_goals
data["controlled_values"]["learning_goals"] = [
    "Đúng hạn",
    "Học vượt",
    "Giảm tải"
]

# 3. Update descriptions
desc_map = {
    "mssv": "Mã sinh viên duy nhất, ánh xạ với StudentID.",
    "nam_vao_hoc": "Năm bắt đầu học, ánh xạ với enrollmentYear.",
    "chuyen_nganh_chon": "Chuyên ngành sinh viên đã chọn.",
    "danh_sach_mon_da_hoc": "Danh sách mã môn đã từng học, gồm cả môn đạt và chưa đạt.",
    "diem_tung_mon": "Map mã môn -> điểm hệ 10.",
    "trang_thai_dat_chua_dat": "Map mã môn -> đạt/chưa_đạt.",
    "so_tin_chi_da_tich_luy": "Tổng số tín chỉ chỉ tính cho các môn đạt.",
    "hoc_ky_hien_tai": "Học kỳ hiện tại theo ontology Semester1..Semester8.",
    "muc_tieu_hoc_tap": "Mục tiêu học tập hiện tại: Đúng hạn, Học vượt, Giảm tải."
}
for key, desc in desc_map.items():
    if key in data["field_spec"]:
        data["field_spec"][key]["description"] = desc

# 4. Update records
for record in data["records"]:
    if "chuyen_nganh_chon" in record:
        if record["chuyen_nganh_chon"]["ma"] == "CNPM":
            record["chuyen_nganh_chon"]["ten"] = "Công nghệ phần mềm"
        elif record["chuyen_nganh_chon"]["ma"] == "HTTT":
            record["chuyen_nganh_chon"]["ten"] = "Hệ thống thông tin"
        elif record["chuyen_nganh_chon"]["ma"] == "TTMMT":
            record["chuyen_nganh_chon"]["ten"] = "Truyền thông và mạng máy tính"
    
    if "muc_tieu_hoc_tap" in record:
        if record["muc_tieu_hoc_tap"] == "dung_han":
            record["muc_tieu_hoc_tap"] = "Đúng hạn"
        elif record["muc_tieu_hoc_tap"] == "hoc_vuot":
            record["muc_tieu_hoc_tap"] = "Học vượt"
        elif record["muc_tieu_hoc_tap"] == "giam_tai":
            record["muc_tieu_hoc_tap"] = "Giảm tải"

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated JSON successfully!")
