# -*- coding: utf-8 -*-
"""
DraveExplorer - toegankelijke, snelle file explorer (Dravenlock).
Lokaal, offline, donationware. PyQt6.

Versie: 0.1
"""

import os
import sys
import shutil
import traceback



APP_NAAM = "DraveExplorer"
APP_VERSIE = "0.7.1"
DONATIE_URL = "https://paypal.me/roger076"
CONTACT = "service@dravenlock.nl"

# ----------------------------------------------------------------------------
# Vroege foutafvanging: schrijf startfouten naar app-fout.txt naast dit bestand
# ----------------------------------------------------------------------------
BASIS = os.path.dirname(os.path.abspath(__file__))
FOUT_BESTAND = os.path.join(BASIS, "app-fout.txt")


def _schrijf_fout(tekst):
    try:
        with open(FOUT_BESTAND, "w", encoding="utf-8") as f:
            f.write(tekst)
    except Exception:
        pass


def _excepthook(exctype, value, tb):
    melding = "".join(traceback.format_exception(exctype, value, tb))
    _schrijf_fout(melding)
    sys.__excepthook__(exctype, value, tb)


sys.excepthook = _excepthook

# ----------------------------------------------------------------------------
# Qt-imports (na de excepthook zodat importfouten ook gelogd worden)
# ----------------------------------------------------------------------------
try:
    from PyQt6.QtCore import (
        Qt, QDir, QStorageInfo, QUrl, QSortFilterProxyModel,
        QThread, pyqtSignal, QLocale, QTimer, QFileInfo,
        QThreadPool, QRunnable, QObject, QSize,
    )
    from PyQt6.QtGui import (
        QAction, QIcon, QFileSystemModel, QStandardItemModel, QStandardItem,
        QDesktopServices, QKeySequence, QFont, QColor, QPainter, QPixmap,
        QImage, QImageReader, QPalette, QMovie,
    )
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTreeView, QTabWidget, QLineEdit, QToolButton, QLabel, QScrollArea,
        QFrame, QPushButton, QSplitter, QStackedWidget, QMenu, QMessageBox,
        QInputDialog, QFileIconProvider, QHeaderView,
        QDialog, QTextBrowser, QComboBox, QSpinBox, QFormLayout, QCheckBox,
        QDialogButtonBox, QStatusBar, QAbstractItemView,
        QListView, QStyledItemDelegate, QPlainTextEdit, QSlider,
    )
    # Optionele Qt-modules voor PDF- en mediavoorbeeld (horen bij PyQt6)
    try:
        from PyQt6.QtPdf import QPdfDocument
        from PyQt6.QtPdfWidgets import QPdfView
        HEEFT_PDF = True
    except Exception:
        HEEFT_PDF = False
    try:
        from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
        from PyQt6.QtMultimediaWidgets import QVideoWidget
        HEEFT_MEDIA = True
    except Exception:
        HEEFT_MEDIA = False
except Exception:
    _schrijf_fout(traceback.format_exc())
    raise

# Optioneel: send2trash voor veilig verwijderen naar de prullenbak
try:
    from send2trash import send2trash
    HEEFT_PRULLENBAK = True
except Exception:
    HEEFT_PRULLENBAK = False

IS_WINDOWS = os.name == "nt"

# ----------------------------------------------------------------------------
# Huisstijl (Dravenlock)
# ----------------------------------------------------------------------------
BG = "#0e0e11"
PANEL = "#16161b"
PANEL2 = "#1c1c22"
TEXT = "#d4d4d4"
MUTED = "#8a8a94"
ACCENT = "#6fa3d6"
ACCENT_DIM = "#4d7aa8"
LINE = "#23232b"
WAARSCHUW = "#d68a6f"   # bijna-vol balk
GOED = "#6fa3d6"

# ----------------------------------------------------------------------------
# Vertalingen (NL basis + EN), met OS-taaldetectie en handmatige keuze
# ----------------------------------------------------------------------------
TEKST = {
    "nl": {
        "snelkoppelingen": "Snelkoppelingen",
        "deze_pc": "Deze pc",
        "netwerk": "Netwerk",
        "mappen": "Mappen",
        "home": "Persoonlijke map",
        "bureaublad": "Bureaublad",
        "documenten": "Documenten",
        "downloads": "Downloads",
        "afbeeldingen": "Afbeeldingen",
        "muziek": "Muziek",
        "video": "Video's",
        "terug": "Terug",
        "vooruit": "Vooruit",
        "omhoog": "Omhoog",
        "vernieuwen": "Vernieuwen",
        "nieuwe_tab": "Nieuwe tab",
        "adres": "Pad of locatie...",
        "filter": "Filter / zoek in deze map...",
        "vrij_van": "{vrij} vrij van {totaal}",
        "items": "{n} items",
        "items_sel": "{n} items - {sel} geselecteerd ({grootte})",
        "kol_naam": "Naam",
        "kol_grootte": "Grootte",
        "kol_type": "Type",
        "kol_gewijzigd": "Gewijzigd",
        "kol_pad": "Locatie",
        "openen": "Openen",
        "open_nieuwe_tab": "Openen in nieuwe tab",
        "open_map_locatie": "Map openen in verkenner",
        "knippen": "Knippen",
        "kopieren": "Kopieren",
        "plakken": "Plakken",
        "verwijderen": "Verwijderen",
        "hernoemen": "Hernoemen",
        "nieuwe_map": "Nieuwe map",
        "alles_select": "Alles selecteren",
        "eigenschappen": "Eigenschappen",
        "kopieer_pad": "Pad kopieren",
        "menu_bestand": "Bestand",
        "menu_bewerken": "Bewerken",
        "menu_beeld": "Beeld",
        "menu_help": "Help",
        "verborgen_tonen": "Verborgen bestanden tonen",
        "weergave_lijst": "Lijstweergave",
        "weergave_iconen": "Grote iconen",
        "weergave": "Weergave",
        "favorieten": "Favorieten",
        "fav_toevoegen": "Aan favorieten toevoegen",
        "fav_verwijderen": "Uit favorieten verwijderen",
        "icoon_grootte_lbl": "Icoongrootte (iconenweergave)",
        "vrij_op_station": "{vrij} vrij van {totaal} op dit station",
        "type_filter": "Type",
        "type_alles": "Alle bestanden",
        "type_afbeeldingen": "Afbeeldingen",
        "type_documenten": "Documenten",
        "type_muziek": "Muziek",
        "type_video": "Video",
        "type_archieven": "Archieven",
        "voorbeeld": "Voorbeeld",
        "voorbeeld_leeg": "Selecteer een bestand voor een voorbeeld",
        "voorbeeld_geen": "Geen voorbeeld voor dit bestandstype",
        "voorbeeld_sluiten": "Voorbeeld sluiten",
        "afspelen": "Afspelen",
        "pauze": "Pauze",
        "stop": "Stop",
        "tekst_groter": "Tekst groter",
        "tekst_kleiner": "Tekst kleiner",
        "instellingen": "Instellingen",
        "afsluiten": "Afsluiten",
        "snelgids": "Snelgids",
        "over": "Over / Donatie",
        "diep_zoeken": "In submappen zoeken",
        "zoeken_bezig": "Zoeken in submappen...",
        "zoekresultaten": "{n} resultaten voor \"{term}\"",
        "geen_resultaten": "Geen resultaten",
        "stop": "Stop",
        "wis_zoeken": "Zoekresultaten wissen",
        "bevestig_verwijder_titel": "Verwijderen",
        "bevestig_verwijder": "{n} item(s) verwijderen?",
        "naar_prullenbak": "Naar prullenbak",
        "permanent_verwijder": "Permanent verwijderen",
        "permanent_vraag": "{n} item(s) PERMANENT verwijderen? Dit kan niet ongedaan gemaakt worden.",
        "fout": "Fout",
        "nieuwe_map_naam": "Naam van de nieuwe map:",
        "hernoem_naar": "Nieuwe naam:",
        "map_naam_bestaat": "Er bestaat al een item met die naam.",
        "kan_niet_openen": "Kan dit item niet openen.",
        "taal": "Taal",
        "taal_auto": "Automatisch (computertaal)",
        "lettergrootte": "Lettergrootte",
        "hoog_contrast": "Extra hoog contrast",
        "opslaan": "Opslaan",
        "annuleren": "Annuleren",
        "naam": "Naam",
        "locatie": "Locatie",
        "grootte": "Grootte",
        "type_lbl": "Type",
        "gewijzigd": "Gewijzigd",
        "gemaakt": "Gemaakt",
        "map": "Map",
        "bestand": "Bestand",
        "bevat": "Bevat",
        "n_bestanden_mappen": "{b} bestanden, {m} mappen",
        "donatie": "Donatie",
        "leeg": "(leeg)",
        "berekenen": "berekenen...",
    },
    "en": {
        "snelkoppelingen": "Shortcuts",
        "deze_pc": "This PC",
        "netwerk": "Network",
        "mappen": "Folders",
        "home": "Home folder",
        "bureaublad": "Desktop",
        "documenten": "Documents",
        "downloads": "Downloads",
        "afbeeldingen": "Pictures",
        "muziek": "Music",
        "video": "Videos",
        "terug": "Back",
        "vooruit": "Forward",
        "omhoog": "Up",
        "vernieuwen": "Refresh",
        "nieuwe_tab": "New tab",
        "adres": "Path or location...",
        "filter": "Filter / search this folder...",
        "vrij_van": "{vrij} free of {totaal}",
        "items": "{n} items",
        "items_sel": "{n} items - {sel} selected ({grootte})",
        "kol_naam": "Name",
        "kol_grootte": "Size",
        "kol_type": "Type",
        "kol_gewijzigd": "Modified",
        "kol_pad": "Location",
        "openen": "Open",
        "open_nieuwe_tab": "Open in new tab",
        "open_map_locatie": "Open folder in explorer",
        "knippen": "Cut",
        "kopieren": "Copy",
        "plakken": "Paste",
        "verwijderen": "Delete",
        "hernoemen": "Rename",
        "nieuwe_map": "New folder",
        "alles_select": "Select all",
        "eigenschappen": "Properties",
        "kopieer_pad": "Copy path",
        "menu_bestand": "File",
        "menu_bewerken": "Edit",
        "menu_beeld": "View",
        "menu_help": "Help",
        "verborgen_tonen": "Show hidden files",
        "weergave_lijst": "List view",
        "weergave_iconen": "Large icons",
        "weergave": "View as",
        "favorieten": "Favorites",
        "fav_toevoegen": "Add to favorites",
        "fav_verwijderen": "Remove from favorites",
        "icoon_grootte_lbl": "Icon size (icon view)",
        "vrij_op_station": "{vrij} free of {totaal} on this drive",
        "type_filter": "Type",
        "type_alles": "All files",
        "type_afbeeldingen": "Images",
        "type_documenten": "Documents",
        "type_muziek": "Music",
        "type_video": "Video",
        "type_archieven": "Archives",
        "voorbeeld": "Preview",
        "voorbeeld_leeg": "Select a file to preview",
        "voorbeeld_geen": "No preview for this file type",
        "voorbeeld_sluiten": "Close preview",
        "afspelen": "Play",
        "pauze": "Pause",
        "stop": "Stop",
        "tekst_groter": "Larger text",
        "tekst_kleiner": "Smaller text",
        "instellingen": "Settings",
        "afsluiten": "Quit",
        "snelgids": "Quick guide",
        "over": "About / Donate",
        "diep_zoeken": "Search subfolders",
        "zoeken_bezig": "Searching subfolders...",
        "zoekresultaten": "{n} results for \"{term}\"",
        "geen_resultaten": "No results",
        "stop": "Stop",
        "wis_zoeken": "Clear search results",
        "bevestig_verwijder_titel": "Delete",
        "bevestig_verwijder": "Delete {n} item(s)?",
        "naar_prullenbak": "To recycle bin",
        "permanent_verwijder": "Delete permanently",
        "permanent_vraag": "Permanently delete {n} item(s)? This cannot be undone.",
        "fout": "Error",
        "nieuwe_map_naam": "Name of the new folder:",
        "hernoem_naar": "New name:",
        "map_naam_bestaat": "An item with that name already exists.",
        "kan_niet_openen": "Cannot open this item.",
        "taal": "Language",
        "taal_auto": "Automatic (system language)",
        "lettergrootte": "Font size",
        "hoog_contrast": "Extra high contrast",
        "opslaan": "Save",
        "annuleren": "Cancel",
        "naam": "Name",
        "locatie": "Location",
        "grootte": "Size",
        "type_lbl": "Type",
        "gewijzigd": "Modified",
        "gemaakt": "Created",
        "map": "Folder",
        "bestand": "File",
        "bevat": "Contains",
        "n_bestanden_mappen": "{b} files, {m} folders",
        "donatie": "Donate",
        "leeg": "(empty)",
        "berekenen": "calculating...",
    },
}


def detecteer_taal():
    """Bepaal NL of EN op basis van de computertaal."""
    try:
        naam = QLocale.system().name().lower()  # bv 'nl_nl'
        if naam.startswith("nl"):
            return "nl"
    except Exception:
        pass
    return "en"


# ----------------------------------------------------------------------------
# Config (portable JSON naast app)
# ----------------------------------------------------------------------------
import json

CONFIG_BESTAND = os.path.join(BASIS, "config.json")
STANDAARD_CONFIG = {
    "taal": "auto",
    "lettergrootte": 11,
    "hoog_contrast": False,
    "verborgen_tonen": False,
    "weergave": "lijst",
    "icoon_grootte": 128,
    "favorieten": [],
    "voorbeeld_zichtbaar": False,
    "laatste_pad": "",
    "open_tabs": [],
    "actieve_tab": 0,
    "venster": [1100, 720],
}


def laad_config():
    cfg = dict(STANDAARD_CONFIG)
    try:
        if os.path.exists(CONFIG_BESTAND):
            with open(CONFIG_BESTAND, "r", encoding="utf-8") as f:
                cfg.update(json.load(f))
    except Exception:
        pass
    return cfg


