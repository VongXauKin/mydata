import os
import datetime
import math # Thư viện mới để tính toán kích thước file

# --- CẤU HÌNH ---
ROOT_DIR = "."
# Các file/thư mục cấu hình cần loại trừ
EXCLUDES = [
    '.git', '_site', '_scripts', 'node_modules', '_layouts', 
    '_config.yml', 'Gemfile', 'Gemfile.lock', 'styles.css', 
    'index.md', 'README.md', 'readme.md', 'LICENSE', 
    'index.html', 'search.json',
    
    # THÊM CÁC THƯ MỤC NẾU CHÚNG KHÔNG PHẢI LÀ NỘI DUNG
    # (Giữ nguyên vì bạn đã loại bỏ lọc)
    'documents', 
    'photos', 
    'videos' 
]
# Các phần mở rộng của file ảnh
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
# Các phần mở rộng của file video
VIDEO_EXTENSIONS = ('.mp4', '.mov', '.webm', '.ogg', '.mkv', '.avi')
# Các phần mở rộng của file tài liệu (Office & PDF)
DOCUMENT_EXTENSIONS = ('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt')
# Kết hợp TẤT CẢ các extension cần hiển thị
DISPLAY_EXTENSIONS = IMAGE_EXTENSIONS + VIDEO_EXTENSIONS + DOCUMENT_EXTENSIONS


# --- HÀM HỖ TRỢ ---

def format_file_size(size_bytes):
    """Chuyển đổi kích thước byte sang định dạng KB, MB, GB."""
    if size_bytes == 0:
        return "0 Bytes"
    size_name = ("Bytes", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    i = min(i, 4) 
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def get_file_icon(item):
    """Trả về class Font Awesome icon dựa trên phần mở rộng file."""
    ext = os.path.splitext(item)[1].lower()
    
    # Logic icon đã được tinh giản lại
    if ext in ('.jpg', '.jpeg', '.png', '.gif', '.webp'):
        return '<i class="fa-solid fa-image icon" style="color: #4CAF50;"></i>'
    elif ext in ('.mp4', '.mov', '.webm', '.ogg', '.mkv', '.avi'):
        return '<i class="fa-solid fa-video icon" style="color: #FFC107;"></i>'
    elif ext in ('.pdf',):
        return '<i class="fa-solid fa-file-pdf icon" style="color: #E60023;"></i>'
    elif ext in ('.doc', '.docx'):
        return '<i class="fa-solid fa-file-word icon" style="color: #2196F3;"></i>'
    elif ext in ('.xls', '.xlsx'):
        return '<i class="fa-solid fa-file-excel icon" style="color: #4CAF50;"></i>'
    elif ext in ('.ppt', '.pptx'):
        return '<i class="fa-solid fa-file-powerpoint icon" style="color: #FF5722;"></i>'
    elif ext in ('.txt',):
        return '<i class="fa-solid fa-file-lines icon" style="color: #9E9E9E;"></i>'
    else:
        return '<i class="fa-regular fa-file icon"></i>'


# --- HÀM TẠO INDEX CHÍNH ---

def generate_index_content(directory_path, root_dir):
    """
    Tạo file mục lục (index.html) cho một thư mục.
    """
    
    # 1. TÍNH TOÁN PERMALINK VÀ TIÊU ĐỀ
    relative_path = os.path.relpath(directory_path, root_dir).replace('\\', '/')
    current_dir_name = os.path.basename(os.path.abspath(directory_path))

    # Thiết lập Tiêu đề và Permalink
    if relative_path == '.':
        title = "Home Page" # THAY ĐỔI THEO YÊU CẦU MỚI
        permalink = "" 
    else:
        # Sử dụng tên thư mục làm tiêu đề, định dạng lại
        title = current_dir_name.replace('-', ' ').title()
        permalink = relative_path
        
    # 2. TẠO FRONT MATTER CHUẨN JEKYLL
    final_content = (
        f'---\nlayout: default\ntitle: {title}\npermalink: /{permalink}/\n---\n\n'
    )
    
    # Bắt đầu bảng
    html_table_start = f'\n'
    html_table_start += '<table class="file-table">\n<thead><tr><th>Tên File/Thư Mục</th><th>Kích Thước</th><th>Ngày Tạo/Sửa Đổi</th></tr></thead>\n<tbody>\n'
    final_content += html_table_start

    # 3. Quét thư mục và xử lý từng mục
    if os.path.exists(directory_path):
        lower_excludes = [e.lower() for e in EXCLUDES]
        
        # Sắp xếp các mục (Thư mục lên đầu)
        sorted_items = sorted(
            os.listdir(directory_path),
            key=lambda x: (not os.path.isdir(os.path.join(directory_path, x)), x.lower())
        )
        
        for item in sorted_items:
            full_path = os.path.join(directory_path, item)
            
            # --- LỌC NỘI DUNG CẤU HÌNH ---
            if item.startswith('.') or item.startswith('_') or item.lower() in lower_excludes:
                continue
                
            icon_html = ""
            
            # Nếu là thư mục
            if os.path.isdir(full_path):
                icon_html = '<i class="fa-solid fa-folder icon" style="color: #ffc107;"></i>' # Icon Thư mục
                
                # Liên kết đến thư mục con
                link = f"/{relative_path}/{item}" if relative_path != '.' else f"/{item}"
                
                # Gọi đệ quy cho thư mục con
                generate_index_content(full_path, root_dir)
                
                # Thêm Thư mục vào bảng
                final_content += f'<tr>\n'
                final_content += f'  <td class="file-name-col">{icon_html} <a href="{link}/">{item}</a></td>\n'
                final_content += f'  <td>Folder</td>\n' 
                final_content += f'  <td>{datetime.datetime.fromtimestamp(os.path.getmtime(full_path)).strftime("%d/%m/%Y %H:%M")}</td>\n' 
                final_content += f'</tr>\n'
                
            # XỬ LÝ MEDIA VÀ TÀI LIỆU (File)
            elif os.path.isfile(full_path) and item.lower().endswith(DISPLAY_EXTENSIONS):
                
                file_stats = os.stat(full_path)
                size_display = format_file_size(file_stats.st_size)
                date_modified = datetime.datetime.fromtimestamp(file_stats.st_mtime).strftime('%d/%m/%Y %H:%M')
                
                # Liên kết file
                link = f"/{relative_path}/{item}" if relative_path != '.' else f"/{item}"
                
                icon_html = get_file_icon(item) 
                
                # Thêm File vào bảng
                final_content += f'<tr>\n'
                final_content += f'  <td class="file-name-col">{icon_html} <a href="{link}" target="_blank">{item}</a></td>\n'
                final_content += f'  <td>{size_display}</td>\n'
                final_content += f'  <td>{date_modified}</td>\n'
                final_content += f'</tr>\n'

    # 4. Kết thúc nội dung và ghi file
    final_content += "</tbody>\n</table>\n"

    # Ghi file index.html
    output_path = os.path.join(directory_path, "index.html")

    os.makedirs(directory_path, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
        
    print(f"✅ Created/Updated index file: {output_path}")


# --- HÀM MAIN ---

if __name__ == "__main__":
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    print("--- Starting multi-level index generation ---")
    generate_index_content(root_dir, root_dir)
    print("--- Index generation complete ---")
