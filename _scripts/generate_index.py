import os
import datetime

# Đường dẫn của thư mục gốc cần quét
ROOT_DIR = "."
OUTPUT_FILE = "index.md" 

# Các thư mục/file cần loại trừ (tất cả các file/thư mục cấu hình)
EXCLUDES = ['.git', '_site', '_scripts', 'node_modules', '_layouts', '_config.yml', 'Gemfile', 'Gemfile.lock', 'styles.css', 'index.md']

def generate_markdown():
    # 1. Phần cấu hình Jekyll (Front Matter)
    markdown_content = (
        "---\n"
        "layout: default\n"
        "title: Mục Lục Kho Lưu Trữ Tự Động\n"
        f"date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S +0700')}\n"
        "---\n\n"
        "# 📂 Danh Sách Kho Lưu Trữ (Tự Động Hóa)\n\n"
        "Đây là danh sách các thư mục cấp 1 được tạo tự động sau mỗi lần cập nhật Repository.\n"
        f"*Lần cập nhật cuối: {datetime.datetime.now().strftime('%H:%M:%S ngày %d/%m/%Y')} (Giờ Việt Nam)*\n\n"
        "## Liên Kết Thư Mục Chính\n\n"
        "<ul>\n"
    )

    # 2. Quét nội dung thư mục gốc
    # Lấy danh sách các mục cấp 1, sắp xếp theo thứ tự
    for item in sorted(os.listdir(ROOT_DIR)):
        
        # Bỏ qua các file ẩn (bắt đầu bằng dấu chấm) và các file cấu hình
        if item.startswith('.') or item in EXCLUDES or item.startswith('_'):
            continue
        
        # Đảm bảo chỉ tạo liên kết cho các thư mục hoặc file cấp 1
        if os.path.isdir(os.path.join(ROOT_DIR, item)):
            # Thư mục: Liên kết đến /<tên_thư_mục>/ (Jekyll/Pages sẽ tìm index.html/md bên trong)
            link = f'<a href="{item}/">{item}</a>'
            markdown_content += f'  <li>📁 {link}</li>\n'
        else:
            # File: Liên kết trực tiếp đến file
            link = f'<a href="{item}">{item}</a>'
            markdown_content += f'  <li>📄 {link}</li>\n'

    markdown_content += "</ul>\n"
    
    # 3. Ghi nội dung vào file index.md
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

if __name__ == "__main__":
    generate_markdown()