def bewaar_config(cfg):
    try:
        tmp = CONFIG_BESTAND + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
        os.replace(tmp, CONFIG_BESTAND)
    except Exception:
        pass


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def mensvriendelijke_grootte(aantal_bytes):
    """Bytes -> leesbaar (B/KB/MB/GB/TB)."""
    try:
        b = float(aantal_bytes)
    except Exception:
        return ""
    if b < 1024:
        return "%d B" % int(b)
    for eenheid in ("KB", "MB", "GB", "TB", "PB"):
        b /= 1024.0
        if b < 1024 or eenheid == "PB":
            if b < 10:
                return "%.1f %s" % (b, eenheid)
            return "%.0f %s" % (b, eenheid)
    return "%.0f PB" % b


def windows_drive_type(root):
    """Geef het stationstype op Windows: removable/fixed/remote/cdrom/ramdisk."""
    try:
        import ctypes
        t = ctypes.windll.kernel32.GetDriveTypeW(ctypes.c_wchar_p(root))
        return {2: "removable", 3: "fixed", 4: "remote",
                5: "cdrom", 6: "ramdisk"}.get(t, "unknown")
    except Exception:
        return "unknown"


def bepaal_drive_type(volume):
    """Bepaal het type station (cross-platform best effort)."""
    root = volume.rootPath()
    if IS_WINDOWS:
        r = root
        if not r.endswith("\\"):
            r = r + "\\"
        return windows_drive_type(r)
    # Niet-Windows: heuristiek op bestandssysteemtype
    fs = bytes(volume.fileSystemType()).decode("ascii", "ignore").lower()
    if any(k in fs for k in ("cifs", "smb", "nfs", "afp", "fuse.sshfs")):
        return "remote"
    return "fixed"


def verzamel_stations():
    """Lijst van stations als dicts: {root, naam, totaal, vrij, gebruikt, type}."""
    resultaat = []
    for v in QStorageInfo.mountedVolumes():
        try:
            if not (v.isValid() and v.isReady()):
                continue
            totaal = v.bytesTotal()
            if totaal <= 0:
                continue
            root = v.rootPath()
            # Pseudo-mounts op Linux overslaan (niet relevant op Windows)
            if not IS_WINDOWS:
                if root.startswith(("/snap", "/proc", "/sys", "/dev", "/run")):
                    continue
            vrij = v.bytesAvailable()
            naam = v.displayName() or root
            resultaat.append({
                "root": root,
                "naam": naam,
                "totaal": totaal,
                "vrij": vrij,
                "gebruikt": max(0, totaal - vrij),
                "type": bepaal_drive_type(v),
            })
        except Exception:
            continue
    return resultaat


def standaard_mappen():
    """Geef bekende gebruikersmappen terug als {sleutel: pad}."""
    thuis = os.path.expanduser("~")
    m = {"home": thuis}
    paren = {
        "bureaublad": ["Desktop", "Bureaublad"],
        "documenten": ["Documents", "Documenten"],
        "downloads": ["Downloads"],
        "afbeeldingen": ["Pictures", "Afbeeldingen"],
        "muziek": ["Music", "Muziek"],
        "video": ["Videos", "Video's"],
    }
    for sleutel, namen in paren.items():
        for n in namen:
            p = os.path.join(thuis, n)
            if os.path.isdir(p):
                m[sleutel] = p
                break
    return m


def pad_segmenten(pad):
    """Splits een pad in (volledig_pad, label)-paren voor de broodkruimel."""
    pad = os.path.normpath(pad)
    delen = []
    drive, rest = os.path.splitdrive(pad)
    if drive:
        # Windows: C: , dan submappen
        wortel = drive + os.sep
        delen.append((wortel, drive))
        huidig = wortel
        for seg in rest.split(os.sep):
            if seg:
                huidig = os.path.join(huidig, seg)
                delen.append((huidig, seg))
    elif pad.startswith("/"):
        # Unix: begin bij /
        delen.append(("/", "/"))
        huidig = "/"
        for seg in pad.split("/"):
            if seg:
                huidig = os.path.join(huidig, seg)
                delen.append((huidig, seg))
    else:
        huidig = ""
        for seg in pad.split(os.sep):
            if seg:
                huidig = os.path.join(huidig, seg) if huidig else seg
                delen.append((huidig, seg))
    return delen


# ----------------------------------------------------------------------------
# Miniaturen (thumbnails) voor afbeeldingen: laden op de achtergrond + cache
# ----------------------------------------------------------------------------
AFBEELDING_EXT = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp",
                  ".tif", ".tiff", ".ico"}

# Categorieën voor het type-filter (op basis van extensie)
DOCUMENT_EXT = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
                ".txt", ".rtf", ".odt", ".ods", ".odp", ".md", ".csv", ".epub"}
MUZIEK_EXT = {".mp3", ".flac", ".m4a", ".ogg", ".wav", ".aac", ".wma",
              ".opus", ".aiff", ".alac"}
VIDEO_EXT = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
             ".m4v", ".mpg", ".mpeg", ".3gp", ".ts"}
ARCHIEF_EXT = {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".cab",
               ".iso"}

# Tekstbestanden die in het voorbeeldvenster getoond kunnen worden
TEKST_EXT = {".txt", ".md", ".markdown", ".csv", ".tsv", ".log", ".ini",
             ".cfg", ".conf", ".json", ".xml", ".yaml", ".yml", ".html",
             ".htm", ".css", ".js", ".ts", ".py", ".java", ".c", ".cpp",
             ".h", ".hpp", ".cs", ".rb", ".go", ".rs", ".php", ".sql",
             ".sh", ".bat", ".ps1", ".tex", ".srt", ".vtt", ".nfo", ".rtf"}

# (sleutel, extensieset) voor de keuzelijst; None = alles tonen
TYPE_CATEGORIEEN = [
    ("type_alles", None),
    ("type_afbeeldingen", AFBEELDING_EXT | {".svg", ".heic", ".heif"}),
    ("type_documenten", DOCUMENT_EXT),
    ("type_muziek", MUZIEK_EXT),
    ("type_video", VIDEO_EXT),
    ("type_archieven", ARCHIEF_EXT),
]


def is_afbeelding(pad):
    return os.path.splitext(pad)[1].lower() in AFBEELDING_EXT


class _ThumbSignalen(QObject):
    klaar = pyqtSignal(str, QImage)


class _ThumbTaak(QRunnable):
    def __init__(self, pad, grootte, signalen):
        super().__init__()
        self.pad = pad
        self.grootte = grootte
        self.signalen = signalen

    def run(self):
        try:
            reader = QImageReader(self.pad)
            reader.setAutoTransform(True)
            sz = reader.size()
            if sz.isValid() and (sz.width() > self.grootte or sz.height() > self.grootte):
                sz.scale(self.grootte, self.grootte, Qt.AspectRatioMode.KeepAspectRatio)
                reader.setScaledSize(sz)
            img = reader.read()
            if not img.isNull():
                self.signalen.klaar.emit(self.pad, img)
        except Exception:
            pass


class ThumbnailManager(QObject):
    """Beheert het laden en cachen van miniaturen voor afbeeldingsbestanden."""
    bijgewerkt = pyqtSignal(str)  # pad

    def __init__(self, grootte=128, parent=None):
        super().__init__(parent)
        self.grootte = grootte
        self.cache = {}        # pad -> QPixmap
        self.bezig = set()     # paden in de wachtrij
        self.signalen = _ThumbSignalen()
        self.signalen.klaar.connect(self._ontvangen)
        self.pool = QThreadPool.globalInstance()

    def zet_grootte(self, grootte):
        if grootte != self.grootte:
            self.grootte = grootte
            self.cache.clear()
            self.bezig.clear()

    def vraag(self, pad):
        """Geef de miniatuur als die klaar is, anders None (en start het laden)."""
        pm = self.cache.get(pad)
        if pm is not None:
            return pm
        if pad in self.bezig:
            return None
        try:
            if os.path.getsize(pad) > 40 * 1024 * 1024:  # >40MB overslaan
                return None
        except Exception:
            return None
        self.bezig.add(pad)
        self.pool.start(_ThumbTaak(pad, self.grootte, self.signalen))
        return None

    def _ontvangen(self, pad, img):
        self.bezig.discard(pad)
        try:
            pm = QPixmap.fromImage(img)
            if not pm.isNull():
                if len(self.cache) > 600:   # cache begrenzen
                    self.cache.clear()
                self.cache[pad] = pm
                self.bijgewerkt.emit(pad)
        except Exception:
            pass


class MiniatuurDelegate(QStyledItemDelegate):
    """Vervangt het pictogram door een miniatuur voor afbeeldingsbestanden."""
    def __init__(self, manager, parent=None):
        super().__init__(parent)
        self.manager = manager

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        try:
            pad = index.data(QFileSystemModel.Roles.FilePathRole)
        except Exception:
            pad = None
        if pad and is_afbeelding(pad):
            pm = self.manager.vraag(pad)
            if pm is not None and not pm.isNull():
                # Alleen het pictogram vervangen; de icoonmaat NIET verkleinen,
                # zodat elk item (map of foto) evenveel ruimte voor de naam houdt.
                option.icon = QIcon(pm)


# ----------------------------------------------------------------------------
# Proxy: mappen eerst sorteren + naamfilter binnen de huidige map
# ----------------------------------------------------------------------------
class MapEersteProxy(QSortFilterProxyModel):
    def __init__(self, fs_model, parent=None):
        super().__init__(parent)
        self.fs = fs_model
        self.setSourceModel(fs_model)
        self._filter = ""
        self._root_pad = ""
        self._type_ext = None   # None = alle types; anders een set extensies
        self.kolom_labels = None
        self.setDynamicSortFilter(True)

    def headerData(self, section, orientation, role):
        if (orientation == Qt.Orientation.Horizontal and
                role == Qt.ItemDataRole.DisplayRole and self.kolom_labels and
                0 <= section < len(self.kolom_labels)):
            return self.kolom_labels[section]
        return super().headerData(section, orientation, role)

    def zet_root_pad(self, pad):
        self._root_pad = os.path.normpath(pad) if pad else ""

    def zet_filter(self, tekst):
        self._filter = (tekst or "").strip().lower()
        self.invalidateFilter()

    def zet_type(self, ext_set):
        self._type_ext = ext_set
        self.invalidateFilter()

    def filterAcceptsRow(self, row, parent):
        if not self._filter and self._type_ext is None:
            return True
        # Alleen filteren binnen de huidige map; ouder-keten blijft intact
        try:
            parent_pad = os.path.normpath(self.fs.filePath(parent)) if parent.isValid() else ""
        except Exception:
            parent_pad = ""
        if self._root_pad and parent_pad != self._root_pad:
            return True
        idx = self.fs.index(row, 0, parent)
        naam = self.fs.fileName(idx).lower()
        if self._filter and self._filter not in naam:
            return False
        # Type-filter alleen op bestanden; mappen blijven zichtbaar voor navigatie
        if self._type_ext is not None and not self.fs.isDir(idx):
            ext = os.path.splitext(naam)[1].lower()
            if ext not in self._type_ext:
                return False
        return True

    def lessThan(self, links, rechts):
        l_is_map = self.fs.isDir(links)
        r_is_map = self.fs.isDir(rechts)
        if l_is_map != r_is_map:
            # Mappen altijd boven bestanden, ongeacht sorteervolgorde
            volgorde = self.sortOrder()
            mappen_eerst = (l_is_map and not r_is_map)
            if volgorde == Qt.SortOrder.AscendingOrder:
                return mappen_eerst
            return not mappen_eerst
        kolom = links.column()
        if kolom == 1:  # grootte: numeriek vergelijken
            return self.fs.size(links) < self.fs.size(rechts)
        if kolom == 3:  # gewijzigd: op datum
            return self.fs.fileInfo(links).lastModified() < self.fs.fileInfo(rechts).lastModified()
        return self.fs.fileName(links).lower() < self.fs.fileName(rechts).lower()


# ----------------------------------------------------------------------------
# Zoekthread: recursief door submappen (os.walk) zonder de UI te blokkeren
# ----------------------------------------------------------------------------
class ZoekThread(QThread):
    gevonden = pyqtSignal(str)   # volledig pad
    klaar = pyqtSignal(int)      # aantal

    def __init__(self, basis, term):
        super().__init__()
        self.basis = basis
        self.term = term.lower()
        self._stop = False

    def stop(self):
        self._stop = True

    def run(self):
        aantal = 0
        try:
            for wortel, mappen, bestanden in os.walk(self.basis):
                if self._stop:
                    break
                for naam in list(mappen) + list(bestanden):
                    if self._stop:
                        break
                    if self.term in naam.lower():
                        self.gevonden.emit(os.path.join(wortel, naam))
                        aantal += 1
                        if aantal >= 5000:
                            self._stop = True
                            break
        except Exception:
            pass
        self.klaar.emit(aantal)


# ----------------------------------------------------------------------------
# Opslagbalk: klikbare stationswidget met visuele gebruikte/vrije ruimte
# ----------------------------------------------------------------------------
class OpslagBalk(QFrame):
    def __init__(self, info, taal, klik_handler, parent=None):
        super().__init__(parent)
        self.root = info["root"]
        self.klik_handler = klik_handler
        self.setObjectName("opslagbalk")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty("class", "drive")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 7, 10, 7)
        lay.setSpacing(4)

        pct = 0
        if info["totaal"] > 0:
            pct = int(round(info["gebruikt"] * 100.0 / info["totaal"]))

        icoon = {"removable": "[USB]", "remote": "[NET]", "cdrom": "[CD]"}.get(info["type"], "[HDD]")
        titel = QLabel("%s  %s" % (icoon, info["naam"]))
        titel.setObjectName("drivetitel")
        titel.setWordWrap(True)
        lay.addWidget(titel)

        self.balk = _BalkTekening(pct)
        self.balk.setFixedHeight(10)
        lay.addWidget(self.balk)

        sub = TEKST[taal]["vrij_van"].format(
            vrij=mensvriendelijke_grootte(info["vrij"]),
            totaal=mensvriendelijke_grootte(info["totaal"]),
        )
        onder = QLabel(sub)
        onder.setObjectName("drivesub")
        lay.addWidget(onder)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.klik_handler(self.root)
        super().mouseReleaseEvent(e)


