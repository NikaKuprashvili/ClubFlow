from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class SquadPage(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        title_label = QLabel("გუნდის მენეჯერი (Squad Overview)")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF;")
        main_layout.addWidget(title_label)

        self.players_mock_data = [
            {"id": 1, "name": "Marcus Perez", "pos": "FW", "rating": 88, "wage": "€1,250,000", "vfm": "7.5 VFM",
             "vfm_color": "#2ecc71"},
            {"id": 2, "name": "Daniel Cannon", "pos": "MF", "rating": 85, "wage": "€1,360,000", "vfm": "7.1 VFM",
             "vfm_color": "#2ecc71"},
            {"id": 3, "name": "Leonard James", "pos": "DF", "rating": 82, "wage": "€1,380,000", "vfm": "6.8 VFM",
             "vfm_color": "#2ecc71"},
            {"id": 4, "name": "John Banker", "pos": "GK", "rating": 80, "wage": "€1,330,000", "vfm": "6.6 VFM",
             "vfm_color": "#2ecc71"},
            {"id": 5, "name": "Oliver Sanchez", "pos": "FW", "rating": 79, "wage": "€1,100,000", "vfm": "6.5 VFM",
             "vfm_color": "#2ecc71"}
        ]

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setRowCount(len(self.players_mock_data))
        self.table.setHorizontalHeaderLabels(
            ["მოთამაშე", "პოზიცია", "რეიტინგი", "ყოველკვირეული ხელფასი", "VFM ინდექსი"])

        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setShowGrid(False)

        v_header = self.table.verticalHeader()
        if v_header:
            v_header.setVisible(False)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2A2A2A;
                border-radius: 12px;
                border: none;
                gridline-color: transparent;
                padding: 10px;
            }
            QTableWidget::item {
                color: #FFFFFF;
                font-size: 14px;
                padding: 12px;
                border-bottom: 1px solid #3A3A3A;
            }
            QTableWidget::item:selected {
                background-color: #3D3D3D;
                color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #2A2A2A;
                color: #AAAAAA;
                font-size: 13px;
                font-weight: bold;
                border: none;
                padding: 10px;
                border-bottom: 2px solid #444444;
            }
        """)

        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Interactive)

        for row_idx, player in enumerate(self.players_mock_data):
            p_name = str(player["name"])
            p_pos = str(player["pos"])
            p_rating = str(player["rating"])
            p_wage = str(player["wage"])
            p_vfm = str(player["vfm"])
            p_vfm_color = str(player["vfm_color"])

            name_item = QTableWidgetItem(p_name)

            pos_item = QTableWidgetItem(p_pos)
            pos_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            rating_item = QTableWidgetItem(p_rating)
            rating_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            wage_item = QTableWidgetItem(p_wage)
            wage_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            vfm_item = QTableWidgetItem(p_vfm)
            vfm_item.setForeground(QColor(p_vfm_color))

            current_font = name_item.font()
            current_font.setBold(True)
            vfm_item.setFont(current_font)
            vfm_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(row_idx, 0, name_item)
            self.table.setItem(row_idx, 1, pos_item)
            self.table.setItem(row_idx, 2, rating_item)
            self.table.setItem(row_idx, 3, wage_item)
            self.table.setItem(row_idx, 4, vfm_item)

        main_layout.addWidget(self.table)

        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 9)