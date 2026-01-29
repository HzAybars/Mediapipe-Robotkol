<div align="center">

# Yapay Zeka Destekli 6 Eksen Robot Kol Kontrolcüsü

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-Arduino-red?style=for-the-badge&logo=arduino&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Computer%20Vision-green?style=for-the-badge&logo=google&logoColor=white)
![Lisans](https://img.shields.io/badge/Lisans-MIT-grey?style=for-the-badge)

<br>

<p>
  Bu proje, bilgisayar görüsü (computer vision) tekniklerini kullanarak insan el hareketlerini milisaniyeler içinde analiz eder ve 
  bu verileri 6 eksenli bir robotik kola eş zamanlı olarak aktarır. 
  Sistem, görüntü işleme için <strong>MediaPipe</strong>, donanım kontrolü için <strong>ESP32</strong> mikrodenetleyicisini kullanır.
</p>

</div>

<hr>

## Proje Hakkında

Bu sistem, el hareketlerini takip etmek için pahalı sensör eldivenlerine ihtiyaç duymaz. Standart bir web kamerası üzerinden alınan görüntü işlenir, eklem açıları matematiksel olarak hesaplanır ve robot kola iletilir.

### Temel Özellikler

* **Temassız Kontrol:** Sadece kamera görüntüsü ile hassas kontrol.
* **Çift Modlu Bağlantı:** USB (Seri) veya Wi-Fi (UDP) üzerinden haberleşme seçeneği.
* **Akıllı Filtreleme:** Titremeyi önleyen dinamik yumuşatma algoritmaları.
* **Perspektif Düzeltme:** Elin kameraya olan uzaklığına göre derinlik algılama.

---

## Donanım ve Bağlantı Şeması

Proje, ESP32 geliştirme kartı ve 6 adet servo motor üzerine kuruludur. Servo motorlar harici bir güç kaynağı ile beslenmelidir.

### Pin Konfigürasyonu

| Robot Ekseni | Servo İşlevi | ESP32 GPIO Pin |
| :--- | :--- | :--- |
| **Eksen 1** | Taban Dönüşü (Sağ/Sol) | `GPIO 13` |
| **Eksen 2** | Omuz Hareketi (Yukarı/Aşağı) | `GPIO 12` |
| **Eksen 3** | Dirsek Hareketi (İleri/Geri) | `GPIO 14` |
| **Eksen 4** | Bilek Dikey (Eğim) | `GPIO 27` |
| **Eksen 5** | Bilek Rotasyon (Dönüş) | `GPIO 26` |
| **Eksen 6** | Kıskaç (Açma/Kapama) | `GPIO 25` |

> **Güç Uyarısı:** Servo motorları asla doğrudan ESP32'nin 5V pininden beslemeyiniz. En az 3A akım verebilen harici bir güç kaynağı kullanınız ve güç kaynağının GND ucu ile ESP32'nin GND ucunu birleştirmeyi unutmayınız.

---

## Kurulum

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin.

### Yazılım Gereksinimleri

Python 3.x sürümünün yüklü olduğundan emin olun. Proje dizininde terminali açarak gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
---

## Yapılandırma ve Kullanım

### Bağlantı Modunu Seçme

Python kodunun başındaki ayar bloğunu düzenleyerek çalışma modunu belirleyebilirsiniz:

```python
# Kodu USB üzerinden çalıştırmak için:
BAGLANTI_MODU = "USB"
USB_PORT = "COM3"  # Aygıt yöneticisinden kontrol ediniz

# Kodu Wi-Fi üzerinden çalıştırmak için:
BAGLANTI_MODU = "WIFI"
WIFI_IP = "192.168.4.1" # ESP32'nin IP adresi
---

### MIT License

Copyright (c) 2026 HzAybars

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.