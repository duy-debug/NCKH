import json
import csv

json_path = r"d:\NTU\CNTT\NCKH\Code\StudentDataStandardization\student_input_standard.json"
csv_path = r"d:\NTU\CNTT\NCKH\Code\StudentDataStandardization\data.csv"

name_map = {
    "SV0001": "Nguyễn Văn Anh",
    "SV0002": "Trần Thị Bình",
    "SV0005": "Lê Văn Cường",
    "SV0006": "Phạm Thị Dung",
    "SV0007": "Hoàng Văn Em",
    "SV0008": "Võ Thị Phượng",
    "SV0009": "Đặng Văn Trường",
    "SV0010": "Bùi Thị Quyên",
    "SV0011": "Đỗ Văn Trí",
    "SV0012": "Hồ Thị Linh",
    "SV0013": "Ngô Văn Bảo",
    "SV0014": "Dương Thị Hoài",
    "SV0015": "Lý Văn Hoàng"
}

# Update JSON
with open(json_path, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

# Add to required fields and spec
if "ten_sinh_vien" not in data["required_fields"]:
    data["required_fields"].insert(1, "ten_sinh_vien")
if "ten_sinh_vien" not in data["field_spec"]:
    data["field_spec"]["ten_sinh_vien"] = {
        "type": "string",
        "description": "Họ và tên sinh viên."
    }

# Update course status labels
data["controlled_values"]["course_status"] = ["Đạt", "Chưa đạt"]
desc_map = {
    "trang_thai_dat_chua_dat": "Map mã môn -> Đạt/Chưa đạt.",
}
if "trang_thai_dat_chua_dat" in data["field_spec"]:
    data["field_spec"]["trang_thai_dat_chua_dat"]["description"] = "Map mã môn -> Đạt/Chưa đạt."

for i, rule in enumerate(data.get("validation_rules", [])):
    rule = rule.replace("'dat'", "'Đạt'").replace("'chua_dat'", "'Chưa đạt'")
    data["validation_rules"][i] = rule

for record in data["records"]:
    mssv = record["mssv"]
    record["ten_sinh_vien"] = name_map.get(mssv, "Chưa cập nhật")
    
    # Needs to be ordered if we want to be clean, but dict in python 3.7+ keeps insertion order. We can just recreate it.
    new_record = {}
    new_record["mssv"] = record["mssv"]
    new_record["ten_sinh_vien"] = record["ten_sinh_vien"]
    for k, v in record.items():
        if k not in ["mssv", "ten_sinh_vien"]:
            new_record[k] = v
            
    # Modify statuses
    if "trang_thai_dat_chua_dat" in new_record:
        for course, status in new_record["trang_thai_dat_chua_dat"].items():
            if status == "dat":
                new_record["trang_thai_dat_chua_dat"][course] = "Đạt"
            elif status == "chua_dat":
                new_record["trang_thai_dat_chua_dat"][course] = "Chưa đạt"
    
    # replace record inplace in the list
    idx = data["records"].index(record)
    data["records"][idx] = new_record

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated JSON successfully!")

# Update CSV
rows = []
with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    if "ten_sinh_vien" not in fieldnames:
        fieldnames.insert(1, "ten_sinh_vien")
    
    for row in reader:
        mssv = row.get("mssv", "")
        row["ten_sinh_vien"] = name_map.get(mssv, "Chưa cập nhật")
        
        # update Statuses JSON inside the CSV cell
        sts_str = row.get("trang_thai_dat_chua_dat", "{}")
        try:
            sts = json.loads(sts_str)
            for k, v in sts.items():
                if v == "dat": sts[k] = "Đạt"
                elif v == "chua_dat": sts[k] = "Chưa đạt"
            row["trang_thai_dat_chua_dat"] = json.dumps(sts, separators=(',', ':'))
        except:
            pass
            
        rows.append(row)

with open(csv_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Updated CSV successfully!")
