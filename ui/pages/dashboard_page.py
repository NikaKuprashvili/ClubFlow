from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        title_label = QLabel("კლუბის ანალიტიკური პანელი (Dashboard)")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF;")
        main_layout.addWidget(title_label)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        kpi_data = [
            ("ხელმისაწვდომი ბიუჯეტი", "€ 10,000,000", "#2ecc71"),
            ("გუნდის საშუალო რეიტინგი", "78.4 / 100", "#3498db"),
            ("აქტიური ტრანსფერები", "4 მოთამაშე", "#e67e22")
        ]

        for title, value, color in kpi_data:
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
            c_value.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {color}; margin-top: 5px;")

            card_layout.addWidget(c_title)
            card_layout.addWidget(c_value)
            cards_layout.addWidget(card)

        main_layout.addLayout(cards_layout)

        chart_frame = QFrame()
        chart_frame.setStyleSheet("""
            QFrame {
                background-color: #2A2A2A;
                border-radius: 12px;
                border: 2px dashed #444444;
            }
        """)
        chart_layout = QVBoxLayout(chart_frame)

        chart_placeholder_text = QLabel("აქ განთავსდება გუნდის პროგრესის დინამიური გრაფიკი (Matplotlib Chart)")
        chart_placeholder_text.setStyleSheet("color: #888888; font-size: 14px; font-style: italic;")

        chart_placeholder_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        chart_layout.addWidget(chart_placeholder_text)

        main_layout.addWidget(chart_frame)

        main_layout.setStretch(1, 1)
        main_layout.setStretch(2, 4)