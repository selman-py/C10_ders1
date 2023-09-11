import json

class isciler():
    "bu sınıf işçileri kayıt etmenin ana yeridir"
    def __init__(self, name, surname, age, **kwargs):
        self.name = name
        self.surname = surname
        self.age = age
        self.bolum = kwargs.get('bolum')

        for key, value in kwargs.items():
            setattr(self, key, value)

    def ekle(self):
        # Mevcut verileri okuyuma
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
            #Diğer özel özellikleri de ekleyebilirsiniz
        })

        #Verileri dosyaya gecırme yerı
        with open('isciler.json', 'w') as file:
            json.dump(data, file, indent=4)

# örnek:
yeni_isci = isciler(name="selman", surname="burdurlu", age=15, bolum="yazılım")
yeni_isci.ekle()