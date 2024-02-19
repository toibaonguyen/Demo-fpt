Bước 1: Cài đặt python 3.12.1
Bước 2: Clone source này về
Bước 3: Mở terminal và chạy các lệnh sau để tạo môi trường ảo:
  py -3.12.1 -m pip install virtualenv
  py -3.12.1 -m virtualenv venv
Bước 4: Kích hoạt môi trường ảo bằng lệnh sau:
  venv\Scripts\activate
Bước 5: Chạy các lệnh sau để cài các thư viện cần thiết:
  pip install opencv-python
  pip install numpy
  pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
  pip install easyocr
Bước 6: Cài các extension sau:
![image](https://github.com/toibaonguyen/Demo-fpt/assets/103349629/13596372-affa-4041-bf17-edd364d9f75b)
Bước 7: Bỏ ảnh đúng format của table vào thư mục images:
![image](https://github.com/toibaonguyen/Demo-fpt/assets/103349629/e4486fff-5d73-49be-a846-8ad1f5350466)
Bước 8: Đặt giá trị đường dẫn của ảnh vào biến path_to_image trong file main.py:
![image](https://github.com/toibaonguyen/Demo-fpt/assets/103349629/a4e6709b-2a6e-4aa7-a848-fa2fc2764f6d)
Bước 9: Chạy file main.py dựa vào nút sau hoặc có thể sử dụng cmd để chạy:
![image](https://github.com/toibaonguyen/Demo-fpt/assets/103349629/302530c8-6b4f-445c-864b-30100ca4586e)
Bước 10: Kiểm tra output trong file output.txt:
![image](https://github.com/toibaonguyen/Demo-fpt/assets/103349629/2fed226b-0f83-4422-a522-6ce933056b1e)

* CHÚ THÍCH:
- Các ảnh bên trong folder process_images là các ảnh ghi lại quá trình chuyển đổi của ảnh:
![image](https://github.com/toibaonguyen/Demo-fpt/assets/103349629/0f3a613b-53fc-4af5-9eff-a81ef73e03a7)
- Các ảnh bên trong folder ocr_slices là các ảnh được cắt nhỏ ra từ bảng để thực hiện việc đưa vào model ocr để detect text
![image](https://github.com/toibaonguyen/Demo-fpt/assets/103349629/7bc90215-9214-47de-bef4-3806df41100b)

* LƯU Ý:
- Format đúng của ảnh phải là một bảng hình chữ nhật gồm N hàng x M cột và các đoạn text, trong mỗi ô nhỏ hình chữ nhật không được quá sát nhau để tránh gây ra vấn đề khi lọc ô:
+ Dưới đây là 2 mẫu chuẩn có thể sử dụng:
  ![image](https://github.com/toibaonguyen/Demo-fpt/assets/103349629/105ab9e5-72c7-4f56-8558-47d1e2398c62)
  ![image](https://github.com/toibaonguyen/Demo-fpt/assets/103349629/18696036-f91b-47c5-a836-06b13e397f95)
+ Dưới đây là mẫu không được:
  ![image](https://github.com/toibaonguyen/Demo-fpt/assets/103349629/5c2b77fb-eca9-4b1f-b601-17cb50bd4a3b)
  Lý do là vì các text trong ô của 2 cột sau quá sát nhau:
  ![image](https://github.com/toibaonguyen/Demo-fpt/assets/103349629/e84b82ae-2d36-4217-88fe-10bc6ea0c505)
- Ngoài ra có thể sử dụng những model ocr tiếng việt khác để thay thế khi detect text trong từng ô.


  


  







