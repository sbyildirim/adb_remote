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

Uygulamayı kullanmak için sadece Python gerekiyor:

1. **Python**: Bilgisayarınızda Python 3.6 veya daha yeni bir sürüm olmalı

**ADB Otomatik Kurulum**: Uygulama ilk çalıştırıldığında ADB (Android Debug Bridge) yüklü değilse, otomatik olarak indirip kuracaktır. Manuel olarak ADB kurmanıza gerek yoktur!

Kurulum adımları:
1. Bu projeyi bilgisayarınıza indirin
2. Komut satırında proje klasörüne gidin
3. `python adb_remote.py` komutuyla uygulamayı başlatın
4. İlk çalıştırmada ADB otomatik olarak indirilip kurulacaktır

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

4. ADB Durumunu Kontrol Etme:
   - "ADB Durumunu Kontrol Et" düğmesine tıklayarak ADB'nin durumunu görebilirsiniz
   - Bu özellik, ADB'nin doğru şekilde kurulup kurulmadığını kontrol etmenizi sağlar
   - ADB sürümü, yolu ve platform-tools klasörü hakkında bilgi verir

Not: Sistem uygulamalarını kaldırmak cihazınıza zarar verebilir. Sadece bildiğiniz uygulamaları kaldırın.

##  İletişim

Proje Sahibi - @sbyildirim

Proje Linki: https://github.com/sbyildirim/adb_remote
