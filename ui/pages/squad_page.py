from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QTableWidget, QTableWidgetItem, \
    QHeaderView
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

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        squad_kpi_data = [
            ("მიმდინარე პოზიცია", "La Liga, 1st", "#2ecc71"),
            ("სატრანსფერო ბიუჯეტი", "€120,500,000", "#3498db"),
            ("გუნდის რეიტინგი", "88 OVR", "#9b59b6"),
            ("კონტრაქტების სტატუსი", "3 იწურება მალე", "#e74c3c")
        ]

        for title, value, color in squad_kpi_data:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #2A2A2A;
                    border-radius: 10px;
                    padding: 15px;
                }
            """)
            card_layout = QVBoxLayout(card)

            c_title = QLabel(title)
            c_title.setStyleSheet("font-size: 13px; color: #AAAAAA; font-weight: 500;")

            c_value = QLabel(value)
            c_value.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {color}; margin-top: 5px;")

            card_layout.addWidget(c_title)
            card_layout.addWidget(c_value)
            cards_layout.addWidget(card)

        main_layout.addLayout(cards_layout)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(25)

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
                font-size: 13px;
                padding: 8px;
                border-bottom: 1px solid #3A3A3A;
            }
            QTableWidget::item:selected {
                background-color: #3D3D3D;
                color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #2A2A2A;
                color: #AAAAAA;
                font-size: 12px;
                font-weight: bold;
                border: none;
                padding: 8px;
                border-bottom: 2px solid #444444;
                text-align: center;
            }
        """)

        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)

            header.resizeSection(0, 130)
            header.resizeSection(1, 75)
            header.resizeSection(2, 75)
            header.resizeSection(3, 190)
            header.resizeSection(4, 120)

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
            wage_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

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

        content_layout.addWidget(self.table)

        side_panel = QFrame()
        side_panel.setStyleSheet("""
            QFrame {
                background-color: #2A2A2A;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        side_layout = QVBoxLayout(side_panel)
        side_layout.setSpacing(15)

        schedule_title = QLabel("მატჩების განრიგი (Schedule)")
        schedule_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")
        side_layout.addWidget(schedule_title)

        matches_mock = [
            ("28 აგვ, 18:00", "vs Palies", "Barroal Club"),
            ("30 აგვ, 13:00", "vs Prarwarsi", "Bolnson Iberian")
        ]

        for m_date, m_opp, m_venue in matches_mock:
            m_frame = QFrame()
            m_frame.setStyleSheet("background-color: #333333; border-radius: 8px; padding: 10px;")
            m_layout = QHBoxLayout(m_frame)

            lbl_date = QLabel(m_date)
            lbl_date.setStyleSheet("color: #3498db; font-size: 13px; font-weight: bold;")

            lbl_opp = QLabel(m_opp)
            lbl_opp.setStyleSheet("color: #FFFFFF; font-size: 13px;")

            lbl_venue = QLabel(m_venue)
            lbl_venue.setStyleSheet("color: #AAAAAA; font-size: 11px;")
            lbl_venue.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            m_layout.addWidget(lbl_date)
            m_layout.addWidget(lbl_opp)
            m_layout.addWidget(lbl_venue)
            side_layout.addWidget(m_frame)

        side_layout.addStretch()
        content_layout.addWidget(side_panel)

        content_layout.setStretch(0, 65)
        content_layout.setStretch(1, 35)

        main_layout.addLayout(content_layout)

        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 2)
        main_layout.setStretch(2, 7)