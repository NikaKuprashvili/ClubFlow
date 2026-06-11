from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget, QLabel
from ui.pages.dashboard_page import DashboardPage
from ui.pages.squad_page import SquadPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ClubFlow - Advanced Football Analytics")
        self.resize(1100, 700)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)

        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_squad = QPushButton("Squad Manager")
        self.btn_scouting = QPushButton("Scouting Market")
        self.btn_finance = QPushButton("Financial Simulator")

        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_squad)
        sidebar_layout.addWidget(self.btn_scouting)
        sidebar_layout.addWidget(self.btn_finance)
        sidebar_layout.addStretch()

        self.page_container = QStackedWidget()

        self.page_container.addWidget(DashboardPage())
        self.page_container.addWidget(SquadPage())
        self.page_container.addWidget(QLabel("Scouting Market Content (Placeholder)"))
        self.page_container.addWidget(QLabel("Financial Simulator Content (Placeholder)"))

        self.btn_dashboard.clicked.connect(lambda: self.page_container.setCurrentIndex(0))
        self.btn_squad.clicked.connect(lambda: self.page_container.setCurrentIndex(1))
        self.btn_scouting.clicked.connect(lambda: self.page_container.setCurrentIndex(2))
        self.btn_finance.clicked.connect(lambda: self.page_container.setCurrentIndex(3))

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.page_container)

        self.setStyleSheet("""
                    QMainWindow {
                        background-color: #1E1E1E;
                    }
                    QPushButton {
                        background-color: #2D2D2D;
                        color: #FFFFFF;
                        border: none;
                        border-radius: 5px;
                        padding: 8px 15px;
                        font-size: 13px;
                        text-align: left;
                    }
                    QPushButton:hover {
                        background-color: #3D3D3D;
                    }
                    QPushButton:pressed {
                        background-color: #4D4D4D;
                    }
                """)