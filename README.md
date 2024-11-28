# DoAn_MMT_NTTrung_2024

**Đồ án Điều khiển máy tính từ xa, lớp Mạng Máy Tính, học kỳ 1 Năm học 2024-2025 - HCMUS**

    Thành viên: Nguyễn Thế Trung - MSSV: 23880092 - Đóng góp: 100%

Đã hoàn thành tất cả các chức năng:

   1.	List / Start / Stop các Applications đang chạy SERVER 
   2.	List / Start / Stop Services (Processes) đang chạy SERVER 
   3.	Shutdown / Reset máy SERVER 
   4.	Xem màn hình hiện thời của máy SERVER 
   5.	Khóa / Bắt phím nhấn (keylogger) ở máy SERVER 
   6.	Xóa files ; Copy files từ máy SERVER

_________________________________________________________________________________________
*Hướng dẫn cài đặt chương trình và các thư viện trên máy thật và máy ảo:
    
- Cài đặt **python 3.12.7 trở xuống**:
  + Đường link file cài đặt python:
  
        https://www.python.org/downloads/windows/
    
  + Cài đặt thư viện thêm các **thư viện cho python**: vidstream, pynput, keyboard **bằng cmd**:
        
        pip install vidstream pynput keyboard
    
- Cài đặt **git bash**:
  + Đường link file cài đặt git bash:
  
        https://git-scm.com/downloads/win
    
  + Git clone đồ án về **bằng git bash**:
        
        git clone https://github.com/Royalthneu/DoAn_MMT_NTTrung_2024.git   

- Trên máy ảo với vai trò máy server, chạy file **server.py**: 
  + Truy cập folder server trên máy ảo vừa clone về và chạy file server.py **bằng cmd**:
         
         python server.py
  
- Trên máy thật với vai trò máy client, chạy file **client.py**:
  + Trên máy ảo, Truy cập folder client trên máy thật vừa clone về và chạy file client.py **bằng cmd**:
         
         python client.py

* Mô tả chương trình và Hướng dẫn sử dụng: ... đường link

