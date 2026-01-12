import sys
from PyQt5.QtWidgets import QApplication
from symulacja_ui import SymulacjaProcesu

def main():
    app = QApplication(sys.argv)
    okno = SymulacjaProcesu()
    okno.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()