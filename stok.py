
import tkinter as tk
from tkinter import ttk
import sqlite3

class stok_takip_uygulamasi:
    def __init__(self,root):
        #ana pencereyi oluştur
        self.root=root
        self.root.title("Stok Takip Uygulaması")

        #veri tabanı ve gerekli tablolar
        self.conn=sqlite3.connect("stok_takip.db")
        self.cursor=self.conn.cursor()
        self.cursor.execute("""
             CREATE TABLE IF NOT EXISTS stok(
                            id TEXT PRIMARY KEY,
                            urun_adi TEXT,
                            adet INTEGER,
                            birim_fiyati REAL,
                            toplam_deger REAL
                            )
        """ )
        self.conn.commit()
        #GİRİŞ ALANLARI
        self.id_label=tk.Label(root,text="ID: ")
        self.id_label.grid(row=0,column=0)
        self.id_entry=tk.Entry(root)
        self.id_entry.grid(row=0,column=1)

        #ÜRÜN ADI ETİKETİ VE GİRİŞ KUTUSU
        self.urun_adi_label=tk.Label(root,text="Ürün Adı: ")
        self.urun_adi_label.grid(row=1,column=0)
        self.urun_adi_entry=tk.Entry(root)
        self.urun_adi_entry.grid(row=1,column=1)
