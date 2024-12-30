# Verslag

## Vereisten

Om deze code correct te doen werken zijn er een aantal vereisten:
- Alle dependancies moeten geinstaleerd worden (zie requirements.txt)
- Er moet in de root directory een bestand genaamd ip_addresses.txt aanwezig zijn met 2 ip address per lijn (elke lijn is gescheiden met een enter)
- In de root directory moet een token.txt bestand aanwezig zijn met daarin de token voor de dropbox repo waar je je backups in gaat maken
- In het healt_monitoring.py script moet de log_dir aangepast worden naar het pad waar de github repo waar je de log files wilt opslaan staat
- De variable git_path in het main script moet aangepast worden naar het pad naar de github repo die je gebruikt om backups op te slaan
- In het commando.py script moet de correcte informatie voor je eigen github repo ingevuld worden
- Het script main.py moet steeds uitgevoerd worden vanuit de root directory

## main.py

Dit is het main script waaruit je met variablen de andere script kan aanroepen. De mogelijke variablen zijn de volgende:
- -m roept het healt_monitoring.py script aan. Deze zal elke 60 seconden de systeem informatie loggen (zowel naar de console als naar de logs directory). Dit script zal dit doen voor alle ip addressen in de ip_addresses.py. Bij de -m module is het -u argument verplicht. Het -u argument wordt gebruikt om de username in te geven. We gaan hiervoor uit dat elke machine een user heeft met dezelfde naam (om systeembeheer te vergemakkelijken). De authenticatie gebeurd via een key, dus passwoorden zijn niet nodig.
- -b roept het script backup_drive.py aan. Achter de -b moet je het ip address van de host specifieren waar je een backup van gaat maken. Vervolgens heb je ook nog het -u argument nodig en ook het -d argument. Het -d argument specifierd de directory waar je een backup van gaat maken. Voor de backup is er gekozen voor dropbox. Hier heb je ook een token voor nodig die je steekt in de token.txt in de root folden.
- -c roept het script commandos.py aan. Dit script maakt ook gebruik van de ip_adresses.txt file. Hier moet ook echter het -u argument gebruikt worden om de username in te geven voor de hosts. Voor de authenticatie geld hier hetzelfde pricipe als bij -m.

Bij de -m module zal het script oneindig blijven lopen tot de gebruiker dit geforceerd stopt met crt+C. Als de gebruiker deze toesten induwt zullen de logs gepushed worden naar de opgegeven github repo.

## Modules

Hieronder enkele belangrijke punten bij de modules:
- Bij de -c module is het belangrijk dat de commands in een yml file staan. Een voorbeeld van een goed opgestelde yml:
```
commands:
  - uname -a
  - uptime
```
- Bij de -m en -c module wordt de ip_addresses.txt gebruikt. Een voorbeeld van een goed opgestelde txt:
```
192.168.0.195
192.168.0.111
```
- Voor de -b module wordt er gebruik gemaakt van dropbox. Dit komt omdat het een gratis optie had tot 2 gigabyte. In een echte omgeving moet dit natuurlijk aangepast worden aan de cloud opslag die het bedrijf/omgeving gebruikt.
- De naamgeving van de logs is eenvoudig (bij de -m module). Het ip address van de host wordt gebruikt als naam. Vervolgens worden alle nieuwe logs vanonder in de log file geplakt.
- De naamgeving bij de -b module werkt als volgt:
```
[ip address van host]_[YEAR-MOTH-DAY]
```

## Ethische reflectie

Deze oplossing maakt het beheer van IT infrastructuur veel eenvoudiger en sneller. De health monitoring van de IT apparaten gebreurt automatisch en ook gratis. Je kan het script laten draaien en de logs blijven verzamelen. Op deze manier kan je bijvoorbeeld zien of er ineens een spike in CPU gebruik is om dit dan vervolgens te onderzoeken en op te lossen indien dit onverwacht zou zijn (bijvoorbeeld iemand die ongewenst de resources gebruikt). Het is ook gratis wat het voor kleinere omgevingen makkelijker maakt omdat ze geen dure oplossingen hoeven aan te schaffen. 
<br>
<br>
De commando module maakt het ook erg eenvoudig om verschillende presets van commando's klaar te zetten. Zo kan je deze op alle machines die dit nodig hebben uitvoeren zonder dat je via SSH naar alle machines appart moet verbinden en dit 1 voor 1 uitvoeren.
<br>
<br>
Met backups maak je je infrastructuur ook veel beter bestendig tegen aanvallen. Als al je data bijvoorbeeld encrypted wordt dan kan je deze nog altijd herstellen doordat je een backup hebt. Ook als er iets mis gaat met je data kan je hier nog op terug vallen.
<br>
<br>
Bij gebruik van deze script zijn er echter aan aantal zaken erg belangrijk:
- Deze scripts maken SSH connecties met de hosts. Als deze script dus op de een of andere mannier aangepast worden kunnen deze scripts dus mogelijk malicious zaken doen op de hosts. Daarom is het van uiterst balang dat het apparaat dat deze scripts uitvoerd goed beveiligd is.
- De github repo waarnaar de logs gepushed worden kan best op privaat gezet worden. Anders kan iedereen de log files zonder toestemming bekijken.
- De uitvoerder van deze scripts moet de systemen bezitten of toestemming hebben om dit uit te voeren op de desbetreffende systemen.