class _BalkTekening(QWidget):
    def __init__(self, pct):
        super().__init__()
        self.pct = max(0, min(100, pct))

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect()
        # achtergrond
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(LINE))
        p.drawRoundedRect(r, 4, 4)
        # gevuld deel
        vul = int(r.width() * self.pct / 100.0)
        if vul > 0:
            kleur = QColor(WAARSCHUW if self.pct >= 90 else GOED)
            p.setBrush(kleur)
            vr = r.adjusted(0, 0, vul - r.width(), 0)
            p.drawRoundedRect(vr, 4, 4)
        p.end()


# ----------------------------------------------------------------------------
# Broodkruimel-balk: klikbare padonderdelen (scrollt bij lange paden)
# ----------------------------------------------------------------------------
class BroodkruimelBalk(QScrollArea):
    def __init__(self, venster):
        super().__init__()
        self.venster = venster
        self.setObjectName("kruimelbalk")
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setFixedHeight(40)
        self.inhoud = QWidget()
        self.inhoud.setObjectName("kruimelinhoud")
        self.setWidget(self.inhoud)
        self.lay = QHBoxLayout(self.inhoud)
        self.lay.setContentsMargins(8, 0, 8, 0)
        self.lay.setSpacing(2)
        self.lay.addStretch(1)

    def zet_pad(self, pad):
        # bestaande knoppen/scheiders wissen
        while self.lay.count():
            item = self.lay.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
                w.deleteLater()
        if not pad:
            self.lay.addStretch(1)
            return
        eerste = True
        for vol_pad, label in pad_segmenten(pad):
            if not eerste:
                schei = QLabel("\u203a")  # ›
                schei.setObjectName("kruimelschei")
                self.lay.addWidget(schei)
            eerste = False
            knop = QToolButton()
            knop.setText(label)
            knop.setObjectName("kruimelknop")
            knop.setCursor(Qt.CursorShape.PointingHandCursor)
            knop.setToolTip(vol_pad)
            knop.clicked.connect(lambda _=False, p=vol_pad: self.venster.navigeer(p))
            self.lay.addWidget(knop)
        self.lay.addStretch(1)
        # naar het einde scrollen zodat de huidige map zichtbaar is
        QTimer.singleShot(0, lambda: self.horizontalScrollBar().setValue(
            self.horizontalScrollBar().maximum()))


# ----------------------------------------------------------------------------
# Mappenboom: uitklapbare boom met alleen mappen/stations
# ----------------------------------------------------------------------------
class MappenBoom(QWidget):
    def __init__(self, venster):
        super().__init__()
        self.venster = venster
        self._negeer_klik = False
        lay = QVBoxLayout(self)
        lay.setContentsMargins(8, 6, 8, 8)
        lay.setSpacing(4)

        kop = QLabel(venster.t("mappen").upper())
        kop.setObjectName("sectiekop")
        lay.addWidget(kop)

        # Eigen model: alleen mappen en stations (geen bestanden)
        self.model = QFileSystemModel()
        self.model.setFilter(QDir.Filter.Dirs | QDir.Filter.Drives |
                             QDir.Filter.NoDotAndDotDot)
        self.model.setRootPath("")

        self.view = QTreeView()
        self.view.setObjectName("mappenboom")
        self.view.setModel(self.model)
        self.view.setHeaderHidden(True)
        for k in (1, 2, 3):
            self.view.setColumnHidden(k, True)
        self.view.setRootIsDecorated(True)
        self.view.setAnimated(False)
        self.view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.view.setUniformRowHeights(True)
        self.view.clicked.connect(self._geklikt)
        lay.addWidget(self.view, 1)

    def _geklikt(self, idx):
        if self._negeer_klik:
            return
        pad = self.model.filePath(idx)
        if pad and os.path.isdir(pad):
            self.venster.navigeer(pad)

    def toon_pad(self, pad):
        """Best-effort: selecteer en toon het pad in de boom."""
        try:
            idx = self.model.index(pad)
            if idx.isValid():
                self._negeer_klik = True
                self.view.setCurrentIndex(idx)
                self.view.scrollTo(idx, QAbstractItemView.ScrollHint.PositionAtCenter)
                self._negeer_klik = False
        except Exception:
            self._negeer_klik = False


# ----------------------------------------------------------------------------
# Zijpaneel: snelkoppelingen/stations boven, mappenboom onder (verticale split)
# ----------------------------------------------------------------------------
class ZijPaneel(QWidget):
    def __init__(self, venster):
        super().__init__()
        self.venster = venster
        self.setObjectName("zijpaneel")
        self.setMinimumWidth(210)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        self.split = QSplitter(Qt.Orientation.Vertical)
        self.zijbalk = Zijbalk(venster)
        self.mappenboom = MappenBoom(venster)
        self.split.addWidget(self.zijbalk)
        self.split.addWidget(self.mappenboom)
        self.split.setStretchFactor(0, 0)
        self.split.setStretchFactor(1, 1)
        self.split.setSizes([360, 360])
        lay.addWidget(self.split)


# ----------------------------------------------------------------------------
# Zijbalk: snelkoppelingen + stations (opslag) + netwerk
# ----------------------------------------------------------------------------
class Zijbalk(QScrollArea):
    def __init__(self, venster):
        super().__init__()
        self.venster = venster
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.inhoud = QWidget()
        self.inhoud.setObjectName("zijbalk")
        self.setWidget(self.inhoud)
        self.lay = QVBoxLayout(self.inhoud)
        self.lay.setContentsMargins(8, 8, 8, 8)
        self.lay.setSpacing(4)
        self.lay.addStretch(1)
        self.herbouw()

    def _kop(self, tekst):
        lbl = QLabel(tekst.upper())
        lbl.setObjectName("sectiekop")
        return lbl

    def _snelknop(self, tekst, pad):
        b = QPushButton("   " + tekst)
        b.setObjectName("snelknop")
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.clicked.connect(lambda: self.venster.navigeer(pad))
        return b

    def _favknop(self, pad):
        naam = os.path.basename(pad.rstrip("/\\")) or pad
        b = QPushButton("  \u2605 " + naam)   # ★
        b.setObjectName("favknop")
        b.setToolTip(pad)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.clicked.connect(lambda: self.venster.navigeer(pad))
        b.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        def menu(punt):
            m = QMenu(b)
            m.addAction(self.venster.t("fav_verwijderen"),
                        lambda: self.venster.wissel_favoriet(pad))
            m.exec(b.mapToGlobal(punt))
        b.customContextMenuRequested.connect(menu)
        return b

    def herbouw(self):
        # bestaande widgets wissen
        while self.lay.count():
            item = self.lay.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
                w.deleteLater()
        t = self.venster.t

        # Favorieten (eigen, vastgezet door de gebruiker)
        favs = [p for p in self.venster.cfg.get("favorieten", []) if os.path.isdir(p)]
        if favs:
            self.lay.addWidget(self._kop(t("favorieten")))
            for p in favs:
                self.lay.addWidget(self._favknop(p))
            self.lay.addSpacing(6)

        # Snelkoppelingen
        self.lay.addWidget(self._kop(t("snelkoppelingen")))
        mappen = standaard_mappen()
        volgorde = ["home", "bureaublad", "documenten", "downloads",
                    "afbeeldingen", "muziek", "video"]
        for sleutel in volgorde:
            if sleutel in mappen:
                self.lay.addWidget(self._snelknop(t(sleutel), mappen[sleutel]))

        # Stations
        stations = verzamel_stations()
        lokaal = [s for s in stations if s["type"] != "remote"]
        netwerk = [s for s in stations if s["type"] == "remote"]

        if lokaal:
            self.lay.addSpacing(6)
            self.lay.addWidget(self._kop(t("deze_pc")))
            for s in lokaal:
                self.lay.addWidget(OpslagBalk(s, self.venster.taal, self.venster.navigeer))

        if netwerk:
            self.lay.addSpacing(6)
            self.lay.addWidget(self._kop(t("netwerk")))
            for s in netwerk:
                self.lay.addWidget(OpslagBalk(s, self.venster.taal, self.venster.navigeer))

        self.lay.addStretch(1)


