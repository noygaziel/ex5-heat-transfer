import numpy as np

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget

CONFETTI_COLORS = ["#ef4444", "#f59e0b", "#facc15", "#22c55e", "#3b82f6", "#a855f7"]
PIECES = 150
TICK_MS = 30          # time between frames [ms]
DURATION_MS = 3500    # how long the confetti falls [ms]


class ConfettiWidget(QWidget):
    """Transparent layer on top of the main window that shows falling confetti."""

    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)   # clicks go through to the window
        self.hide()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_pieces)
        self.elapsed = 0

        # one value per piece (numpy arrays)
        self.x = np.zeros(PIECES)
        self.y = np.zeros(PIECES)
        self.speed = np.zeros(PIECES)
        self.drift = np.zeros(PIECES)
        self.piece_size = np.zeros(PIECES)
        self.angle = np.zeros(PIECES)
        self.spin = np.zeros(PIECES)
        self.colors = []

    def start(self):
        # cover the whole parent window
        self.resize(self.parent().size())
        width = self.width()
        height = self.height()

        # random start values for every piece
        self.x = np.random.uniform(0, width, PIECES)
        self.y = np.random.uniform(-height, 0, PIECES)       # start above the top edge
        self.speed = np.random.uniform(3, 8, PIECES)          # falling speed [px/tick]
        self.drift = np.random.uniform(-1.5, 1.5, PIECES)     # small sideways movement
        self.piece_size = np.random.uniform(6, 12, PIECES)
        self.angle = np.random.uniform(0, 360, PIECES)
        self.spin = np.random.uniform(-10, 10, PIECES)        # rotation per tick [deg]
        self.colors = [QColor(np.random.choice(CONFETTI_COLORS)) for _ in range(PIECES)]

        self.elapsed = 0
        self.raise_()
        self.show()
        self.timer.start(TICK_MS)

    def move_pieces(self):
        self.y += self.speed
        self.x += self.drift
        self.angle += self.spin
        self.elapsed += TICK_MS
        if self.elapsed >= DURATION_MS:
            self.timer.stop()
            self.hide()
        self.update()       # redraw (calls paintEvent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        for i in range(PIECES):
            painter.save()
            painter.translate(self.x[i], self.y[i])
            painter.rotate(self.angle[i])
            painter.setBrush(self.colors[i])
            # a small rectangle, a bit longer than it is wide
            painter.drawRect(int(-self.piece_size[i] / 2), int(-self.piece_size[i] / 4),
                             int(self.piece_size[i]), int(self.piece_size[i] / 2))
            painter.restore()
        painter.end()
