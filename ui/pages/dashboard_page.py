from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QTableWidget, QTableWidgetItem, \
    QHeaderView
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from services.player_service import PlayerService

import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.player_service = PlayerService()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(20)

        header_layout = QHBoxLayout()
        club_title = QLabel("REAL MADRID C.F.  |  EXECUTIVE ANALYTICS")
        club_title.setStyleSheet("font-size: 22px; font-weight: 800; color: #FFFFFF; letter-spacing: 1px;")

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

        header_layout.addWidget(club_title)
        header_layout.addStretch()
        header_layout.addWidget(profile_container)
        main_layout.addLayout(header_layout)

        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(15)
        kpis = [
            ("Club Health Index", "94 / 100", "#2ecc71", "📈"),
            ("Financial Status", "Stable / Surplus", "#3498db", "💰"),
            ("Annual Wage Cap", "€285.5M / €310M", "#9b59b6", "📊"),
            ("Market Asset Value", "€842.1M", "#f1c40f", "💎")
        ]

        for title, value, color, icon in kpis:
            card = QFrame()
            card.setStyleSheet("""
                QFrame { 
                    background-color: #242A32; 
                    border-radius: 12px; 
                    border: 1px solid #2D3540; 
                }
            """)
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
            kpi_layout.addWidget(card)
        main_layout.addLayout(kpi_layout)

        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)

        perf_frame = QFrame()
        perf_frame.setStyleSheet("background-color: #242A32; border-radius: 14px; border: 1px solid #2D3540;")
        perf_layout = QVBoxLayout(perf_frame)
        perf_layout.setContentsMargins(15, 15, 15, 15)
        perf_title = QLabel("Performance vs. Wage Correlation")
        perf_title.setStyleSheet(
            "color: #FFFFFF; font-size: 14px; font-weight: 700; padding-bottom: 5px; border: none;")
        perf_layout.addWidget(perf_title)

        fig_perf = Figure(figsize=(5, 3.2), facecolor='#242A32')
        canvas_perf = FigureCanvas(fig_perf)
        ax_perf = fig_perf.add_subplot(111)
        ax_perf.set_facecolor('#242A32')

        players = self.player_service.get_all_players()
        p_names = [p["name"].split()[0] for p in players[:6]]
        p_ratings = [p["rating"] for p in players[:6]]

        ax_perf.bar(p_names, p_ratings, color='#3498db', width=0.35, alpha=0.9, edgecolor='#2980b9', linewidth=1)
        ax_perf.tick_params(colors='#8F9CAE', labelsize=8)
        ax_perf.grid(axis='y', linestyle='--', alpha=0.15, color='#8F9CAE')
        ax_perf.set_ylim(0, 105)

        for s in ax_perf.spines.values():
            s.set_visible(False)

        fig_perf.tight_layout()
        perf_layout.addWidget(canvas_perf)
        charts_layout.addWidget(perf_frame, stretch=50)

        age_frame = QFrame()
        age_frame.setStyleSheet("background-color: #242A32; border-radius: 14px; border: 1px solid #2D3540;")
        age_layout = QVBoxLayout(age_frame)
        age_layout.setContentsMargins(15, 15, 15, 15)
        age_title = QLabel("Squad Balance: Age Structure")
        age_title.setStyleSheet("color: #FFFFFF; font-size: 14px; font-weight: 700; padding-bottom: 5px; border: none;")
        age_layout.addWidget(age_title)

        fig_age = Figure(figsize=(5, 3.2), facecolor='#242A32')
        canvas_age = FigureCanvas(fig_age)
        ax_age = fig_age.add_subplot(111)
        ax_age.set_facecolor('#242A32')

        age_labels = ['18-22', '23-28', '29-32', '33+']
        age_counts = [5, 12, 6, 3]

        ax_age.bar(age_labels, age_counts, color='#2ecc71', width=0.45, alpha=0.9, edgecolor='#27ae60', linewidth=1)
        ax_age.tick_params(colors='#8F9CAE', labelsize=8)
        ax_age.grid(axis='y', linestyle='--', alpha=0.15, color='#8F9CAE')
        ax_age.set_ylim(0, 15)

        for s in ax_age.spines.values():
            s.set_visible(False)

        fig_age.tight_layout()
        age_layout.addWidget(canvas_age)
        charts_layout.addWidget(age_frame, stretch=50)
        main_layout.addLayout(charts_layout, stretch=45)

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        deficit_frame = QFrame()
        deficit_frame.setStyleSheet("background-color: #242A32; border-radius: 14px; border: 1px solid #2D3540;")
        deficit_layout = QVBoxLayout(deficit_frame)
        deficit_layout.setContentsMargins(18, 15, 18, 15)
        dt = QLabel("Positional Deficit Analysis")
        dt.setStyleSheet("color: #FFFFFF; font-size: 14px; font-weight: 700; padding-bottom: 5px; border: none;")
        deficit_layout.addWidget(dt)

        deficit_table = QTableWidget(4, 3)
        deficit_table.setHorizontalHeaderLabels(["Position", "Status", "Deficit / Surplus"])
        deficit_table.setShowGrid(False)
        deficit_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        v_header = deficit_table.verticalHeader()
        if v_header is not None:
            v_header.setVisible(False)

        deficit_table.setStyleSheet("""
            QTableWidget { background: transparent; border: none; } 
            QTableWidget::item { color: #FFFFFF; font-size: 12px; border-bottom: 1px solid #2D3540; padding: 8px; } 
            QHeaderView::section { background: transparent; color: #8F9CAE; font-size: 11px; font-weight: 700; border: none; border-bottom: 2px solid #2D3540; padding-bottom: 5px; }
        """)

        h_header = deficit_table.horizontalHeader()
        if h_header is not None:
            h_header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
            h_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        def_data = [
            ("Left Back (LB)", "Critical", "-12.5%"),
            ("Striker (ST)", "Optimal", "+5.2%"),
            ("Center Mid (CM)", "Surplus", "+18.0%"),
            ("Goalkeeper (GK)", "Stable", "0.0%")
        ]

        for i, (pos, stat, val) in enumerate(def_data):
            p_i = QTableWidgetItem(pos)
            p_i.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            deficit_table.setItem(i, 0, p_i)

            s_i = QTableWidgetItem(stat)
            s_i.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if stat == "Critical":
                s_i.setForeground(QColor("#e74c3c"))
            elif stat == "Optimal":
                s_i.setForeground(QColor("#2ecc71"))
            elif stat == "Surplus":
                s_i.setForeground(QColor("#3498db"))
            else:
                s_i.setForeground(QColor("#95a5a6"))
            deficit_table.setItem(i, 1, s_i)

            v_i = QTableWidgetItem(val)
            v_i.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if val.startswith("-"):
                v_i.setForeground(QColor("#e74c3c"))
            elif val.startswith("+"):
                v_i.setForeground(QColor("#2ecc71"))
            deficit_table.setItem(i, 2, v_i)

        deficit_layout.addWidget(deficit_table)
        bottom_layout.addWidget(deficit_frame, stretch=53)

        alerts_frame = QFrame()
        alerts_frame.setStyleSheet("background-color: #242A32; border-radius: 14px; border: 1px solid #2D3540;")
        alerts_layout = QVBoxLayout(alerts_frame)
        alerts_layout.setContentsMargins(18, 15, 18, 15)
        at = QLabel("System Smart Alerts")
        at.setStyleSheet("color: #FFFFFF; font-size: 14px; font-weight: 700; padding-bottom: 5px; border: none;")
        alerts_layout.addWidget(at)

        alerts = [
            ("⚠️ LB rating is 12% lower than league average.", "#e67e22", "border-left: 4px solid #e67e22;"),
            ("✅ Financial Fair Play (FFP) status: Compliant.", "#2ecc71", "border-left: 4px solid #2ecc71;"),
            ("🔔 3 key players entering final year of contract.", "#3498db", "border-left: 4px solid #3498db;"),
            ("⚠️ Wage-to-Revenue ratio approaching 70% limit.", "#e74c3c", "border-left: 4px solid #e74c3c;")
        ]

        for text, color, border_style in alerts:
            al = QLabel(text)
            al.setStyleSheet(f"""
                color: {color}; 
                font-size: 12px; 
                font-weight: 500;
                background-color: #1C2127; 
                padding: 10px 12px; 
                border-radius: 6px; 
                margin-bottom: 4px;
                {border_style}
            """)
            al.setWordWrap(True)
            alerts_layout.addWidget(al)

        alerts_layout.addStretch()
        bottom_layout.addWidget(alerts_frame, stretch=47)

        main_layout.addLayout(bottom_layout, stretch=35)