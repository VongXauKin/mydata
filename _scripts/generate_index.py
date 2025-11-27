import os
import datetime
import math # Thư viện mới để tính toán kích thước file

# --- CẤU HÌNH ---
ROOT_DIR = "."
OUTPUT_FILE_ROOT = "index.md" 
# Các file/thư mục cấu hình cần loại trừ
EXCLUDES = [
    '.git', '_site', '_scripts', 'node_modules', '_layouts', 
    '_config.yml', 'Gemfile', 'Gemfile.lock', 'styles.css', 
    'index.md', 'README.md', 'readme.md', 'LICENSE', 
    'index.html'
]
# Các phần mở rộng của file ảnh
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
# Các phần mở rộng của file video
VIDEO_EXTENSIONS = ('.mp4', '.mov', '.webm', '.ogg', '.mkv', '.avi')

# BỔ SUNG: Các phần mở rộng của file tài liệu (Office & PDF)
DOCUMENT_EXTENSIONS = ('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt')

# Kết hợp TẤT CẢ các extension cần hiển thị
DISPLAY_EXTENSIONS = IMAGE_EXTENSIONS + VIDEO_EXTENSIONS + DOCUMENT_EXTENSIONS

# --- HÀM HỖ TRỢ ---

def format_file_size(size_bytes):
    """Chuyển đổi kích thước byte sang định dạng KB, MB, GB."""
    if size_bytes == 0:
        return "0 Bytes"
    # Các đơn vị đo lường
    size_name = ("Bytes", "KB", "MB", "GB", "TB")
    # Tính index của đơn vị
    i = int(math.floor(math.log(size_bytes, 1024)))
    # Giới hạn index tối đa là 4 (TB)
    i = min(i, 4) 
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def get_file_icon(item):
    """
    Trả về class Font Awesome icon dựa trên phần mở rộng file.
    YÊU CẦU: Thêm thư viện Font Awesome vào default.html
    """
    ext = os.path.splitext(item)[1].lower()
    
    if ext in ('.jpg', '.jpeg', '.png', '.gif', '.webp'):
        return '<i class="fa-regular fa-image icon" style="color: #4CAF50;"></i>' # Ảnh
    elif ext in ('.mp4', '.mov', '.webm', '.ogg', '.mkv', '.avi'):
        return '<i class="fa-solid fa-video icon" style="color: #FFC107;"></i>' # Video
    elif ext in ('.pdf',):
        return '<i class="fa-solid fa-file-pdf icon" style="color: #E60023;"></i>' # PDF
    elif ext in ('.doc', '.docx'):
        return '<i class="fa-solid fa-file-word icon" style="color: #2196F3;"></i>' # Word
    elif ext in ('.xls', '.xlsx'):
        return '<i class="fa-solid fa-file-excel icon" style="color: #4CAF50;"></i>' # Excel
    elif ext in ('.ppt', '.pptx'):
        return '<i class="fa-solid fa-file-powerpoint icon" style="color: #FF5722;"></i>' # PowerPoint
    elif ext in ('.txt',):
        return '<i class="fa-solid fa-file-lines icon" style="color: #9E9E9E;"></i>' # Text
    else:
        return '<i class="fa-regular fa-file icon"></i>' # File chung

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
    """
    
    # ... (Phần tạo thư mục đích và back_link_path giữ nguyên) ...
    if directory_path != ROOT_DIR and not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
    
    # 1. Cấu hình liên kết CSS/Quay lại
    css_path = "../" * (relative_level + 1) + "styles.css"
    back_link_path = "{{ site.baseurl }}/"
    
    # ... (Logic tạo Front Matter và Tiêu đề Trang Chủ giữ nguyên) ...
    if directory_path == ROOT_DIR:
        # Trang chủ
        back_link_html = ""
        output_filename = OUTPUT_FILE_ROOT
        
        # Tạo phần Front Matter và tiêu đề cho trang chủ
        content = generate_front_matter("Mục Lục Kho Lưu Trữ Tự Động", "default")
        content += (
            f"# 📂 Danh Sách Kho Lưu Trữ (Tự Động Hóa)\n\n"
            f"*Lần cập nhật cuối: {datetime.datetime.now().strftime('%H:%M:%S ngày %d/%m/%Y')}*\n\n"
            f"## Liên Kết Thư Mục Chính\n\n"
        )
        # Bắt đầu bảng cho Trang Chủ (Chỉ hiển thị tên)
        content += '<table class="file-table">\n<thead><tr><th>Tên Thư Mục</th><th>Kích Thước</th><th>Ngày Tạo/Sửa Đổi</th></tr></thead>\n<tbody>\n'
    else:
        # Mục lục thư mục con (index.html)
        output_filename = os.path.join(directory_path, "index.html")
        folder_name = os.path.basename(directory_path)
        
        # CHÚ Ý: Cần chỉnh lại Layout default.html để thêm các thẻ div .container, .sidebar, .main-content
        content = (
            f'---\nlayout: default\ntitle: Mục lục {folder_name}\n---\n'
            f'<div class="header-bar"><div class="title">Tài liệu và Hình ảnh</div></div>\n'
            f'<h2>Danh Sách Nội Dung: {folder_name}</h2>\n'
        )
        
        # Bắt đầu bảng cho Thư mục con
        content += '<table class="file-table">\n<thead><tr><th>Tên File</th><th>Kích Thước</th><th>Ngày Tạo/Sửa Đổi</th></tr></thead>\n<tbody>\n'
        
        # 2. Tạo HTML Back Link (Giữ nguyên logic)
        parent_dir_link = "../" * (relative_level) + "index.html"
        
        if relative_level == 1:
            back_link_html = f'<p class="back-link"><a href="{back_link_path}">← Quay lại Trang Chủ</a></p>'
        else:
            back_link_html = f'<p class="back-link"><a href="{parent_dir_link}">← Quay lại Thư Mục Cha</a> | <a href="{back_link_path}">← Quay lại Trang Chủ</a></p>'

    
    # 3. Quét thư mục và xử lý từng mục
    if os.path.exists(directory_path):
        lower_excludes = [e.lower() for e in EXCLUDES]
        
        for item in sorted(os.listdir(directory_path)):
            full_path = os.path.join(directory_path, item)
            
            # --- LỌC NỘI DUNG ---
            if item.startswith('.') or item.startswith('_') or item.lower() in lower_excludes:
                continue
            
            # Khởi tạo các giá trị cho hàng bảng
            size_display = "-"
            date_modified = "-"
            link = ""
            icon_html = ""
            
            # Nếu là thư mục
            if os.path.isdir(full_path):
                icon_html = '<i class="fa-solid fa-folder icon" style="color: #ffc107;"></i>' # Icon Thư mục
                
                if directory_path == ROOT_DIR:
                    # Cấp 1: tên thư mục
                    link = f'<a href="{item}/">{item}</a>'
                    # Gọi đệ quy cho thư mục con (cấp độ 1)
                    generate_index_content(full_path, relative_level=1)
                else:
                    # Cấp sâu hơn: Đường dẫn là directory_path/item
                    link = f'<a href="{item}/">{item}</a>'
                    # Gọi đệ quy cho thư mục con (cấp độ tăng lên)
                    generate_index_content(full_path, relative_level + 1)
                
                # CHÚ Ý: Thư mục được thêm vào bảng
                content += f'<tr>\n'
                content += f'  <td class="file-name-col">{icon_html} {link}</td>\n'
                content += f'  <td>-</td>\n' # Thư mục không hiển thị kích thước
                content += f'  <td>-</td>\n' # Thư mục không hiển thị ngày
                content += f'</tr>\n'
            
            # --- XỬ LÝ MEDIA VÀ TÀI LIỆU (File) ---
            elif os.path.isfile(full_path) and item.lower().endswith(DISPLAY_EXTENSIONS):
                
                # Lấy kích thước và ngày tháng
                file_stats = os.stat(full_path)
                size_display = format_file_size(file_stats.st_size)
                date_modified = datetime.datetime.fromtimestamp(file_stats.st_mtime).strftime('%d/%m/%Y %H:%M')
                
                link = f'<a href="{item}" target="_blank">{item}</a>'
                icon_html = get_file_icon(item) # Lấy icon dựa trên loại file
                
                # CHÚ Ý: File được thêm vào bảng
                content += f'<tr>\n'
                content += f'  <td class="file-name-col">{icon_html} {link}</td>\n'
                content += f'  <td>{size_display}</td>\n'
                content += f'  <td>{date_modified}</td>\n'
                content += f'</tr>\n'

            # Khối else cuối cùng: Bỏ qua các file không thuộc display_extensions.
            else:
                 continue

    # 4. Kết thúc nội dung và ghi file
    # CHÚ Ý: Thay đổi để kết thúc thẻ <table>
    if directory_path == ROOT_DIR:
        content += "</tbody>\n</table>\n"
    else:
        content += "</tbody>\n</table>\n" # Kết thúc bảng
        content += "</section>\n" # Giữ nguyên nếu bạn dùng section
        content += back_link_html + '\n' # Thêm link quay lại
        content += '<footer>\n  <p>&copy; 2025 Data Repository.</p>\n</footer>\n'
        
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Created/Updated index file: {output_filename}")


if __name__ == "__main__":
    print("--- Starting multi-level index generation ---")
    generate_index_content(ROOT_DIR, 0)
    print("--- Index generation complete ---")
