#include <ESP32Servo.h>

Servo s[6];
// PINLER: Taban, Omuz, Dirsek, Bilek_Dikey, Bilek_Donus, Kiskac
const int servoPinleri[6] = {13, 12, 14, 27, 26, 25}; 

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(5); // Gecikmeyi düşür

  // Servoları Başlat
  for(int i=0; i<6; i++) {
    s[i].attach(servoPinleri[i]);
  }
  // Başlangıç Duruşu
  hareketEt(90, 90, 90, 90, 90, 0); 
}

void loop() {
  if (Serial.available() > 0) {
    String veri = Serial.readStringUntil('\n');
    cozumle(veri);
  }
}

void cozumle(String veri) {
  int degerler[6];
  int sonVirgul = -1;
  
  for (int i = 0; i < 6; i++) {
    int sonrakiVirgul = veri.indexOf(',', sonVirgul + 1);
    if (i == 5) sonrakiVirgul = veri.length();
    
    degerler[i] = veri.substring(sonVirgul + 1, sonrakiVirgul).toInt();
    
    // Güvenlik sınırları
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