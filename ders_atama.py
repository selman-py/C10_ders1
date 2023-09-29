import tkinter as tk
from tkinter import simpledialog
from datetime import datetime

class Gorev:
    def __init__(self, baslik, icerik, tarih):
        self.baslik = baslik
        self.icerik = icerik
        self.tarih = tarih

class Isci:
    def __init__(self, adi, soyadi, kart_no):
        self.adi = adi
        self.soyadi = soyadi
        self.kart_no = kart_no
        self.gorevler = []

    def isci_bilgileri(self):
        return f"Isci Adı: {self.adi}\nIsci Soyadı: {self.soyadi}\nIsci No: {self.kart_no}"

    def gorev_ekle(self, gorev):
        self.gorevler.append(gorev)

class Uygulama(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Isci Gorev Atama Sistemi")
        self.geometry("400x400")

        self.isci_listesi = []
        self.gorev_listesi = []

        self.liste_isci = tk.Listbox(self, selectmode=tk.SINGLE)
        self.liste_isci.pack(pady=10)

        self.liste_gorev = tk.Listbox(self, selectmode=tk.SINGLE)
        self.liste_gorev.pack(pady=10)

        self.atama_btn = tk.Button(self, text="Gorev Ata", command=self.gorev_ata)
        self.atama_btn.pack()

    def yeni_isci_ekle(self):
        adi = simpledialog.askstring("Yeni Isci Ekle", "Isci Adı:")
        soyadi = simpledialog.askstring("Yeni Isci Ekle", "Isci Soyadı:")
        isci_no = simpledialog.askstring("Yeni Isci Ekle", "Isci No:")

        if adi and soyadi and isci_no:
            yeni_isci = Isci(adi, soyadi, isci_no)
            self.isci_listesi.append(yeni_isci)
            self.liste_isci.insert(tk.END, f"{yeni_isci.adi} {yeni_isci.soyadi}")

    def yeni_gorev_ekle(self):
        baslik = simpledialog.askstring("Yeni Gorev Ekle", "Gorev Başlığı:")
        icerik = simpledialog.askstring("Yeni Gorev Ekle", "Gorev İçeriği:")
        tarih = simpledialog.askstring("Yeni Gorev Ekle", "Gorev Tarihi:")

        if baslik and icerik and tarih:
            yeni_gorev = Gorev(baslik, icerik, tarih)
            self.gorev_listesi.append(yeni_gorev)
            self.liste_gorev.insert(tk.END, yeni_gorev.baslik)

    def gorev_ata(self):
        selected_isci_index = self.liste_isci.curselection()
        #selected_gorev_index = self.liste_gorev.curselection()

        if selected_isci_index:
            isci = self.isci_listesi[selected_isci_index[0]]
            #gorev = self.gorev_listesi[selected_gorev_index[0]]

            isci.gorev_ekle(self.gorev_listesi[0])
            print(f"{isci.adi} {isci.soyadi} adlı isciye {self.gorev_listesi[0].baslik} gorevi atanmıştır.")

if __name__ == "__main__":
    app = Uygulama()
    
    yeni_isci_btn = tk.Button(app, text="Yeni Isci Ekle", command=app.yeni_isci_ekle)
    yeni_isci_btn.pack()

    yeni_gorev_btn = tk.Button(app, text="Yeni Gorev Ekle", command=app.yeni_gorev_ekle)
    yeni_gorev_btn.pack()

    app.mainloop()
