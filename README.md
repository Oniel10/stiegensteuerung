# Stiege

Die Vorlage beschreibt die Loxone-Logik als Grundlage für Wiederaufbau und HA-Ersatzbetrieb. Die Automation in HA muss für die jeweilige Installation eingerichtet und getestet werden.

## Signale zuordnen

| Signal | Herkunft oder Ziel |
| --- | --- |
| Eintritt unten und Austritt unten | Zwei Richtungsimpulse des unteren Melders |
| Eintritt oben und Austritt oben | Zwei Richtungsimpulse des oberen Melders |
| Helligkeit unten und oben | KNX-Helligkeitswerte in Lux |
| Dauer-EIN | Status des Bedienelements |
| Lichtbefehl und Rückmeldung | Lichtaktor |
| Nachtsperre unten | Sperrobjekt des unteren Melders |
| Lebenszeichen | Eigene KNX-Gruppenadresse vom Loxone-Miniserver |

## Ablauf

- Tagsüber löst ein Eintritt bei ausreichender Dunkelheit den Nachlauf aus und erhöht die geschätzte Belegung. Ein Austritt zählt nur bei vorhandener Belegung. Nach dem letzten Austritt bleiben 30 Sekunden Restlicht.
- Nachts von 22:00 bis 06:00 ist der untere Melder gesperrt. Ein Eintritt oben startet den verkürzten Nachlauf bei Dunkelheit.
- Richtwerte sind 6 Lux, 10 Minuten tags und 2 Minuten nachts. Bei bereits laufendem Lichtbedarf darf dessen Eigenlicht eine Verlängerung nicht verhindern.
- Dauer-EIN hat Vorrang und ist auf 8 Stunden begrenzt.
- Loxone sendet alle 30 Sekunden ein Lebenszeichen. Nach 60 Sekunden ohne Empfang soll der HA-Notbetrieb übernehmen. Nach Wiederkehr darf nur eine Steuerung Lichtbefehle ausgeben. In HA den aktiven Steuerungsmodus anzeigen.
- Personenstand, laufende Zeiten und Handbetrieb beim Ausfall und bei der Rückgabe ausdrücklich prüfen. Ein fehlender KNX-Zugang lässt sich durch den HA-Notbetrieb nicht ersetzen.

## Abnahme

Tag, Nacht, letzter Austritt, Dauer-EIN, HA-Neustart und Rückgabe an Loxone prüfen. Bei der Umschaltung muss der aktive Steuerungsmodus erkennbar sein.
