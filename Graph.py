from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class GraphWindow(QWidget):

    def __init__(self, main_window):
        super().__init__()

        # access to the main window (its data will be used for drawing)
        self.main_window = main_window

        self.setWindowTitle("Graph Window")
        self.setObjectName("graph_window")
        self.resize(720, 440)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # ===== the graph =====
        self.figure = Figure(figsize=(6, 4))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas, 1)
        self.setup_axes()

        # ===== controls on the right =====
        controls = QVBoxLayout()
        controls.setSpacing(8)

        self.body_combo = QComboBox()
        self.body_combo.addItems(["Body 1", "Body 2"])
        controls.addWidget(self.body_combo)

        self.draw_button = QPushButton("Draw")
        self.draw_button.setCursor(Qt.PointingHandCursor)
        controls.addWidget(self.draw_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setCursor(Qt.PointingHandCursor)
        controls.addWidget(self.clear_button)

        self.export_button = QPushButton("Export to CSV")
        self.export_button.setCursor(Qt.PointingHandCursor)
        controls.addWidget(self.export_button)

        controls.addStretch()
        layout.addLayout(controls)

    def setup_axes(self):
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.grid(True, alpha=0.3)
        self.figure.tight_layout()
        self.canvas.draw()
