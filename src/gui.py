import sys
import psutil
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import QThread, pyqtSignal, QTimer

class SystemStatsThread(QThread):
    update_signal = pyqtSignal(dict)

    def run(self):
        while True:
            stats = {
                "cpu": psutil.cpu_percent(),
                "ram": psutil.virtual_memory().percent,
                "disk": psutil.disk_usage('/').percent,
                "net_speed": psutil.net_io_counters().bytes_sent / 1024,  # KB/s
                "battery": psutil.sensors_battery().percent if psutil.sensors_battery() else None
            }
            self.update_signal.emit(stats)
            self.msleep(1000)  # Update every second

class SystemMonitorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced System Monitor")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        # CPU Usage
        self.cpu_label = QLabel("CPU Usage:")
        self.cpu_bar = QProgressBar()
        self.cpu_graph = pg.PlotWidget(title="CPU Usage (%)")
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_bar)
        layout.addWidget(self.cpu_graph)

        # RAM Usage
        self.ram_label = QLabel("RAM Usage:")
        self.ram_bar = QProgressBar()
        self.ram_graph = pg.PlotWidget(title="RAM Usage (%)")
        layout.addWidget(self.ram_label)
        layout.addWidget(self.ram_bar)
        layout.addWidget(self.ram_graph)

        # Network Speed
        self.net_label = QLabel("Network Speed: 0 KB/s")
        layout.addWidget(self.net_label)

        # Battery Status
        self.battery_label = QLabel("Battery: N/A")
        layout.addWidget(self.battery_label)

        self.setLayout(layout)

        # Start background thread
        self.stats_thread = SystemStatsThread()
        self.stats_thread.update_signal.connect(self.update_stats)
        self.stats_thread.start()

        # Data storage for graphs
        self.cpu_data = []
        self.ram_data = []

    def update_stats(self, stats):
        self.cpu_bar.setValue(int(stats["cpu"]))
        self.ram_bar.setValue(int(stats["ram"]))
        self.net_label.setText(f"Network Speed: {stats['net_speed']:.2f} KB/s")

        if stats["battery"] is not None:
            self.battery_label.setText(f"Battery: {stats['battery']}%")

        # Update Graphs
        self.cpu_data.append(stats["cpu"])
        self.ram_data.append(stats["ram"])
        self.cpu_graph.plot(self.cpu_data, clear=True, pen='r')
        self.ram_graph.plot(self.ram_data, clear=True, pen='b')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemMonitorApp()
    window.show()
    sys.exit(app.exec())
