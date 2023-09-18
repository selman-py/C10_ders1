import json

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

# Bölümleri ve maaşlarını tanımlayın
Bolum.bolum_ekle("python", 15000, 10)
Bolum.bolum_ekle("js", 20000, 8)
Bolum.bolum_ekle("C#", 17000, 14)

yeni_isci = Isciler(name="selman", surname="burdurlu", age=15, bolum="python", maas=Bolum.bolumler["python"].maas)
yeni_isci.ekle()

# Kalan kontenjanı veri tabanina kaydeTme yeri
kalan_kontenjan = Bolum.bolumler["python"].get_kontenjan()
