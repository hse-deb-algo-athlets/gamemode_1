# Anleitung Open-Vpn Verbindung auf einem Jetson Nano einrichten

## OpenVpn Zertifikat im Vorfeld erstellen
1. Anleitung auf der Intranet Seite vom Rechenzentrum der HS-Esslingen:
https://intranetportal.hs-esslingen.de/meine-hochschule/hochschul-services/rechenzentrum/zugang-zum-hochschulnetz-mobile-net-netzlaufwerke

2. Aus dem eigenem OpenVPN-HE Ordner (z.B.: C:\Users\vnnnnn\OpenVPN-HE) folgende Dateien auf einem USB Stick kopieren:

- he-ca.txt
- cert.txt
- key.txt

## Installation auf 

### Jetson Nano Orin starten und in WLAN einwählen

1. Unter Applications / Settings / Date & Time (ganz unten in der Liste) das aktuelle Datum und die Uhrzeit einstellen.
2. Unter Applications / Settings / Wi-Fi den WiFi Schalter einschalten und das W-Lan   VPN/WEB anwählen

### Setup VPN

1. Applications / Settings / Network öffnen
2. Hier beim VPN über die + Fläche eine neue OpenVPN Verbindung erstellen
3. Im Fenster Add VPN die erste Option OpenVPN (Compatible with OpenVPN Server) wählen
4. Im neuem Fenster im Reiter Identity folgende Eingaben machen

**Name:** Selbst genannte Name der Verbindung

**General:**
   - Gateway:  
    - openvpn-mia.hs-esslingen.de   (Mitarbeiter der HS-Esslingen)  
    - openvpn.hs-esslingen.de       (Studierender der HS-Esslingen)  

**Authentication:**

|  |  |
|---|---|
| Type:     |                        Password with Certificates (TLS)| 
| User name:           |        Hochschul account  (z.B. Max Schmid=mschmidt)| 
|Passwort:           |         Passwort vom Hochschul Account|
|CA certificate:      |      he-ca.txt   Zertifikat vom USB Stick kopieren|
|User certificate:     |    cert.txt   Zertifikat vom USB Stick kopieren|
|User private key:    |   key.txt   Zertifikat vom USB Stick kopieren|
|User key password : |Ihr Passwort vom Hochschul Account|

> [!WARNING]
> 1. Speichern sie ihr Passwort für den Hochschul Account nicht. 
> 2. Löschen sie die VPN-Konfiguration nach dam Workshop.

1. Mit dem Add  Button oben rechts die Eingabe bestätigen.
2. Die selbst erstellte OpenVpn Verbindung mit dem Schalter starten.