# ----------------------------------------------------------------------------
# Voorbeeldvenster: toont een voorbeeld van het geselecteerde bestand
# ----------------------------------------------------------------------------
class VoorbeeldPaneel(QWidget):
    def __init__(self, venster):
        super().__init__()
        self.venster = venster
        self.setObjectName("voorbeeldpaneel")
        self.setMinimumWidth(240)
        self._movie = None
        self._speler = None
        self._audio = None
        self._huidig_pad = None

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # kop met bestandsnaam + sluitknop
        kop = QWidget()
        kop.setObjectName("voorbeeldkop")
        kl = QHBoxLayout(kop)
        kl.setContentsMargins(10, 6, 6, 6)
        self.titel = QLabel(venster.t("voorbeeld"))
        self.titel.setObjectName("voorbeeldtitel")
        self.titel.setWordWrap(True)
        kl.addWidget(self.titel, 1)
        sluit = QToolButton()
        sluit.setText("\u2715")  # X
        sluit.setObjectName("tbtn")
        sluit.setToolTip(venster.t("voorbeeld_sluiten"))
        sluit.setCursor(Qt.CursorShape.PointingHandCursor)
        sluit.clicked.connect(lambda: venster._wissel_voorbeeld(False))
        kl.addWidget(sluit)
        lay.addWidget(kop)

        self.stack = QStackedWidget()
        lay.addWidget(self.stack, 1)

        # 0: leeg
        self.pag_leeg = self._tekstpagina(venster.t("voorbeeld_leeg"))
        self.stack.addWidget(self.pag_leeg)

        # 1: afbeelding
        self.afb_scroll = QScrollArea()
        self.afb_scroll.setWidgetResizable(True)
        self.afb_scroll.setObjectName("voorbeeldscroll")
        self.afb_label = QLabel()
        self.afb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.afb_scroll.setWidget(self.afb_label)
        self.stack.addWidget(self.afb_scroll)

        # 2: tekst
        self.tekst = QPlainTextEdit()
        self.tekst.setReadOnly(True)
        self.tekst.setObjectName("voorbeeldtekst")
        self.stack.addWidget(self.tekst)

        # 3: pdf
        if HEEFT_PDF:
            self.pdf_doc = QPdfDocument(self)
            self.pdf_view = QPdfView(self)
            self.pdf_view.setObjectName("voorbeeldpdf")
            self.pdf_view.setDocument(self.pdf_doc)
            try:
                self.pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
            except Exception:
                pass
            self.stack.addWidget(self.pdf_view)
        else:
            self.pdf_view = self._tekstpagina(venster.t("voorbeeld_geen"))
            self.stack.addWidget(self.pdf_view)

        # 4: media (video-widget of muziek-info + bediening)
        self.media_pag = QWidget()
        ml = QVBoxLayout(self.media_pag)
        ml.setContentsMargins(8, 8, 8, 8)
        ml.setSpacing(8)
        if HEEFT_MEDIA:
            self.video = QVideoWidget()
            self.video.setObjectName("voorbeeldvideo")
            self.video.setMinimumHeight(160)
            ml.addWidget(self.video, 1)
        self.media_info = QLabel("\u266a")
        self.media_info.setObjectName("medianoot")
        self.media_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.media_info.setWordWrap(True)
        ml.addWidget(self.media_info)
        # bediening
        bed = QWidget()
        bl = QHBoxLayout(bed)
        bl.setContentsMargins(0, 0, 0, 0)
        self.btn_speel = QToolButton()
        self.btn_speel.setText("\u25b6")  # play
        self.btn_speel.setObjectName("tbtn")
        self.btn_speel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_speel.clicked.connect(self._speel_pauze)
        bl.addWidget(self.btn_speel)
        self.schuif = QSlider(Qt.Orientation.Horizontal)
        self.schuif.setObjectName("mediaschuif")
        self.schuif.sliderMoved.connect(self._zoek)
        bl.addWidget(self.schuif, 1)
        self.tijd = QLabel("0:00")
        self.tijd.setObjectName("mediatijd")
        bl.addWidget(self.tijd)
        ml.addWidget(bed)
        self.stack.addWidget(self.media_pag)

        # 5: geen voorbeeld
        self.pag_geen = self._tekstpagina(venster.t("voorbeeld_geen"))
        self.stack.addWidget(self.pag_geen)

        self.stack.setCurrentIndex(0)

    def _tekstpagina(self, tekst):
        w = QLabel(tekst)
        w.setAlignment(Qt.AlignmentFlag.AlignCenter)
        w.setWordWrap(True)
        w.setObjectName("voorbeeldmelding")
        return w

    # ---- mediaspeler lui aanmaken ----
    def _zorg_speler(self):
        if self._speler is not None or not HEEFT_MEDIA:
            return self._speler is not None
        try:
            self._speler = QMediaPlayer(self)
            self._audio = QAudioOutput(self)
            self._speler.setAudioOutput(self._audio)
            self._speler.setVideoOutput(self.video)
            self._speler.positionChanged.connect(self._positie)
            self._speler.durationChanged.connect(self._duur)
            self._speler.playbackStateChanged.connect(self._status_speler)
            return True
        except Exception:
            self._speler = None
            return False

    # ---- hoofd: toon voorbeeld van een pad ----
    def toon(self, pad):
        if pad == self._huidig_pad:
            return
        self.stop_media()
        self._huidig_pad = pad
        if not pad or not os.path.isfile(pad):
            self.titel.setText(self.venster.t("voorbeeld"))
            self.stack.setCurrentIndex(0)
            return
        self.titel.setText(os.path.basename(pad))
        ext = os.path.splitext(pad)[1].lower()
        try:
            if ext in AFBEELDING_EXT or ext == ".svg":
                self._toon_afbeelding(pad, ext)
            elif ext == ".pdf" and HEEFT_PDF:
                self.pdf_doc.load(pad)
                self.stack.setCurrentIndex(3)
            elif ext in TEKST_EXT:
                self._toon_tekst(pad)
            elif ext in VIDEO_EXT and HEEFT_MEDIA:
                self._toon_media(pad, is_video=True)
            elif ext in MUZIEK_EXT and HEEFT_MEDIA:
                self._toon_media(pad, is_video=False)
            else:
                self.stack.setCurrentIndex(5)
        except Exception:
            self.stack.setCurrentIndex(5)

    def _toon_afbeelding(self, pad, ext):
        if ext == ".gif":
            self._movie = QMovie(pad)
            self.afb_label.setMovie(self._movie)
            self._movie.start()
        else:
            pm = QPixmap(pad)
            if pm.isNull():
                self.stack.setCurrentIndex(5)
                return
            breedte = max(200, self.afb_scroll.viewport().width() - 16)
            if pm.width() > breedte:
                pm = pm.scaledToWidth(breedte, Qt.TransformationMode.SmoothTransformation)
            self.afb_label.setPixmap(pm)
        self.stack.setCurrentIndex(1)

    def _toon_tekst(self, pad):
        try:
            with open(pad, "r", encoding="utf-8", errors="replace") as f:
                inhoud = f.read(256 * 1024)
            if len(inhoud) >= 256 * 1024:
                inhoud += "\n\n[... voorbeeld afgekapt ...]"
        except Exception:
            self.stack.setCurrentIndex(5)
            return
        self.tekst.setPlainText(inhoud)
        self.stack.setCurrentIndex(2)

    def _toon_media(self, pad, is_video):
        if not self._zorg_speler():
            self.stack.setCurrentIndex(5)
            return
        if HEEFT_MEDIA:
            self.video.setVisible(is_video)
        if is_video:
            self.media_info.setText("")
        else:
            self.media_info.setText("\u266a  " + os.path.basename(pad))
        self._speler.setSource(QUrl.fromLocalFile(pad))
        self.stack.setCurrentIndex(4)
        self.btn_speel.setText("\u25b6")

    # ---- mediabediening ----
    def _speel_pauze(self):
        if not self._speler:
            return
        if self._speler.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self._speler.pause()
        else:
            self._speler.play()

    def _zoek(self, waarde):
        if self._speler:
            self._speler.setPosition(waarde)

    def _positie(self, pos):
        self.schuif.blockSignals(True)
        self.schuif.setValue(pos)
        self.schuif.blockSignals(False)
        self.tijd.setText(self._mmss(pos) + " / " + self._mmss(self.schuif.maximum()))

    def _duur(self, duur):
        self.schuif.setRange(0, duur)

    def _status_speler(self, *a):
        if self._speler and self._speler.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.btn_speel.setText("\u23f8")  # pause
        else:
            self.btn_speel.setText("\u25b6")

    def _mmss(self, ms):
        s = int(ms / 1000)
        return "%d:%02d" % (s // 60, s % 60)

    def stop_media(self):
        if self._movie:
            self._movie.stop()
            self._movie = None
            self.afb_label.setMovie(None)
        if self._speler:
            try:
                self._speler.stop()
                self._speler.setSource(QUrl())
            except Exception:
                pass

    def leeg(self):
        self.stop_media()
        self._huidig_pad = None
        self.titel.setText(self.venster.t("voorbeeld"))
        self.stack.setCurrentIndex(0)


# ----------------------------------------------------------------------------
# FileTab: een tabblad met navigatiegeschiedenis, fs-weergave en zoekweergave
# ----------------------------------------------------------------------------
class FileTab(QWidget):
    def __init__(self, venster, start_pad):
        super().__init__()
        self.venster = venster
        self.geschiedenis = []
        self.positie = -1
        self.zoek_thread = None

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Stapel: pagina 0 = bestandssysteem, pagina 1 = zoekresultaten
        self.stack = QStackedWidget()
        lay.addWidget(self.stack)

        # --- fs-weergave ---
        self.proxy = MapEersteProxy(self.venster.fs_model)
        self.view = QTreeView()
        self.view.setModel(self.proxy)
        self.view.setRootIsDecorated(False)
        self.view.setItemsExpandable(False)
        self.view.setSortingEnabled(True)
        self.view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.view.setUniformRowHeights(True)
        self.view.setAllColumnsShowFocus(True)
        self.view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self._context_menu)
        self.view.doubleClicked.connect(self._dubbelklik)
        self.view.activated.connect(self._dubbelklik)
        self.view.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        sm = self.view.selectionModel()
        if sm:
            sm.selectionChanged.connect(lambda *a: self.venster.werk_status_bij())
        self.view.setMouseTracking(True)
        self.view.viewport().installEventFilter(self)
        self.stack.addWidget(self.view)

        # --- zoekweergave ---
        self.zoek_model = QStandardItemModel()
        self.zoek_view = QTreeView()
        self.zoek_view.setModel(self.zoek_model)
        self.zoek_view.setRootIsDecorated(False)
        self.zoek_view.setSortingEnabled(True)
        self.zoek_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.zoek_view.setUniformRowHeights(True)
        self.zoek_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.zoek_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.zoek_view.customContextMenuRequested.connect(self._zoek_context_menu)
        self.zoek_view.doubleClicked.connect(self._zoek_dubbelklik)
        self.stack.addWidget(self.zoek_view)

        # --- icoon-weergave (grote iconen + miniaturen) ---
        self.icon_view = QListView()
        self.icon_view.setModel(self.proxy)
        self.icon_view.setViewMode(QListView.ViewMode.IconMode)
        self.icon_view.setResizeMode(QListView.ResizeMode.Adjust)
        self.icon_view.setMovement(QListView.Movement.Static)
        self.icon_view.setUniformItemSizes(True)
        self.icon_view.setWordWrap(True)
        self.icon_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.icon_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.icon_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.icon_view.customContextMenuRequested.connect(self._icon_context_menu)
        self.icon_view.doubleClicked.connect(self._dubbelklik)
        self.icon_view.setItemDelegate(MiniatuurDelegate(self.venster.thumbs, self.icon_view))
        self.icon_view.viewport().installEventFilter(self)
        self._stel_icoon_grootte_in()
        ism = self.icon_view.selectionModel()
        if ism:
            ism.selectionChanged.connect(lambda *a: self.venster.werk_status_bij())
        self.stack.addWidget(self.icon_view)

        self._zet_kolomkoppen()
        if start_pad and os.path.isdir(start_pad):
            self.ga_naar(start_pad, onthoud=True)

    def _stel_icoon_grootte_in(self):
        g = self.venster.cfg.get("icoon_grootte", 128)
        ls = self.venster.cfg.get("lettergrootte", 11)
        # Alle iconen zijn nu even hoog (g). Tekstband = ruimte voor ~2 regels
        # naam onder het icoon, ruim genoeg zodat de naam altijd verschijnt.
        regelhoogte = int(ls * 1.6) + 2
        tekstband = regelhoogte * 2 + 18
        self.icon_view.setIconSize(QSize(g, g))
        self.icon_view.setGridSize(QSize(g + 24, g + tekstband))
        self.icon_view.setSpacing(6)
        self.icon_view.setWordWrap(True)

    # ---- welke fs-view is actief (lijst of iconen) ----
    def fs_view(self):
        return self.icon_view if self.venster.weergave == "iconen" else self.view

    def fs_index(self):
        return 2 if self.venster.weergave == "iconen" else 0

    # ---- kolommen ----
    def _zet_kolomkoppen(self):
        t = self.venster.t
        self.proxy.kolom_labels = [t("kol_naam"), t("kol_grootte"),
                                   t("kol_type"), t("kol_gewijzigd")]
        hdr = self.view.header()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.view.setColumnWidth(0, 320)
        self.view.setColumnWidth(1, 90)
        self.view.setColumnWidth(2, 130)
        self.zoek_model.setHorizontalHeaderLabels(
            [t("kol_naam"), t("kol_pad"), t("kol_grootte"), t("kol_gewijzigd")])
        self.zoek_view.setColumnWidth(0, 240)
        self.zoek_view.setColumnWidth(1, 320)

    # ---- huidige pad ----
    def huidig_pad(self):
        if 0 <= self.positie < len(self.geschiedenis):
            return self.geschiedenis[self.positie]
        return ""

    # ---- navigeren ----
    def ga_naar(self, pad, onthoud=True):
        pad = os.path.normpath(pad)
        if not os.path.isdir(pad):
            return False
        self.stop_zoeken()
        self.proxy.zet_filter("")
        self.proxy.zet_type(None)
        self.proxy.zet_root_pad(pad)
        bron_idx = self.venster.fs_model.setRootPath(pad)
        proxy_root = self.proxy.mapFromSource(bron_idx)
        self.view.setRootIndex(proxy_root)
        self.icon_view.setRootIndex(proxy_root)
        self.stack.setCurrentIndex(self.fs_index())
        if onthoud:
            # kap eventuele 'vooruit'-geschiedenis af
            if self.positie < len(self.geschiedenis) - 1:
                self.geschiedenis = self.geschiedenis[:self.positie + 1]
            if not self.geschiedenis or self.geschiedenis[-1] != pad:
                self.geschiedenis.append(pad)
                self.positie = len(self.geschiedenis) - 1
        self.venster.na_navigatie(self)
        return True

    def terug(self):
        if self.positie > 0:
            self.positie -= 1
            self.ga_naar(self.geschiedenis[self.positie], onthoud=False)

    def vooruit(self):
        if self.positie < len(self.geschiedenis) - 1:
            self.positie += 1
            self.ga_naar(self.geschiedenis[self.positie], onthoud=False)

    def omhoog(self):
        h = self.huidig_pad()
        ouder = os.path.dirname(h)
        if ouder and ouder != h and os.path.isdir(ouder):
            self.ga_naar(ouder, onthoud=True)

    def kan_terug(self):
        return self.positie > 0

    def kan_vooruit(self):
        return self.positie < len(self.geschiedenis) - 1

    # ---- filter ----
    def zet_filter(self, tekst):
        if self.stack.currentIndex() != 1:   # niet in zoekmodus
            self.proxy.zet_filter(tekst)
            self.venster.werk_status_bij()

    def zet_type(self, ext_set):
        if self.stack.currentIndex() != 1:
            self.proxy.zet_type(ext_set)
            self.venster.werk_status_bij()

    # ---- dubbelklik ----
    def _dubbelklik(self, proxy_idx):
        bron = self.proxy.mapToSource(proxy_idx)
        pad = self.venster.fs_model.filePath(bron)
        if os.path.isdir(pad):
            self.ga_naar(pad, onthoud=True)
        else:
            self.venster.open_bestand(pad)

    def _zoek_dubbelklik(self, idx):
        rij = idx.row()
        pad_item = self.zoek_model.item(rij, 1)
        naam_item = self.zoek_model.item(rij, 0)
        if not pad_item or not naam_item:
            return
        vol = os.path.join(pad_item.text(), naam_item.text())
        if os.path.isdir(vol):
            self.venster.nieuwe_tab(vol)
        elif os.path.isfile(vol):
            self.venster.open_bestand(vol)

    # ---- geselecteerde paden ----
    def geselecteerde_paden(self):
        paden = []
        if self.stack.currentIndex() != 1:   # lijst- of icoonweergave
            view = self.fs_view()
            sm = view.selectionModel()
            if not sm:
                return paden
            for idx in sm.selectedIndexes():
                if idx.column() != 0:
                    continue
                bron = self.proxy.mapToSource(idx)
                paden.append(self.venster.fs_model.filePath(bron))
        else:
            sm = self.zoek_view.selectionModel()
            if not sm:
                return paden
            for idx in sm.selectedRows(0):
                rij = idx.row()
                p = self.zoek_model.item(rij, 1)
                n = self.zoek_model.item(rij, 0)
                if p and n:
                    paden.append(os.path.join(p.text(), n.text()))
        return paden

    def huidig_focus_pad(self):
        """Pad van de op dit moment gefocuste rij (voor het voorbeeld), ook als
        er alleen een cel i.p.v. een hele rij geselecteerd is."""
        if self.stack.currentIndex() == 1:
            return None
        view = self.fs_view()
        idx = view.currentIndex()
        if not idx.isValid():
            return None
        idx0 = idx.sibling(idx.row(), 0)
        bron = self.proxy.mapToSource(idx0)
        return self.venster.fs_model.filePath(bron)

    def aantal_items(self):
        if self.stack.currentIndex() != 1:
            root = self.fs_view().rootIndex()
            return self.proxy.rowCount(root)
        return self.zoek_model.rowCount()

    # ---- middenklik = nieuwe tab ----
    def eventFilter(self, obj, e):
        iv = getattr(self, "icon_view", None)
        viewports = [self.view.viewport()]
        if iv is not None:
            viewports.append(iv.viewport())
        if (obj in viewports and e.type() == e.Type.MouseButtonRelease
                and e.button() == Qt.MouseButton.MiddleButton):
            bron_view = self.view if obj is self.view.viewport() else iv
            idx = bron_view.indexAt(e.position().toPoint())
            if idx.isValid():
                bron = self.proxy.mapToSource(idx)
                pad = self.venster.fs_model.filePath(bron)
                if os.path.isdir(pad):
                    self.venster.nieuwe_tab(pad)
                    return True
        return super().eventFilter(obj, e)

    # ---- context-menu's ----
    def _context_menu(self, punt):
        self.venster.toon_context_menu(self, self.view.viewport().mapToGlobal(punt))

    def _icon_context_menu(self, punt):
        self.venster.toon_context_menu(self, self.icon_view.viewport().mapToGlobal(punt))

    def _zoek_context_menu(self, punt):
        self.venster.toon_context_menu(self, self.zoek_view.viewport().mapToGlobal(punt))

    # ---- zoeken in submappen ----
    def start_zoeken(self, term):
        basis = self.huidig_pad()
        if not basis or not term.strip():
            return
        self.stop_zoeken()
        self.zoek_model.clear()
        t = self.venster.t
        self.zoek_model.setHorizontalHeaderLabels(
            [t("kol_naam"), t("kol_pad"), t("kol_grootte"), t("kol_gewijzigd")])
        self.stack.setCurrentIndex(1)
        self.venster.zet_zoekstatus(t("zoeken_bezig"))
        self.zoek_thread = ZoekThread(basis, term)
        self.zoek_thread.gevonden.connect(self._zoek_treffer)
        self.zoek_thread.klaar.connect(lambda n: self._zoek_klaar(n, term))
        self.zoek_thread.start()

    def _zoek_treffer(self, vol_pad):
        try:
            mp, naam = os.path.split(vol_pad)
            info = QFileInfo(vol_pad)
            grootte = "" if info.isDir() else mensvriendelijke_grootte(info.size())
            gew = info.lastModified().toString("yyyy-MM-dd HH:mm")
            rij = [QStandardItem(naam), QStandardItem(mp),
                   QStandardItem(grootte), QStandardItem(gew)]
            for it in rij:
                it.setEditable(False)
            self.zoek_model.appendRow(rij)
        except Exception:
            pass

    def _zoek_klaar(self, n, term):
        t = self.venster.t
        if n == 0:
            self.venster.zet_zoekstatus(t("geen_resultaten"))
        else:
            self.venster.zet_zoekstatus(t("zoekresultaten").format(n=n, term=term))

    def stop_zoeken(self):
        if self.zoek_thread and self.zoek_thread.isRunning():
            self.zoek_thread.stop()
            self.zoek_thread.wait(1500)
        self.zoek_thread = None

    def toon_fs_weer(self):
        self.stop_zoeken()
        self.stack.setCurrentIndex(self.fs_index())
        self.venster.werk_status_bij()

    def pas_weergave_toe(self):
        """Schakel tussen lijst- en icoonweergave (bij niet-zoeken)."""
        self._stel_icoon_grootte_in()
        if self.stack.currentIndex() != 1:
            self.stack.setCurrentIndex(self.fs_index())


