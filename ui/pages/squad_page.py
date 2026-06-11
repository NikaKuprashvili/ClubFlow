from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QTableWidget, QTableWidgetItem, \
    QHeaderView, QProgressBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from services.player_service import PlayerService


class SquadPage(QWidget):
    def __init__(self):
        super().__init__()

        self.player_service = PlayerService()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(20)

        header_layout = QHBoxLayout()
        title_label = QLabel("REAL MADRID C.F.  |  SQUAD PERFORMANCE MANAGER")
        title_label.setStyleSheet("font-size: 22px; font-weight: 800; color: #FFFFFF; letter-spacing: 1px;")

        profile_container = QWidget()
        profile_layout = QHBoxLayout(profile_container)
        profile_layout.setContentsMargins(0, 0, 0, 0)
        profile_layout.setSpacing(10)
        profile_name = QLabel("Premium Admin")
        profile_name.setStyleSheet("color: #8F9CAE; font-size: 13px; font-weight: 600;")
        profile_avatar = QLabel("👤")
        profile_avatar.setStyleSheet(
            "font-size: 16px; background-color: #2D3540; padding: 6px; border-radius: 14px; color: #3498db;")
        profile_layout.addWidget(profile_name)
        profile_layout.addWidget(profile_avatar)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(profile_container)
        main_layout.addLayout(header_layout)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)

        squad_kpi_data = [
            ("Squad Size", "26 Active", "#ffffff", "👥"),
            ("Average Age", "25.4 Years", "#3498db", "⏳"),
            ("Avg Squad Rating", "88.2 OVR", "#2ecc71", "🔥"),
            ("Critical Expired", "3 Players", "#e74c3c", "🚨")
        ]

        for title, value, color, icon in squad_kpi_data:
            card = QFrame()
            card.setStyleSheet("background-color: #242A32; border-radius: 12px; border: 1px solid #2D3540;")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(18, 16, 18, 16)

            t_row = QHBoxLayout()
            tl = QLabel(title)
            tl.setStyleSheet(
                "font-size: 11px; color: #8F9CAE; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; border: none; background: transparent;")
            ti = QLabel(icon)
            ti.setStyleSheet("font-size: 14px; border: none; background: transparent;")
            t_row.addWidget(tl)
            t_row.addStretch()
            t_row.addWidget(ti)

            vl = QLabel(value)
            vl.setStyleSheet(
                f"font-size: 19px; font-weight: 800; color: {color}; margin-top: 10px; border: none; background: transparent;")

            card_layout.addLayout(t_row)
            card_layout.addWidget(vl)
            cards_layout.addWidget(card)

        main_layout.addLayout(cards_layout)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        table_frame = QFrame()
        table_frame.setStyleSheet("background-color: #242A32; border-radius: 14px; border: 1px solid #2D3540;")
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(18, 15, 18, 15)

        table_title = QLabel("Squad Performance & Health Audit")
        table_title.setStyleSheet(
            "color: #FFFFFF; font-size: 14px; font-weight: 700; padding-bottom: 5px; border: none;")
        table_layout.addWidget(table_title)

        players_data = self.player_service.get_all_players()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setRowCount(len(players_data))
        self.table.setHorizontalHeaderLabels(["Player", "Pos", "Rating", "Injury Risk", "VFM Index"])

        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setShowGrid(False)

        v_header = self.table.verticalHeader()
        if v_header:
            v_header.setVisible(False)

        self.table.setStyleSheet("""
            QTableWidget { background: transparent; border: none; } 
            QTableWidget::item { color: #FFFFFF; font-size: 12px; border-bottom: 1px solid #2D3540; padding: 8px; } 
            QTableWidget::item:selected { background-color: #2D3540; color: #FFFFFF; }
            QHeaderView::section { background: transparent; color: #8F9CAE; font-size: 11px; font-weight: 700; border: none; border-bottom: 2px solid #2D3540; padding-bottom: 5px; }
        """)

        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
            header.resizeSection(0, 140)
            header.resizeSection(1, 55)
            header.resizeSection(2, 60)
            header.resizeSection(3, 105)

        mock_additional_data = [
            ("High Risk", "#e74c3c", 85),
            ("Medium Risk", "#e67e22", 72),
            ("Low Risk", "#2ecc71", 58),
            ("Low Risk", "#2ecc71", 45),
            ("Medium Risk", "#e67e22", 30)
        ]

        for row_idx, player in enumerate(players_data):
            p_name = str(player["name"])
            p_pos = str(player["pos"])
            p_rating = str(player["rating"])

            risk_text, risk_color, vfm_val = mock_additional_data[row_idx % len(mock_additional_data)]

            name_item = QTableWidgetItem(p_name)
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_idx, 0, name_item)

            pos_item = QTableWidgetItem(p_pos)
            pos_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 1, pos_item)

            rating_item = QTableWidgetItem(p_rating)
            rating_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 2, rating_item)

            risk_item = QTableWidgetItem(risk_text)
            risk_item.setForeground(QColor(risk_color))
            risk_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 3, risk_item)

            progress_container = QWidget()
            progress_layout = QHBoxLayout(progress_container)
            progress_layout.setContentsMargins(10, 4, 10, 4)

            pbar = QProgressBar()
            pbar.setRange(0, 100)
            pbar.setValue(vfm_val)
            pbar.setTextVisible(False)

            bar_color = "#2ecc71" if vfm_val > 70 else ("#e67e22" if vfm_val > 40 else "#e74c3c")
            pbar.setStyleSheet(f"""
                QProgressBar {{
                    background-color: #1C2127;
                    border-radius: 4px;
                    border: none;
                    height: 8px;
                }}
                QProgressBar::chunk {{
                    background-color: {bar_color};
                    border-radius: 4px;
                }}
            """)
            progress_layout.addWidget(pbar)
            self.table.setCellWidget(row_idx, 4, progress_container)

        table_layout.addWidget(self.table)
        content_layout.addWidget(table_frame, stretch=62)

        matrix_frame = QFrame()
        matrix_frame.setStyleSheet("background-color: #242A32; border-radius: 14px; border: 1px solid #2D3540;")
        matrix_layout = QVBoxLayout(matrix_frame)
        matrix_layout.setContentsMargins(18, 15, 18, 15)
        matrix_layout.setSpacing(10)

        matrix_title = QLabel("Contract Expiry Matrix")
        matrix_title.setStyleSheet(
            "color: #FFFFFF; font-size: 14px; font-weight: 700; padding-bottom: 5px; border: none;")
        matrix_layout.addWidget(matrix_title)

        expiry_groups = [
            ("Urgent Actions (2026)", "Marcus Perez, Daniel Cannon", "#e74c3c", "border-left: 4px solid #e74c3c;"),
            ("Attention Needed (2027)", "Leonard James, Oliver Sanchez", "#e67e22", "border-left: 4px solid #e67e22;"),
            ("Stable Assets (2028+)", "John Banker, Jude Bellingham", "#2ecc71", "border-left: 4px solid #2ecc71;")
        ]

        for group_title, players_list, color, border_style in expiry_groups:
            group_box = QFrame()
            group_box.setStyleSheet(f"""
                QFrame {{
                    background-color: #1C2127;
                    border-radius: 6px;
                    padding: 10px 12px;
                    {border_style}
                }}
            """)
            box_layout = QVBoxLayout(group_box)
            box_layout.setContentsMargins(10, 8, 10, 8)
            box_layout.setSpacing(4)

            gt = QLabel(group_title)
            gt.setStyleSheet(
                f"color: {color}; font-size: 11px; font-weight: 700; text-transform: uppercase; border: none;")

            gl = QLabel(players_list)
            gl.setStyleSheet("color: #FFFFFF; font-size: 12px; font-weight: 500; border: none;")
            gl.setWordWrap(True)

            box_layout.addWidget(gt)
            box_layout.addWidget(gl)
            matrix_layout.addWidget(group_box)

        matrix_layout.addStretch()
        content_layout.addWidget(matrix_frame, stretch=38)

        main_layout.addLayout(content_layout, stretch=80)