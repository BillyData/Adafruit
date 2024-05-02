def display_hometown(name):
    hometown  = {
        "Khang\n":"Quang Nam",
        "Khoa\n":"Huế",
        "Trang\n":"Ha Noi",
        "Hung\n":"Quang Ngai",
        "Bao\n":"Sai Gon",
        "Khoi\n":"Tien Giang",
        "Background\n":"Nowhere"
    }
    client.publish("Hometown", hometown[name])