#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ADB Remote - WiFi üzerinden Android uygulama yönetimi
# Yazan: sbyildirim, 2025

import os
import subprocess
import re
import time
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class ADBRemote:
    def __init__(self):
        # Bağlantı bilgilerini saklamak için değişkenler
        self.device_ip = None
        self.connected = False
        self.device_name = None
    
    def check_adb_installed(self):
        # ADB komutunun çalışıp çalışmadığını kontrol et
        try:
            # ADB sürümünü sorgula
            subprocess.run(["adb", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            # Hata alındıysa ADB yüklü değil demektir
            return False
    
    def get_connected_devices(self):
        # Şu anda ADB'ye bağlı tüm cihazları listele
        result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, text=True)
        # Çıktıyı satırlara böl ve ilk satırı atla (başlık satırı)
        lines = result.stdout.strip().split('\n')[1:]
        devices = []
        
        # Her satırı işle
        for line in lines:
            if line.strip():  # Boş satırları atla
                parts = line.split('\t')
                if len(parts) >= 2:
                    device_id = parts[0].strip()
                    status = parts[1].strip()
                    # Cihaz ID'si ve durumunu listeye ekle
                    devices.append((device_id, status))
        
        return devices
    
    def connect_to_device(self, ip, port=5555):
        # IP adresi kontrolü
        if not ip:
            return False, "IP adresi belirtilmedi."
        
        # Temiz bir başlangıç için ADB sunucusunu yeniden başlat
        # Bazen eski bağlantılar sorun çıkarabiliyor
        subprocess.run(["adb", "kill-server"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(0.5)  # Sunucunun kapanması için kısa bir bekleme
        subprocess.run(["adb", "start-server"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Cihaza bağlanmayı dene
        full_ip = f"{ip}:{port}"
        result = subprocess.run(["adb", "connect", full_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Bağlantı başarılı mı kontrol et
        if "connected" in result.stdout.lower():
            # Bağlantı bilgilerini kaydet
            self.device_ip = full_ip
            self.connected = True
            
            # Cihaz bilgilerini almaya çalış
            try:
                # Cihaz modelini al
                model_cmd = ["adb", "-s", full_ip, "shell", "getprop", "ro.product.model"]
                model = subprocess.run(model_cmd, stdout=subprocess.PIPE, text=True).stdout.strip()
                
                # Üretici bilgisini al
                manuf_cmd = ["adb", "-s", full_ip, "shell", "getprop", "ro.product.manufacturer"]
                manufacturer = subprocess.run(manuf_cmd, stdout=subprocess.PIPE, text=True).stdout.strip()
                
                # Cihaz adını oluştur
                self.device_name = f"{manufacturer} {model}"
            except Exception as e:
                # Bilgi alınamazsa varsayılan isim kullan
                self.device_name = "Bilinmeyen Cihaz"
                print(f"Cihaz bilgisi alınamadı: {e}")
                
            return True, f"{self.device_name} cihazına bağlandı."
        else:
            # Bağlantı başarısız olduysa hata mesajı döndür
            return False, f"Bağlantı hatası: {result.stdout} {result.stderr}"
    
    def disconnect_device(self):
        # Bağlı cihaz varsa bağlantıyı kes
        if self.device_ip:
            # ADB disconnect komutunu çalıştır
            subprocess.run(["adb", "disconnect", self.device_ip], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Bağlantı bilgilerini temizle
            self.device_ip = None
            self.connected = False
            self.device_name = None
            return True, "Cihaz bağlantısı kesildi."
        
        # Bağlı cihaz yoksa hata mesajı döndür
        return False, "Bağlı cihaz yok."
    
    def get_installed_apps(self, system_apps=False):
        # Bağlantı kontrolü
        if not self.connected or not self.device_ip:
            return False, "Bağlı cihaz yok."
        
        try:
            # Hangi uygulamaları listeleyeceğimizi belirle
            if system_apps:
                # Tüm uygulamaları listele (sistem uygulamaları dahil)
                cmd = ["adb", "-s", self.device_ip, "shell", "pm", "list", "packages", "-f"]
            else:
                # Sadece kullanıcının yüklediği uygulamaları listele
                cmd = ["adb", "-s", self.device_ip, "shell", "pm", "list", "packages", "-3", "-f"]
            
            # Komutu çalıştır
            result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
            
            # Hata kontrolü
            if result.returncode != 0:
                return False, "Uygulama listesi alınamadı."
            
            # Uygulama listesini oluştur
            app_list = []
            
            # Her satırı işle
            for line in result.stdout.strip().split('\n'):
                if not line:  # Boş satırları atla
                    continue
                    
                # Paket bilgisini ayrıştır
                # Örnek format: package:/data/app/com.example.app-hash/base.apk=com.example.app
                match = re.search(r'package:(.+)=(.+)', line)
                if match:
                    apk_path = match.group(1)
                    package_name = match.group(2)
                    
                    # Uygulama adını almaya çalış
                    # Not: Bu her zaman çalışmayabilir, cihaza bağlı olarak değişebilir
                    label_cmd = ["adb", "-s", self.device_ip, "shell", "dumpsys", "package", 
                                package_name, "|", "grep", "labelRes"]
                    label_result = subprocess.run(label_cmd, stdout=subprocess.PIPE, 
                                                stderr=subprocess.PIPE, text=True, shell=True)
                    
                    # Varsayılan olarak paket adını kullan
                    app_name = package_name
                    
                    # Eğer uygulama adı bilgisi varsa, daha kullanıcı dostu bir isim oluşturmaya çalış
                    if "labelRes" in label_result.stdout:
                        try:
                            # Ana aktiviteyi bulmaya çalış
                            name_cmd = ["adb", "-s", self.device_ip, "shell", "dumpsys", "package", 
                                      package_name, "|", "grep", "android.intent.action.MAIN"]
                            name_result = subprocess.run(name_cmd, stdout=subprocess.PIPE, 
                                                      stderr=subprocess.PIPE, text=True, shell=True)
                            
                            # Eğer ana aktivite bulunduysa, paket adının son kısmını kullan
                            if name_result.stdout:
                                app_name = package_name.split('.')[-1].capitalize()
                        except Exception as e:
                            # Hata olursa sessizce devam et
                            print(f"Uygulama adı alınamadı: {e}")
                    
                    # Listeye ekle
                    app_list.append((app_name, package_name, apk_path))
            
            # Kullanıcı için alfabetik sırala
            app_list.sort(key=lambda x: x[0].lower())
            return True, app_list
            
        except Exception as e:
            # Herhangi bir hata durumunda
            return False, f"Uygulama listesi alınırken hata: {str(e)}"
    
    def uninstall_app(self, package_name):
        # Bağlantı kontrolü
        if not self.connected or not self.device_ip:
            return False, "Bağlı cihaz yok."
        
        try:
            # Uygulamayı kaldırma komutunu çalıştır
            cmd = ["adb", "-s", self.device_ip, "uninstall", package_name]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Sonucu kontrol et
            if "Success" in result.stdout:
                # Başarılı
                return True, f"{package_name} başarıyla kaldırıldı."
            else:
                # Başarısız - hata mesajını döndür
                return False, f"Kaldırma hatası: {result.stdout} {result.stderr}"
        except Exception as e:
            # Beklenmeyen hata
            return False, f"Uygulama kaldırılırken hata oluştu: {str(e)}"


class ADBRemoteGUI:
    def __init__(self, root):
        # Ana pencere ayarları
        self.root = root
        self.root.title("ADB Remote - WiFi Üzerinden Uygulama Yönetimi")
        self.root.geometry("800x600")  # Başlangıç boyutu
        self.root.minsize(800, 600)    # Minimum boyut
        
        # ADB işlemleri için sınıf örneği oluştur
        self.adb = ADBRemote()
        
        # ADB yüklü mü kontrol et
        if not self.adb.check_adb_installed():
            # Yüklü değilse hata mesajı göster ve uygulamayı kapat
            messagebox.showerror(
                "Hata", 
                "ADB (Android Debug Bridge) yüklü değil.\n\n"
                "Lütfen Android SDK Platform Tools'u indirip kurun ve "
                "PATH değişkenine eklediğinizden emin olun."
            )
            root.destroy()
            return
        
        # Arayüz elemanlarını oluştur
        self.create_widgets()
    
    def create_widgets(self):
        # Ana çerçeve - tüm içeriği tutacak
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ===== BAĞLANTI PANELİ =====
        connection_frame = ttk.LabelFrame(main_frame, text="Cihaz Bağlantısı", padding="10")
        connection_frame.pack(fill=tk.X, pady=5)
        
        # IP Adresi girişi
        ip_label = ttk.Label(connection_frame, text="Android Cihaz IP Adresi:")
        ip_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.ip_entry = ttk.Entry(connection_frame, width=20)
        self.ip_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Port girişi
        port_label = ttk.Label(connection_frame, text="Port (genellikle 5555):")
        port_label.grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        
        self.port_entry = ttk.Entry(connection_frame, width=10)
        self.port_entry.insert(0, "5555")  # Varsayılan port
        self.port_entry.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Bağlantı düğmeleri
        self.connect_btn = ttk.Button(
            connection_frame, 
            text="Bağlan", 
            command=self.connect_to_device
        )
        self.connect_btn.grid(row=0, column=4, padx=5, pady=5)
        
        self.disconnect_btn = ttk.Button(
            connection_frame, 
            text="Bağlantıyı Kes", 
            command=self.disconnect_device, 
            state=tk.DISABLED  # Başlangıçta devre dışı
        )
        self.disconnect_btn.grid(row=0, column=5, padx=5, pady=5)
        
        # Durum bilgisi
        self.status_var = tk.StringVar(value="Durum: Bağlı değil")
        status_label = ttk.Label(
            connection_frame, 
            textvariable=self.status_var,
            font=("", 9, "italic")  # Biraz daha stilize
        )
        status_label.grid(row=1, column=0, columnspan=6, sticky=tk.W, padx=5, pady=5)
        
        # ===== UYGULAMA LİSTESİ PANELİ =====
        app_frame = ttk.LabelFrame(main_frame, text="Yüklü Uygulamalar", padding="10")
        app_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Kontrol düğmeleri ve arama kutusu
        control_frame = ttk.Frame(app_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        # Sistem uygulamaları gösterme seçeneği
        self.show_system_apps_var = tk.BooleanVar(value=False)
        show_system_apps_cb = ttk.Checkbutton(
            control_frame, 
            text="Sistem Uygulamalarını Göster", 
            variable=self.show_system_apps_var, 
            command=self.refresh_app_list
        )
        show_system_apps_cb.pack(side=tk.LEFT, padx=5)
        
        # Yenileme düğmesi
        self.refresh_btn = ttk.Button(
            control_frame, 
            text="Yenile", 
            command=self.refresh_app_list, 
            state=tk.DISABLED  # Başlangıçta devre dışı
        )
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Arama kutusu
        search_label = ttk.Label(control_frame, text="Ara:")
        search_label.pack(side=tk.RIGHT, padx=5)
        
        self.search_var = tk.StringVar()
        # Değişiklik olduğunda filtreleme fonksiyonunu çağır
        self.search_var.trace("w", lambda name, index, mode: self.filter_app_list())
        
        search_entry = ttk.Entry(control_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.RIGHT, padx=5)
        
        # Uygulama listesi tablosu
        list_frame = ttk.Frame(app_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Tablo sütunları
        columns = ("name", "package", "path")
        self.app_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Sütun başlıkları
        self.app_tree.heading("name", text="Uygulama Adı")
        self.app_tree.heading("package", text="Paket Adı")
        self.app_tree.heading("path", text="APK Yolu")
        
        # Sütun genişlikleri
        self.app_tree.column("name", width=150, minwidth=100)
        self.app_tree.column("package", width=250, minwidth=150)
        self.app_tree.column("path", width=350, minwidth=200)
        
        # Kaydırma çubuğu
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.app_tree.yview)
        self.app_tree.configure(yscroll=scrollbar.set)
        
        # Yerleştirme
        self.app_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Sağ tıklama menüsü
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(
            label="Uygulamayı Kaldır", 
            command=self.uninstall_selected_app
        )
        
        # Fare olayları
        self.app_tree.bind("<Button-3>", self.show_context_menu)  # Sağ tık
        self.app_tree.bind("<Double-1>", lambda e: self.uninstall_selected_app())  # Çift tık
        
        # ===== ALT PANEL - İŞLEM DÜĞMELERİ =====
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        # Kaldırma düğmesi
        self.uninstall_btn = ttk.Button(
            action_frame, 
            text="Seçili Uygulamayı Kaldır", 
            command=self.uninstall_selected_app, 
            state=tk.DISABLED  # Başlangıçta devre dışı
        )
        self.uninstall_btn.pack(side=tk.RIGHT, padx=5)
        
        # Yardım düğmesi
        help_btn = ttk.Button(
            action_frame, 
            text="Yardım", 
            command=self.show_help
        )
        help_btn.pack(side=tk.LEFT, padx=5)
        
        # ===== DURUM ÇUBUĞU =====
        self.statusbar = ttk.Label(
            self.root, 
            text="Hazır", 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            font=("", 8)  # Küçük yazı tipi
        )
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def connect_to_device(self):
        """Cihaza bağlanma işlemini gerçekleştirir"""
        # Kullanıcı girdilerini al
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()
        
        # IP adresi kontrolü
        if not ip:
            messagebox.showerror("Hata", "Lütfen IP adresini girin.")
            return
        
        # Port numarası kontrolü
        try:
            port = int(port)
            if port <= 0 or port > 65535:
                raise ValueError("Geçersiz port aralığı")
        except ValueError:
            messagebox.showerror("Hata", "Port numarası geçerli değil. 1-65535 arası bir sayı girin.")
            return
        
        # Durum çubuğunu güncelle
        self.statusbar.config(text="Cihaza bağlanılıyor... Lütfen bekleyin.")
        self.root.update()  # Arayüzü güncelle
        
        # Bağlantıyı dene
        success, message = self.adb.connect_to_device(ip, port)
        
        if success:
            # Bağlantı başarılı
            self.status_var.set(f"Durum: {message}")
            
            # Düğme durumlarını güncelle
            self.connect_btn.config(state=tk.DISABLED)
            self.disconnect_btn.config(state=tk.NORMAL)
            self.refresh_btn.config(state=tk.NORMAL)
            self.uninstall_btn.config(state=tk.NORMAL)
            
            # Uygulama listesini yükle
            self.refresh_app_list()
        else:
            # Bağlantı başarısız
            messagebox.showerror("Bağlantı Hatası", message)
            self.status_var.set("Durum: Bağlı değil")
        
        # Durum çubuğunu güncelle
        self.statusbar.config(text="Hazır")
    
    def disconnect_device(self):
        """Cihaz bağlantısını keser"""
        # Bağlantıyı kes
        success, message = self.adb.disconnect_device()
        
        if success:
            # Bağlantı kesme başarılı
            self.status_var.set("Durum: Bağlı değil")
            
            # Düğme durumlarını güncelle
            self.connect_btn.config(state=tk.NORMAL)
            self.disconnect_btn.config(state=tk.DISABLED)
            self.refresh_btn.config(state=tk.DISABLED)
            self.uninstall_btn.config(state=tk.DISABLED)
            
            # Uygulama listesini temizle
            self.clear_app_list()
        else:
            # Bağlantı kesme başarısız
            messagebox.showerror("Bağlantı Kesme Hatası", message)
    
    def refresh_app_list(self):
        """Uygulama listesini yeniler"""
        # Bağlantı kontrolü
        if not self.adb.connected:
            return
        
        # Listeyi temizle
        self.clear_app_list()
        
        # Durum çubuğunu güncelle
        self.statusbar.config(text="Uygulama listesi alınıyor... Bu işlem biraz zaman alabilir.")
        self.root.update()  # Arayüzü güncelle
        
        # Sistem uygulamaları gösterilsin mi?
        show_system = self.show_system_apps_var.get()
        
        # Uygulama listesini al
        success, result = self.adb.get_installed_apps(system_apps=show_system)
        
        if success:
            # Başarılı - listeyi doldur
            for app_name, package_name, apk_path in result:
                self.app_tree.insert("", tk.END, values=(app_name, package_name, apk_path))
            
            # Durum çubuğunu güncelle
            self.statusbar.config(text=f"{len(result)} uygulama listelendi.")
        else:
            # Başarısız - hata mesajı göster
            messagebox.showerror("Uygulama Listesi Hatası", result)
            self.statusbar.config(text="Hata: Uygulama listesi alınamadı.")
    
    def clear_app_list(self):
        """Uygulama listesini temizler"""
        # Tüm öğeleri sil
        for item in self.app_tree.get_children():
            self.app_tree.delete(item)
    
    def filter_app_list(self):
        """Arama kutusuna göre uygulama listesini filtreler"""
        # Arama metnini al
        search_text = self.search_var.get().lower()
        
        # Listeyi temizle
        self.clear_app_list()
        
        # Bağlantı kontrolü
        if not self.adb.connected:
            return
        
        # Sistem uygulamaları gösterilsin mi?
        show_system = self.show_system_apps_var.get()
        
        # Uygulama listesini al
        success, result = self.adb.get_installed_apps(system_apps=show_system)
        
        if success:
            # Arama kriterine göre filtrele
            count = 0
            for app_name, package_name, apk_path in result:
                # Uygulama adı veya paket adında arama metni var mı?
                if (search_text in app_name.lower() or search_text in package_name.lower()):
                    # Eşleşen uygulamayı listeye ekle
                    self.app_tree.insert("", tk.END, values=(app_name, package_name, apk_path))
                    count += 1
            
            # Durum çubuğunu güncelle
            if search_text:
                self.statusbar.config(text=f"'{search_text}' araması: {count} uygulama bulundu.")
            else:
                self.statusbar.config(text=f"{count} uygulama listelendi.")
    
    def show_context_menu(self, event):
        """Sağ tıklama menüsünü gösterir"""
        # Bağlantı kontrolü
        if not self.adb.connected:
            return
        
        # Tıklanan satırı bul
        item = self.app_tree.identify_row(event.y)
        
        # Eğer bir satır tıklandıysa
        if item:
            # Satırı seç
            self.app_tree.selection_set(item)
            # Menüyü göster
            self.context_menu.post(event.x_root, event.y_root)
    
    def uninstall_selected_app(self):
        """Seçili uygulamayı kaldırır"""
        # Bağlantı kontrolü
        if not self.adb.connected:
            return
        
        # Seçili öğeleri al
        selected_items = self.app_tree.selection()
        
        # Seçili öğe yoksa uyarı ver
        if not selected_items:
            messagebox.showinfo("Bilgi", "Lütfen kaldırılacak bir uygulama seçin.")
            return
        
        # Seçili uygulamanın bilgilerini al
        item = selected_items[0]
        app_name = self.app_tree.item(item, "values")[0]
        package_name = self.app_tree.item(item, "values")[1]
        
        # Kullanıcıdan onay iste
        confirm = messagebox.askyesno(
            "Onay", 
            f"{app_name} ({package_name}) uygulamasını kaldırmak istediğinizden emin misiniz?"
        )
        
        # İptal edildiyse çık
        if not confirm:
            return
        
        # Durum çubuğunu güncelle
        self.statusbar.config(text=f"{package_name} kaldırılıyor...")
        self.root.update()  # Arayüzü güncelle
        
        # Uygulamayı kaldır
        success, message = self.adb.uninstall_app(package_name)
        
        if success:
            # Başarılı - listeden kaldır
            self.app_tree.delete(item)
            self.statusbar.config(text=message)
        else:
            # Başarısız - hata mesajı göster
            messagebox.showerror("Kaldırma Hatası", message)
            self.statusbar.config(text="Hata: Uygulama kaldırılamadı.")
    
    def show_help(self):
        help_text = """
ADB Remote - WiFi Üzerinden Uygulama Yönetimi

Kullanım:

1. Android Cihazınızı Hazırlama:
   - Geliştirici seçeneklerini açın (Ayarlar > Telefon Hakkında > Yazılım Bilgisi > Derleme numarasına 7 kez tıklayın)
   - Geliştirici seçeneklerinde "USB Hata Ayıklama" ve "ADB Kablosuz Hata Ayıklama"yı etkinleştirin
   - Cihazınızın IP adresini öğrenin (Ayarlar > Bağlantılar > WiFi > Bağlı olduğunuz ağa tıklayın > IP adresi)

2. Bağlantı:
   - Cihazınızın IP adresini girin
   - Port genellikle 5555'tir, değiştirmeyin
   - "Bağlan" düğmesine tıklayın

3. Uygulama Yönetimi:
   - Yüklü uygulamaların listesi görüntülenecektir
   - Kaldırmak istediğiniz uygulamaya çift tıklayın veya sağ tıklayıp "Uygulamayı Kaldır"ı seçin
   - Arama kutusunu kullanarak uygulamaları filtreleyebilirsiniz
   - "Sistem Uygulamalarını Göster" seçeneğini işaretleyerek sistem uygulamalarını da görebilirsiniz

Not: Sistem uygulamalarını kaldırmak cihazınıza zarar verebilir. Sadece bildiğiniz uygulamaları kaldırın.
"""
        messagebox.showinfo("Yardım", help_text)


def main():
    root = tk.Tk()
    app = ADBRemoteGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
