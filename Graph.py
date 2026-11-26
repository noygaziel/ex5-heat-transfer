from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox, QFileDialog, QMessageBox,
)
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

        # connect the buttons
        self.draw_button.clicked.connect(self.draw_graph)
        self.clear_button.clicked.connect(self.clear_graph)
        self.export_button.clicked.connect(self.export_csv)

    def setup_axes(self):
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.grid(True, alpha=0.3)
        self.figure.tight_layout()
        self.canvas.draw()

    def draw_graph(self):
        # add the selected body's temperature to the graph (does not clear what is already drawn)
        times = self.main_window.time_history
        if len(times) == 0:
            QMessageBox.information(self, "No data", "Run a simulation first (press Start).")
            return
        if self.body_combo.currentText() == "Body 1":
            temps = self.main_window.body1_temp_history
            color = "#dc2626"
        else:
            temps = self.main_window.body2_temp_history
            color = "#2563eb"
        self.ax.plot(times, temps, color=color, linewidth=2, label=self.body_combo.currentText())
        self.ax.set_title("Temperature vs. Time")
        self.ax.legend()
        self.figure.tight_layout()
        self.canvas.draw()

    def clear_graph(self):
        self.ax.clear()
        self.setup_axes()

    def export_csv(self):
        # save all the experiment data: time, temperature 1, temperature 2
        times = self.main_window.time_history
        if len(times) == 0:
            QMessageBox.information(self, "No data", "Run a simulation first (press Start).")
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "heat_transfer.csv", "CSV files (*.csv)")
        if not file_path:
            return
        with open(file_path, "w") as f:
            f.write("Time (s),Temperature 1 (C),Temperature 2 (C)\n")
            for i in range(len(times)):
                f.write(f"{times[i]:.2f},{self.main_window.body1_temp_history[i]:.3f},"
                        f"{self.main_window.body2_temp_history[i]:.3f}\n")
        # open the file in Excel (the default program for .csv)
        QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