# ----------------------------------------------------------------------------
# Hoofdvenster
# ----------------------------------------------------------------------------
class Verkenner(QMainWindow):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.taal = cfg["taal"] if cfg["taal"] in ("nl", "en") else detecteer_taal()
        self.klembord = []          # lijst paden
        self.klembord_knip = False  # True = knippen (verplaatsen)

        self.setWindowTitle("%s  v%s" % (APP_NAAM, APP_VERSIE))
        bg = cfg.get("venster", [1100, 720])
        self.resize(bg[0], bg[1])
        self.setWindowIcon(maak_app_icoon())

        # Gedeeld bestandssysteem-model
        self.fs_model = QFileSystemModel()
        self.fs_model.setRootPath("")
        self.fs_model.setIconProvider(QFileIconProvider())
        self.fs_model.directoryLoaded.connect(self._map_geladen)
        self._pas_fs_filter_toe()

        # Weergave (lijst/iconen) + miniatuur-beheer
        self.weergave = cfg.get("weergave", "lijst")
        if self.weergave not in ("lijst", "iconen"):
            self.weergave = "lijst"
        self.thumbs = ThumbnailManager(cfg.get("icoon_grootte", 128), self)
        self.thumbs.bijgewerkt.connect(self._thumb_klaar)

        self._bouw_ui()
        self._bouw_menu()
        self.pas_stijl_toe()

        # Tabs herstellen van vorige sessie, of een eerste tab openen
        herstel = [p for p in cfg.get("open_tabs", []) if isinstance(p, str) and os.path.isdir(p)]
        if herstel:
            for p in herstel:
                self.nieuwe_tab(p)
            actief = cfg.get("actieve_tab", 0)
            if 0 <= actief < self.tabs.count():
                self.tabs.setCurrentIndex(actief)
        else:
            start = cfg.get("laatste_pad") or os.path.expanduser("~")
            if not os.path.isdir(start):
                start = os.path.expanduser("~")
            self.nieuwe_tab(start)

    # ---- vertaalhelper ----
    def t(self, sleutel):
        return TEKST[self.taal].get(sleutel, sleutel)

    # ---- fs filter (verborgen bestanden) ----
    def _pas_fs_filter_toe(self):
        f = (QDir.Filter.AllEntries | QDir.Filter.NoDotAndDotDot |
             QDir.Filter.AllDirs)
        if self.cfg.get("verborgen_tonen"):
            f |= QDir.Filter.Hidden | QDir.Filter.System
        self.fs_model.setFilter(f)

    # ---- UI opbouw ----
    def _bouw_ui(self):
        centraal = QWidget()
        self.setCentralWidget(centraal)
        hoofd = QVBoxLayout(centraal)
        hoofd.setContentsMargins(0, 0, 0, 0)
        hoofd.setSpacing(0)

        # --- werkbalk ---
        balk = QWidget()
        balk.setObjectName("werkbalk")
        bl = QHBoxLayout(balk)
        bl.setContentsMargins(8, 6, 8, 6)
        bl.setSpacing(6)

        self.btn_terug = self._tbtn("\u2190", self.t("terug"), self._terug)
        self.btn_vooruit = self._tbtn("\u2192", self.t("vooruit"), self._vooruit)
        self.btn_omhoog = self._tbtn("\u2191", self.t("omhoog"), self._omhoog)
        self.btn_vernieuw = self._tbtn("\u27f3", self.t("vernieuwen"), self._vernieuw)
        for b in (self.btn_terug, self.btn_vooruit, self.btn_omhoog, self.btn_vernieuw):
            bl.addWidget(b)

        self.adres = QLineEdit()
        self.adres.setObjectName("adres")
        self.adres.setPlaceholderText(self.t("adres"))
        self.adres.returnPressed.connect(self._adres_enter)
        bl.addWidget(self.adres, 3)

        self.filter = QLineEdit()
        self.filter.setObjectName("filter")
        self.filter.setPlaceholderText(self.t("filter"))
        self.filter.textChanged.connect(self._filter_gewijzigd)
        self.filter.returnPressed.connect(self._filter_enter)
        bl.addWidget(self.filter, 2)

        self.type_keuze = QComboBox()
        self.type_keuze.setObjectName("typekeuze")
        self.type_keuze.setToolTip(self.t("type_filter"))
        for sleutel, _ in TYPE_CATEGORIEEN:
            self.type_keuze.addItem(self.t(sleutel))
        self.type_keuze.currentIndexChanged.connect(self._type_gewijzigd)
        bl.addWidget(self.type_keuze)

        self.btn_diep = self._tbtn("\u2315", self.t("diep_zoeken"), self._diep_zoeken)
        bl.addWidget(self.btn_diep)

        start_iconen = (self.weergave == "iconen")
        self.btn_weergave = self._tbtn(
            "\u2630" if start_iconen else "\u25a6",
            self.t("weergave_lijst") if start_iconen else self.t("weergave_iconen"),
            lambda: self._wissel_weergave())
        bl.addWidget(self.btn_weergave)

        self.btn_voorbeeld = self._tbtn("\u25a4", self.t("voorbeeld"),
                                        lambda: self._wissel_voorbeeld())
        self.btn_voorbeeld.setCheckable(True)
        self.btn_voorbeeld.setChecked(bool(self.cfg.get("voorbeeld_zichtbaar")))
        bl.addWidget(self.btn_voorbeeld)

        self.btn_nieuwe_tab = self._tbtn("\uff0b", self.t("nieuwe_tab"),
                                         lambda: self.nieuwe_tab(self.huidige_tab().huidig_pad() if self.huidige_tab() else os.path.expanduser("~")))
        bl.addWidget(self.btn_nieuwe_tab)
        hoofd.addWidget(balk)

        # --- broodkruimel-balk ---
        self.broodkruimel = BroodkruimelBalk(self)
        hoofd.addWidget(self.broodkruimel)

        # --- splitter: zijpaneel | tabs ---
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.zijpaneel = ZijPaneel(self)
        self.zijbalk = self.zijpaneel.zijbalk
        self.mappenboom = self.zijpaneel.mappenboom
        self.splitter.addWidget(self.zijpaneel)

        self.tabs = QTabWidget()
        self.tabs.setObjectName("tabs")
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.tabCloseRequested.connect(self._sluit_tab)
        self.tabs.currentChanged.connect(self._tab_gewijzigd)
        self.splitter.addWidget(self.tabs)
        self.splitter.setStretchFactor(1, 1)

        self.voorbeeld = VoorbeeldPaneel(self)
        self.splitter.addWidget(self.voorbeeld)
        self.splitter.setStretchFactor(2, 0)
        self.voorbeeld_zichtbaar = bool(self.cfg.get("voorbeeld_zichtbaar"))
        self.voorbeeld.setVisible(self.voorbeeld_zichtbaar)
        self.splitter.setSizes([250, 650, 300] if self.voorbeeld_zichtbaar else [250, 850, 0])

        # korte vertraging zodat snel doorklikken het voorbeeld niet overbelast
        self._voorbeeld_timer = QTimer(self)
        self._voorbeeld_timer.setSingleShot(True)
        self._voorbeeld_timer.setInterval(160)
        self._voorbeeld_timer.timeout.connect(self._voorbeeld_nu)
        hoofd.addWidget(self.splitter, 1)

        # --- statusbalk ---
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status_links = QLabel("")
        self.status.addWidget(self.status_links, 1)
        self.status_station = QLabel("")
        self.status_station.setObjectName("statusstation")
        self.status.addPermanentWidget(self.status_station)
        self.btn_donatie = QPushButton(" \u2665 " + self.t("donatie"))
        self.btn_donatie.setObjectName("donatie")
        self.btn_donatie.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_donatie.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(DONATIE_URL)))
        self.status.addPermanentWidget(self.btn_donatie)

    def _tbtn(self, tekst, tip, handler):
        b = QToolButton()
        b.setText(tekst)
        b.setToolTip(tip)
        b.setObjectName("tbtn")
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.clicked.connect(handler)
        return b

    # ---- menu ----
    def _bouw_menu(self):
        mb = self.menuBar()
        m_best = mb.addMenu(self.t("menu_bestand"))
        self._act(m_best, self.t("nieuwe_tab"), "Ctrl+T",
                  lambda: self.nieuwe_tab(self.huidige_tab().huidig_pad()))
        self._act(m_best, self.t("nieuwe_map"), "Ctrl+Shift+N", self._nieuwe_map)
        self._act(m_best, self.t("fav_toevoegen"), "Ctrl+D",
                  self.voeg_huidige_toe_aan_favorieten)
        self._act(m_best, self.t("eigenschappen"), "Alt+Return", self._eigenschappen)
        m_best.addSeparator()
        self._act(m_best, self.t("afsluiten"), "Ctrl+Q", self.close)

        m_bew = mb.addMenu(self.t("menu_bewerken"))
        self._act(m_bew, self.t("knippen"), "Ctrl+X", self._knippen)
        self._act(m_bew, self.t("kopieren"), "Ctrl+C", self._kopieren)
        self._act(m_bew, self.t("plakken"), "Ctrl+V", self._plakken)
        m_bew.addSeparator()
        self._act(m_bew, self.t("hernoemen"), "F2", self._hernoemen)
        self._act(m_bew, self.t("verwijderen"), "Delete", self._verwijderen)
        self._act(m_bew, self.t("permanent_verwijder"), "Shift+Delete",
                  lambda: self._verwijderen(permanent=True))
        m_bew.addSeparator()
        self._act(m_bew, self.t("alles_select"), "Ctrl+A", self._alles_select)

        m_beeld = mb.addMenu(self.t("menu_beeld"))
        self._act(m_beeld, self.t("vernieuwen"), "F5", self._vernieuw)
        self.act_verborgen = self._act(m_beeld, self.t("verborgen_tonen"),
                                       "Ctrl+H", self._wissel_verborgen, vink=True)
        self.act_verborgen.setChecked(bool(self.cfg.get("verborgen_tonen")))
        m_beeld.addSeparator()
        self._act(m_beeld, self.t("weergave_lijst"), "Ctrl+1",
                  lambda: self._wissel_weergave("lijst"))
        self._act(m_beeld, self.t("weergave_iconen"), "Ctrl+2",
                  lambda: self._wissel_weergave("iconen"))
        self.act_voorbeeld = self._act(m_beeld, self.t("voorbeeld"), "Ctrl+P",
                                       self._wissel_voorbeeld, vink=True)
        self.act_voorbeeld.setChecked(bool(self.cfg.get("voorbeeld_zichtbaar")))
        m_beeld.addSeparator()
        self._act(m_beeld, self.t("tekst_groter"), "Ctrl++",
                  lambda: self._wijzig_letter(1))
        self._act(m_beeld, self.t("tekst_kleiner"), "Ctrl+-",
                  lambda: self._wijzig_letter(-1))
        m_beeld.addSeparator()
        self._act(m_beeld, self.t("instellingen"), "", self._instellingen)

        m_help = mb.addMenu(self.t("menu_help"))
        self._act(m_help, self.t("snelgids"), "F1", self._snelgids)
        self._act(m_help, "\u2665 " + self.t("donatie"), "",
                  lambda: QDesktopServices.openUrl(QUrl(DONATIE_URL)))
        self._act(m_help, self.t("over"), "", self._over)

    def _act(self, menu, tekst, sneltoets, handler, vink=False):
        a = QAction(tekst, self)
        if sneltoets:
            a.setShortcut(QKeySequence(sneltoets))
        if vink:
            a.setCheckable(True)
        a.triggered.connect(lambda checked=False: handler())
        menu.addAction(a)
        self.addAction(a)  # ook werkzaam als menu verborgen is
        return a

    # ---- tab-beheer ----
    def huidige_tab(self):
        w = self.tabs.currentWidget()
        return w if isinstance(w, FileTab) else None

    def nieuwe_tab(self, pad):
        if not pad or not os.path.isdir(pad):
            pad = os.path.expanduser("~")
        tab = FileTab(self, pad)
        naam = os.path.basename(pad.rstrip("/\\")) or pad
        idx = self.tabs.addTab(tab, naam)
        self.tabs.setCurrentIndex(idx)
        return tab

    def _sluit_tab(self, index):
        if self.tabs.count() <= 1:
            return
        w = self.tabs.widget(index)
        if isinstance(w, FileTab):
            w.stop_zoeken()
        self.tabs.removeTab(index)
        w.deleteLater()

    def _tab_gewijzigd(self, index):
        tab = self.huidige_tab()
        if tab:
            self.na_navigatie(tab)

    def na_navigatie(self, tab):
        if tab is not self.huidige_tab():
            return
        pad = tab.huidig_pad()
        self.adres.setText(pad)
        self.broodkruimel.zet_pad(pad)
        self.mappenboom.toon_pad(pad)
        naam = os.path.basename(pad.rstrip("/\\")) or pad
        idx = self.tabs.indexOf(tab)
        if idx >= 0:
            self.tabs.setTabText(idx, naam)
            self.tabs.setTabToolTip(idx, pad)
        self.btn_terug.setEnabled(tab.kan_terug())
        self.btn_vooruit.setEnabled(tab.kan_vooruit())
        self.filter.blockSignals(True)
        self.filter.clear()
        self.filter.blockSignals(False)
        self.type_keuze.blockSignals(True)
        self.type_keuze.setCurrentIndex(0)
        self.type_keuze.blockSignals(False)
        self.werk_status_bij()
        self.cfg["laatste_pad"] = pad

    def navigeer(self, pad):
        tab = self.huidige_tab()
        if tab:
            tab.ga_naar(pad, onthoud=True)

    # ---- favorieten ----
    def is_favoriet(self, pad):
        return os.path.normpath(pad) in [os.path.normpath(p)
                                         for p in self.cfg.get("favorieten", [])]

    def wissel_favoriet(self, pad):
        pad = os.path.normpath(pad)
        fav = self.cfg.get("favorieten", [])
        genormaliseerd = [os.path.normpath(p) for p in fav]
        if pad in genormaliseerd:
            fav = [p for p in fav if os.path.normpath(p) != pad]
        else:
            fav = fav + [pad]
        self.cfg["favorieten"] = fav
        bewaar_config(self.cfg)
        self.zijbalk.herbouw()

    def voeg_huidige_toe_aan_favorieten(self):
        tab = self.huidige_tab()
        if tab:
            p = tab.huidig_pad()
            if p and os.path.isdir(p) and not self.is_favoriet(p):
                self.wissel_favoriet(p)

    # ---- status ----
    def werk_status_bij(self):
        self.werk_voorbeeld_bij()
        tab = self.huidige_tab()
        if not tab:
            self.status_links.setText("")
            self.status_station.setText("")
            return
        if tab.stack.currentIndex() == 1:
            return  # zoekstatus blijft staan
        n = tab.aantal_items()
        sel = tab.geselecteerde_paden()
        if sel:
            totaal = 0
            for p in sel:
                try:
                    if os.path.isfile(p):
                        totaal += os.path.getsize(p)
                except Exception:
                    pass
            self.status_links.setText(self.t("items_sel").format(
                n=n, sel=len(sel), grootte=mensvriendelijke_grootte(totaal)))
        else:
            self.status_links.setText(self.t("items").format(n=n))
        self._werk_station_status_bij(tab.huidig_pad())

    def _werk_station_status_bij(self, pad):
        try:
            si = QStorageInfo(pad)
            if si.isValid() and si.isReady() and si.bytesTotal() > 0:
                self.status_station.setText(self.t("vrij_op_station").format(
                    vrij=mensvriendelijke_grootte(si.bytesAvailable()),
                    totaal=mensvriendelijke_grootte(si.bytesTotal())))
                return
        except Exception:
            pass
        self.status_station.setText("")

    def zet_zoekstatus(self, tekst):
        self.status_links.setText(tekst)

    def _map_geladen(self, pad):
        tab = self.huidige_tab()
        if tab and tab.stack.currentIndex() != 1:
            try:
                if os.path.normpath(tab.huidig_pad()) == os.path.normpath(pad):
                    self.werk_status_bij()
            except Exception:
                pass

    def _thumb_klaar(self, pad):
        # ververs de icoon-weergave van de huidige tab als die zichtbaar is
        tab = self.huidige_tab()
        if tab and tab.stack.currentIndex() == 2:
            tab.icon_view.viewport().update()

    # ---- voorbeeldvenster ----
    def _wissel_voorbeeld(self, toon=None):
        if toon not in (True, False):
            toon = not self.voorbeeld_zichtbaar
        self.voorbeeld_zichtbaar = toon
        self.cfg["voorbeeld_zichtbaar"] = toon
        self.voorbeeld.setVisible(toon)
        if toon:
            tot = self.splitter.width()
            self.splitter.setSizes([250, max(300, tot - 250 - 320), 320])
            self.werk_voorbeeld_bij()
        else:
            self.voorbeeld.leeg()
        if hasattr(self, "btn_voorbeeld"):
            self.btn_voorbeeld.setChecked(toon)
        if hasattr(self, "act_voorbeeld"):
            self.act_voorbeeld.setChecked(toon)

    def werk_voorbeeld_bij(self):
        if not self.voorbeeld_zichtbaar:
            return
        self._voorbeeld_timer.start()

    def _voorbeeld_nu(self):
        if not self.voorbeeld_zichtbaar:
            return
        tab = self.huidige_tab()
        if not tab or tab.stack.currentIndex() == 1:
            self.voorbeeld.leeg()
            return
        sel = tab.geselecteerde_paden()
        pad = None
        if len(sel) == 1:
            pad = sel[0]
        elif not sel:
            pad = tab.huidig_focus_pad()   # klik selecteert soms alleen een cel
        if pad and os.path.isfile(pad):
            self.voorbeeld.toon(pad)
        else:
            self.voorbeeld.leeg()

    def _wissel_weergave(self, modus=None):
        if modus not in ("lijst", "iconen"):
            modus = "iconen" if self.weergave == "lijst" else "lijst"
        self.weergave = modus
        self.cfg["weergave"] = modus
        for i in range(self.tabs.count()):
            w = self.tabs.widget(i)
            if isinstance(w, FileTab):
                w.pas_weergave_toe()
        if hasattr(self, "btn_weergave"):
            self.btn_weergave.setText("\u2630" if modus == "iconen" else "\u25a6")
            self.btn_weergave.setToolTip(
                self.t("weergave_lijst") if modus == "iconen" else self.t("weergave_iconen"))
        self.werk_status_bij()

    # ---- werkbalk-acties ----
    def _terug(self):
        if self.huidige_tab():
            self.huidige_tab().terug()

    def _vooruit(self):
        if self.huidige_tab():
            self.huidige_tab().vooruit()

    def _omhoog(self):
        if self.huidige_tab():
            self.huidige_tab().omhoog()

    def _vernieuw(self):
        tab = self.huidige_tab()
        if tab:
            pad = tab.huidig_pad()
            self.fs_model.setRootPath("")
            tab.ga_naar(pad, onthoud=False)

    def _adres_enter(self):
        pad = self.adres.text().strip()
        if os.path.isdir(pad):
            self.navigeer(pad)
        elif os.path.isfile(pad):
            self.open_bestand(pad)
        else:
            self._fout(self.t("kan_niet_openen"))

    def _filter_gewijzigd(self, tekst):
        tab = self.huidige_tab()
        if tab:
            tab.zet_filter(tekst)

    def _type_gewijzigd(self, index):
        tab = self.huidige_tab()
        if tab and 0 <= index < len(TYPE_CATEGORIEEN):
            tab.zet_type(TYPE_CATEGORIEEN[index][1])

    def _filter_enter(self):
        # Enter in het filterveld: niets extra (filter is al live).
        pass

    def _diep_zoeken(self):
        tab = self.huidige_tab()
        term = self.filter.text().strip()
        if tab and term:
            tab.start_zoeken(term)

    # ---- bestand openen ----
    def open_bestand(self, pad):
        try:
            QDesktopServices.openUrl(QUrl.fromLocalFile(pad))
        except Exception:
            self._fout(self.t("kan_niet_openen"))

    # ---- context-menu ----
    def toon_context_menu(self, tab, globaal_punt):
        paden = tab.geselecteerde_paden()
        m = QMenu(self)
        if paden:
            if len(paden) == 1 and os.path.isdir(paden[0]):
                m.addAction(self.t("openen"),
                            lambda: tab.ga_naar(paden[0], onthoud=True))
                m.addAction(self.t("open_nieuwe_tab"),
                            lambda: self.nieuwe_tab(paden[0]))
                if self.is_favoriet(paden[0]):
                    m.addAction(self.t("fav_verwijderen"),
                                lambda: self.wissel_favoriet(paden[0]))
                else:
                    m.addAction(self.t("fav_toevoegen"),
                                lambda: self.wissel_favoriet(paden[0]))
            elif len(paden) == 1:
                m.addAction(self.t("openen"),
                            lambda: self.open_bestand(paden[0]))
            m.addSeparator()
            m.addAction(self.t("knippen"), self._knippen)
            m.addAction(self.t("kopieren"), self._kopieren)
        if self.klembord:
            m.addAction(self.t("plakken"), self._plakken)
        m.addSeparator()
        if paden:
            m.addAction(self.t("hernoemen"), self._hernoemen)
            m.addAction(self.t("verwijderen"), self._verwijderen)
            m.addAction(self.t("kopieer_pad"), self._kopieer_pad)
        m.addSeparator()
        m.addAction(self.t("nieuwe_map"), self._nieuwe_map)
        if paden:
            m.addAction(self.t("eigenschappen"), self._eigenschappen)
        m.exec(globaal_punt)

    # ---- bestandsoperaties ----
    def _kopieren(self):
        tab = self.huidige_tab()
        if tab:
            self.klembord = tab.geselecteerde_paden()
            self.klembord_knip = False

    def _knippen(self):
        tab = self.huidige_tab()
        if tab:
            self.klembord = tab.geselecteerde_paden()
            self.klembord_knip = True

    def _plakken(self):
        tab = self.huidige_tab()
        if not tab or not self.klembord:
            return
        doel = tab.huidig_pad()
        if not os.path.isdir(doel):
            return
        for bron in self.klembord:
            try:
                naam = os.path.basename(bron.rstrip("/\\"))
                doelpad = os.path.join(doel, naam)
                doelpad = self._uniek_pad(doelpad)
                if self.klembord_knip:
                    shutil.move(bron, doelpad)
                else:
                    if os.path.isdir(bron):
                        shutil.copytree(bron, doelpad)
                    else:
                        shutil.copy2(bron, doelpad)
            except Exception as ex:
                self._fout(str(ex))
        if self.klembord_knip:
            self.klembord = []
            self.klembord_knip = False
        self._vernieuw()

    def _uniek_pad(self, pad):
        if not os.path.exists(pad):
            return pad
        wortel, ext = os.path.splitext(pad)
        i = 2
        while True:
            nieuw = "%s (%d)%s" % (wortel, i, ext)
            if not os.path.exists(nieuw):
                return nieuw
            i += 1

    def _verwijderen(self, permanent=False):
        tab = self.huidige_tab()
        if not tab:
            return
        paden = tab.geselecteerde_paden()
        if not paden:
            return
        n = len(paden)
        if permanent or not HEEFT_PRULLENBAK:
            vraag = self.t("permanent_vraag").format(n=n)
        else:
            vraag = self.t("bevestig_verwijder").format(n=n)
        antwoord = QMessageBox.question(
            self, self.t("bevestig_verwijder_titel"), vraag,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if antwoord != QMessageBox.StandardButton.Yes:
            return
        for p in paden:
            try:
                if HEEFT_PRULLENBAK and not permanent:
                    send2trash(os.path.normpath(p))
                else:
                    if os.path.isdir(p):
                        shutil.rmtree(p)
                    else:
                        os.remove(p)
            except Exception as ex:
                self._fout(str(ex))
        self._vernieuw()

    def _hernoemen(self):
        tab = self.huidige_tab()
        if not tab:
            return
        paden = tab.geselecteerde_paden()
        if len(paden) != 1:
            return
        oud = paden[0]
        oude_naam = os.path.basename(oud.rstrip("/\\"))
        nieuw, ok = QInputDialog.getText(
            self, self.t("hernoemen"), self.t("hernoem_naar"),
            text=oude_naam)
        if not ok or not nieuw.strip() or nieuw == oude_naam:
            return
        nieuw_pad = os.path.join(os.path.dirname(oud), nieuw.strip())
        if os.path.exists(nieuw_pad):
            self._fout(self.t("map_naam_bestaat"))
            return
        try:
            os.rename(oud, nieuw_pad)
        except Exception as ex:
            self._fout(str(ex))
        self._vernieuw()

    def _nieuwe_map(self):
        tab = self.huidige_tab()
        if not tab:
            return
        doel = tab.huidig_pad()
        naam, ok = QInputDialog.getText(
            self, self.t("nieuwe_map"), self.t("nieuwe_map_naam"),
            text=self.t("nieuwe_map"))
        if not ok or not naam.strip():
            return
        nieuw_pad = os.path.join(doel, naam.strip())
        if os.path.exists(nieuw_pad):
            self._fout(self.t("map_naam_bestaat"))
            return
        try:
            os.makedirs(nieuw_pad)
        except Exception as ex:
            self._fout(str(ex))
        self._vernieuw()

    def _alles_select(self):
        tab = self.huidige_tab()
        if not tab:
            return
        if tab.stack.currentIndex() == 0:
            tab.view.selectAll()
        else:
            tab.zoek_view.selectAll()

    def _kopieer_pad(self):
        tab = self.huidige_tab()
        if not tab:
            return
        paden = tab.geselecteerde_paden()
        if paden:
            QApplication.clipboard().setText("\n".join(paden))

    def _eigenschappen(self):
        tab = self.huidige_tab()
        if not tab:
            return
        paden = tab.geselecteerde_paden()
        if not paden:
            paden = [tab.huidig_pad()]
        EigenschappenDialoog(self, paden).exec()

    # ---- beeld ----
    def _wissel_verborgen(self):
        self.cfg["verborgen_tonen"] = self.act_verborgen.isChecked()
        self._pas_fs_filter_toe()
        self._vernieuw()

    def _wijzig_letter(self, delta):
        self.cfg["lettergrootte"] = max(8, min(20, self.cfg["lettergrootte"] + delta))
        self.pas_stijl_toe()

    def _instellingen(self):
        d = InstellingenDialoog(self)
        if d.exec():
            self.taal = self.cfg["taal"] if self.cfg["taal"] in ("nl", "en") else detecteer_taal()
            self._pas_fs_filter_toe()
            self.thumbs.zet_grootte(self.cfg.get("icoon_grootte", 128))
            for i in range(self.tabs.count()):
                w = self.tabs.widget(i)
                if isinstance(w, FileTab):
                    w._stel_icoon_grootte_in()
            self.pas_stijl_toe()
            QMessageBox.information(self, APP_NAAM,
                                   "OK" if self.taal == "en" else "Opgeslagen.")

    def _snelgids(self):
        SnelgidsDialoog(self).exec()

    def _over(self):
        OverDialoog(self).exec()

    # ---- fout ----
    def _fout(self, tekst):
        QMessageBox.warning(self, self.t("fout"), tekst)

    # ---- stijl ----
    def pas_stijl_toe(self):
        ls = self.cfg.get("lettergrootte", 11)
        hc = self.cfg.get("hoog_contrast", False)
        tekst_kleur = "#ffffff" if hc else TEXT
        self.setStyleSheet(STIJL.format(
            bg=BG, panel=PANEL, panel2=PANEL2, text=tekst_kleur, muted=MUTED,
            accent=ACCENT, accent_dim=ACCENT_DIM, line=LINE, ls=ls, ls_klein=max(8, ls - 1)))
        f = QFont()
        f.setPointSize(ls)
        app = QApplication.instance()
        app.setFont(f)
        self._pas_palet_toe(tekst_kleur)

    def _pas_palet_toe(self, tekst_kleur):
        """Donker palet zodat ook door het systeem getekende tekst leesbaar is
        (bv. de namen onder de iconen in de grote-iconenweergave op Windows)."""
        pal = QPalette()
        rol = QPalette.ColorRole
        groep = QPalette.ColorGroup
        pal.setColor(rol.Window, QColor(BG))
        pal.setColor(rol.WindowText, QColor(tekst_kleur))
        pal.setColor(rol.Base, QColor(BG))
        pal.setColor(rol.AlternateBase, QColor(PANEL))
        pal.setColor(rol.Text, QColor(tekst_kleur))
        pal.setColor(rol.Button, QColor(PANEL2))
        pal.setColor(rol.ButtonText, QColor(tekst_kleur))
        pal.setColor(rol.ToolTipBase, QColor(PANEL2))
        pal.setColor(rol.ToolTipText, QColor(tekst_kleur))
        pal.setColor(rol.Highlight, QColor(ACCENT))
        pal.setColor(rol.HighlightedText, QColor("#0e0e11"))
        try:
            pal.setColor(rol.PlaceholderText, QColor(MUTED))
        except Exception:
            pass
        for r in (rol.Text, rol.WindowText, rol.ButtonText):
            pal.setColor(groep.Disabled, r, QColor(MUTED))
        QApplication.instance().setPalette(pal)

    # ---- afsluiten ----
    def closeEvent(self, e):
        try:
            self.voorbeeld.stop_media()
        except Exception:
            pass
        open_paden = []
        for i in range(self.tabs.count()):
            w = self.tabs.widget(i)
            if isinstance(w, FileTab):
                w.stop_zoeken()
                p = w.huidig_pad()
                if p and os.path.isdir(p):
                    open_paden.append(p)
        self.cfg["open_tabs"] = open_paden
        self.cfg["actieve_tab"] = self.tabs.currentIndex()
        self.cfg["venster"] = [self.width(), self.height()]
        bewaar_config(self.cfg)
        super().closeEvent(e)


# ----------------------------------------------------------------------------
# Dialogen
# ----------------------------------------------------------------------------
class InstellingenDialoog(QDialog):
    def __init__(self, venster):
        super().__init__(venster)
        self.v = venster
        self.setWindowTitle(venster.t("instellingen"))
        self.setMinimumWidth(380)
        lay = QFormLayout(self)

        self.taal_box = QComboBox()
        self.taal_box.addItem(venster.t("taal_auto"), "auto")
        self.taal_box.addItem("Nederlands", "nl")
        self.taal_box.addItem("English", "en")
        huidig = venster.cfg.get("taal", "auto")
        idx = self.taal_box.findData(huidig)
        self.taal_box.setCurrentIndex(idx if idx >= 0 else 0)
        lay.addRow(venster.t("taal"), self.taal_box)

        self.letter = QSpinBox()
        self.letter.setRange(8, 20)
        self.letter.setValue(venster.cfg.get("lettergrootte", 11))
        lay.addRow(venster.t("lettergrootte"), self.letter)

        self.icoongrootte = QSpinBox()
        self.icoongrootte.setRange(64, 256)
        self.icoongrootte.setSingleStep(16)
        self.icoongrootte.setValue(venster.cfg.get("icoon_grootte", 128))
        lay.addRow(venster.t("icoon_grootte_lbl"), self.icoongrootte)

        self.contrast = QCheckBox()
        self.contrast.setChecked(bool(venster.cfg.get("hoog_contrast")))
        lay.addRow(venster.t("hoog_contrast"), self.contrast)

        knoppen = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        knoppen.accepted.connect(self._opslaan)
        knoppen.rejected.connect(self.reject)
        lay.addRow(knoppen)

    def _opslaan(self):
        self.v.cfg["taal"] = self.taal_box.currentData()
        self.v.cfg["lettergrootte"] = self.letter.value()
        self.v.cfg["icoon_grootte"] = self.icoongrootte.value()
        self.v.cfg["hoog_contrast"] = self.contrast.isChecked()
        bewaar_config(self.v.cfg)
        self.accept()


class SnelgidsDialoog(QDialog):
    def __init__(self, venster):
        super().__init__(venster)
        self.setWindowTitle("%s - %s" % (APP_NAAM, venster.t("snelgids")))
        self.resize(640, 560)
        lay = QVBoxLayout(self)
        tb = QTextBrowser()
        tb.setOpenExternalLinks(True)
        tb.setHtml(SNELGIDS_NL if venster.taal == "nl" else SNELGIDS_EN)
        lay.addWidget(tb)
        b = QPushButton("OK")
        b.clicked.connect(self.accept)
        lay.addWidget(b)


class OverDialoog(QDialog):
    def __init__(self, venster):
        super().__init__(venster)
        self.setWindowTitle(venster.t("over"))
        self.setMinimumWidth(420)
        lay = QVBoxLayout(self)
        titel = QLabel("%s  v%s" % (APP_NAAM, APP_VERSIE))
        titel.setStyleSheet("font-size: %dpt; font-weight: bold; color: %s;"
                            % (venster.cfg.get("lettergrootte", 11) + 4, ACCENT))
        lay.addWidget(titel)
        if venster.taal == "nl":
            tekst = ("Een snelle, toegankelijke file explorer.\n"
                     "Lokaal en offline. Donationware.\n\n"
                     "Steun de ontwikkeling met een vrijwillige donatie.\n"
                     "Contact: %s" % CONTACT)
        else:
            tekst = ("A fast, accessible file explorer.\n"
                     "Local and offline. Donationware.\n\n"
                     "Support development with a voluntary donation.\n"
                     "Contact: %s" % CONTACT)
        lbl = QLabel(tekst)
        lbl.setWordWrap(True)
        lay.addWidget(lbl)
        b = QPushButton(" \u2665 " + venster.t("donatie"))
        b.setObjectName("donatie")
        b.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(DONATIE_URL)))
        lay.addWidget(b)
        sluit = QPushButton("OK")
        sluit.clicked.connect(self.accept)
        lay.addWidget(sluit)


