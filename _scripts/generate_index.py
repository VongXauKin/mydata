import os
import datetime

# --- CẤU HÌNH ---
ROOT_DIR = "."
OUTPUT_FILE_ROOT = "index.md" 
# Các file/thư mục cấu hình cần loại trừ
EXCLUDES = [
    '.git', '_site', '_scripts', 'node_modules', '_layouts', 
    '_config.yml', 'Gemfile', 'Gemfile.lock', 'styles.css', 
    'index.md', 'README.md', 'LICENSE'
]
# Các phần mở rộng của file ảnh
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
# Các phần mở rộng của file video (ĐÃ THÊM)
VIDEO_EXTENSIONS = ('.mp4', '.mov', '.webm', '.ogg', '.mkv', '.avi')

# Kết hợp cả hai để quét
MEDIA_EXTENSIONS = IMAGE_EXTENSIONS + VIDEO_EXTENSIONS 

# --- HÀM TẠO CẤU TRÚC HTML/MARKDOWN ---

def generate_front_matter(title, layout, back_link=None):
    """Tạo phần Front Matter cho Jekyll."""
    content = (
        "---\n"
        f"layout: {layout}\n"
        f"title: {title}\n"
        f"date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S +0700')}\n"
    )
    if back_link:
        content += f"back_link: {back_link}\n"
    content += "---\n\n"
    return content

def generate_index_content(directory_path, relative_level=0):
    """
    Tạo file mục lục (index.html hoặc index.md) cho một thư mục.
    """
    
    # 1. Cấu hình liên kết CSS/Quay lại
    css_path = "../" * (relative_level + 1) + "styles.css"
    back_link_path = "../" * relative_level + "index.md" 
    
    if directory_path == ROOT_DIR:
        back_link_html = ""
        output_filename = OUTPUT_FILE_ROOT
        
        # Tạo phần Front Matter và tiêu đề cho trang chủ
        content = generate_front_matter("Mục Lục Kho Lưu Trữ Tự Động", "default")
        content += (
            f"# 📂 Danh Sách Kho Lưu Trữ (Tự Động Hóa)\n\n"
            f"*Lần cập nhật cuối: {datetime.datetime.now().strftime('%H:%M:%S ngày %d/%m/%Y')} (Giờ Việt Nam)*\n\n"
            "## Liên Kết Thư Mục Chính\n\n"
            "<ul>\n"
        )
    else:
        # Mục lục thư mục con sử dụng HTML và Back Link
        output_filename = os.path.join(directory_path, "index.html")
        folder_name = os.path.basename(directory_path)
        
        content = (
            f'---\nlayout: default\ntitle: Mục lục {folder_name}\n---\n'
            f'<link rel="stylesheet" href="{css_path}">\n'
            f'<header>\n'
            f'  <h1>🖼️ {folder_name}</h1>\n'
            f'</header>\n\n'
            f'<section id="directory">\n'
            f'  <h2>Danh Sách Nội Dung</h2>\n'
            f'  <p class="back-link"><a href="{back_link_path}">← Quay lại Mục lục</a></p>\n'
            f'  <ul class="file-list">\n'
        )
        back_link_html = f'<p class="back-link"><a href="{back_link_path}">← Quay lại Mục lục</a></p>'

    
    # 2. Quét thư mục và xử lý từng mục
    if os.path.exists(directory_path):
        for item in sorted(os.listdir(directory_path)):
            full_path = os.path.join(directory_path, item)
            
            # Loại trừ các file/thư mục cấu hình (bắt đầu bằng dấu chấm hoặc gạch dưới)
            if item.startswith('.') or item.startswith('_') or item in EXCLUDES:
                continue
            
            if os.path.isdir(full_path):
                # Nếu là thư mục, tạo liên kết và gọi đệ quy để tạo index.html bên trong
                if directory_path == ROOT_DIR:
                    link = f'<a href="{item}/">{item}</a>'
                    content += f'  <li>📁 {link}</li>\n'
                    generate_index_content(full_path, relative_level=1)
                else:
                    link = f'<a href="{item}/">{item}</a>'
                    content += f'  <li>📁 {link}</li>\n'
                    generate_index_content(full_path, relative_level + 1)

            elif os.path.isfile(full_path) and item.lower().endswith(MEDIA_EXTENSIONS):
                # --- PHẦN XỬ LÝ MEDIA MỚI ---
                link = f'<a href="{item}" target="_blank">{item}</a>'
                
                # Xác định loại media và tạo thẻ HTML tương ứng
                if item.lower().endswith(IMAGE_EXTENSIONS):
                    media_tag = f'<img src="{item}" alt="{item}" style="max-width: 300px; display: block; border: 1px solid #ccc;">'
                elif item.lower().endswith(VIDEO_EXTENSIONS):
                    # Tạo thẻ <video> với thuộc tính controls để người dùng có thể phát
                    file_extension = item.split('.')[-1]
                    media_tag = (
                        f'<video controls style="max-width: 500px; display: block; border: 1px solid #ccc;">'
                        f'<source src="{item}" type="video/{file_extension}">'
                        f'Trình duyệt của bạn không hỗ trợ video.'
                        f'</video>'
                    )
                else:
                    continue # Bỏ qua nếu không phải ảnh hoặc video

                # Thêm vào file mục lục
                if directory_path != ROOT_DIR:
                    content += f'    <li class="media-item">\n'
                    content += f'      <p>🎬 {link}</p>\n'
                    content += f'      {media_tag}\n'
                    content += f'    </li>\n'
                
            elif os.path.isfile(full_path):
                # Nếu là file khác, tạo liên kết file
                link = f'<a href="{item}" target="_blank">{item}</a>'
                if directory_path == ROOT_DIR:
                    content += f'  <li>📄 {link}</li>\n'
                else:
                    content += f'  <li>📄 {link}</li>\n'


    # 3. Kết thúc nội dung và ghi file
    if directory_path == ROOT_DIR:
        content += "</ul>\n"
    else:
        content += "  </ul>\n"
        content += "</section>\n"
        content += back_link_html + '\n' # Thêm link quay lại
        content += '<footer>\n  <p>&copy; 2025 Data Repository.</p>\n</footer>\n'
        
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Created/Updated index file: {output_filename}")


if __name__ == "__main__":
    print("--- Starting multi-level index generation ---") # <--- ĐÃ SỬA
    generate_index_content(ROOT_DIR, 0)
    print("--- Index generation complete ---")
