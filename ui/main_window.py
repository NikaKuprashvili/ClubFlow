from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel
)
from ui.pages.dashboard_page import DashboardPage
from ui.pages.squad_page import SquadPage
from ui.pages.scouting_page import ScoutingPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ClubFlow - Advanced Football Analytics")
        self.resize(1240, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(240)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 30)
        sidebar_layout.setSpacing(10)

        logo_lbl = QLabel("⚡ ClubFlow")
        logo_lbl.setStyleSheet("""
            color: #FFFFFF; 
            font-size: 22px; 
            font-weight: 800; 
            padding-left: 10px; 
            margin-bottom: 25px;
        """)
        sidebar_layout.addWidget(logo_lbl)

        self.btn_dashboard = QPushButton("  📊  Dashboard")
        self.btn_squad = QPushButton("  👥  Squad Manager")
        self.btn_scouting = QPushButton("  🔍  Scouting Market")
        self.btn_finance = QPushButton("  💼  Financial Simulator")

        self.menu_buttons = [
            self.btn_dashboard,
            self.btn_squad,
            self.btn_scouting,
            self.btn_finance
        ]

        for btn in self.menu_buttons:
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        layout.addWidget(sidebar)

        self.stacked_widget = QStackedWidget()

        self.dashboard_page = DashboardPage()
        self.squad_page = SquadPage()
        self.scouting_page = ScoutingPage()

        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.squad_page)
        self.stacked_widget.addWidget(self.scouting_page)

        layout.addWidget(self.stacked_widget)

        self.btn_dashboard.clicked.connect(lambda: self.change_page(0, self.btn_dashboard))
        self.btn_squad.clicked.connect(lambda: self.change_page(1, self.btn_squad))
        self.btn_scouting.clicked.connect(lambda: self.change_page(2, self.btn_scouting))
        self.btn_finance.clicked.connect(lambda: self.change_page(3, self.btn_finance))

        self.setStyleSheet("""
            QMainWindow {
                background-color: #171C24;
            }
            QWidget#sidebar {
                background-color: #1C2127;
                border-right: 1px solid #2D3540;
            }
            QPushButton {
                background-color: transparent;
                color: #8F9CAE;
                border: none;
                border-radius: 8px;
                padding: 14px 18px;
                font-size: 13px;
                font-weight: 600;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #242A32;
                color: #FFFFFF;
            }
            QPushButton[active="true"] {
                background-color: #242A32;
                color: #FFFFFF;
                border-left: 4px solid #3498db;
                border-top-left-radius: 0px;
                border-bottom-left-radius: 0px;
            }
        """)

        self.change_page(0, self.btn_dashboard)

    def change_page(self, index, clicked_button):
        self.stacked_widget.setCurrentIndex(index)

        for btn in self.menu_buttons:
            btn.setProperty("active", "false")

        clicked_button.setProperty("active", "true")

        current_style = self.style()
        if current_style is not None:
            for btn in self.menu_buttons:
                current_style.unpolish(btn)
                current_style.polish(btn)