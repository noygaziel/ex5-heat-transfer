import sys
import os

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QSlider, QDoubleSpinBox, QFrame,
)

from About import AboutWindow
from Graph import GraphWindow
from Body import Body
from Confetti import ConfettiWidget


class HeatTransfer(QWidget):

    def __init__(self):
        super().__init__()

        # other windows (created when their button is pressed)
        self.about_window = None
        self.graph_window = None

        self.setWindowTitle("Heat Transfer")
        self.setObjectName("main_window")
        self.resize(760, 460)
        # simulation variables
        self.body1 = None
        self.body2 = None
        self.time_step = 0.05          # [s]
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_method)
        # history of the experiment (for the graph window)
        self.current_time = 0.0
        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []
        # BONUS: position of the moving "heat pulse" in the connecting bar (0 to 1)
        self.flow_phase = 0.0

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
        self.left_slider.valueChanged.connect(self.left_temperature_changed)
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
        self.right_slider.valueChanged.connect(self.right_temperature_changed)
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
        self.start_button.clicked.connect(self.start_stop_button_method)
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

        # BONUS: confetti layer (hidden until the temperatures are equal)
        self.confetti = ConfettiWidget(self)

        # BONUS: picture that pops up when the temperatures are equal (hidden for now)
        self.leny_label = QLabel(self)
        leny_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leny.webp")
        self.leny_label.setPixmap(QPixmap(leny_path).scaled(250, 250, Qt.KeepAspectRatio,
                                                            Qt.SmoothTransformation))
        self.leny_label.adjustSize()
        self.leny_label.hide()

    def left_temperature_changed(self):
        # update the number and the color while dragging the slider
        temperature = self.left_slider.value()# return the slider possition - numbers between 0-200
        self.left_temp_label.setText(f"{temperature:.1f} °C")# write the number
        red = int(temperature / 200 * 255)# 0 °C = black, 200 °C = full red 
        self.left_body.setStyleSheet(f"background-color: rgb({red}, 0, 0);")

    def right_temperature_changed(self):
        temperature = self.right_slider.value()
        self.right_temp_label.setText(f"{temperature:.1f} °C")
        red = int(temperature / 200 * 255)
        self.right_body.setStyleSheet(f"background-color: rgb({red}, 0, 0);")

    def update_flow_animation(self, t1, t2):
        # BONUS: a bright pulse that moves along the bar from the hot body to the cold body
        if abs(t1 - t2) < 0.1:
            # equal temperatures - the bar gets the same color as the two bodies
            red = int(t1 / 200 * 255)
            self.connector.setStyleSheet(f"background-color: rgb({red}, 0, 0); border-radius: 4px;")
            return
        self.flow_phase = (self.flow_phase + 0.08) % 1.0
        position = self.flow_phase if t1 > t2 else 1 - self.flow_phase
        p = min(max(position, 0.02), 0.98)
        a = max(0.01, p - 0.12)
        b = min(0.99, p + 0.12)
        left_color = f"rgb({int(t1 / 200 * 255)}, 0, 0)"
        right_color = f"rgb({int(t2 / 200 * 255)}, 0, 0)"
        self.connector.setStyleSheet(
            f"background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 {left_color}, stop:{a:.3f} {left_color}, stop:{p:.3f} #fde047, "
            f"stop:{b:.3f} {right_color}, stop:1 {right_color}); border-radius: 4px;")

    def start_stop_button_method(self):
        if self.start_button.isChecked():
            # pressed - create the bodies from the values on the screen and start
            self.body1 = Body(self.left_mass_spin.value(), self.left_capacity_spin.value(),
                              self.left_slider.value())
            self.body2 = Body(self.right_mass_spin.value(), self.right_capacity_spin.value(),
                              self.right_slider.value())
            # new experiment - reset the history and save the starting point
            self.current_time = 0.0
            self.time_history = [0.0]
            self.body1_temp_history = [self.body1.temperature]
            self.body2_temp_history = [self.body2.temperature]
            self.start_button.setText("Stop")
            self.timer.start(int(self.time_step * 1000))   # [ms]
        else:
            # released - stop the simulation
            self.timer.stop()
            self.start_button.setText("Start")
            self.connector.setStyleSheet("")                 # stop the heat-flow animation

    def timer_method(self):
        # physics step - equations from page 1
        sigma = self.conductivity_spin.value()
        t1 = self.body1.temperature
        t2 = self.body2.temperature
        i1 = sigma * (t2 - t1)          # heat flow into body 1
        i2 = sigma * (t1 - t2)          # heat flow into body 2
        q1 = i1 * self.time_step        # ΔQ = I · Δt
        q2 = i2 * self.time_step
        new_t1 = self.body1.add_heat(q1)
        new_t2 = self.body2.add_heat(q2)

        # save the data for the graph
        self.current_time += self.time_step
        self.time_history.append(self.current_time)
        self.body1_temp_history.append(new_t1)
        self.body2_temp_history.append(new_t2)

        # UI update - the sliders also update the colors (valueChanged)
        self.left_slider.setValue(round(new_t1))
        self.right_slider.setValue(round(new_t2))
        # show the exact value (the slider only holds whole numbers)
        self.left_temp_label.setText(f"{new_t1:.1f} °C")
        self.right_temp_label.setText(f"{new_t2:.1f} °C")
        # BONUS: move the heat pulse in the connecting bar
        self.update_flow_animation(new_t1, new_t2)

        # BONUS: automatic stop when the temperatures are equal
        if abs(new_t1 - new_t2) < 0.1:
            self.start_button.setChecked(False)     # release the toggle button
            self.start_stop_button_method()         # stop the timer + "Start" text
            self.update_flow_animation(new_t1, new_t2)  # bar in the bodies' color (Stop made it gray)
            self.confetti.start()                   # BONUS: confetti
            self.show_leny()

    def show_leny(self):
        # put the picture in the middle of the window for 3 seconds
        x = (self.width() - self.leny_label.width()) // 2
        y = (self.height() - self.leny_label.height()) // 2
        self.leny_label.move(x, y)
        self.leny_label.raise_()                    # on top of everything
        self.leny_label.show()
        QTimer.singleShot(3000, self.leny_label.hide)

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
