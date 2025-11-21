import os

# Đường dẫn của thư mục gốc cần quét
ROOT_DIR = "." # Quét từ thư mục hiện tại (gốc repo)
OUTPUT_FILE = "index.md" # File đầu ra cho Jekyll

# Các thư mục/file cần loại trừ khỏi danh sách (cấu hình Jekyll và script)
EXCLUDES = ['.git', '_site', '_scripts', 'node_modules', '_layouts', 'Gemfile', '_config.yml', 'styles.css', 'index.md']

def generate_markdown():
    markdown_content = (
        "---\n"
        "layout: default\n"
        "title: Trang Chủ Tự Động\n"
        "---\n\n"
        "# 📂 Danh Sách Kho Lưu Trữ (Tự Động Hóa)\n\n"
        "Đây là danh sách các thư mục cấp 1 được tạo tự động sau mỗi lần cập nhật Repository.\n\n"
        "## Liên Kết Thư Mục Chính\n\n"
        "<ul>\n"
    )

    # Quét nội dung thư mục gốc
    for item in sorted(os.listdir(ROOT_DIR)):
        if item in EXCLUDES or item.startswith('.'):
            continue
        
        # Kiểm tra xem có phải là thư mục hay không
        if os.path.isdir(os.path.join(ROOT_DIR, item)):
            # Tạo liên kết cho thư mục
            link = f'<a href="{item}/index.html">{item}</a>'
            markdown_content += f'  <li>{link} (Thư mục)</li>\n'
        else:
            # Tạo liên kết cho file (nếu bạn muốn liệt kê file ở trang chủ)
            link = f'<a href="{item}">{item}</a>'
            markdown_content += f'  <li>{link} (File)</li>\n'

    markdown_content += "</ul>\n"
    
    # Ghi nội dung vào file index.md
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

if __name__ == "__main__":
    generate_markdown()
