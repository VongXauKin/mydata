import os
import datetime

# --- CẤU HÌNH ---

# Các file/thư mục cấu hình cần loại trừ khỏi việc xử lý index
EXCLUDES = [
    '.git', '_site', '_scripts', 'node_modules', '_layouts', 
    '_config.yml', 'Gemfile', 'Gemfile.lock', 'styles.css', 
    'index.md', 'README.md', 'readme.md', 'LICENSE', 
    'index.html', 'search.json',
    
    # THƯ MỤC NỘI DUNG MỚI (Cần được loại trừ để script không xóa chúng)
    'documents', 
    'photos', 
    'videos' 
]

# --- ĐỊNH NGHĨA BỘ LỌC FILE TYPES ---

# Office Documents
DOCUMENT_EXTENSIONS = (
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.txt', '.rtf'
)

# Images
PHOTO_EXTENSIONS = (
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'
)

# Videos
VIDEO_EXTENSIONS = (
    '.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm'
)

# --- THÔNG TIN CHUNG ---

# Template YAML Front Matter
FRONT_MATTER = """---
layout: default
title: Mục lục {title}
permalink: /{path}/
---
"""

# Template HTML
HTML_TEMPLATE_START = """
<table class="file-table">
    <thead>
        <tr>
            <th>Name</th>
            <th>Size</th>
            <th>Last Modified</th>
        </tr>
    </thead>
    <tbody>
"""

HTML_TEMPLATE_END = """
    </tbody>
</table>
"""

# Định nghĩa Icon cho các loại file và thư mục
ICONS = {
    'folder': 'fa-folder',
    'file': 'fa-file',
    'pdf': 'fa-file-pdf',
    'doc': 'fa-file-word',
    'docx': 'fa-file-word',
    'xls': 'fa-file-excel',
    'xlsx': 'fa-file-excel',
    'ppt': 'fa-file-powerpoint',
    'pptx': 'fa-file-powerpoint',
    'zip': 'fa-file-archive',
    'rar': 'fa-file-archive',
    '7z': 'fa-file-archive',
    'jpg': 'fa-file-image',
    'jpeg': 'fa-file-image',
    'png': 'fa-file-image',
    'gif': 'fa-file-image',
    'mp4': 'fa-file-video',
    'mov': 'fa-file-video',
    'avi': 'fa-file-video',
    'mp3': 'fa-file-audio',
    'wav': 'fa-file-audio',
    'txt': 'fa-file-alt',
    'md': 'fa-file-alt',
    'html': 'fa-file-code',
    'css': 'fa-file-code',
    'js': 'fa-file-code',
    'py': 'fa-file-code'
}

# --- CÁC HÀM HỖ TRỢ ---

def get_icon(filename, is_dir=False):
    """Trả về lớp icon Font Awesome dựa trên loại file/thư mục."""
    if is_dir:
        return ICONS['folder']
    
    # Lấy phần mở rộng file
    ext = os.path.splitext(filename)[1].lstrip('.').lower()
    return ICONS.get(ext, ICONS['file'])

def get_file_size(size_bytes):
    """Chuyển đổi kích thước byte thành định dạng dễ đọc (KB, MB, GB)."""
    if size_bytes < 1024:
        return f"{size_bytes} Bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def get_last_modified(timestamp):
    """Chuyển đổi timestamp thành định dạng ngày tháng dễ đọc."""
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# --- HÀM TẠO INDEX CHÍNH ---

def generate_index(directory, root_dir):
    """Tạo file index.html cho thư mục đã cho."""
    
    # Lấy tên thư mục hiện tại và đường dẫn tương đối
    current_dir_name = os.path.basename(os.path.abspath(directory))
    relative_path = os.path.relpath(directory, root_dir).replace('\\', '/')
    
    # Thiết lập bộ lọc file rỗng
    file_filter = None 

    # ÁP DỤNG BỘ LỌC DỰA TRÊN ĐƯỜNG DẪN TƯƠNG ĐỐI
    # LƯU Ý: relative_path == '.' là thư mục gốc (My Files)
    if relative_path == 'documents':
        file_filter = DOCUMENT_EXTENSIONS
    elif relative_path == 'photos':
        file_filter = PHOTO_EXTENSIONS
    elif relative_path == 'videos':
        file_filter = VIDEO_EXTENSIONS
    
    # Tiêu đề cho YAML Front Matter (Sửa lại để dễ quản lý hơn)
    if relative_path == '.':
        title = "My Files"
        permalink = "" # Trang chủ
    else:
        # Sử dụng tên thư mục làm tiêu đề, nhưng định dạng lại
        title = current_dir_name.replace('-', ' ').title()
        permalink = relative_path
        
    # Bắt đầu nội dung HTML
    html_content = HTML_TEMPLATE_START
    
    # Lấy danh sách các mục (files và folders)
    try:
        items = os.listdir(directory)
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
        return
        
    # Sắp xếp các mục (Thư mục lên đầu)
    sorted_items = sorted(
        items,
        key=lambda x: (not os.path.isdir(os.path.join(directory, x)), x.lower())
    )
    
    # Lặp qua các mục
    for item in sorted_items:
        if item in EXCLUDES or item.startswith('.'):
            continue
            
        item_path = os.path.join(directory, item)
        is_dir = os.path.isdir(item_path)
        
        # Xử lý thư mục
        if is_dir:
            # Liên kết đến thư mục con
            link = f"/{relative_path}/{item}" if relative_path != '.' else f"/{item}"
            
            # Tự động gọi đệ quy để tạo index cho thư mục con
            generate_index(item_path, root_dir)
            
            # Thêm dòng cho thư mục vào bảng
            html_content += f"""
            <tr>
                <td class="file-name-col">
                    <i class="fas {get_icon(item, is_dir=True)} icon"></i>
                    <a href="{link}/">{item}</a>
                </td>
                <td>Folder</td>
                <td>{get_last_modified(os.path.getmtime(item_path))}</td>
            </tr>
            """
            
        # Xử lý file
        else:
            # KIỂM TRA BỘ LỌC FILE: Nếu có bộ lọc và file không khớp, bỏ qua
            ext = os.path.splitext(item)[1].lower()
            if file_filter and ext not in file_filter:
                continue
                
            # Tạo liên kết file
            link = f"/{relative_path}/{item}" if relative_path != '.' else f"/{item}"
            
            # Kích thước và ngày chỉnh sửa
            size = get_file_size(os.path.getsize(item_path))
            modified = get_last_modified(os.path.getmtime(item_path))
            
            # Thêm dòng cho file vào bảng
            html_content += f"""
            <tr>
                <td class="file-name-col">
                    <i class="fas {get_icon(item)} icon"></i>
                    <a href="{link}">{item}</a>
                </td>
                <td>{size}</td>
                <td>{modified}</td>
            </tr>
            """

    # Kết thúc nội dung HTML
    html_content += HTML_TEMPLATE_END
    
    # Tạo nội dung file index.html
    final_content = (
        FRONT_MATTER.format(title=title, path=permalink) +
        html_content
    )
    
    # Ghi file index.html
    output_dir = directory
    output_path = os.path.join(output_dir, 'index.html')
    
    # Đảm bảo thư mục tồn tại
    os.makedirs(output_dir, exist_ok=True)
    
    # Ghi file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
        
    print(f"Generated index for: {output_path}")


# --- HÀM MAIN ---

def main():
    """Hàm chính để bắt đầu quá trình tạo index."""
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    print(f"Starting index generation in: {root_dir}")
    generate_index(root_dir, root_dir)

if __name__ == '__main__':
    main()