class EigenschappenDialoog(QDialog):
    def __init__(self, venster, paden):
        super().__init__(venster)
        self.v = venster
        self.setWindowTitle(venster.t("eigenschappen"))
        self.setMinimumWidth(420)
        lay = QFormLayout(self)
        t = venster.t

        if len(paden) == 1:
            p = paden[0]
            info = QFileInfo(p)
            lay.addRow(t("naam"), self._w(os.path.basename(p.rstrip("/\\")) or p))
            lay.addRow(t("locatie"), self._w(os.path.dirname(p)))
            is_map = os.path.isdir(p)
            lay.addRow(t("type_lbl"), self._w(t("map") if is_map else (info.suffix().upper() + " " + t("bestand")).strip()))
            if is_map:
                self.groot_lbl = self._w(t("berekenen"))
                lay.addRow(t("grootte"), self.groot_lbl)
                self.bevat_lbl = self._w(t("berekenen"))
                lay.addRow(t("bevat"), self.bevat_lbl)
                QTimer.singleShot(50, lambda: self._bereken_map(p))
            else:
                lay.addRow(t("grootte"), self._w("%s (%s bytes)" % (
                    mensvriendelijke_grootte(info.size()), "{:,}".format(info.size()))))
            lay.addRow(t("gewijzigd"), self._w(info.lastModified().toString("yyyy-MM-dd HH:mm:ss")))
            try:
                gemaakt = info.birthTime().toString("yyyy-MM-dd HH:mm:ss")
                if gemaakt:
                    lay.addRow(t("gemaakt"), self._w(gemaakt))
            except Exception:
                pass
        else:
            lay.addRow(t("naam"), self._w("%d items" % len(paden)))
            totaal = 0
            for p in paden:
                try:
                    totaal += os.path.getsize(p) if os.path.isfile(p) else 0
                except Exception:
                    pass
            lay.addRow(t("grootte"), self._w(mensvriendelijke_grootte(totaal)))

        b = QPushButton("OK")
        b.clicked.connect(self.accept)
        lay.addRow(b)

    def _w(self, tekst):
        lbl = QLabel(str(tekst))
        lbl.setTextInteractionByMouse = True
        lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        lbl.setWordWrap(True)
        return lbl

    def _bereken_map(self, pad):
        totaal = 0
        n_best = 0
        n_map = 0
        try:
            for wortel, mappen, bestanden in os.walk(pad):
                n_map += len(mappen)
                for b in bestanden:
                    n_best += 1
                    try:
                        totaal += os.path.getsize(os.path.join(wortel, b))
                    except Exception:
                        pass
        except Exception:
            pass
        self.groot_lbl.setText("%s (%s bytes)" % (
            mensvriendelijke_grootte(totaal), "{:,}".format(totaal)))
        self.bevat_lbl.setText(self.v.t("n_bestanden_mappen").format(b=n_best, m=n_map))


