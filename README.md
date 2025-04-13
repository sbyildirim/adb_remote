# 📱 ADB Remote - WiFi Üzerinden Android Uygulama Yönetimi

Merhaba! Bu proje, Android telefonunuzdaki uygulamaları WiFi üzerinden kolayca yönetmenizi sağlayan bir araç. Telefonunuzu bilgisayarınıza kablo olmadan bağlayıp, istediğiniz uygulamaları tek tıkla kaldırabilirsiniz.

## 🚀 Neler Yapabilirsiniz?

Bu uygulama ile:
- Telefonunuza WiFi üzerinden bağlanabilirsiniz (kablo gerekmez!)
- Telefonunuzda yüklü tüm uygulamaları görebilirsiniz
- İstediğiniz uygulamayı hızlıca bulabilirsiniz (arama özelliği var)
- Gereksiz uygulamaları kolayca kaldırabilirsiniz
- İsterseniz sistem uygulamalarını da görüntüleyebilirsiniz (dikkatli olun!)

## 🔧 Kurulum

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

## 📱 Telefonunuzu Hazırlama

Uygulamayı kullanmadan önce telefonunuzda birkaç ayar yapmanız gerekiyor:

1. **Geliştirici Seçeneklerini Açın**:
   - Ayarlar > Telefon Hakkında > Yazılım Bilgisi bölümüne gidin
   - "Derleme numarası" üzerine 7 kez tıklayın (evet, gerçekten 7 kez!)
   - "Artık bir geliştiricisiniz" mesajını görene kadar bekleyin

2. **Hata Ayıklama Seçeneklerini Açın**:
   - Ayarlar > Geliştirici Seçenekleri bölümüne gidin
   - "USB Hata Ayıklama" seçeneğini açın
   - "Kablosuz Hata Ayıklama" veya "ADB Kablosuz" seçeneğini açın

3. **Telefonunuzun IP Adresini Öğrenin**:
   - Ayarlar > WiFi bölümüne gidin
   - Bağlı olduğunuz ağa tıklayın
   - IP adresini not alın (genellikle 192.168.x.x formatında)

## 💡 Kullanım İpuçları

- Telefonunuz ve bilgisayarınız **aynı WiFi ağına** bağlı olmalı
- Bazı telefonlarda kablosuz ADB'yi etkinleştirmek için önce USB kablosuyla bağlanmanız gerekebilir
- Sistem uygulamalarını kaldırırken çok dikkatli olun! Telefonunuzun çalışmasını bozabilirsiniz
- Bir uygulamayı kaldırmadan önce ne olduğundan emin değilseniz, Google'da aratın
- Arama kutusunu kullanarak istediğiniz uygulamayı hızlıca bulabilirsiniz

## ❓ Sorun Giderme

**"ADB yüklü değil" hatası alıyorum:**
ADB'yi doğru şekilde yüklediniz mi? Komut satırında `adb version` yazarak kontrol edin. Çalışmıyorsa, ADB'yi yeniden yükleyin ve PATH'e eklendiğinden emin olun.

**Telefonuma bağlanamıyorum:**
- Telefonunuz ve bilgisayarınız aynı WiFi ağında mı?
- Telefonunuzda geliştirici seçenekleri ve USB hata ayıklama açık mı?
- IP adresini doğru girdiğinizden emin olun
- Bazı telefonlarda önce USB ile bağlanıp sonra "Kablosuz hata ayıklamaya geç" seçeneğini kullanmanız gerekebilir

**Uygulama listesi gelmiyor:**
Telefonunuzda izinleri onayladınız mı? Bağlantı sırasında telefonda bir izin penceresi açılabilir, "İzin ver" seçeneğini işaretleyin.
