from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import Qt

class ObslugaUI:
    def __init__(self, okno_glowne):

        self.okno = okno_glowne

    def init_ui(self):
        # 1. Najpierw tworzymy Przycisk START
        self.okno.btn_start = QPushButton("START / STOP", self.okno)
        self.okno.btn_start.setGeometry(380, 690, 150, 40)
        
        # 2. Najpierw tworzymy Etykietę STATUS
        self.okno.lbl_status = QLabel("STAN: OCZEKIWANIE", self.okno)
        self.okno.lbl_status.setGeometry(550, 690, 300, 40)
        self.okno.lbl_status.setStyleSheet("font-size: 14px; color: #aaa;")

        # 3. Teraz bezpiecznie ustawiamy domyślny wygląd
        self.ustaw_wyglad_nieaktywny()
        
        # Podpinamy kliknięcie
        self.okno.btn_start.clicked.connect(self.okno.toggle_process)

        # Przycisk STATYSTYKI
        self.okno.btn_stats = QPushButton("Statystyki (ESC)", self.okno)
        self.okno.btn_stats.setGeometry(950, 10, 130, 40)
        self.okno.btn_stats.setStyleSheet("""
            QPushButton { background-color: #555; color: white; border: 1px solid #777; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { background-color: #777; }
        """)
        self.okno.btn_stats.clicked.connect(self.toggle_statystyki)

    def ustaw_wyglad_aktywny(self):
        self.okno.btn_start.setStyleSheet("background-color: #388E3C; border: 2px solid #1B5E20; color: white; font-weight: bold;")
        self.okno.lbl_status.setText("STAN: PRACA AUTOMATYCZNA")

    def ustaw_wyglad_nieaktywny(self):
        self.okno.btn_start.setStyleSheet("""
            QPushButton { background-color: #d32f2f; border: 2px solid #b71c1c; border-radius: 4px; color: white; font-weight: bold; }
            QPushButton:hover { background-color: #f44336; }
        """)
        self.okno.lbl_status.setText("STAN: ZATRZYMANY")

    def toggle_statystyki(self):
        if self.okno.okno_statystyk.isVisible():
            self.okno.okno_statystyk.hide()
        else:
            self.okno.okno_statystyk.show()
            self.okno.okno_statystyk.raise_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.toggle_statystyki()

    def mousePressEvent(self, event):
        urzadzenia = self.okno.uklad.lista_urzadzen
        wymagane_odswiezenie = False

        for urzadzenie in urzadzenia:

            if hasattr(urzadzenie, 'sprawdz_klikniecie'):
                if urzadzenie.sprawdz_klikniecie(event.x(), event.y()):
                    wymagane_odswiezenie = True
        
        if wymagane_odswiezenie:
            self.okno.update()