import os
import datetime

# --- CẤU HÌNH ---
ROOT_DIR = "."
OUTPUT_FILE_ROOT = "index.md" 
# Các file/thư mục cấu hình cần loại trừ
EXCLUDES = [
    '.git', '_site', '_scripts', 'node_modules', '_layouts', 
    '_config.yml', 'Gemfile', 'Gemfile.lock', 'styles.css', 
    'index.md', 'README.md', 'readme.md', 'LICENSE', 
    'index.html' # Thêm index.html vào EXCLUDES cho mục đích lọc
]
# Các phần mở rộng của file ảnh
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
# Các phần mở rộng của file video
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
        f"date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" 
    )
    if back_link:
        content += f"back_link: {back_link}\n"
    content += "---\n\n"
    return content

def generate_index_content(directory_path, relative_level=0):
    """
    Tạo file mục lục (index.html hoặc index.md) cho một thư mục.
    relative_level: số cấp thư mục mà thư mục hiện tại nằm dưới thư mục gốc.
    """
    
    # Đảm bảo thư mục đích tồn tại trước khi ghi file
    if directory_path != ROOT_DIR and not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
    
    # 1. Cấu hình liên kết CSS/Quay lại
    css_path = "../" * (relative_level + 1) + "styles.css"
    
    # SỬA LỖI 404: Cố định đường dẫn Trang Chủ bằng cú pháp Jekyll
    # Jekyll sẽ thay thế {{ site.baseurl }} bằng /mydata
    back_link_path = "{{ site.baseurl }}/"
    
    if directory_path == ROOT_DIR:
        # Trang chủ
        back_link_html = ""
        output_filename = OUTPUT_FILE_ROOT
        
        # Tạo phần Front Matter và tiêu đề cho trang chủ
        content = generate_front_matter("Mục Lục Kho Lưu Trữ Tự Động", "default")
        content += (
            f"# 📂 Danh Sách Kho Lưu Trữ (Tự Động Hóa)\n\n"
            f"*Lần cập nhật cuối: {datetime.datetime.now().strftime('%H:%M:%S ngày %d/%m/%Y')}*\n\n"
            "## Liên Kết Thư Mục Chính\n\n"
            "<ul>\n"
        )
    else:
        # Mục lục thư mục con (index.html)
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
            f'  <p class="back-link"><a href="{back_link_path}">← Quay lại Trang Chủ</a></p>\n'
            f'  <ul class="file-list">\n'
        )
        # 2. Tạo HTML Back Link (Khoảng dòng 98)
        # Đây là phần tạo liên kết "Quay lại Thư Mục Cha" và "Quay lại Trang Chủ"
        parent_dir_link = "../" * (relative_level) + "index.html"
    
        # --- LOGIC ĐIỀU CHỈNH QUAN TRỌNG NHẤT (SỬA 404) ---
        if relative_level == 1:
            # Ở cấp 1 (hinh-anh-ki-niem), Thư mục Cha chính là Trang Chủ.
            # Chỉ hiển thị 1 liên kết duy nhất: Quay lại Trang Chủ (sử dụng baseurl)
            back_link_html = f'<p class="back-link"><a href="{back_link_path}">← Quay lại Trang Chủ</a></p>'
        else:
            # Ở cấp 2 trở lên (nam-2016), hiển thị cả hai.
            # Liên kết Trang Chủ vẫn là back_link_path = "{{ site.baseurl }}/"
            back_link_html = f'<p class="back-link"><a href="{parent_dir_link}">← Quay lại Thư Mục Cha</a> | <a href="{back_link_path}">← Quay lại Trang Chủ</a></p>'
    
    # 2. Quét thư mục và xử lý từng mục
    if os.path.exists(directory_path):
        # Tạo danh sách loại trừ bằng chữ thường để so sánh case-insensitive
        lower_excludes = [e.lower() for e in EXCLUDES]
        
        for item in sorted(os.listdir(directory_path)):
            full_path = os.path.join(directory_path, item)
            
            # --- SỬA LỖI LỌC NỘI DUNG (Ẩn README.md/index.html ở mọi cấp) ---
            # Loại trừ các file/thư mục cấu hình (bắt đầu bằng dấu chấm hoặc gạch dưới)
            if item.startswith('.') or item.startswith('_') or item.lower() in lower_excludes:
                continue
            
            # Nếu là thư mục
            if os.path.isdir(full_path):
                # ... (Logic gọi đệ quy giữ nguyên) ...
                if directory_path == ROOT_DIR:
                    # Cấp 1: tên thư mục
                    nested_dir = item
                    link = f'<a href="{nested_dir}/">{item}</a>'
                    content += f'  <li>📁 {link}</li>\n'
                    # Gọi đệ quy cho thư mục con (cấp độ 1)
                    generate_index_content(full_path, relative_level=1)
                else:
                    # Cấp sâu hơn: Đường dẫn là directory_path/item
                    nested_dir = os.path.join(directory_path, item)
                    link = f'<a href="{item}/">{item}</a>'
                    content += f'  <li>📁 {link}</li>\n'
                    # Gọi đệ quy cho thư mục con (cấp độ tăng lên)
                    generate_index_content(full_path, relative_level + 1)
            
            # Nếu là file media (Ảnh & Video)
            elif os.path.isfile(full_path) and item.lower().endswith(MEDIA_EXTENSIONS):
                # ... (Phần xử lý media giữ nguyên) ...
                link = f'<a href="{item}" target="_blank">{item}</a>'
                
                if item.lower().endswith(IMAGE_EXTENSIONS):
                    media_tag = f'<img src="{item}" alt="{item}" style="max-width: 300px; display: block; border: 1px solid #ccc;">'
                    icon = "🖼️"
                elif item.lower().endswith(VIDEO_EXTENSIONS):
                    file_extension = item.split('.')[-1]
                    media_tag = (
                        f'<video controls style="max-width: 500px; display: block; border: 1px solid #ccc;">'
                        f'<source src="{item}" type="video/{file_extension}">'
                        f'Trình duyệt của bạn không hỗ trợ video.'
                        f'</video>'
                    )
                    icon = "🎬"
                else:
                    continue 

                # Thêm vào file mục lục
                if directory_path != ROOT_DIR:
                    content += f'    <li class="media-item">\n'
                    content += f'      <p>{icon} {link}</p>\n'
                    content += f'      {media_tag}\n'
                    content += f'    </li>\n'
                
            # Nếu là file khác (ví dụ: .pdf, .docx,...) 
            elif os.path.isfile(full_path):
                # Phần này được giữ lại để hiển thị các file tài liệu khác (nếu cần)
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
    print("--- Starting multi-level index generation ---")
    generate_index_content(ROOT_DIR, 0)
    print("--- Index generation complete ---")
