import os
import webbrowser

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QImageReader
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

GITHUB_URL = "https://github.com/noygaziel/ex5-heat-transfer"
FOLDER = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(FOLDER, "about_image.png")
PHOTO_PATH = os.path.join(FOLDER, "me.jpg")
PHOTO_SIZE = 96


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setFixedSize(400, 480)
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

        # profile row: round photo on the left, name and subtitle on the right
        profile_row = QHBoxLayout()
        profile_row.setSpacing(14)

        photo = QLabel()
        photo.setFixedSize(PHOTO_SIZE, PHOTO_SIZE)
        round_photo = self.make_round_photo(PHOTO_PATH, PHOTO_SIZE)
        if round_photo is not None:
            photo.setPixmap(round_photo)
        profile_row.addWidget(photo)

        name_column = QVBoxLayout()
        name_column.addStretch()
        name = QLabel("Noy Gaziel")
        name.setObjectName("name")
        name_column.addWidget(name)
        subtitle = QLabel("Heat Transfer – Exercise 5")
        subtitle.setObjectName("subtitle")
        name_column.addWidget(subtitle)
        name_column.addStretch()
        profile_row.addLayout(name_column, 1)

        layout.addLayout(profile_row)

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

    def make_round_photo(self, path, size):
        # load the photo (auto-rotate according to the camera), crop it to a square
        # in the center and cut it into a circle
        reader = QImageReader(path)
        reader.setAutoTransform(True)
        image = reader.read()
        if image.isNull():
            return None
        square = QPixmap.fromImage(image).scaled(
            size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        x = (square.width() - size) // 2
        y = (square.height() - size) // 2
        square = square.copy(x, y, size, size)

        result = QPixmap(size, size)
        result.fill(Qt.transparent)
        painter = QPainter(result)
        painter.setRenderHint(QPainter.Antialiasing)
        circle = QPainterPath()
        circle.addEllipse(0, 0, size, size)
        painter.setClipPath(circle)
        painter.drawPixmap(0, 0, square)
        painter.end()
        return result

    def open_github(self):
        webbrowser.open(GITHUB_URL)
