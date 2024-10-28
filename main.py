import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QSplitter, QCheckBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt, QSettings

#By BrianX340

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("RTSP Stream Viewer")
        
        self.settings = QSettings("RTSPStreamViewer", "RTSPStreamViewer")

        self.main_layout = QVBoxLayout(self)

        self.login_layout = QVBoxLayout()
        self.login_layout.setAlignment(Qt.AlignCenter)


        self.ip_input = QLineEdit(self)
        self.ip_input.setPlaceholderText("IP")
        self.login_layout.addWidget(self.ip_input)

        self.port_input = QLineEdit(self)
        self.port_input.setPlaceholderText("Port")
        self.login_layout.addWidget(self.port_input)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Usuario")
        self.login_layout.addWidget(self.user_input)

        self.pass_input = QLineEdit(self)
        self.pass_input.setPlaceholderText("Contraseña")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.login_layout.addWidget(self.pass_input)

        self.qty_channels_input = QLineEdit(self)
        self.qty_channels_input.setPlaceholderText("Cantidad de Canales")
        self.login_layout.addWidget(self.qty_channels_input)

        self.remember_checkbox = QCheckBox("Recordar", self)
        self.login_layout.addWidget(self.remember_checkbox)

        self.login_button = QPushButton("Iniciar", self)
        self.login_button.clicked.connect(self.start_streaming)
        self.login_layout.addWidget(self.login_button)

        self.main_layout.addStretch()
        self.main_layout.addLayout(self.login_layout)
        self.main_layout.addStretch()

        self.video_splitter = QSplitter(Qt.Vertical)
        self.main_layout.addWidget(self.video_splitter)

        self.players = []

        self.load_settings()

    def start_streaming(self):
        ip = self.ip_input.text().strip()
        port = self.port_input.text().strip()

        user = self.user_input.text().strip()
        password = self.pass_input.text().strip()

        if not user or not password:
            QMessageBox.warning(self, "Error", "Por favor, ingrese el usuario y la contraseña.")
            return

        if self.remember_checkbox.isChecked():
            self.save_settings()

        base_url = f"rtsp://{user}:{password}@{ip}:{port}/?channel={{}}&stream=0"

        self.resize(1000, 800)
        self.video_splitter.show()

        top_row_splitter = QSplitter(Qt.Horizontal)
        bottom_row_splitter = QSplitter(Qt.Horizontal)

        self.video_splitter.addWidget(top_row_splitter)
        self.video_splitter.addWidget(bottom_row_splitter)

        try:
            num_channels = int(self.qty_channels_input.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Error", "Ingrese un número válido de canales.")
            return

        for channel in range(1, num_channels + 1):
            stream_url = base_url.format(channel)

            video_widget = QVideoWidget(self)
            media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
            media_player.setVideoOutput(video_widget)
            media_player.setMedia(QMediaContent(QUrl(stream_url)))

            media_player.play()
            self.players.append(media_player)

            if channel <= 2:
                top_row_splitter.addWidget(video_widget)
            else:
                bottom_row_splitter.addWidget(video_widget)

        for i in reversed(range(self.login_layout.count())): 
            widget = self.login_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

    def save_settings(self):
        """Guardar el usuario y la cantidad de canales en QSettings"""
        self.settings.setValue("ip", self.ip_input.text().strip())
        self.settings.setValue("port", self.port_input.text().strip())
        self.settings.setValue("usuario", self.user_input.text().strip())
        self.settings.setValue("canales", self.qty_channels_input.text().strip())
        self.settings.setValue("remember", self.remember_checkbox.isChecked())

    def load_settings(self):
        """Cargar configuraciones guardadas en QSettings"""
        if self.settings.value("remember", False, type=bool):
            self.ip_input.setText(self.settings.value("ip", ""))
            self.port_input.setText(self.settings.value("port", ""))
            self.user_input.setText(self.settings.value("usuario", ""))
            self.qty_channels_input.setText(self.settings.value("canales", ""))
            self.remember_checkbox.setChecked(True)

    def closeEvent(self, event):
        for player in self.players:
            player.stop()
            player.deleteLater()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
