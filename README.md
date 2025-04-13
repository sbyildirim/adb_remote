# 📱 ADB Remote - WiFi Üzerinden Android Uygulama Yönetimi

Merhaba! Bu proje, Android telefonunuzdaki uygulamaları WiFi üzerinden kolayca yönetmenizi sağlayan bir araç. Telefonunuzu bilgisayarınıza kablo olmadan bağlayıp, istediğiniz uygulamaları tek tıkla kaldırabilirsiniz.

##  Neler Yapabilirsiniz?

Bu uygulama ile:
- Telefonunuza WiFi üzerinden bağlanabilirsiniz
- Telefonunuzda yüklü tüm uygulamaları görebilirsiniz
- İstediğiniz uygulamayı hızlıca bulabilirsiniz, arama özelliği var.
- Gereksiz uygulamaları kolayca kaldırabilirsiniz
- İsterseniz sistem uygulamalarını da görüntüleyebilirsiniz, dikkatli olun.

##  Kurulum

Uygulamayı kullanmak için birkaç şey gerekiyor:

1. **Python**: Bilgisayarınızda Python 3.6 veya daha yeni bir sürüm olmalı
2. **ADB**: Android Debug Bridge aracı yüklü olmalı
   - Windows için: [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools)'u indirin ve PATH'e ekleyin
   - Mac için: Terminal'de `brew install android-platform-tools` komutunu çalıştırın
   - Linux için: `sudo apt install adb` komutunu çalıştırın

Sonra:
1. Bu projeyi bilgisayarınıza indirin
2. Komut satırında proje klasörüne gidin
3. `python adb_remote.py` komutuyla uygulamayı başlatın

##  Kullanım:

1. Android Cihazınızı Hazırlama:
   - Geliştirici seçeneklerini açın (Ayarlar > Telefon Hakkında > Yazılım Bilgisi > Derleme numarasına 7 kez tıklayın)
   - Geliştirici seçeneklerinde "USB Hata Ayıklama" ve "ADB Kablosuz Hata Ayıklama"yı etkinleştirin
   - Cihazınızın IP adresini öğrenin (Ayarlar > Bağlantılar > WiFi > Bağlı olduğunuz ağa tıklayın > IP adresi (genellikle 192.168.x.x formatında)) 

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

##  İletişim

Proje Sahibi - @sbyildirim

Proje Linki: https://github.com/sbyildirim/adb_remote