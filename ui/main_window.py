from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget, QLabel


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

        self.page_container.addWidget(QLabel("Dashboard Page Content (Placeholder)"))
        self.page_container.addWidget(QLabel("Squad Manager Content (Placeholder)"))
        self.page_container.addWidget(QLabel("Scouting Market Content (Placeholder)"))
        self.page_container.addWidget(QLabel("Financial Simulator Content (Placeholder)"))

        self.btn_dashboard.clicked.connect(lambda: self.page_container.setCurrentIndex(0))
        self.btn_squad.clicked.connect(lambda: self.page_container.setCurrentIndex(1))
        self.btn_scouting.clicked.connect(lambda: self.page_container.setCurrentIndex(2))
        self.btn_finance.clicked.connect(lambda: self.page_container.setCurrentIndex(3))

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.page_container)