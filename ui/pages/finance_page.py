import os
import re
from datetime import datetime
import numpy as np
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout,
                             QFrame, QPushButton, QLineEdit, QSpinBox,
                             QComboBox, QTextEdit, QGridLayout, QMessageBox)
import matplotlib

matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


class FinancialSimulatorPage(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(20)

        header_layout = QHBoxLayout()
        title_label = QLabel("REAL MADRID C.F.  |  FINANCIAL SIMULATOR & FFP")
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

        sandbox_frame = QFrame()
        sandbox_frame.setStyleSheet("background-color: #242A32; border-radius: 12px; border: 1px solid #2D3540;")
        sandbox_layout = QHBoxLayout(sandbox_frame)
        sandbox_layout.setContentsMargins(20, 20, 20, 20)
        sandbox_layout.setSpacing(15)

        input_style = """
            QLineEdit, QSpinBox, QComboBox {
                background-color: #1C2127;
                color: #FFFFFF;
                border: 1px solid #2D3540;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                font-weight: 600;
            }
            QSpinBox::up-button, QSpinBox::down-button { width: 0px; } 
        """

        self.player_input = QLineEdit("Kylian Mbappe")
        self.player_input.setStyleSheet(input_style)
        self.player_input.setPlaceholderText("Target Player")

        fee_label = QLabel("Fee (€M):")
        fee_label.setStyleSheet("color: #8F9CAE; font-weight: 700; font-size: 12px;")
        self.fee_input = QSpinBox()
        self.fee_input.setRange(0, 300)
        self.fee_input.setValue(150)
        self.fee_input.setStyleSheet(input_style)

        wage_label = QLabel("Wage (€K/wk):")
        wage_label.setStyleSheet("color: #8F9CAE; font-weight: 700; font-size: 12px;")
        self.wage_input = QSpinBox()
        self.wage_input.setRange(0, 2000)
        self.wage_input.setValue(350)
        self.wage_input.setSingleStep(10)
        self.wage_input.setStyleSheet(input_style)

        contract_label = QLabel("Contract (Yrs):")
        contract_label.setStyleSheet("color: #8F9CAE; font-weight: 700; font-size: 12px;")
        self.contract_input = QComboBox()
        self.contract_input.addItems(["1", "2", "3", "4", "5", "6"])
        self.contract_input.setCurrentText("5")
        self.contract_input.setStyleSheet(input_style)

        simulate_btn = QPushButton("Run Simulation")
        simulate_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: #FFFFFF;
                font-weight: 700;
                font-size: 12px;
                text-transform: uppercase;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        simulate_btn.clicked.connect(self.run_simulation)

        sandbox_layout.addWidget(self.player_input, stretch=2)
        sandbox_layout.addWidget(fee_label)
        sandbox_layout.addWidget(self.fee_input, stretch=1)
        sandbox_layout.addWidget(wage_label)
        sandbox_layout.addWidget(self.wage_input, stretch=1)
        sandbox_layout.addWidget(contract_label)
        sandbox_layout.addWidget(self.contract_input, stretch=1)
        sandbox_layout.addWidget(simulate_btn)

        main_layout.addWidget(sandbox_frame)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        left_col_layout = QVBoxLayout()
        left_col_layout.setSpacing(20)

        metrics_frame = QFrame()
        metrics_frame.setStyleSheet("background-color: transparent;")
        metrics_layout = QGridLayout(metrics_frame)
        metrics_layout.setContentsMargins(0, 0, 0, 0)
        metrics_layout.setSpacing(15)

        self.card_total = self.create_metric_card("Total Financial Commitment", "€0.0M", "#3498db")
        self.card_amort = self.create_metric_card("Annual Amortization Impact", "€0.0M", "#e67e22")
        self.card_wage = self.create_metric_card("Annual Salary Impact", "€0.0M", "#9b59b6")
        self.card_ffp = self.create_metric_card("FFP Compliance Risk", "SAFE", "#2ecc71")

        metrics_layout.addWidget(self.card_total['frame'], 0, 0)
        metrics_layout.addWidget(self.card_amort['frame'], 0, 1)
        metrics_layout.addWidget(self.card_wage['frame'], 1, 0)
        metrics_layout.addWidget(self.card_ffp['frame'], 1, 1)

        left_col_layout.addWidget(metrics_frame)

        summary_frame = QFrame()
        summary_frame.setStyleSheet("background-color: #242A32; border-radius: 14px; border: 1px solid #2D3540;")
        summary_layout = QVBoxLayout(summary_frame)
        summary_layout.setContentsMargins(20, 20, 20, 20)

        summary_title = QLabel("Automated Executive Summary")
        summary_title.setStyleSheet("color: #FFFFFF; font-size: 14px; font-weight: 700; border: none;")

        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setStyleSheet("""
            QTextEdit {
                background-color: #1C2127;
                color: #8F9CAE;
                border: 1px solid #2D3540;
                border-radius: 8px;
                padding: 12px;
                font-size: 13px;
                line-height: 1.5;
            }
        """)

        export_btn = QPushButton("📄 Generate PDF Report")
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #2D3540;
                color: #FFFFFF;
                font-weight: 700;
                font-size: 12px;
                border: 1px solid #4E5D6C;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton:hover { background-color: #3498db; border: 1px solid #3498db; }
        """)
        export_btn.clicked.connect(self.export_pdf_mock)

        summary_layout.addWidget(summary_title)
        summary_layout.addSpacing(10)
        summary_layout.addWidget(self.summary_text)
        summary_layout.addSpacing(10)
        summary_layout.addWidget(export_btn)

        left_col_layout.addWidget(summary_frame, stretch=1)
        content_layout.addLayout(left_col_layout, stretch=50)

        chart_frame = QFrame()
        chart_frame.setStyleSheet("background-color: #242A32; border-radius: 14px; border: 1px solid #2D3540;")
        chart_layout = QVBoxLayout(chart_frame)
        chart_layout.setContentsMargins(15, 20, 15, 15)

        chart_title = QLabel("3-Year FFP Expenditure Projection")
        chart_title.setStyleSheet(
            "color: #FFFFFF; font-size: 14px; font-weight: 700; border: none; padding-left: 10px;")
        chart_layout.addWidget(chart_title)

        self.fig = Figure(figsize=(5, 4.5), facecolor='#242A32')
        self.canvas = FigureCanvas(self.fig)
        chart_layout.addWidget(self.canvas)

        content_layout.addWidget(chart_frame, stretch=50)
        main_layout.addLayout(content_layout, stretch=1)

        self.run_simulation()

    @staticmethod
    def create_metric_card(title: str, value: str, color: str) -> dict:
        frame = QFrame()
        frame.setStyleSheet(
            f"background-color: #242A32; border-radius: 12px; border-left: 4px solid {color}; border-top: 1px solid #2D3540; border-right: 1px solid #2D3540; border-bottom: 1px solid #2D3540;")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(
            "color: #8F9CAE; font-size: 11px; font-weight: 700; text-transform: uppercase; border: none;")

        value_lbl = QLabel(value)
        value_lbl.setStyleSheet("color: #FFFFFF; font-size: 20px; font-weight: 800; border: none;")

        layout.addWidget(title_lbl)
        layout.addWidget(value_lbl)
        layout.addStretch()

        return {'frame': frame, 'value_label': value_lbl}

    @staticmethod
    def _calculate_metrics(fee_m: float, wage_k: float, years: int) -> dict:
        annual_wage_m = (wage_k * 52) / 1000.0
        annual_amort_m = fee_m / years
        annual_impact_m = annual_wage_m + annual_amort_m
        total_commitment_m = fee_m + (annual_wage_m * years)
        current_expenditure = 450.0
        ffp_limit = 500.0
        projected_total = current_expenditure + annual_impact_m

        return {
            "wage_m": annual_wage_m,
            "amort_m": annual_amort_m,
            "impact_m": annual_impact_m,
            "total_m": total_commitment_m,
            "curr_exp": current_expenditure,
            "ffp_limit": ffp_limit,
            "proj_total": projected_total
        }

    def run_simulation(self):
        player = self.player_input.text() or "Unknown Player"
        years = int(self.contract_input.currentText())

        m = self._calculate_metrics(self.fee_input.value(), self.wage_input.value(), years)

        self.card_total['value_label'].setText(f"€{m['total_m']:.1f}M")
        self.card_amort['value_label'].setText(f"€{m['amort_m']:.1f}M")
        self.card_wage['value_label'].setText(f"€{m['wage_m']:.1f}M")

        if m['proj_total'] > m['ffp_limit']:
            status, color = "HIGH RISK", "#e74c3c"
        else:
            buffer = m['ffp_limit'] - m['proj_total']
            status = "SAFE" if buffer > 20 else "WARNING"
            color = "#2ecc71" if status == "SAFE" else "#f1c40f"

        self.card_ffp['value_label'].setText(status)
        self.card_ffp['value_label'].setStyleSheet(f"color: {color}; font-size: 20px; font-weight: 800; border: none;")

        base_style = "background-color: #242A32; border-radius: 12px; border-top: 1px solid #2D3540; border-right: 1px solid #2D3540; border-bottom: 1px solid #2D3540;"
        self.card_ffp['frame'].setStyleSheet(f"{base_style} border-left: 4px solid {color};")

        summary = f"""<b>EXECUTIVE TRANSFER SUMMARY: {player.upper()}</b><br><br>
The proposed transfer parameters for <b>{player}</b> result in a total gross financial commitment of <b>€{m['total_m']:.1f}M</b> spread over a {years}-year period.<br><br>
<b>Accounting Impact:</b><br>
• Transfer Amortization: €{m['amort_m']:.1f}M / year<br>
• Salary Expenditure: €{m['wage_m']:.1f}M / year<br>
• Combined Annual Burden: <b>€{m['impact_m']:.1f}M / year</b><br><br>
<b>Strategic FFP Conclusion:</b><br>"""

        if m['proj_total'] > m['ffp_limit']:
            summary += f'<span style="color: #e74c3c;"><b>REJECTED/HIGH RISK.</b></span> The addition pushes the projected annual expenditure to €{m["proj_total"]:.1f}M, breaching the UEFA FFP limit of €{m["ffp_limit"]}M by €{(m["proj_total"] - m["ffp_limit"]):.1f}M. Player sales are required before sanctioning this operation.'
        else:
            summary += f'<span style="color: #2ecc71;"><b>APPROVED.</b></span> The operation keeps the club within FFP parameters. Projected expenditure reaches €{m["proj_total"]:.1f}M, leaving a strategic buffer of €{(m["ffp_limit"] - m["proj_total"]):.1f}M against the €{m["ffp_limit"]}M cap.'

        self.summary_text.setHtml(summary)
        self.update_chart(m['curr_exp'], m['impact_m'], m['ffp_limit'])

    def update_chart(self, base: float, new_impact: float, limit: float):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.set_facecolor('#242A32')

        years = ['2026/27', '2027/28', '2028/29']
        x = np.arange(len(years))
        width = 0.5

        base_exp = np.array([base, base - 15, base - 35])

        ax.bar(x, base_exp, width, label='Current Roster Exp.', color='#4E5D6C', edgecolor='none')
        ax.bar(x, [new_impact] * 3, width, bottom=base_exp, label='New Transfer Impact', color='#3498db',
               edgecolor='none')

        ax.axhline(y=limit, color='#e74c3c', linestyle='--', linewidth=2, label=f'FFP Limit (€{limit}M)')

        ax.set_xticks(x)
        ax.set_xticklabels(years, color='#8F9CAE', fontsize=10, fontweight='bold')
        ax.tick_params(colors='#8F9CAE')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#2D3540')
        ax.spines['bottom'].set_color('#2D3540')

        ax.set_ylabel('Expenditure (€ Millions)', color='#8F9CAE', fontsize=10)
        ax.set_ylim(0, limit + 100)

        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), facecolor='#1C2127', edgecolor='#2D3540',
                  labelcolor='#FFFFFF', fontsize=9, ncol=2)

        self.fig.tight_layout()
        self.canvas.draw()

    def export_pdf_mock(self):
        try:
            player = self.player_input.text() or "Unknown Player"
            fee_m = self.fee_input.value()
            wage_k = self.wage_input.value()
            years = int(self.contract_input.currentText())

            m = self._calculate_metrics(fee_m, wage_k, years)
            is_safe = m['proj_total'] <= m['ffp_limit']

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_player_name = re.sub(r'[^a-zA-Z0-9]', '_', player)
            filename = f"Financial_Report_{safe_player_name}_{timestamp}.pdf"

            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            file_path = os.path.join(desktop_path, filename)

            doc = SimpleDocTemplate(
                file_path, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottom=40
            )

            styles = getSampleStyleSheet()

            title_style = ParagraphStyle(
                'DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold',
                fontSize=22, leading=26, textColor=colors.HexColor('#11161E'), spaceAfter=4
            )

            subtitle_style = ParagraphStyle(
                'DocSubTitle', parent=styles['Normal'], fontName='Helvetica-Bold',
                fontSize=10, leading=12, textColor=colors.HexColor('#7F8C8D'), spaceAfter=25
            )

            section_heading = ParagraphStyle(
                'SectionHeading', parent=styles['Heading2'], fontName='Helvetica-Bold',
                fontSize=13, leading=16, textColor=colors.HexColor('#11161E'), spaceBefore=15, spaceAfter=10
            )

            body_style = ParagraphStyle(
                'BodyTextCustom', parent=styles['Normal'], fontName='Helvetica',
                fontSize=10.5, leading=16, textColor=colors.HexColor('#2C3E50')
            )

            table_text = ParagraphStyle(
                'TableText', parent=styles['Normal'], fontName='Helvetica',
                fontSize=10, leading=12, textColor=colors.HexColor('#2C3E50')
            )

            table_header = ParagraphStyle(
                'TableHeader', parent=styles['Normal'], fontName='Helvetica-Bold',
                fontSize=10, leading=12, textColor=colors.white
            )

            status_style = ParagraphStyle(
                'StatusStyle', parent=styles['Normal'], fontName='Helvetica-Bold',
                fontSize=12, leading=14, textColor=colors.white, alignment=1
            )

            c_bg, c_align, c_valign = 'BACKGROUND', 'ALIGN', 'VALIGN'
            c_grid = 'GRID'
            c_bpad = 'BOTTOM' + 'PADDING'
            c_tpad = 'TOP' + 'PADDING'
            c_lpad = 'LEFT' + 'PADDING'
            c_rpad = 'RIGHT' + 'PADDING'
            c_rowbg = 'ROW' + 'BACKGROUNDS'
            c_flow = 'CLUB' + 'FLOW'

            gen_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            subtitle_txt = f"{c_flow} INTELLIGENCE UNIT &bull; GENERATED: {gen_time}"
            intro_txt = f"This strategic document outlines the structural financial indicators and Financial Fair Play (FFP) compliance vectors regarding the potential acquisition of <b>{player}</b>. The simulation model reviews a definitive contract lifecycle of {years} fiscal years."

            data = [
                [Paragraph("Financial Metric Vector", table_header), Paragraph("Value Impact", table_header)],
                [Paragraph("Initial Capital Investment (Transfer Fee)", table_text),
                 Paragraph(f"&euro;{fee_m:.1f}M", table_text)],
                [Paragraph("Contract Duration Lifecycle", table_text), Paragraph(f"{years} Years", table_text)],
                [Paragraph("Gross Salary Obligation (Weekly)", table_text),
                 Paragraph(f"&euro;{wage_k:.1f}K / wk", table_text)],
                [Paragraph("Annualized Amortization Book-Value", table_text),
                 Paragraph(f"&euro;{m['amort_m']:.1f}M / yr", table_text)],
                [Paragraph("Annualized Gross Wage Expenditure", table_text),
                 Paragraph(f"&euro;{m['wage_m']:.1f}M / yr", table_text)],
                [Paragraph("<b>Combined Annual Fiscal Burden</b>", table_text),
                 Paragraph(f"<b>&euro;{m['impact_m']:.1f}M / yr</b>", table_text)],
                [Paragraph("<b>Total Gross Contractual Commitment</b>", table_text),
                 Paragraph(f"<b>&euro;{m['total_m']:.1f}M</b>", table_text)]
            ]

            t = Table(data, colWidths=[330, 200])
            t.setStyle(TableStyle([
                (c_bg, (0, 0), (-1, 0), colors.HexColor('#11161E')),
                (c_align, (0, 0), (-1, -1), 'LEFT'),
                (c_valign, (0, 0), (-1, -1), 'MIDDLE'),
                (c_bpad, (0, 0), (-1, 0), 8),
                (c_tpad, (0, 0), (-1, 0), 8),
                (c_bg, (0, 1), (-1, -1), colors.HexColor('#F8F9FA')),
                (c_rowbg, (0, 1), (-1, -1), [colors.HexColor('#F8F9FA'), colors.white]),
                (c_grid, (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
                (c_tpad, (0, 1), (-1, -1), 10),
                (c_bpad, (0, 1), (-1, -1), 10),
                (c_lpad, (0, 0), (-1, -1), 12),
                (c_rpad, (0, 0), (-1, -1), 12),
            ]))

            if is_safe:
                conc_txt = f"The operation strictly coordinates with current UEFA financial governance profiles. The integrated framework places the club's projected annual portfolio at &euro;{m['proj_total']:.1f}M, securing a definitive operational headroom buffer of <b>&euro;{(m['ffp_limit'] - m['proj_total']):.1f}M</b> below the maximum expenditure ceiling cap (&euro;{m['ffp_limit']:.1f}M)."
                s_color, s_text = '#2ECC71', 'APPROVED / COMPLIANT'
            else:
                conc_txt = f"CRITICAL OVERSIGHT: The submitted transaction exceeds sustainable regulatory bounds. Processing this framework drives total project expenditure to &euro;{m['proj_total']:.1f}M, directly breaching the UEFA FFP maximum regulatory ceiling cap (&euro;{m['ffp_limit']:.1f}M) by an absolute delta of <b>&euro;{(m['proj_total'] - m['ffp_limit']):.1f}M</b>. Immediate roster amortization offsets or auxiliary player sales are mandatory before sanctioning."
                s_color, s_text = '#E74C3C', 'REJECTED / HIGH RISK'

            status_table = Table([[Paragraph(s_text, status_style)]], colWidths=[530])
            status_table.setStyle(TableStyle([
                (c_bg, (0, 0), (-1, -1), colors.HexColor(s_color)),
                (c_tpad, (0, 0), (-1, -1), 12),
                (c_bpad, (0, 0), (-1, -1), 12),
                (c_align, (0, 0), (-1, -1), 'CENTER'),
                (c_valign, (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            story = [
                Paragraph("REAL MADRID C.F. MANAGEMENT REPORT", title_style),
                Paragraph(subtitle_txt, subtitle_style),
                Paragraph(f"Executive Transfer Summary: {player.upper()}", section_heading),
                Paragraph(intro_txt, body_style),
                Spacer(1, 15),
                t,
                Spacer(1, 20),
                Paragraph("Strategic FFP Compliance Assessment", section_heading),
                Paragraph(conc_txt, body_style),
                Spacer(1, 20),
                status_table
            ]

            doc.build(story)

            QMessageBox.information(self, "Export Successful",
                                    f"The Executive Summary PDF has been generated and saved to your desktop:\n{filename}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Could not generate PDF: {str(e)}")

    def load_player_from_scouting(self, data: dict):
        self.player_input.setText(data.get("name", ""))
        self.fee_input.setValue(data.get("fee", 0))
        self.wage_input.setValue(data.get("wage", 0))
        self.contract_input.setCurrentText(str(data.get("contract", 5)))
        self.run_simulation()