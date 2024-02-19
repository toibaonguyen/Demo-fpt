								=====================Lưu ý======================
Source này đã được dựng đúng với format của bảng được cung cấp vì vậy việc sử dụng những kiểu bảng có kiểu khác chắc chắn sẽ xảy ra lỗi
CÙNG FORMAT NGHĨA LÀ: hàng đầu tiên sẽ tương ứng với các key của từng object đối với mỗi hàng tiếp theo tương ứng với value được map với key


Chia ra làm 3 giai đoạn để thực hiện task này

Giai đoạn 1: Xác định Bảng
- Mục đích của bước này: Xác định bảng mà ta sẽ thưc hiện OCR, nhằm trám các xung đột từ các bảng bên ngoài
- Tóm tắt: Tìm các contour (*1) và từ đó xác định hình chữ nhật lớn nhất nhằm xác định cái bảng ta muốn Detect
- Các bước áp dụng:
    + Preprocessing:
        1> Grey-scaling: Do không cần phải chú tâm đến màu sắc nên loại bỏ màu giúp việc detect diễn ra nhanh hơn
        2> Thresholding: Không cần quan tâm đến sắc thái của màu xám do bước phía trên tạo ra thành màu "đen" hoặc "trắng" để tối ưu hóa tốc độ như bước phía trên
        3> Inverting: Mình sẽ đảo ngược hình ảnh cho nó thành text màu đen và nền màu trắng
        4> Dilating: Ở bước này ta sẽ làm cho các viền và các đường thẳng trở nên dày hơn để dễ xác định các contour để từ đó có thể xác định được bảng ta muốn Detect
    + Tìm và lọc các contour để tìm contour hình chữ nhật lớn nhất:
        1> Dùng thư viện opencv để tìm hết các contour.
        2> Lọc qua các contour và chỉ để lại các contour hình chữ nhật
        3> Tìm contour lớn nhất => đây sẽ là cái bảng mình dùng để detect (*2)
    + Làm cho bảng phù hợp cho việc detect
        1> Xác định 4 điểm trong contour hình chữ nhật lớn nhất mà mình đã xác định ở bước trước
        2> Dựa trên 4 điểm này ta sẽ ước tính bảng sẽ được generate
        3> Áp dụng biến đổi phối cảnh (perspective transform)

Giai đoạn 2: Loại bỏ các đường kẻ của bảng
- Mục đích của bước này: Giai đoạn này chủ yếu là loại bỏ các đường kẻ trên bảng . Điều này sẽ giúp chúng ta 
có được hình ảnh rõ ràng cho quá trình OCR. Cuối cùng, thứ duy nhất còn lại của hình ảnh sẽ là văn bản trong các ô của bảng
- Tóm tắt: Xóa lần lượt các đường kẻ trong ảnh
- Các bước áp dụng:
    + Xói mòn (*3) các đường thẳng đứng
    + Xói mòn các đường thẳng ngang 
    + Kết hợp đường thẳng dọc và ngang
    + Xóa các đường thẳng dọc và ngang

Giai đoạn 3: Tìm ô và trích xuất văn bản bằng OCR
- Mục đích của bước này: Tìm các ô và với mỗi ô tương ứng ta sẽ xác định rõ từng đoạn text trong ô đó bằng OCR để từ đó  có thể đưa ra output mong muốn
- Các bước áp dụng:
    + Hình ảnh lúc này chỉ còn là đoạn text rời rạc, ta sẽ tiến hành convert text sang blob
    + Tìm vị trí các blob vừa được convert
    + Vẽ các ô xung quanh các blob đó
    + Chia tấm ảnh thành các ô nhỏ chỉ có chữ 
    + Với mỗi tấm ảnh nhỏ đã được ta cắt ra ta sẽ sử dụng model OCR của bên thứ 3 để từ đó đưa ra output mong muốn của từng tấm ảnh nhỏ
rồi từ đó ta sẽ đưa ra output theo format mà ta mong muốn


    

