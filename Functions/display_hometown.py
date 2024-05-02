def display_hometown(name):
    hometown  = {
        "Khang\n":"Quang Nam",
        "Khoa\n":"Huế",
        "Trang\n":"Ha Noi",
        "Hưng\n":"Quang Ngai",
        "Bảo\n":"Sai Gon",
        "Khôi\n":"Tien Giang",
        "Background\n":"Nowhere"
    }
    client.publish("Hometown", hometown[name])