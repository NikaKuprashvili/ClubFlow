import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QTableWidget, QTableWidgetItem, \
    QHeaderView, QComboBox, QPushButton, QProxyStyle, QStyle
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class CleanPopupStyle(QProxyStyle):
    def styleHint(self, hint: QStyle.StyleHint, *args, **kwargs):
        if hint == QStyle.StyleHint.SH_ComboBox_Popup:
            return 0
        return super().styleHint(hint, *args, **kwargs)


class ScoutingPage(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(20)

        header_layout = QHBoxLayout()
        title_label = QLabel("REAL MADRID C.F.  |  ADVANCED SCOUTING MARKET")
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

        control_frame = QFrame()
        control_frame.setStyleSheet("background-color: #242A32; border-radius: 12px; border: 1px solid #2D3540;")
        control_layout = QHBoxLayout(control_frame)
        control_layout.setContentsMargins(20, 15, 20, 15)
        control_layout.setSpacing(15)

        selector_label = QLabel("Select Target Elite Player:")
        selector_label.setStyleSheet(
            "color: #8F9CAE; font-size: 13px; font-weight: 700; text-transform: uppercase; border: none;")

        self.player_selector = QComboBox()
        self.combo_style = CleanPopupStyle()
        self.player_selector.setStyle(self.combo_style)

        self.player_selector.addItems(["Kylian Mbappé", "Erling Haaland", "Kevin De Bruyne", "Jude Bellingham"])

        self.player_selector.setStyleSheet("""
            QComboBox {
                background-color: #1C2127;
                color: #FFFFFF;
                border: 1px solid #2D3540;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                font-weight: 600;
                min-width: 200px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background-color: #1C2127;
                color: #FFFFFF;
                selection-background-color: #2D3540;
                border: 1px solid #2D3540;
                padding: 4px;
                show-decoration-selected: 1;
            }
        """)

        search_btn = QPushButton("Run Similarity Search")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: #FFFFFF;
                font-weight: 700;
                font-size: 12px;
                text-transform: uppercase;
                border: none;
                border-radius: 6px;
                padding: 9px 20px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        search_btn.clicked.connect(self.calculate_similarity)

        control_layout.addWidget(selector_label)
        control_layout.addWidget(self.player_selector)
        control_layout.addStretch()
        control_layout.addWidget(search_btn)
        main_layout.addWidget(control_frame)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        table_frame = QFrame()
        table_frame.setStyleSheet("background-color: #242A32; border-radius: 14px; border: 1px solid #2D3540;")
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(18, 15, 18, 15)

        table_title = QLabel("Statistical Underpriced Match")
        table_title.setStyleSheet(
            "color: #FFFFFF; font-size: 14px; font-weight: 700; padding-bottom: 5px; border: none;")
        table_layout.addWidget(table_title)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Alternative Option", "Age", "Market Value", "Est. Wage", "Match Index"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setShowGrid(False)
        self.table.setCornerButtonEnabled(False)
        self.table.setMinimumWidth(460)

        v_header = self.table.verticalHeader()
        if v_header:
            v_header.setVisible(False)

        self.table.setStyleSheet("""
            QTableWidget { 
                background: transparent; 
                border: none; 
            } 
            QTableWidget::item { 
                color: #FFFFFF; 
                font-size: 12px; 
                border-bottom: 1px solid #2D3540; 
                padding: 12px 10px; 
            } 
            QTableWidget::item:selected { 
                background-color: #1C2127; 
                color: #FFFFFF; 
            }
            QHeaderView { 
                background: transparent; 
            }
            QHeaderView::section { 
                background: transparent; 
                color: #8F9CAE; 
                font-size: 11px; 
                font-weight: 700; 
                border: none; 
                border-bottom: 2px solid #2D3540; 
                padding-top: 5px;
                padding-bottom: 8px;
                padding-left: 10px;
                padding-right: 10px;
            }
            QTableWidget QTableCornerButton::section { 
                background: transparent; 
                border: none; 
            }
            QScrollBar:horizontal {
                border: none;
                background-color: #1C2127;
                height: 8px;
                margin: 0px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background-color: #4E5D6C;
                min-width: 30px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #3498db;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
            }
        """)

        header = self.table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
            header.setStretchLastSection(True)

            header.resizeSection(0, 150)
            header.resizeSection(1, 55)
            header.resizeSection(2, 95)
            header.resizeSection(3, 95)
            header.resizeSection(4, 90)

            header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

            assert header is not None
            header_model = header.model()

            if header_model is not None:
                assert header_model is not None
                header_model.setHeaderData(
                    0,
                    Qt.Orientation.Horizontal,
                    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                    Qt.ItemDataRole.TextAlignmentRole
                )

        table_layout.addWidget(self.table)
        content_layout.addWidget(table_frame, stretch=56)

        radar_frame = QFrame()
        radar_frame.setStyleSheet("background-color: #242A32; border-radius: 14px; border: 1px solid #2D3540;")
        radar_layout = QVBoxLayout(radar_frame)
        radar_layout.setContentsMargins(10, 15, 10, 10)

        radar_title = QLabel("Profile Radar Comparison Overlap")
        radar_title.setStyleSheet(
            "color: #FFFFFF; font-size: 14px; font-weight: 700; padding-bottom: 5px; border: none; padding-left: 10px;")
        radar_layout.addWidget(radar_title)

        self.fig = Figure(figsize=(4.5, 4.8), facecolor='#242A32')
        self.canvas = FigureCanvas(self.fig)
        radar_layout.addWidget(self.canvas)
        content_layout.addWidget(radar_frame, stretch=44)

        main_layout.addLayout(content_layout, stretch=85)

        self.mock_database = {
            "Kylian Mbappé": [
                ("Jonathan David", "24", "€45.0M", "€90K/wk", "94.2%", [92, 88, 74, 85, 40, 55]),
                ("Loïs Openda", "24", "€55.0M", "€100K/wk", "91.8%", [90, 84, 68, 80, 45, 50]),
                ("Amine Gouiri", "26", "€28.0M", "€65K/wk", "86.5%", [84, 78, 80, 82, 38, 62])
            ],
            "Erling Haaland": [
                ("Benjamin Šeško", "22", "€40.0M", "€75K/wk", "95.1%", [85, 94, 60, 70, 42, 68]),
                ("Viktor Gyökeres", "27", "€65.0M", "€110K/wk", "93.4%", [88, 91, 72, 78, 55, 75]),
                ("Santiago Giménez", "25", "€35.0M", "€60K/wk", "88.7%", [80, 87, 64, 68, 35, 60])
            ],
            "Kevin De Bruyne": [
                ("Florian Wirtz", "23", "€110.0M", "€140K/wk", "96.4%", [78, 76, 95, 92, 58, 65]),
                ("Xavi Simons", "23", "€80.0M", "€120K/wk", "92.1%", [84, 72, 89, 88, 62, 58]),
                ("Lovro Majer", "28", "€22.0M", "€55K/wk", "85.3%", [70, 68, 85, 82, 50, 60])
            ],
            "Jude Bellingham": [
                ("João Neves", "21", "€55.0M", "€70K/wk", "93.8%", [76, 72, 86, 84, 85, 82]),
                ("Warren Zaïre-Emery", "20", "€60.0M", "€80K/wk", "91.2%", [78, 74, 84, 82, 80, 85]),
                ("Orkun Kökçü", "25", "€30.0M", "€65K/wk", "87.4%", [72, 75, 88, 85, 68, 74])
            ]
        }

        self.table.itemSelectionChanged.connect(self.update_radar_chart)
        self.calculate_similarity()

    def calculate_similarity(self):
        target = self.player_selector.currentText()
        alternatives = self.mock_database[target]

        self.table.blockSignals(True)
        self.table.setRowCount(len(alternatives))
        for i, (name, age, val, wage, idx, stats) in enumerate(alternatives):
            n_i = QTableWidgetItem(name)
            self.table.setItem(i, 0, n_i)

            a_i = QTableWidgetItem(age)
            a_i.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 1, a_i)

            v_i = QTableWidgetItem(val)
            v_i.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            v_i.setForeground(QColor("#2ecc71"))
            self.table.setItem(i, 2, v_i)

            w_i = QTableWidgetItem(wage)
            w_i.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 3, w_i)

            id_i = QTableWidgetItem(idx)
            id_i.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            id_i.setForeground(QColor("#3498db"))
            current_font = id_i.font()
            current_font.setBold(True)
            id_i.setFont(current_font)
            self.table.setItem(i, 4, id_i)

        self.table.blockSignals(False)
        self.table.selectRow(0)
        self.update_radar_chart()

    def update_radar_chart(self):
        self.fig.clear()

        target = self.player_selector.currentText()
        selected_row = self.table.currentRow()
        if selected_row < 0:
            selected_row = 0

        table_item = self.table.item(selected_row, 0)
        if table_item is None:
            return

        alt_name = table_item.text()
        alt_stats = list(self.mock_database[target][selected_row][5])

        target_profiles = {
            "Kylian Mbappé": [97, 92, 80, 89, 35, 60],
            "Erling Haaland": [82, 96, 65, 72, 38, 76],
            "Kevin De Bruyne": [74, 82, 97, 95, 60, 70],
            "Jude Bellingham": [82, 80, 88, 86, 84, 88]
        }
        target_stats = list(target_profiles[target])

        categories = ['Pace', 'Finishing', 'Passing', 'Dribbling', 'Defending', 'Physical']
        n_categories = len(categories)

        angles = [n / float(n_categories) * 2 * np.pi for n in range(n_categories)]
        angles += angles[:1]

        target_stats += target_stats[:1]
        alt_stats += alt_stats[:1]

        ax = self.fig.add_subplot(111, polar=True)
        ax.set_facecolor('#242A32')

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, color='#8F9CAE', size=9)

        for label, angle in zip(ax.get_xticklabels(), angles[:-1]):
            if angle == 0 or angle == np.pi:
                label.set_horizontalalignment('center')
            elif 0 < angle < np.pi:
                label.set_horizontalalignment('left')
            else:
                label.set_horizontalalignment('right')

        ax.tick_params(colors='#4E5D6C', pad=10)
        ax.grid(color='#2D3540', linestyle='-', linewidth=0.8)

        ax.plot(angles, target_stats, linewidth=1.8, linestyle='solid', color='#e74c3c', label=target)
        ax.fill(angles, target_stats, color='#e74c3c', alpha=0.12)

        ax.plot(angles, alt_stats, linewidth=1.8, linestyle='solid', color='#3498db', label=alt_name)
        ax.fill(angles, alt_stats, color='#3498db', alpha=0.22)

        ax.set_ylim(0, 100)
        ax.set_yticklabels([])

        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), facecolor='#1C2127', edgecolor='#2D3540',
                  labelcolor='#FFFFFF', fontsize=9, ncol=2)

        self.fig.tight_layout()
        self.canvas.draw()