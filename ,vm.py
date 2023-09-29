import json
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage  # Resim eklemek için PhotoImage kullanılır
from tkinter import simpledialog
from PIL import Image, ImageTk
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.hash import sha256_crypt
from ders_atama import*


class Isciler():

    "bu sınıf işçileri kayıt etmenin ana yeridir"
    def __init__(self, name, surname, age, bolum, **kwargs):
        self.name = name
        self.surname = surname
        self.age = age
        self.bolum = bolum
        self.maas = kwargs.get('maas', 0)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def ekle(self):
        try:
            with open('isciler.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        # Yeni işçiyi verilere ekleme yeri
        data.append({
            'name': self.name,
            'surname': self.surname,
            'age': self.age,
            'bolum': self.bolum,
            'maas': self.maas,
        })
        # Verileri dosyaya geçirme yeri
        with open('isciler.json', 'w') as file:
            json.dump(data, file, indent=4)
        # İşçi kaydı yapıldığında kontenjanı azaltın ve veritabanına güncel değeri kaydedin
        Bolum.bolumler[self.bolum].azalt_kontenjan()
        self.kaydet_kontenjan(Bolum.bolumler[self.bolum].get_kontenjan())
    def kaydet_kontenjan(self, kontenjan):
        try:
            with open('kontenjan.json', 'r') as file:
                kontenjan_data = json.load(file)
        except FileNotFoundError:
            kontenjan_data = {}
        kontenjan_data[self.bolum] = kontenjan
        # Verileri dosyaya geçirme yeri
        with open('kontenjan.json', 'w') as file:
            json.dump(kontenjan_data, file, indent=4)
            
class Bolum():
    bolumler = {}
    def __init__(self, bolum_adi, maas, kontenjan):
        self.maas = maas
        self.kontenjan = kontenjan
        self.isciler = []
        self.bolum_adi = bolum_adi
        # Bölümü sözlüğe ekleyin
        Bolum.bolumler[bolum_adi] = self
    @classmethod
    def bolum_ekle(cls, bolum_adi, maas, kontenjan):
        yeni_bolum = cls(bolum_adi, maas, kontenjan)
        print(f"{bolum_adi} bolumu eklendi")
    def azalt_kontenjan(self):
        self.kontenjan -= 1
    def get_kontenjan(self):
        return self.kontenjan



engine = create_engine('sqlite:///user.db', echo=False)
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True) # eşsiz
    password = Column(String)
    kart = Column(String)

Base.metadata.create_all(engine)

# Tkinter uygulaması oluşturma

app = tk.Tk()
app.title("ISCI_KAYI_UYGULAMASI")
app.geometry("1000x600")

# Arka plan resmini eklemek için ImageTk kullanımı

bg_image = Image.open("images/burj_khalifa.jpg")  # Arka plan resmi dosyasının adını ve yolunu belirtin
bg_image = bg_image.resize((1000, 600), Image.BILINEAR)  # Resmi pencere boyutuna uygun olarak yeniden boyutlandırın
bg_image = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(app, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Giriş bilgileri giriş kutuları

bg_color = "#6B4B7C"
username_label = tk.Label(app, text="Kullanıcı Adı:", font=("Helvetica", 16), bg=bg_color)
username_label.place(x=700, y=150)

username_entry = tk.Entry(app, font=("Helvetica", 16), bg=bg_color)
username_entry.place(x=700, y=200)

password_label = tk.Label(app, text="Şifre:", font=("Helvetica", 16), bg=bg_color)
password_label.place(x=700, y=250)

password_entry = tk.Entry(app, show="*", font=("Helvetica", 16), bg=bg_color)
password_entry.place(x=700, y=300)

kart_label = tk.Label(app, text="kart_numarasi:", font=("Helvetica", 16), bg=bg_color)
kart_label.place(x=700, y=350)

kart_entry = tk.Entry(app, show="*", font=("Helvetica", 16), bg=bg_color)
kart_entry.place(x=700, y=400)

def save_user():

    username = username_entry.get()
    password = password_entry.get()
    kart = kart_entry.get()

    # Şifreyi güvenli bir şekilde hashleme
    hashed_password = sha256_crypt.hash(password)
    hashed_kart = sha256_crypt.hash(kart)

    # SQLAlchemy ile kullanıcı bilgilerini veritabanına kaydetme
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        new_user = User(username=username, password=hashed_password,kart=hashed_kart)
        session.add(new_user)
        session.commit()  # kayıt etti
        session.close()
        messagebox.showinfo("Başarılı", "Kullanıcı başarıyla kaydedildi.")
    except:
        messagebox.showerror("Hata", "Kullanıcı kayıt edilemedi!")

# Kullanıcının veritabanına giriş işlemi

def login():

    username = username_entry.get()
    password = password_entry.get()
    kart = kart_entry.get()
    # SQLAlchemy ile kullanıcı bilgilerini veritabanından sorgulama
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter_by(username=username).first()

    if user and sha256_crypt.verify(password, user.password):
        messagebox.showinfo("Başarılı", "Giriş başarılı!")
        liste = app.place_slaves()
        for l in liste:
            l.destroy()  # yok et

        if len(kart) > 3 and sha256_crypt.verify(kart,user.kart):
            yonetici_app = Uygulama()

            yeni_isci_btn = tk.Button(yonetici_app, text="Yeni Isci Ekle", command=yonetici_app.yeni_isci_ekle)
            yeni_isci_btn.pack()

            yeni_gorev_btn = tk.Button(yonetici_app, text="Yeni Gorev Ekle", command=yonetici_app.yeni_gorev_ekle)
            yeni_gorev_btn.pack()


            
    else:
        messagebox.showerror("Hata", "Kullanıcı adı veya kartnumarasi veya şifre yanlış!")
    session.close()
# Kaydet ve Giriş butonları
save_button = tk.Button(app, text="Kaydet", command=save_user, font=("Helvetica", 16))
save_button.place(x=700, y=450)

login_button = tk.Button(app, text="Giriş   ", command=login, font=("Helvetica", 16))
login_button.place(x=850, y=450)


# Bölümleri ve maaşlarını tanımlayın
Bolum.bolum_ekle("python", 15000, 10)
Bolum.bolum_ekle("js", 20000, 8)
Bolum.bolum_ekle("C#", 17000, 14)

yeni_isci = Isciler(name="selman", surname="burdurlu", age=15, bolum="python", maas=Bolum.bolumler["python"].maas)
yeni_isci.ekle()
# Kalan kontenjanı veri tabanina kaydeTme yeri
kalan_kontenjan = Bolum.bolumler["python"].get_kontenjan()
print(f"Kalan kontenjan: {kalan_kontenjan}")

app.mainloop()
