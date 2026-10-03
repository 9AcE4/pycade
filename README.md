# PyCade

PyCade ist eine modulare Retro-Arcade-Anwendung in Python/Pygame.
Die grafische Oberfläche verwendet Unicode-Rahmen, Text und ein animiertes Logo
für einen Terminal-Look. Sie läuft in einem Pygame-Fenster.

## Technologien

- Python
- pygame-ce für Fenster, Eingaben, Darstellung und Zeitsteuerung;
  der Python-Importname bleibt `pygame`
- Python-Standardbibliothek, unter anderem `dataclasses`, `importlib`, `pathlib`
  und `textwrap`

## Aktueller Entwicklungsstatus und Funktionsumfang

PyCade ist ein Oberflächen- und Architekturprototyp. Aktuell vorhanden sind:

- Zweistufiger Splashscreen mit Überblendungen und Enter-Bestätigung
- Hauptmenü mit den Einträgen GAMES, SCORES, OPTIONS, ABOUT und EXIT
- Tastaturnavigation mit Pfeiltasten und Enter
- Animierte Snake-Vorschau im Hauptmenü
- Automatisch geladene Spielebibliothek mit Titeln, Beschreibungen und Scrolllogik
- Öffnen des Snake-Menüs mit PLAY, OPTIONS und BACK
- Rücknavigation mit Escape aus der Spielebibliothek und dem Snake-Menü
- Beenden über EXIT oder ein Pygame-QUIT-Ereignis

Es gibt noch kein tatsächlich spielbares Snake oder Pong. Im Snake-Menü führen
PLAY und OPTIONS noch keine Aktion aus. Pong erscheint im Katalog, ist aber
nicht startbar. SCORES, OPTIONS und ABOUT im Hauptmenü besitzen bislang nur
Vorschautexte; ihre Bestätigung öffnet keinen weiteren Bildschirm.

## Projektstruktur

```text
PyCade/
├── README.md                  Projektbeschreibung und aktueller Stand
├── .gitignore
├── pyproject.toml             Projektmetadaten, Dependencies und Packaging
├── pycade.py                  Einstiegspunkt
├── coordinator.py             Zentraler Programmablauf und Hauptschleife
├── assets/fonts/              Mitgelieferte Liberation Mono und Lizenz
├── ascii/
│   ├── frames.py              Unicode-Rahmen
│   └── logos.py               PyCade-Logo
├── engine/
│   ├── window.py              Portable Fenster- und Zeichenflächenerstellung
│   └── controls.py            Globale Ereignisse und Menüsteuerung
├── games/
│   ├── catalog.py             Spieleerkennung und Metadatenprüfung
│   ├── launcher.py            Erzeugung und Prüfung von Spielobjekten
│   ├── snake/
│   │   ├── meta.py            Snake-Metadaten
│   │   ├── start.py           Snake-Menü und Spielfabrik
│   │   └── visuals.py         Darstellung des Snake-Menüs
│   └── pong/
│       ├── meta.py            Pong-Metadaten
│       └── start.py           Noch leer
└── ui/
    ├── layout.py              Größen, Abstände und Panelpositionen
    ├── fonts.py               Zentraler Loader für die mitgelieferte Schrift
    ├── palette.py             Vorbereitete Spielfarben
    ├── rendering.py           Text, Rahmen und animiertes Logo
    ├── splash.py              Startbildschirm
    ├── themes.py              Farbthemen
    ├── games/
    │   └── selection.py       Spielebibliothek
    └── hub/
        ├── mainscreen.py      Hauptmenü
        └── previews/
            ├── about_preview.py
            ├── exit_preview.py
            ├── games_preview.py
            ├── options_preview.py
            └── scores_preview.py
```

Die Python-Paketverzeichnisse enthalten zusätzlich `__init__.py`-Dateien.

## Architektur und Programmfluss

`pycade.py` erstellt den Coordinator und startet dessen Hauptschleife.
Der Coordinator initialisiert Pygame und die Bildschirme, liest Ereignisse,
aktualisiert den aktiven Bereich und zeigt den gezeichneten Frame an.
Nach dem Splashscreen wechselt er zwischen Hauptmenü, Spielebibliothek und
aktivem Spielmodul.

- **Coordinator:** Besitzt Hauptschleife, Bildschirmwechsel und aktives Spiel.
- **Engine:** Erstellt das Fenster und die interne Zeichenfläche; wertet globale
  Beenden-Ereignisse sowie gemeinsame Menüeingaben aus.
- **UI:** Enthält Bildschirme, Layout, Themes und Darstellungsfunktionen.
- **Games:** Erkennt Spielmodule, prüft Metadaten und erstellt Spielobjekte.

Alle Bildschirme zeichnen auf eine interne logische Fläche von **640 × 360**.
Der Coordinator skaliert diese Fläche auf die Fenstergröße und zeigt sie an.
Die Hauptschleife ist auf 60 FPS begrenzt.

