import sys
import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QSlider, QDoubleSpinBox, QFrame,
)

from About import AboutWindow
from Graph import GraphWindow


class HeatTransfer(QWidget):

    def __init__(self):
        super().__init__()

        # other windows (created when their button is pressed)
        self.about_window = None
        self.graph_window = None

        self.setWindowTitle("Heat Transfer")
        self.setObjectName("main_window")
        self.resize(760, 460)

        self.setupUI()

    def setupUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(14)

        # ===== title =====
        title = QLabel("Heat Transfer Simulation")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # ===== top row: slider | body 1 | connector | body 2 | slider =====
        bodies_row = QHBoxLayout()
        bodies_row.setSpacing(12)

        # left temperature slider (0-200 °C)
        self.left_slider = QSlider(Qt.Vertical)
        self.left_slider.setRange(0, 200)
        self.left_slider.setValue(200)
        self.left_slider.setFixedHeight(170)
        bodies_row.addWidget(self.left_slider)

        # body 1 – a colored rectangle
        self.left_body = QFrame()
        self.left_body.setObjectName("left_body")
        self.left_body.setFixedSize(130, 170)
        bodies_row.addWidget(self.left_body)

        # middle: conductivity above the connecting bar
        middle_column = QVBoxLayout()
        middle_column.addStretch()
        conductivity_label = QLabel("Conductivity")
        conductivity_label.setAlignment(Qt.AlignCenter)
        middle_column.addWidget(conductivity_label)

        self.conductivity_spin = QDoubleSpinBox()
        self.conductivity_spin.setRange(0.01, 100.0)
        self.conductivity_spin.setValue(1.00)
        self.conductivity_spin.setDecimals(2)
        self.conductivity_spin.setSingleStep(0.1)
        self.conductivity_spin.setSuffix(" J/s°C")
        self.conductivity_spin.setFixedWidth(130)
        middle_column.addWidget(self.conductivity_spin, alignment=Qt.AlignCenter)

        # the bar that connects the two bodies
        self.connector = QFrame()
        self.connector.setObjectName("connector")
        self.connector.setFixedHeight(24)
        middle_column.addWidget(self.connector)
        middle_column.addStretch()
        bodies_row.addLayout(middle_column, 1)

        # body 2
        self.right_body = QFrame()
        self.right_body.setObjectName("right_body")
        self.right_body.setFixedSize(130, 170)
        bodies_row.addWidget(self.right_body)

        # right temperature slider
        self.right_slider = QSlider(Qt.Vertical)
        self.right_slider.setRange(0, 200)
        self.right_slider.setValue(0)
        self.right_slider.setFixedHeight(170)
        bodies_row.addWidget(self.right_slider)

        main_layout.addLayout(bodies_row)

        # ===== bottom row: body 1 data | buttons | body 2 data =====
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)

        # body 1 data (labels on the left of the fields)
        left_grid = QGridLayout()
        left_grid.addWidget(QLabel("Temp."), 0, 0)
        self.left_temp_label = QLabel("200.0 °C")     # read only – changed only by the slider
        self.left_temp_label.setObjectName("temp_display")
        left_grid.addWidget(self.left_temp_label, 0, 1)

        left_grid.addWidget(QLabel("Mass"), 1, 0)
        self.left_mass_spin = self.create_mass_spin()
        left_grid.addWidget(self.left_mass_spin, 1, 1)

        left_grid.addWidget(QLabel("H. Cap."), 2, 0)
        self.left_capacity_spin = self.create_capacity_spin()
        left_grid.addWidget(self.left_capacity_spin, 2, 1)
        bottom_row.addLayout(left_grid)

        # buttons in the middle
        buttons_column = QVBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("start_button")
        self.start_button.setCheckable(True)          # toggle button – two states
        self.start_button.setCursor(Qt.PointingHandCursor)
        buttons_column.addWidget(self.start_button)

        self.graphs_button = QPushButton("Graphs")
        self.graphs_button.setCursor(Qt.PointingHandCursor)
        self.graphs_button.clicked.connect(self.show_graphs)
        buttons_column.addWidget(self.graphs_button)

        self.about_button = QPushButton("About")
        self.about_button.setCursor(Qt.PointingHandCursor)
        self.about_button.clicked.connect(self.show_about)
        buttons_column.addWidget(self.about_button)
        bottom_row.addLayout(buttons_column, 1)

        # body 2 data (labels on the right of the fields)
        right_grid = QGridLayout()
        self.right_temp_label = QLabel("0.0 °C")
        self.right_temp_label.setObjectName("temp_display")
        right_grid.addWidget(self.right_temp_label, 0, 0)
        right_grid.addWidget(QLabel("Temp."), 0, 1)

        self.right_mass_spin = self.create_mass_spin()
        right_grid.addWidget(self.right_mass_spin, 1, 0)
        right_grid.addWidget(QLabel("Mass"), 1, 1)

        self.right_capacity_spin = self.create_capacity_spin()
        right_grid.addWidget(self.right_capacity_spin, 2, 0)
        right_grid.addWidget(QLabel("H. Cap."), 2, 1)
        bottom_row.addLayout(right_grid)

        main_layout.addLayout(bottom_row)

    def create_mass_spin(self):
        # mass must be greater than 0
        spin = QDoubleSpinBox()
        spin.setRange(0.01, 1000.0)
        spin.setValue(10.0)
        spin.setDecimals(2)
        spin.setSuffix(" kg")
        return spin

    def create_capacity_spin(self):
        # heat capacity must be greater than 0
        spin = QDoubleSpinBox()
        spin.setRange(0.01, 5000.0)
        spin.setValue(0.40)
        spin.setDecimals(2)
        spin.setSingleStep(0.1)
        spin.setSuffix(" J/kg°C")
        return spin

    def show_about(self):
        self.about_window = AboutWindow()
        self.about_window.show()

    def show_graphs(self):
        # the graph window gets access to the main window
        self.graph_window = GraphWindow(self)
        self.graph_window.show()


def load_stylesheet(app):
    qss_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_stylesheet(app)
    window = HeatTransfer()
    window.show()
    sys.exit(app.exec())
