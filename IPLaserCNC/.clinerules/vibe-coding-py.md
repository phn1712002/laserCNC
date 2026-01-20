# 🐍 Python Coding Standards – General Rules

## 📋 Overview

Tài liệu này định nghĩa quy chuẩn lập trình Python chung, bao gồm: đặt tên, comment, cấu trúc hàm, tổ chức file, code style, và best practices.

---

## 🏷️ Naming Rules

### 1. Class Names

- **PascalCase**
- Ví dụ: `DataProcessor`, `UserProfile`, `ApiHandler`

### 2. Function/Method Names

- **snake_case**
- Ví dụ: `load_data`, `process_request`, `save_to_db`

### 3. Variable Names

- **snake_case**
- Ví dụ: `user_id`, `config_path`, `max_retries`

### 4. Constants

- **UPPER_SNAKE_CASE**
- Ví dụ: `MAX_CONNECTIONS`, `DEFAULT_TIMEOUT`

### 5. Private/Protected Variables

- **Prefix `_`**
- Ví dụ: `_cache`, `_is_ready`, `_registry`

---

## 💬 Commenting Rules

### 1. Docstrings

- Sử dụng **triple quotes** theo chuẩn Google hoặc NumPy style.
  python def connect(url: str, timeout: int = 30) -> bool: """ Establish a connection to a given URL. Args: url: Target URL timeout: Timeout in seconds (default = 30) Returns: True if connection succeeds, False otherwise """
  
  ### 2. Inline Comments

- Viết ngắn gọn, rõ ràng.
  python # Retry up to MAX_RETRIES if request fails for attempt in range(MAX_RETRIES): ...
  
  ### 3. TODO / FIXME
  
  python # TODO: Add support for async requests # FIXME: Handle empty input gracefully

---

## 📝 Function Writing Rules

1. **Function Signature** python def function_name(param1: Type, param2: Type = default_value) -> ReturnType: """Short description."""

2. **Type Hints**: Bắt buộc cho function public.

3. **Function Length**: Không quá 50 dòng. Chia nhỏ nếu cần.

4. **Return Values**: Rõ ràng và thống nhất kiểu trả về.

---

## 📁 File Organization Rules

### 1. Import Rules

python # Standard library import os import sys # Third-party import numpy as np import requests # Local modules from core import BaseClass from utils import load_config

### 2. File Naming

- **snake_case**
- Ví dụ: `data_loader.py`, `user_service.py`

---

## 🔧 Code Style and Formatting

- **Indentation**: 4 spaces

- **Line Length**: Tối đa 88 ký tự (theo PEP8/Black)

- **Whitespace**:
  
  - Có 1 space quanh toán tử: `a + b`
  - Không có space trong ngoặc: `func(x, y)`

---

## 🚀 Best Practices

1. **Code Reusability**
   
   - Dùng class base khi cần

2. **Maintainability**
   
   - Tránh magic numbers (thay bằng constant)
   - Đặt tên biến/hàm rõ nghĩa

3. **Extensibility**
   
   - Viết code dễ mở rộng
   - Dùng `**kwargs` khi cần hỗ trợ thêm tham số

4. **Documentation**
   
   - Đủ docstring cho function/class/module
   - Thêm ví dụ usage nếu cần

---

## 🔍 Code Review Checklist

- [ ] Đúng naming convention
- [ ] Đủ docstring
- [ ] Có type hints
- [ ] Không dùng magic numbers
- [ ] Đủ unit test
- [ ] Code dễ đọc và maintain
- [ ] Performance hợp lý (dùng NumPy/pandas vectorization khi xử lý dữ liệu lớn)