# ----------------------------------------------------------------------------
# App-icoon (programmatisch, in de huisstijl) als fallback voor logo.png
# ----------------------------------------------------------------------------
def maak_app_icoon():
    bestand = os.path.join(BASIS, "logo.png")
    if os.path.exists(bestand):
        ic = QIcon(bestand)
        if not ic.isNull():
            return ic
    # programmatische map met staalblauw accent
    pm = QPixmap(64, 64)
    pm.fill(QColor(BG))
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QColor(ACCENT))
    p.drawRoundedRect(8, 22, 48, 30, 5, 5)
    p.setBrush(QColor(ACCENT_DIM))
    p.drawRoundedRect(8, 14, 24, 12, 4, 4)
    p.setBrush(QColor(PANEL2))
    p.drawRoundedRect(12, 28, 40, 20, 3, 3)
    p.end()
    return QIcon(pm)


# ----------------------------------------------------------------------------
# Snelgids-teksten
# ----------------------------------------------------------------------------
SNELGIDS_NL = """
<h2 style="color:#6fa3d6">DraveExplorer - Snelgids</h2>
<p>Een snelle, toegankelijke bestandsverkenner. Lokaal en offline.</p>
<h3 style="color:#6fa3d6">Navigeren</h3>
<ul>
<li><b>Zijbalk links:</b> snelkoppelingen (Documenten, Downloads...) en al je
<b>stations</b> met een balk die de <b>gebruikte opslag</b> toont. Klik om te openen.</li>
<li><b>Mappenboom</b> (onderin de zijbalk): klap mappen uit met de pijltjes en
klik om er heen te gaan. De boom volgt automatisch waar je bent.</li>
<li><b>Favorieten</b>: zet een map vast met <b>Ctrl+D</b> of via de
rechtermuisknop ("Aan favorieten toevoegen"). Ze verschijnen bovenin de
zijbalk; verwijderen kan met de rechtermuisknop op de favoriet.</li>
<li><b>Werkbalk:</b> Terug / Vooruit / Omhoog / Vernieuwen. De <b>adresbalk</b>
accepteert een pad (Enter) om er direct heen te gaan.</li>
<li><b>Broodkruimel-balk</b> (onder de werkbalk): klik op een onderdeel van
het pad om meteen naar die map te springen.</li>
<li><b>Weergave wisselen</b>: met de knop in de werkbalk (of Ctrl+1 / Ctrl+2)
schakel je tussen <b>lijst</b> en <b>grote iconen</b>. In de iconenweergave
zie je <b>miniaturen van je foto's</b>.</li>
<li><b>Dubbelklik</b> op een map opent die map; op een bestand opent het met het
standaardprogramma.</li>
<li><b>Middenklik</b> op een map opent die in een <b>nieuwe tab</b>.
Rechtsklik geeft "Openen in nieuwe tab". Open tabs komen terug na het
opnieuw opstarten.</li>
</ul>
<h3 style="color:#6fa3d6">Zoeken</h3>
<ul>
<li>Typ in het <b>filterveld</b> om de huidige map live te filteren.</li>
<li>Klik op <b>Q</b> (of vink "in submappen zoeken") om ook onderliggende mappen te
doorzoeken. Wissen: ga ergens heen of vernieuw.</li>
<li>Met de <b>keuzelijst rechts van het filterveld</b> toon je in één keer alleen
een bepaald type (afbeeldingen, documenten, muziek, video, archieven). Mappen
blijven zichtbaar zodat je kunt blijven navigeren.</li>
<li><b>Voorbeeldvenster</b>: klik op de voorbeeldknop in de werkbalk (of
<b>Ctrl+P</b>) om rechts een voorbeeld van het geselecteerde bestand te tonen:
afbeeldingen, tekst, PDF, en een speler voor video en muziek. Voor bestanden
zoals zip of exe verschijnt "geen voorbeeld".</li>
</ul>
<h3 style="color:#6fa3d6">Bestanden beheren</h3>
<ul>
<li>Kopieren <b>Ctrl+C</b>, Knippen <b>Ctrl+X</b>, Plakken <b>Ctrl+V</b>.</li>
<li>Hernoemen <b>F2</b>, Verwijderen <b>Delete</b> (naar prullenbak),
Permanent <b>Shift+Delete</b>.</li>
<li>Nieuwe map <b>Ctrl+Shift+N</b>, Eigenschappen <b>Alt+Enter</b>,
Alles selecteren <b>Ctrl+A</b>.</li>
</ul>
<h3 style="color:#6fa3d6">Toegankelijkheid</h3>
<ul>
<li>Tekst groter/kleiner met <b>Ctrl++</b> / <b>Ctrl+-</b>.</li>
<li>In <b>Beeld &gt; Instellingen</b>: taal (NL/EN/automatisch), lettergrootte,
<b>icoongrootte</b> voor de iconenweergave, en extra hoog contrast.</li>
<li>Verborgen bestanden tonen: <b>Ctrl+H</b>.</li>
</ul>
<p style="color:#8a8a94">Donationware - steun via de hartjes-knop rechtsonder.
Contact: service@dravenlock.nl</p>
"""

