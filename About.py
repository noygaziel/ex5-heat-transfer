import os
import webbrowser

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout

GITHUB_URL = "https://github.com/noygaziel/ex5-heat-transfer"
IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "about_image.png")


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setFixedSize(400, 440)
        self.setStyleSheet("""
            QWidget { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                         stop:0 #0f172a, stop:1 #1e293b);
                      color: #e2e8f0; font-family: "Segoe UI"; font-size: 13px; }
            QLabel { background: transparent; }
            QLabel#name { font-size: 22px; font-weight: 700; color: #ffffff; }
            QLabel#subtitle { color: #fb923c; font-weight: 600; }
            QPushButton { background-color: #ea580c; border: none; border-radius: 6px;
                          padding: 8px; color: white; font-weight: 600; }
            QPushButton:hover { background-color: #c2410c; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(8)

        # image
        image = QLabel()
        image.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(IMAGE_PATH)
        if not pixmap.isNull():
            image.setPixmap(pixmap.scaledToWidth(350, Qt.SmoothTransformation))
        layout.addWidget(image)

        name = QLabel("Noy Gaziel")
        name.setObjectName("name")
        layout.addWidget(name)

        subtitle = QLabel("Heat Transfer – Exercise 5")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)

        layout.addWidget(QLabel("Mechanical Engineering student, Afeka"))
        layout.addWidget(QLabel("Programming for Mechatronics"))

        link = QLabel(f'<a href="{GITHUB_URL}" style="color:#67e8f9;">GitHub repository</a>')
        link.setOpenExternalLinks(True)
        layout.addWidget(link)
        layout.addStretch()

        btn_github = QPushButton("Open GitHub")
        btn_github.setCursor(Qt.PointingHandCursor)
        btn_github.clicked.connect(self.open_github)
        layout.addWidget(btn_github)

    def open_github(self):
        webbrowser.open(GITHUB_URL)