#adet etiketi
        self.adet_label=tk.Label(root,text="Adet: ")
        self.adet_label.grid(row=2,column=0)
        self.adet_entry=tk.Entry(root)
        self.adet_entry.grid(row=2,column=1)
        #birim fiyatı
        self.birim_fiyati_label=tk.Label(root,text="Birim Fiyatı: ")
        self.birim_fiyati_label.grid(row=3,column=0)
        self.birim_fiyati_entry=tk.Entry(root)
        self.birim_fiyati_entry.grid(row=3,column=1)

        #ürün butonları

        self.ekle_buton=tk.Button(root,text="Ekle",command=self.ekle)
        self.ekle_buton.grid(row=4,column=0, columnspan=1)
        #düzelt
        self.duzelt_buton=tk.Button(root,text="Düzelt",command=self.duzelt)
        self.duzelt_buton.grid(row=4,column=1,columnspan=1)
        #sil 
        self.sil_buton=tk.Button(root,text="Sil",command=self.sil)
        self.sil_buton.grid(row=4,column=2,columnspan=1)
        #temizle
        self.temizle_buton=tk.Button(root,text="Temizle",command=self.girisleri_temizle)
        self.temizle_buton.grid(row=4,column=3,columnspan=1)
        #arma çubuğu

        self.arama_label=tk.Label(root,text="Ara")
        self.arama_label.grid(row=5,column=0)
        self.arama_entry=tk.Entry(root)
        self.arama_entry.grid(row=5,column=1)

        #arama tetikleyicisi
        self.arama_entry.bind("<KeyRelease>",self.arama)

        #tablo oluştur

       # tablo oluşturma
        self.tablo = ttk.Treeview(
            root,
            columns=("ID", "ÜRÜN ADI", "ADET", "BİRİM FİYATI", "TOPLAM DEĞER"),
            show="headings",
            height=10
        )

        # sütun başlıkları
        self.tablo.heading("ID", text="ID")
        self.tablo.heading("ÜRÜN ADI", text="ÜRÜN ADI")
        self.tablo.heading("ADET", text="ADET")
        self.tablo.heading("BİRİM FİYATI", text="BİRİM FİYATI")
        self.tablo.heading("TOPLAM DEĞER", text="TOPLAM DEĞER")

        # sütun genişlikleri ve hizalama
        self.tablo.column("ID", width=50, anchor="center")
        self.tablo.column("ÜRÜN ADI", width=150, anchor="w")
        self.tablo.column("ADET", width=80, anchor="center")
        self.tablo.column("BİRİM FİYATI", width=100, anchor="e")
        self.tablo.column("TOPLAM DEĞER", width=120, anchor="e")

        self.tablo.grid(row=6, column=0, columnspan=4, pady=10, sticky="nsew")

        # Satır renkleri (alternatif satır renklendirme)
        self.tablo.tag_configure("evenrow", background="#f0f0f0")  # açık gri
        self.tablo.tag_configure("oddrow", background="white")     # beyaz


        #tabloya tıklandığında veri işlemi başlasın
        self.tablo.bind("<ButtonRelease-1>",self.satir_sec)

        self.verileri_yukle()
        #ana metot bitişi

    def ekle(self):
        id=self.id_entry.get()
        urun_adi=self.urun_adi_entry.get()
        adet=int(self.adet_entry.get())
        birim_fiyati=float(self.birim_fiyati_entry.get())
        toplam_deger=adet*birim_fiyati

        self.cursor.execute("INSERT INTO stok VALUES (?,?,?,?,?)",(id,urun_adi,adet,birim_fiyati,toplam_deger))
        self.conn.commit()
        satir_sayisi = len(self.tablo.get_children())
        etiket = "evenrow" if satir_sayisi % 2 == 0 else "oddrow"
        self.tablo.insert("", "end", values=(id, urun_adi, adet, birim_fiyati, f"{toplam_deger:.2f} TL"), tags=(etiket,))


        self.girisleri_temizle()

    def girisleri_temizle(self):
        self.id_entry.delete(0,tk.END)
        self.urun_adi_entry.delete(0,tk.END)
        self.adet_entry.delete(0,tk.END)
        self.birim_fiyati_entry.delete(0,tk.END) 

    def arama(self,event):
        arama_metni=self.arama_entry.get().lower()
        
        for item in self.tablo.get_children():
            values=self.tablo.item(item,"values")
            
            if (arama_metni in str(values[0]).lower() or
                arama_metni in str(values[1]).lower() or
                arama_metni in str(values[2]).lower() or
                 arama_metni in str(values[3]).lower()):

                self.tablo.selection_set(item)
                self.tablo.see(item)
            else:
                self.tablo.selection_remove(item)

    def satir_sec(self, event):
        secili=self.tablo.selection()

        if secili:
            item=self.tablo.item(secili)
            values=item["values"]
            self.id_entry.delete(0,tk.END)
            self.id_entry.insert(0,values[0])
            self.urun_adi_entry.delete(0,tk.END)
            self.urun_adi_entry.insert(0,values[1])
            self.adet_entry.delete(0,tk.END)
            self.adet_entry.insert(0,values[2])
            self.birim_fiyati_entry.delete(0,tk.END)
            self.birim_fiyati_entry.insert(0,values[3])

    def duzelt(self):
        secili=self.tablo.selection()

        if secili:
            id=self.id_entry.get()
            urun_adi=self.urun_adi_entry.get()
            adet=int(self.adet_entry.get())
            birim_fiyati=float(self.birim_fiyati_entry.get())
            toplam_deger=adet*birim_fiyati
            
            self.cursor.execute("UPDATE stok SET urun_adi=?,adet=?,birim_fiyati=?,toplam_deger=? WHERE id=?" , (urun_adi, adet, birim_fiyati, toplam_deger,id))
            self.conn.commit()
            self.tablo.item(secili, values=(id,urun_adi,adet,birim_fiyati,toplam_deger))
            self.girisleri_temizle()

    def sil(self):
        secili=self.tablo.selection()

        if secili:
            id=self.tablo.item(secili)["values"][0]
            self.cursor.execute("DELETE FROM stok  WHERE id=?",(id,))
            self.conn.commit()
            self.tablo.delete(secili)
            self.girisleri_temizle()
    def verileri_yukle(self):
        for i, row in enumerate(self.cursor.execute("SELECT * FROM stok")):
            id, urun_adi, adet, birim_fiyati, toplam_deger = row
            etiket = "evenrow" if i % 2 == 0 else "oddrow"
            self.tablo.insert("", "end", values=(id, urun_adi, adet, birim_fiyati, f"{toplam_deger:.2f} TL"), tags=(etiket,))





if __name__=="__main__":
    root=tk.Tk()
    app=stok_takip_uygulamasi(root)
    root.mainloop()