Alle UI-Bereiche verwenden die mitgelieferte `LiberationMono-Regular.ttf`.
`ui/fonts.py` bestimmt den absoluten Dateipfad anhand seiner eigenen Position
und lädt die Schrift mit `pygame.font.Font`. Installierte Systemschriften und
das aktuelle Arbeitsverzeichnis beeinflussen die Schriftauswahl damit nicht.
Die Schrift wird unverändert mit ihrer SIL Open Font License 1.1 unter
`assets/fonts/LICENSE.txt` mitgeliefert. Fehlende oder beschädigte
Schriftdateien erzeugen einen Fehler statt eines stillen Systemschrift-Fallbacks.

Initialisierung und Hauptschleife liegen gemeinsam in einem `try/finally`-Block.
Bei normalem Beenden sowie bei Fehlern während der Initialisierung oder der
Hauptschleife setzt der Coordinator `running` auf `False` und ruft
`pygame.quit()` auf. Fehler werden weiterhin an den Aufrufer weitergegeben.

Der Spielekatalog erkennt Unterverzeichnisse mit `__init__.py`, `meta.py` und
`start.py`. Die Metadaten enthalten Titel, Beschreibung und den Status
`playable`. Bei startbaren Einträgen ruft der Launcher `create_game()` auf.
Das zurückgegebene Objekt muss `update(events)` und `draw(surface)` anbieten.
Die Eingaben und Darstellung bleiben damit in die gemeinsame Hauptschleife
eingebunden. Snake ist derzeit als startbar markiert, öffnet aber nur sein Menü.

## Installation und Start

`pyproject.toml` ist die zentrale Projektkonfiguration. Python **>=3.11** ist
eine bewusst gewählte Support-Grenze, keine nachgewiesene technische
Mindestversion des Anwendungscodes. Die einzige externe Runtime-Abhängigkeit
ist **pygame-ce >=2.5.8,<3**. Tatsächlich getestet wurden pygame-ce **2.5.8**
und Python **3.14.7** unter Omarchy/Linux; der Versionsbereich bedeutet nicht,
dass jede darin enthaltene Version bereits geprüft wurde.

Erstelle im Projektordner eine virtuelle Umgebung ohne Systempakete:

| Schritt | Linux (Bash) | Windows (PowerShell) |
|---|---|---|
| Umgebung erstellen | `python3 -m venv .venv` | `py -m venv .venv` |
| Aktivieren | `source .venv/bin/activate` | `.\.venv\Scripts\Activate.ps1` |

Verwende dabei einen Python-Interpreter innerhalb der Support-Grenze.
Nach der Aktivierung sind die Befehle auf beiden Plattformen gleich:

```bash
python -m pip install .
python -m pip check
pycade
```

Der installierte Konsolenbefehl `pycade` ruft `main()` aus `pycade.py` auf und
kann auch außerhalb des Projektordners verwendet werden. Schrift und Lizenz
werden als Paketdaten mitinstalliert. Setuptools wird beim Build benötigt,
ist aber keine zusätzliche Runtime-Abhängigkeit.

Installiere **pygame und pygame-ce nicht gemeinsam in derselben virtuellen
Umgebung**, da beide den Importnamen `pygame` bereitstellen. Verwende für den
neuen Installationsweg eine frische venv; das systemweite Arch-Paket wird dafür
nicht benötigt. Alternativ lässt sich nach der Installation weiterhin
`python -B pycade.py` aus dem Projektordner starten; `-B` verhindert die
Erzeugung von Python-Bytecode-Dateien.

Für einen Distributionsbuild kann das Entwicklungswerkzeug `build` in einer
separaten Build-venv installiert werden. `python -m build` erzeugt Quellarchiv
(sdist) und Wheel unter `dist/`. Für einen Installationstest wird das Wheel
in einer weiteren frischen venv mit `python -m pip install <Wheel-Datei>`
installiert. Prüfe danach `python -m pip check` und starte `pycade` aus einem
anderen Arbeitsverzeichnis, damit der Checkout keine fehlenden Dateien verdeckt.

Windows bleibt Zielplattform, wurde für diesen Packaging-Stand aber noch
nicht praktisch verifiziert.

## Plattformstand und bisherige Prüfung

Der funktionale Kern soll auf Windows und Linux funktionieren. Fenster und
Eingaben verwenden jetzt ausschließlich portable Pygame-Funktionalität.
Das Fenster wird ohne `NOFRAME` erstellt; Fensterbedienung und Dekoration
übernimmt die Desktopumgebung. Die frühere Windows-spezifische Fensterbewegung
wurde vollständig aus `engine/window.py` und `engine/controls.py` entfernt.

Der Commit `92e7550855b6a8e384bcce069e336b5fdc5e41ac` wurde unter Omarchy/Linux
manuell erfolgreich getestet: Start, Splashscreen, Hauptmenü, Navigation und
Snake-Vorschau funktionieren. Es traten keine Laufzeitfehler durch die entfernte
Windows-Fenstersteuerung auf. Eine Windows-Laufzeitprüfung dieses Stands ist
bisher nicht dokumentiert.

