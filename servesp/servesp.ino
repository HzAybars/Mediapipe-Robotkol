#include <WiFi.h>
#include <WiFiUdp.h>
#include <ESP32Servo.h>

// --- MODEM BİLGİLERİNİ GİR ---
const char* ssid = "KENDI_WIFI_ADIN";     // <-- Değiştir
const char* password = "KENDI_WIFI_SIFREN"; // <-- Değiştir

WiFiUDP udp;
unsigned int yerelPort = 4210;
char paketTamponu[255];

Servo s[6];
const int servoPinleri[6] = {13, 12, 14, 27, 26, 25};

void setup() {
  Serial.begin(115200);

  for(int i=0; i<6; i++) s[i].attach(servoPinleri[i]);
  hareketEt(90, 90, 90, 90, 90, 0);

  // Modeme Bağlan
  Serial.print("Baglaniyor");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nBaglandi!");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP()); // *** BU IP'Yİ PYTHON KODUNA YAZ ***

  udp.begin(yerelPort);
}

void loop() {
  int paketBoyutu = udp.parsePacket();
  if (paketBoyutu) {
    int len = udp.read(paketTamponu, 255);
    if (len > 0) paketTamponu[len] = 0;
    cozumle(String(paketTamponu));
  }
}

void cozumle(String veri) {
  int degerler[6];
  int sonVirgul = -1;
  for (int i = 0; i < 6; i++) {
    int sonrakiVirgul = veri.indexOf(',', sonVirgul + 1);
    if (i == 5) sonrakiVirgul = veri.length();
    degerler[i] = veri.substring(sonVirgul + 1, sonrakiVirgul).toInt();
    if (degerler[i] < 0) degerler[i] = 0;
    if (degerler[i] > 180) degerler[i] = 180;
    sonVirgul = sonrakiVirgul;
  }
  hareketEt(degerler[0], degerler[1], degerler[2], degerler[3], degerler[4], degerler[5]);
}

void hareketEt(int s0, int s1, int s2, int s3, int s4, int s5) {
  s[0].write(s0); s[1].write(s1); s[2].write(s2);
  s[3].write(s3); s[4].write(s4); s[5].write(s5);
}