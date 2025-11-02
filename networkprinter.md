# ESC/POS Network Printer - Kurulum ve Kullanım Kılavuzu

Bu dokümantasyon, SmartStock için ESC/POS Network Printer sisteminin kurulumu ve kullanımı hakkında detaylı bilgi içerir.

## İçindekiler

1. [Sistem Hakkında](#sistem-hakkında)
2. [Ön Gereksinimler](#ön-gereksinimler)
3. [Kurulum Adımları](#kurulum-adımları)
4. [Başlatma](#başlatma)
5. [SmartStock Entegrasyonu](#smartstock-entegrasyonu)
6. [Web Arayüzü](#web-arayüzü)
7. [Ortam Değişkenleri](#ortam-değişkenleri)
8. [Sorun Giderme](#sorun-giderme)
9. [Port Bilgileri](#port-bilgileri)

---

## Sistem Hakkında

ESC/POS Network Printer, termal yazıcı komutlarını (ESC/POS) alıp HTML formatına dönüştüren ve web arayüzünde görüntüleyen bir sistemdir. Docker kullanmadan, doğrudan Windows üzerinde çalışır.

### Özellikler

- **ESC/POS Desteği**: Standart termal yazıcı komutlarını işler
- **HTML Dönüştürme**: Fişleri tarayıcıda görüntülenebilir HTML'e çevirir
- **JetDirect Protokolü**: Port 9100 üzerinden yazıcı iletişimi
- **Web Arayüzü**: Tüm yazdırılan fişleri görüntüleme
- **Windows Bildirimleri**: Yazdırma tamamlandığında bildirim gösterir
- **Süre Ölçümü**: Her yazdırma işleminin ne kadar sürdüğünü gösterir

---

## Ön Gereksinimler

### 1. Python Kurulumu

**Gerekli Versiyon**: Python 3.8 veya üstü

**İndirme**:
- https://www.python.org/downloads/
- Kurulum sırasında **"Add Python to PATH"** seçeneğini işaretleyin!

**Kontrol**:
```bash
python --version
```

### 2. PHP ve Composer Kurulumu

**PHP**: 8.2 veya üstü (XAMPP varsa zaten kurulu)

**Composer**:
- https://getcomposer.org/download/
- Global olarak kurulmalı

**Kontrol**:
```bash
php --version
composer --version
```

### 3. XAMPP (Opsiyonel)

Eğer PHP ve Composer ayrı olarak kurmak istemiyorsanız, XAMPP tüm gereksinimleri içerir.

---

## Kurulum Adımları

### Adım 1: Dosyaları Yerleştirme

ESC/POS Network Printer dosyalarını şu konuma kopyalayın:
```
C:\xampp\htdocs\escpos-netprinter\
```

### Adım 2: Python Kütüphanelerini Kurma

Komut satırını (CMD) açın ve şu komutları çalıştırın:

```bash
pip install Flask
pip install lxml
pip install win10toast
```

**Açıklama**:
- **Flask**: Web sunucusu ve HTTP API için
- **lxml**: HTML/XML işleme için
- **win10toast**: Windows 10/11 bildirim sistemi için

### Adım 3: PHP Kütüphanelerini Kurma

Komut satırında escpos-netprinter klasörüne gidin:

```bash
cd C:\xampp\htdocs\escpos-netprinter
composer install
```

Bu komut şu kütüphaneleri kuracak:
- **mike42/escpos-php**: ESC/POS komutlarını işleme
- **chillerlan/php-qrcode**: QR kod oluşturma
- Diğer bağımlılıklar

### Adım 4: Gerekli Klasörleri Oluşturma

Eğer yoksa şu klasörleri oluşturun:

```bash
cd C:\xampp\htdocs\escpos-netprinter
mkdir web\receipts
mkdir web\tmp
```

**Açıklama**:
- **web/receipts**: Yazdırılan HTML fişlerinin saklandığı yer
- **web/tmp**: Geçici dosyaların tutulduğu yer

### Adım 5: Windows Yazıcı Kurulumu

Windows PowerShell'i **Yönetici olarak** açın ve şu komutları çalıştırın:

#### 5.1. Yazıcı Portu Oluşturma

```powershell
Add-PrinterPort -Name "TCP_127.0.0.1_9100" -PrinterHostAddress "127.0.0.1" -PortNumber 9100
```

Bu komut TCP/IP yazıcı portu oluşturur.

#### 5.2. Yazıcıyı Ekleme

```powershell
Add-Printer -Name "ESC/POS Network Printer" -DriverName "Generic / Text Only" -PortName "TCP_127.0.0.1_9100"
```

Bu komut "Generic / Text Only" sürücüsü ile yazıcıyı ekler.

#### 5.3. Kontrol

```powershell
Get-Printer | Where-Object {$_.Name -like "*ESC/POS*"}
```

Yazıcının eklendiğini doğrulayın.

---

## Başlatma

### Basit Başlatma (Varsayılan Ayarlarla)

En basit kullanım:

```bash
cd C:\xampp\htdocs\escpos-netprinter
python escpos-netprinter.py
```

Bu komut şu varsayılan ayarlarla başlatır:
- **Web Arayüzü**: http://localhost:5000
- **JetDirect Port**: 9100
- **Debug Modu**: Kapalı

### Gelişmiş Başlatma (Ortam Değişkenleri İle)

Özelleştirilmiş ayarlarla başlatma:

```bash
cd C:\xampp\htdocs\escpos-netprinter
set FLASK_RUN_HOST=0.0.0.0
set FLASK_RUN_PORT=8100
set PRINTER_PORT=9100
set ESCPOS_DEBUG=False
python escpos-netprinter.py
```

**Açıklama**:
- **FLASK_RUN_HOST=0.0.0.0**: Tüm ağ arayüzlerinden erişim (0.0.0.0 = dışarıdan da erişilebilir)
- **FLASK_RUN_PORT=8100**: Web arayüzü portu (varsayılan: 80)
- **PRINTER_PORT=9100**: JetDirect yazıcı portu
- **ESCPOS_DEBUG=False**: Debug loglarını kapat (True = açık)

### Windows Başlangıcına Ekleme (Opsiyonel)

Bilgisayar açıldığında otomatik başlatmak için:

#### Yöntem 1: Başlangıç Klasörüne Shortcut Ekleme

1. **start-printer.bat** dosyası oluşturun:

```batch
@echo off
cd C:\xampp\htdocs\escpos-netprinter
set FLASK_RUN_HOST=0.0.0.0
set FLASK_RUN_PORT=8100
set PRINTER_PORT=9100
set ESCPOS_DEBUG=False
python escpos-netprinter.py
```

2. Bu bat dosyasının kısayolunu oluşturun
3. Kısayolu şu klasöre kopyalayın:
```
C:\Users\KULLANICI_ADINIZ\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

#### Yöntem 2: Zamanlanmış Görev (Task Scheduler)

Daha gelişmiş kontrol için Windows Task Scheduler kullanabilirsiniz.

---

## SmartStock Entegrasyonu

ESC/POS Network Printer'ın SmartStock ile çalışması için:

### 1. SmartStock Connector'ı Başlatma

SmartStock Connector uygulamasını çalıştırın:

```bash
cd C:\SmartStock-Connector
npm start
```

Veya kurulu EXE dosyasını çalıştırın:
```
C:\SmartStock-Connector\dist\win-unpacked\SmartStock Connector.exe
```

### 2. Yazıcı Ayarları

SmartStock Connector tray icon'una sağ tıklayın:
1. **Settings** menüsüne girin
2. **Default Printer** olarak "ESC/POS Network Printer" seçin
3. **Auto Print** toggle'ını açın

### 3. Test Yazdırma

SmartStock arayüzünde:
1. Bir fatura sayfasını açın
2. "Kargo Etiket" butonuna tıklayın
3. Sağ alt köşede Windows bildirimi görünmeli:
   - "Yazici - Basarili"
   - "Fis yazdirildi! Sure: X.XX saniye"

### 4. Fişi Görüntüleme

Tarayıcınızda http://localhost:5000/recus adresine gidin ve yazdırılan fişi HTML formatında görüntüleyin.

---

## Web Arayüzü

### Ana Sayfa
```
http://localhost:5000/
```

Ana sayfada:
- Sistem durumu
- Son yazdırılan fiş
- Toplam fiş sayısı

### Fiş Listesi
```
http://localhost:5000/recus
```

Tüm yazdırılan fişlerin listesi:
- Tarih ve saat
- Fiş numarası
- HTML görüntüleme linki

### Tek Fiş Görüntüleme
```
http://localhost:5000/recus/DOSYA_ADI.html
```

Belirli bir fişi tam ekran görüntüleme.

---

## Ortam Değişkenleri

Sistemin davranışını kontrol eden ortam değişkenleri:

### FLASK_RUN_HOST

**Varsayılan**: `127.0.0.1` (sadece local)
**Önerilen**: `0.0.0.0` (ağdan erişim için)

```bash
set FLASK_RUN_HOST=0.0.0.0
```

**Kullanım**:
- `127.0.0.1`: Sadece bilgisayarın kendisinden erişilebilir
- `0.0.0.0`: Ağdaki diğer cihazlardan da erişilebilir

### FLASK_RUN_PORT

**Varsayılan**: `80`
**Alternatif**: `5000`, `8100`, vb.

```bash
set FLASK_RUN_PORT=8100
```

**Not**: Port 80 kullanmak için yönetici izni gerekebilir.

### PRINTER_PORT

**Varsayılan**: `9100` (JetDirect standart portu)

```bash
set PRINTER_PORT=9100
```

**Uyarı**: Bu portu değiştirirseniz, Windows yazıcı portu da aynı porta ayarlanmalı!

### ESCPOS_DEBUG

**Varsayılan**: `False`
**Değerler**: `True` veya `False`

```bash
set ESCPOS_DEBUG=True
```

**Debug Modu Açıksa**:
- Tüm ESC/POS komutları loglanır
- CUPS yazıcı sürücüsü logları gösterilir
- JetDirect bağlantı detayları gösterilir
- Web istekleri loglanır
- Geçici dosyalar silinmez (web/tmp/)

**Debug Modu Kapalıysa**:
- Sadece hata mesajları gösterilir
- Daha temiz çıktı
- Geçici dosyalar otomatik silinir

---

## Sorun Giderme

### Problem: Port 9100 kullanımda

**Hata Mesajı**:
```
OSError: [WinError 10048] Only one usage of each socket address
```

**Çözüm**:
```bash
netstat -ano | findstr :9100
taskkill /PID XXXX /F
```

### Problem: Windows bildirimi çıkmıyor

**Kontrol**:
1. Windows Bildirim Ayarları açık mı?
2. Python çalışıyor mu?

**Çözüm**:
```bash
# Python procesini kontrol et
tasklist | findstr python

# Yoksa tekrar başlat
python escpos-netprinter.py
```

### Problem: Yazıcı bulunamıyor

**Kontrol**:
```powershell
Get-Printer | Where-Object {$_.Name -like "*ESC/POS*"}
```

**Çözüm - Yazıcıyı yeniden ekle**:
```powershell
# Önce portu kontrol et
Get-PrinterPort | Where-Object {$_.Name -like "*9100*"}

# Port yoksa oluştur
Add-PrinterPort -Name "TCP_127.0.0.1_9100" -PrinterHostAddress "127.0.0.1" -PortNumber 9100

# Yazıcıyı ekle
Add-Printer -Name "ESC/POS Network Printer" -DriverName "Generic / Text Only" -PortName "TCP_127.0.0.1_9100"
```

### Problem: SmartStock Connector bağlanamıyor

**Hata**: `localhost:37842 refused`

**Çözüm**:
```bash
# Connector çalışıyor mu kontrol et
tasklist | findstr node
tasklist | findstr electron

# Çalışmıyorsa başlat
cd C:\SmartStock-Connector
npm start
```

### Problem: HTML fişleri görünmüyor

**Olası Sebepler**:
1. Dosya oluşturma hatası (error 22)
2. web/receipts klasörü yok
3. İzin sorunu

**Çözüm**:
```bash
# Klasörleri kontrol et
dir C:\xampp\htdocs\escpos-netprinter\web\receipts

# Yoksa oluştur
mkdir C:\xampp\htdocs\escpos-netprinter\web\receipts
mkdir C:\xampp\htdocs\escpos-netprinter\web\tmp

# Python'u yeniden başlat
```

### Problem: "Module not found" hatası

**Hata**: `ModuleNotFoundError: No module named 'Flask'`

**Çözüm**:
```bash
# Tüm gereksinimleri tekrar kur
pip install Flask lxml win10toast

# PHP bağımlılıklarını kur
cd C:\xampp\htdocs\escpos-netprinter
composer install
```

### Problem: Port izni hatası

**Hata**: `Permission denied: 127.0.0.1:80`

**Çözüm 1**: Farklı port kullan
```bash
set FLASK_RUN_PORT=8100
python escpos-netprinter.py
```

**Çözüm 2**: CMD'yi Yönetici olarak aç

---

## Port Bilgileri

Sistem 3 farklı port kullanır:

### Port 9100 - JetDirect (Yazıcı Protokolü)

**Kullanım**: ESC/POS komutlarını almak için
**Protokol**: TCP/IP
**Bağlanan**: SmartStock Connector

**Kontrol**:
```bash
netstat -an | findstr :9100
```

### Port 5000 (veya 8100) - Web Arayüzü

**Kullanım**: Fişleri tarayıcıda görüntüleme
**Protokol**: HTTP
**URL**: http://localhost:5000

**Kontrol**:
```bash
netstat -an | findstr :5000
```

### Port 37842 - SmartStock Connector API

**Kullanım**: SmartStock web arayüzü ile yerel sistem arasında köprü
**Protokol**: HTTP (REST API)
**Kullanıcı**: SmartStock web arayüzü (JavaScript)

**Kontrol**:
```bash
netstat -an | findstr :37842
```

---

## Sistem Mimarisi

```
┌─────────────────────┐
│  SmartStock Web     │  (Uzak Sunucu - smartstock.com)
│   (Laravel/PHP)     │
└──────────┬──────────┘
           │ HTML/JS
           ▼
┌─────────────────────┐
│    Tarayıcı         │  (Kullanıcının PC'si)
│   (Chrome/Edge)     │
└──────────┬──────────┘
           │ fetch('http://localhost:37842/...')
           ▼
┌─────────────────────┐
│ SmartStock Connector│  (Port 37842)
│   (Node.js/Electron)│
└──────────┬──────────┘
           │ TCP Socket (127.0.0.1:9100)
           ▼
┌─────────────────────┐
│ escpos-netprinter   │  (Port 9100 + Web 5000)
│  (Python/Flask)     │
└──────────┬──────────┘
           │
           ├─> HTML fişleri (web/receipts/)
           └─> Windows Bildirimi
```

---

## Güvenlik Notları

### 1. Sadece Yerel Ağda Kullanın

Bu sistem internet üzerinden erişime açık olmamalı:
- Flask development sunucusu kullanıyor (production için uygun değil)
- Kimlik doğrulama yok
- Şifreleme yok

### 2. Güvenlik Duvarı Ayarları

Eğer ağdan erişim gerekiyorsa:
- Sadece güvenilir yerel ağdan erişime izin verin
- Port 9100 ve 5000'i sadece yerel ağa açın
- VPN kullanın

### 3. Fiş Verilerini Koruyun

Yazdırılan fişler hassas bilgi içerebilir:
- `web/receipts/` klasörünü düzenli yedekleyin
- Eski fişleri düzenli silin
- Klasör izinlerini kontrol edin

---

## Performans İpuçları

### 1. Debug Modunu Kapatın

Production kullanımda:
```bash
set ESCPOS_DEBUG=False
```

### 2. Eski Fişleri Temizleyin

Manuel temizlik:
```bash
del /Q C:\xampp\htdocs\escpos-netprinter\web\receipts\*.html
```

Otomatik temizlik için Windows Task Scheduler kullanabilirsiniz.

### 3. Geçici Dosyaları Temizleyin

```bash
del /Q C:\xampp\htdocs\escpos-netprinter\web\tmp\*.*
```

---

## SSS (Sık Sorulan Sorular)

### S: Birden fazla bilgisayarda kullanabilir miyim?

**C**: Evet! Her bilgisayarda:
1. Python ve bağımlılıkları kurun
2. escpos-netprinter'ı başlatın
3. SmartStock Connector'ı başlatın
4. Her bilgisayar kendi fişlerini kendi ekranında gösterecek

### S: Gerçek yazıcıya da yazdırabilir miyim?

**C**: Evet! Windows Printer Sharing kullanarak:
1. ESC/POS Network Printer'ı paylaş
2. Gerçek termal yazıcıda "Copy print jobs" ayarını yapın
3. Hem HTML'de hem kağıtta fiş alabilirsiniz

### S: Fişleri ne kadar süre saklarım?

**C**: İhtiyacınıza göre:
- Muhasebe kayıtları için: Minimum 7 yıl
- Günlük operasyonlar için: 30-90 gün
- Disk alanı sınırlıysa: 7-15 gün

### S: Port 9100 neden kullanılıyor?

**C**: Port 9100, HP JetDirect protokolünün standart portudur. Çoğu yazıcı sürücüsü bu portu otomatik tanır.

### S: SmartStock uzak sunucuda, yazıcı local'de nasıl çalışıyor?

**C**: JavaScript kodu tarayıcıda çalıştığı için `localhost` kullanıcının kendi bilgisayarını işaret eder. Bu sayede uzak sunucudaki kod, local yazıcıya erişebilir.

---

## Lisans ve Telif Hakkı

Bu sistem, açık kaynak ESC/POS araçları kullanılarak geliştirilmiştir:

- **escpos-netprinter**: gilbertfl tarafından geliştirildi
- **mike42/escpos-php**: MIT Lisansı
- **Flask**: BSD Lisansı

SmartStock entegrasyonu için özel olarak uyarlanmıştır.

---

## Destek ve İletişim

Sorun yaşıyorsanız:

1. **Logları kontrol edin**: `ESCPOS_DEBUG=True` ile çalıştırın
2. **Port kontrolü yapın**: `netstat -an | findstr :9100`
3. **Python versiyonunu kontrol edin**: `python --version` (3.8+)

---

**Son Güncelleme**: 2025-01-02
**Versiyon**: 1.0
**Uyumlu SmartStock**: v12.0+