SNELGIDS_EN = """
<h2 style="color:#6fa3d6">DraveExplorer - Quick guide</h2>
<p>A fast, accessible file explorer. Local and offline.</p>
<h3 style="color:#6fa3d6">Navigating</h3>
<ul>
<li><b>Left sidebar:</b> shortcuts (Documents, Downloads...) and all your
<b>drives</b> with a bar showing <b>used storage</b>. Click to open.</li>
<li><b>Folder tree</b> (bottom of the sidebar): expand folders with the arrows
and click to go there. The tree follows where you are.</li>
<li><b>Favorites</b>: pin a folder with <b>Ctrl+D</b> or via right-click
("Add to favorites"). They appear at the top of the sidebar; remove them by
right-clicking the favorite.</li>
<li><b>Toolbar:</b> Back / Forward / Up / Refresh. The <b>address bar</b> accepts a
path (Enter) to jump straight there.</li>
<li><b>Breadcrumb bar</b> (below the toolbar): click any part of the path to
jump straight to that folder.</li>
<li><b>Switch view</b>: use the toolbar button (or Ctrl+1 / Ctrl+2) to toggle
between <b>list</b> and <b>large icons</b>. Icon view shows
<b>thumbnails of your photos</b>.</li>
<li><b>Double-click</b> a folder to open it; a file opens with its default app.</li>
<li><b>Middle-click</b> a folder to open it in a <b>new tab</b>.
Right-click offers "Open in new tab". Open tabs are restored on restart.</li>
</ul>
<h3 style="color:#6fa3d6">Searching</h3>
<ul>
<li>Type in the <b>filter field</b> to filter the current folder live.</li>
<li>Click <b>Q</b> to also search subfolders. Clear by navigating or refreshing.</li>
<li>Use the <b>dropdown next to the filter field</b> to show only one type at a
time (images, documents, music, video, archives). Folders stay visible so you
can keep navigating.</li>
<li><b>Preview pane</b>: click the preview button in the toolbar (or
<b>Ctrl+P</b>) to show a preview of the selected file on the right: images,
text, PDF, and a player for video and music. Files such as zip or exe show
"no preview".</li>
</ul>
<h3 style="color:#6fa3d6">Managing files</h3>
<ul>
<li>Copy <b>Ctrl+C</b>, Cut <b>Ctrl+X</b>, Paste <b>Ctrl+V</b>.</li>
<li>Rename <b>F2</b>, Delete <b>Delete</b> (recycle bin), Permanent <b>Shift+Delete</b>.</li>
<li>New folder <b>Ctrl+Shift+N</b>, Properties <b>Alt+Enter</b>, Select all <b>Ctrl+A</b>.</li>
</ul>
<h3 style="color:#6fa3d6">Accessibility</h3>
<ul>
<li>Larger/smaller text with <b>Ctrl++</b> / <b>Ctrl+-</b>.</li>
<li>In <b>View &gt; Settings</b>: language (EN/NL/automatic), font size,
<b>icon size</b> for the icon view, and extra high contrast.</li>
<li>Show hidden files: <b>Ctrl+H</b>.</li>
</ul>
<p style="color:#8a8a94">Donationware - support via the heart button at the bottom
right. Contact: service@dravenlock.nl</p>
"""


# ----------------------------------------------------------------------------
# Stijl (huisstijl Dravenlock). {ls} = lettergrootte (instelbaar).
# Leesbaar in ALLE toestanden: selectie, disabled, hover.
# ----------------------------------------------------------------------------
STIJL = """
* {{ font-size: {ls}pt; }}
QMainWindow, QWidget {{ background: {bg}; color: {text}; }}
QMenuBar {{ background: {panel}; color: {text}; border-bottom: 1px solid {line}; }}
QMenuBar::item {{ padding: 5px 10px; background: transparent; }}
QMenuBar::item:selected {{ background: {accent_dim}; color: #ffffff; }}
QMenu {{ background: {panel2}; color: {text}; border: 1px solid {line}; }}
QMenu::item {{ padding: 6px 22px; }}
QMenu::item:selected {{ background: {accent_dim}; color: #ffffff; }}
QMenu::separator {{ height: 1px; background: {line}; margin: 4px 8px; }}

#werkbalk {{ background: {panel}; border-bottom: 1px solid {line}; }}
#tbtn {{
    background: {panel2}; color: {text}; border: 1px solid {line};
    border-radius: 6px; padding: 6px 12px; font-weight: bold; min-width: 18px;
}}
#tbtn:hover {{ background: {accent_dim}; color: #ffffff; border-color: {accent}; }}
#tbtn:pressed {{ background: {accent}; color: #0e0e11; }}
#tbtn:disabled {{ color: {muted}; background: {panel}; }}

QLineEdit {{
    background: {panel2}; color: {text}; border: 1px solid {line};
    border-radius: 6px; padding: 6px 9px; selection-background-color: {accent};
    selection-color: #0e0e11;
}}
QLineEdit:focus {{ border-color: {accent}; }}
QLineEdit::placeholder {{ color: {muted}; }}

QSplitter::handle {{ background: {line}; width: 2px; }}

#kruimelbalk {{ background: {panel}; border: none; border-bottom: 1px solid {line}; }}
#kruimelinhoud {{ background: {panel}; }}
#kruimelknop {{
    background: transparent; color: {text}; border: none;
    border-radius: 5px; padding: 5px 9px;
}}
#kruimelknop:hover {{ background: {accent_dim}; color: #ffffff; }}
#kruimelknop:pressed {{ background: {accent}; color: #0e0e11; }}
#kruimelschei {{ color: {muted}; padding: 0 1px; }}

#zijbalk {{ background: {panel}; }}
#zijpaneel {{ background: {panel}; border-right: 1px solid {line}; }}
#mappenboom {{
    background: {panel}; color: {text}; border: none; outline: none;
    selection-background-color: {accent}; selection-color: #0e0e11;
}}
#mappenboom::item {{ padding: 3px 2px; }}
#mappenboom::item:hover {{ background: {panel2}; }}
#mappenboom::item:selected {{ background: {accent}; color: #0e0e11; }}
#mappenboom::item:selected:!active {{ background: {accent_dim}; color: #ffffff; }}
#mappenboom::branch {{ background: {panel}; }}
QScrollArea {{ background: {panel}; border: none; border-right: 1px solid {line}; }}
#sectiekop {{ color: {muted}; font-size: {ls_klein}pt; font-weight: bold;
    padding: 6px 6px 2px 6px; letter-spacing: 1px; }}
#snelknop {{
    background: transparent; color: {text}; border: none; text-align: left;
    padding: 7px 8px; border-radius: 6px;
}}
#snelknop:hover {{ background: {accent_dim}; color: #ffffff; }}
#favknop {{
    background: transparent; color: {text}; border: none; text-align: left;
    padding: 7px 8px; border-radius: 6px;
}}
#favknop:hover {{ background: {accent_dim}; color: #ffffff; }}
#statusstation {{ color: {muted}; padding: 0 10px; }}
.drive {{ background: {panel2}; border: 1px solid {line}; border-radius: 8px;
    margin: 2px 0; }}
.drive:hover {{ border-color: {accent}; }}
#drivetitel {{ color: {text}; font-weight: bold; }}
#drivesub {{ color: {muted}; font-size: {ls_klein}pt; }}

QTabWidget::pane {{ border: none; }}
QTabBar::tab {{
    background: {panel}; color: {muted}; border: 1px solid {line};
    border-bottom: none; border-top-left-radius: 6px; border-top-right-radius: 6px;
    padding: 7px 16px; margin-right: 2px;
}}
QTabBar::tab:selected {{ background: {panel2}; color: {text}; border-color: {accent}; }}
QTabBar::tab:hover {{ color: {text}; }}

QTreeView {{
    background: {bg}; color: {text}; border: none; outline: none;
    alternate-background-color: {panel};
    selection-background-color: {accent}; selection-color: #0e0e11;
}}
QTreeView::item {{ padding: 4px 2px; }}
QTreeView::item:hover {{ background: {panel2}; }}
QTreeView::item:selected {{ background: {accent}; color: #0e0e11; }}
QTreeView::item:selected:!active {{ background: {accent_dim}; color: #ffffff; }}
QHeaderView::section {{
    background: {panel}; color: {text}; border: none;
    border-right: 1px solid {line}; border-bottom: 1px solid {line};
    padding: 6px 8px; font-weight: bold;
}}
QHeaderView::section:hover {{ background: {panel2}; }}

QListView {{
    background: {bg}; color: {text}; border: none; outline: none;
    selection-background-color: {accent}; selection-color: #0e0e11;
}}
QListView::item {{
    color: {text}; border-radius: 6px; padding: 4px;
}}
QListView::item:hover {{ background: {panel2}; }}
QListView::item:selected {{ background: {accent}; color: #0e0e11; }}
QListView::item:selected:!active {{ background: {accent_dim}; color: #ffffff; }}

#voorbeeldpaneel {{ background: {panel}; border-left: 1px solid {line}; }}
#voorbeeldkop {{ background: {panel2}; border-bottom: 1px solid {line}; }}
#voorbeeldtitel {{ color: {text}; font-weight: bold; }}
#voorbeeldmelding {{ color: {muted}; padding: 20px; }}
#voorbeeldscroll {{ background: {bg}; border: none; }}
#voorbeeldtekst {{
    background: {bg}; color: {text}; border: none;
    selection-background-color: {accent}; selection-color: #0e0e11;
}}
#voorbeeldpdf {{ background: {bg}; border: none; }}
#voorbeeldvideo {{ background: #000000; }}
#medianoot {{ color: {accent}; font-size: 22pt; padding: 16px; }}
#mediatijd {{ color: {muted}; padding: 0 6px; }}
#mediaschuif::groove:horizontal {{ background: {line}; height: 6px; border-radius: 3px; }}
#mediaschuif::handle:horizontal {{ background: {accent}; width: 14px; margin: -5px 0; border-radius: 7px; }}
#mediaschuif::sub-page:horizontal {{ background: {accent_dim}; border-radius: 3px; }}

QStatusBar {{ background: {panel}; color: {text}; border-top: 1px solid {line}; }}
QStatusBar::item {{ border: none; }}
#donatie {{
    background: {accent}; color: #0e0e11; border: 1px solid {accent};
    border-radius: 7px; padding: 6px 18px; font-weight: bold;
}}
#donatie:hover {{ background: #8db8e0; border-color: #8db8e0; }}
#donatie:pressed {{ background: {accent_dim}; color: #ffffff; }}

QScrollBar:vertical {{ background: {panel}; width: 12px; margin: 0; }}
QScrollBar::handle:vertical {{ background: {line}; border-radius: 6px; min-height: 28px; }}
QScrollBar::handle:vertical:hover {{ background: {accent_dim}; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; }}
QScrollBar:horizontal {{ background: {panel}; height: 12px; }}
QScrollBar::handle:horizontal {{ background: {line}; border-radius: 6px; min-width: 28px; }}

QDialog {{ background: {bg}; color: {text}; }}
QPushButton {{
    background: {panel2}; color: {text}; border: 1px solid {line};
    border-radius: 6px; padding: 7px 16px;
}}
QPushButton:hover {{ background: {accent_dim}; color: #ffffff; border-color: {accent}; }}
QPushButton:pressed {{ background: {accent}; color: #0e0e11; }}
QComboBox, QSpinBox {{
    background: {panel2}; color: {text}; border: 1px solid {line};
    border-radius: 6px; padding: 5px 8px;
}}
QComboBox QAbstractItemView {{
    background: {panel2}; color: {text}; selection-background-color: {accent};
    selection-color: #0e0e11;
}}
QTextBrowser {{ background: {panel2}; color: {text}; border: 1px solid {line};
    border-radius: 6px; }}
QCheckBox {{ color: {text}; }}
QMessageBox {{ background: {bg}; color: {text}; }}
QToolTip {{ background: {panel2}; color: {text}; border: 1px solid {accent}; padding: 4px; }}
"""


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------
def main():
    try:
        if os.path.exists(FOUT_BESTAND):
            os.remove(FOUT_BESTAND)
    except Exception:
        pass

    QApplication.setApplicationName(APP_NAAM)
    app = QApplication(sys.argv)
    cfg = laad_config()
    venster = Verkenner(cfg)
    venster.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
