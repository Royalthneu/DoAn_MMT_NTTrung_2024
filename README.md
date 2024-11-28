# DoAn_MMT_NTTrung_2024

Đồ án Điều khiển máy tính từ xa - Nhóm 27, lớp Mạng Máy Tính, học kỳ 1 Năm học 2024-2025

Thành viên: Nguyễn Thế Trung - MSSV: 23880092 - Đóng góp: 100%

Đã hoàn thành chức năng:
1.	List / Start / Stop các Applications đang chạy SERVER
2.	List / Start / Stop Services (Processes) đang chạy SERVER
3.	Shutdown / Reset máy SERVER
4.	Xem màn hình hiện thời của máy SERVER
5.	Khóa / Bắt phím nhấn (keylogger) ở máy SERVER
6.	Xóa files ; Copy files từ máy SERVER
_________________________________________________________________________________________
Hướng dẫn cài đặt ứng dụng trên máy thật và máy ảo
- Cài đặt python 3.12.7 trở xuống;
- Cài đặt thư viện thêm các thư viện cho python (lệnh pip install):
    + vidstream 
    + pynput 
    + keyboard
- Copy folder server trên máy ảo và chạy file main.py trong môi trường cmd bằng câu lệnh: python main.py sẽ xuất hiện Giao diện RUN SERVER
- Copy folder client trên máy ảo và chạy file main.py trong môi trường cmd bằng câu lệnh: python main.py sẽ xuất hiện Giao diện RUN CLIENT

Hướng dẫn mở kết nối server và sử dụng:
- Nhấn button "Open Server" để mở cho phép kết nối từ server. Sau khi Kết nối được mở sẽ xuất hiện Server IP và Server Por trong giao diện RUN SERVER

Hướng dẫn kết nối client với server và sử dụng:
- Đảm bảo Server đã được Open và có thông tin Server IP và Server Port
- Nhập IP của server
- Nhập Port của server
- Nhấn button "Kết nối server". Server kết nối thành công khi có Thông báo: Kết nối thành công đến server và các Button không còn bị vô hiệu hóa
- Thực hiện các chức năng của button

