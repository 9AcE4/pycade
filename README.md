# PyCade

PyCade ist eine modulare Retro-Arcade-Anwendung in Python/Pygame.
Die grafische Oberfläche verwendet Unicode-Rahmen, Text und ein animiertes Logo
für einen Terminal-Look. Sie läuft in einem Pygame-Fenster.

## Technologien

- Python
- Pygame für Fenster, Eingaben, Darstellung und Zeitsteuerung
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
├── AGENTS.md                  Arbeitsanweisungen für Coding-Agenten
├── README.md                  Projektbeschreibung und aktueller Stand
├── .gitignore
├── pycade.py                  Einstiegspunkt
├── coordinator.py             Zentraler Programmablauf und Hauptschleife
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

Der Spielekatalog erkennt Unterverzeichnisse mit `__init__.py`, `meta.py` und
`start.py`. Die Metadaten enthalten Titel, Beschreibung und den Status
`playable`. Bei startbaren Einträgen ruft der Launcher `create_game()` auf.
Das zurückgegebene Objekt muss `update(events)` und `draw(surface)` anbieten.
Die Eingaben und Darstellung bleiben damit in die gemeinsame Hauptschleife
eingebunden. Snake ist derzeit als startbar markiert, öffnet aber nur sein Menü.

## Start in einer vorhandenen Python/Pygame-Umgebung

Voraussetzung ist eine vorhandene Python-Umgebung, in der Pygame verfügbar ist.
Starte aus dem Projektordner:

```bash
python pycade.py
```

Der Befehl `python` muss auf diese Umgebung verweisen. Falls er unter Linux
`python3` heißt, verwende entsprechend `python3 pycade.py`.

Optional kann für Tests ohne Python-Bytecode-Erzeugung `python -B pycade.py`
verwendet werden.

Packaging und `pyproject.toml` sind noch nicht umgesetzt. Es gibt bislang keine
zentral deklarierte Dependency-Konfiguration, festgelegten Versionsanforderungen
oder installierbaren Startbefehl.

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

Automatisierte Tests und eine CI-Konfiguration sind noch nicht vorhanden.

## Offene Bereiche

- **Snake:** Eigentliche Spielmechanik, PLAY und OPTIONS fehlen.
- **Pong:** Spielimplementierung fehlt; `start.py` ist leer.
- **Scores:** Es gibt nur einen Vorschautext, keine Score-Verwaltung oder Speicherung.
- **Options:** Es gibt nur einen Vorschautext, keine Einstellungsoberfläche oder
  Speicherung. Farbthemen sind im Code definiert.
- **About:** Es gibt nur einen Vorschautext, keinen eigenen Informationsbildschirm.
- **Fonts:** Consolas ist fest eingestellt und wird nicht mitgeliefert. Eine
  verlässliche plattformübergreifende Schriftstrategie fehlt.
- **Packaging:** `pyproject.toml`, deklarierte Dependencies und ein standardisierter
  Installationsweg fehlen.
- **Tests:** Automatisierte Tests und Prüfungen auf beiden Zielplattformen fehlen.
