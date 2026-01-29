import cv2
import mediapipe as mp
import serial
import socket
import time
import math
import numpy as np

# ================= KULLANICI AYARLARI =================

# Bağlantı Modu Seçimi: "USB" veya "WIFI"
BAGLANTI_MODU = "USB"

# --- USB AYARLARI (Kablolu Mod) ---
USB_PORT = "COM3"       # Aygıt Yöneticisinden portunuza bakın (örn: COM3, COM5)
BAUD_RATE = 115200

# --- WIFI AYARLARI (Kablosuz Mod) ---
# SoftAP Modu kullanıyorsanız varsayılan IP: "192.168.4.1"
# Modem Modu kullanıyorsanız Seri Porttan okuduğunuz IP'yi yazın.
WIFI_IP = "192.168.4.1"
WIFI_PORT = 4210

# --- KALİBRASYON VE HASSASİYET ---
# Referans El Boyutu: Elinizi rahat bir mesafede tutun, ekranda yazan 'Boyut' değerini buraya girin.
REF_EL_BOYUTU = 140     

HASSASIYET_X = 1.8     # Yatay dönüş hızı
HASSASIYET_Y = 1.8     # Dikey kalkış hızı
YUMUSATMA = 0.3        # Titreme filtresi (0.1: Çok Yumuşak - 0.9: Çok Keskin)

# ======================================================

ser = None
sock = None

# 1. Bağlantıyı Başlat
if BAGLANTI_MODU == "USB":
    try:
        ser = serial.Serial(USB_PORT, BAUD_RATE, timeout=0.05)
        print(f"USB Bağlantısı Başarılı: {USB_PORT}")
    except Exception as e:
        print(f"USB Hatası: {e}\n Simülasyon modunda çalışıyor...")

elif BAGLANTI_MODU == "WIFI":
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"Wi-Fi Hedef Ayarlandı: {WIFI_IP}:{WIFI_PORT}")
    except Exception as e:
        print(f"Wi-Fi Hatası: {e}")

# 2. MediaPipe Kurulumu
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# Yumuşatma için önceki açıları sakla
onceki_acilar = [90, 90, 90, 90, 90, 0]

def enterpolasyon(baslangic, bitis, faktor):
    """Hareketleri yumuşatmak için filtre"""
    return baslangic + (bitis - baslangic) * faktor

def aralik_esle(deger, giris_min, giris_max, cikis_min, cikis_max):
    """Değeri bir aralıktan diğerine oranlar"""
    val = (deger - giris_min) * (cikis_max - cikis_min) / (giris_max - giris_min) + cikis_min
    return max(min(val, cikis_max), cikis_min)

print("Sistem Başlatıldı. Çıkmak için 'q' tuşuna basın.")

while True:
    basarili, img = cap.read()
    if not basarili: break
    
    # Görüntüyü çevir (Ayna etkisi)
    img = cv2.flip(img, 1)
    h, w, c = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    sonuclar = hands.process(img_rgb)
    
    # Merkez Çizgileri
    cv2.line(img, (w//2, 0), (w//2, h), (80, 80, 80), 1)
    cv2.line(img, (0, h//2), (w, h//2), (80, 80, 80), 1)

    if sonuclar.multi_hand_landmarks:
        for el_lms in sonuclar.multi_hand_landmarks:
            lm = el_lms.landmark
            
            # --- DERİNLİK HESAPLAMA (Z-Ekseni) ---
            bilek = (lm[0].x * w, lm[0].y * h)
            orta_parmak_kok = (lm[9].x * w, lm[9].y * h)
            mevcut_boyut = math.dist(bilek, orta_parmak_kok)
            
            if mevcut_boyut < 20: mevcut_boyut = 20 # Hata koruması
            
            # Perspektif Düzeltme Katsayısı
            olcek = REF_EL_BOYUTU / mevcut_boyut
            cv2.putText(img, f"Boyut: {int(mevcut_boyut)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # --- KOORDİNAT HESAPLAMA ---
            ham_dx = bilek[0] - (w / 2)
            ham_dy = bilek[1] - (h / 2)
            
            duzeltilmis_dx = ham_dx * olcek * HASSASIYET_X
            duzeltilmis_dy = ham_dy * olcek * HASSASIYET_Y
            
            # Sanal İmleç
            sanal_x = int((w / 2) + duzeltilmis_dx / olcek)
            sanal_y = int((h / 2) + duzeltilmis_dy / olcek)
            cv2.circle(img, (sanal_x, sanal_y), 6, (0, 0, 255), -1)

            # --- AÇI HESAPLAMALARI (6 EKSEN) ---
            
            # 1. Taban (Sağ/Sol)
            aci_taban = aralik_esle(duzeltilmis_dx, -w/2, w/2, 0, 180)
            
            # 2. Omuz (Yukarı/Aşağı)
            aci_omuz = aralik_esle(duzeltilmis_dy, h/2, -h/2, 0, 180)
            
            # 3. Dirsek (İleri/Geri - Derinlik)
            # El büyükse (yakınsa) açı 40, küçükse (uzaksa) açı 160
            aci_dirsek = np.interp(mevcut_boyut, [50, 250], [160, 40])
            
            # 4. Bilek Dikey (Eğim)
            isaret_kok = (lm[5].x * w, lm[5].y * h)
            egim_y = isaret_kok[1] - bilek[1]
            aci_bilek_dikey = np.interp(egim_y, [-80, 80], [180, 0])
            
            # 5. Bilek Dönüş (Burgu)
            serce_kok = (lm[17].x * w, lm[17].y * h)
            dy = serce_kok[1] - isaret_kok[1]
            dx = serce_kok[0] - isaret_kok[0]
            aci_radyan = math.atan2(dy, dx)
            aci_bilek_donus = np.interp(math.degrees(aci_radyan), [-45, 45], [0, 180])
            
            # 6. Kıskaç (Aç/Kapa)
            bas_parmak_uc = (lm[4].x * w, lm[4].y * h)
            isaret_parmak_uc = (lm[8].x * w, lm[8].y * h)
            norm_kiskac = math.dist(bas_parmak_uc, isaret_parmak_uc) * olcek
            aci_kiskac = aralik_esle(norm_kiskac, 20, 130, 0, 180)

            # --- VERİ GÖNDERME ---
            hedefler = [aci_taban, aci_omuz, aci_dirsek, aci_bilek_dikey, aci_bilek_donus, aci_kiskac]
            final_mesaj = []
            
            for i in range(6):
                yumusatilmis = enterpolasyon(onceki_acilar[i], hedefler[i], YUMUSATMA)
                onceki_acilar[i] = yumusatilmis
                final_mesaj.append(int(yumusatilmis))
            
            # Paket Formatı: "90,90,90,90,90,0\n"
            mesaj_str = ",".join(map(str, final_mesaj)) + "\n"
            
            if BAGLANTI_MODU == "USB" and ser:
                ser.write(mesaj_str.encode('utf-8'))
            elif BAGLANTI_MODU == "WIFI" and sock:
                try:
                    sock.sendto(mesaj_str.encode(), (WIFI_IP, WIFI_PORT))
                except: pass

            mp_draw.draw_landmarks(img, el_lms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Robot Kol Kontrol (USB/WiFi)", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if ser: ser.close()
if sock: sock.close()