Am 03.10.2026 wurde die Absicherung von Initialisierung und Shutdown unter
Omarchy/Linux durch einmalige automatisierte Prüfungen mit dem SDL-Dummy-Treiber
(ohne sichtbares Fenster) geprüft:

- Start und Beenden durch ein Pygame-QUIT-Ereignis
- Aufräumen und Weitergabe eines simulierten Fehlers bei der Fenstererstellung
- Aufräumen und Weitergabe eines simulierten Fehlers in der Hauptschleife
- Splashscreen mit Enter-Übergang, Spielebibliothek, Snake-Menü,
  Pfeiltastennavigation, Escape-Rücknavigation und EXIT

Die Prüfungen waren erfolgreich; die Splash-Wartezeiten wurden für den
Navigationstest verkürzt. Der Benutzer hat anschließend die sichtbare
Desktop-Prüfung unter Omarchy/Linux durchgeführt und einen funktionierenden
Ablauf gemeldet. Eine Windows-Laufzeitprüfung steht weiterhin aus.

Eine dauerhaft im Repository hinterlegte automatisierte Testsuite und eine
CI-Konfiguration sind noch nicht vorhanden.

Die anschließende Schriftumstellung wurde ebenfalls ohne sichtbares Fenster
geprüft: Laden beim Arbeitsverzeichnis `/tmp`, vorhandene Rahmen- und
Logozeichen, gleiche Zeichenfortschritte der geprüften Monospace-Zeichen,
Panelbreiten innerhalb von 640 Pixeln sowie Zeichnen und Navigation durch
Splashscreen, alle Hauptmenüvorschauen, Spielebibliothek und Snake-Menü bis EXIT.
Diese Prüfungen waren erfolgreich. Der Benutzer hat anschließend auch die neue
Schrift unter Omarchy/Linux sichtbar getestet und bestätigt, dass PyCade
weiterhin funktioniert. Eine Windows-Prüfung steht noch aus.

## Prüfung des Packaging-Stands

Am 03.10.2026 wurden unter Omarchy/Linux mit Python **3.14.7** und
pygame-ce **2.5.8** folgende Prüfungen erfolgreich durchgeführt:

- Syntax aller 37 Python-Dateien und `git diff --check`
- Build von sdist und Wheel mit Setuptools 84.0.0 und `build` 1.6.1
- Wheel enthält alle 37 Python-Dateien, Schrift und Lizenz, die Dependency
  `pygame-ce>=2.5.8,<3`, Python-Support-Grenze `>=3.11` und `pycade:main`
- sdist enthält die notwendigen Quellen und Ressourcen; ein daraus erneut
  gebautes Wheel hat dieselben Dateiinhalte
- Installation des Wheels samt pygame-ce aus einem fertigen CPython-3.14-Wheel
  in einer neuen venv mit `include-system-site-packages = false`
- `pip check` ohne Dependency-Probleme
- Prüfung außerhalb des Repositorys mit Python-Isolationsmodus: alle
  Modulimporte stammen aus der Test-venv, ebenso der `pygame`-Import von
  pygame-ce; Font und Lizenz sind im installierten Paket vorhanden
- Headless-Prüfung von Font-Zeichen und Darstellung, Layout, Spielekatalog,
  Splash/Enter, allen Hauptmenüvorschauen, Spielebibliothek, Snake-Menü,
  Escape, EXIT, QUIT und Cleanup bei einem Initialisierungsfehler
- Installierter Entry Point und erzeugter `pycade`-Launcher funktionieren;
  der Launcher wurde mit SDL-Dummy-Treiber und kontrolliertem QUIT ausgeführt

Der Build wurde in einer temporären Projektkopie durchgeführt, mit getrennten
Build- und Installations-venvs. Für den Build wurden die Build-Abhängigkeiten
vorab in der Build-venv installiert und `python -m build --no-isolation`
verwendet. Die Navigationstests verkürzten die Splash-Wartezeiten.
Es wurde kein sichtbares Fenster gestartet. Die sichtbare Prüfung dieses
Packaging-/pygame-ce-Stands und eine praktische Windows-Prüfung stehen aus.
Die Prüfskripte waren einmalig; eine dauerhaft hinterlegte Testsuite wurde
dadurch nicht eingeführt.

## Offene Bereiche

- **Snake:** Eigentliche Spielmechanik, PLAY und OPTIONS fehlen.
- **Pong:** Spielimplementierung fehlt; `start.py` ist leer.
- **Scores:** Es gibt nur einen Vorschautext, keine Score-Verwaltung oder Speicherung.
- **Options:** Es gibt nur einen Vorschautext, keine Einstellungsoberfläche oder
  Speicherung. Farbthemen sind im Code definiert.
- **About:** Es gibt nur einen Vorschautext, keinen eigenen Informationsbildschirm.
- **Tests:** Eine dauerhaft hinterlegte Testsuite und CI fehlen;
  eine Windows-Laufzeitprüfung steht aus.
