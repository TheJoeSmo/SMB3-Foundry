from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QButtonGroup,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
)

from foundry import icon, icon_dir
from foundry.gui.CustomDialog import CustomDialog
from foundry.gui.settings import RESIZE_LEFT_CLICK, RESIZE_RIGHT_CLICK, SETTINGS, load_settings, save_settings

load_settings()


class SettingsDialog(CustomDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent, "Settings")

        mouse_box = QGroupBox("Mouse", self)
        mouse_layout = QHBoxLayout(mouse_box)

        self.lmb_radio = QRadioButton("Left Mouse Button")
        rmb_radio = QRadioButton("Right Mouse Button")

        self.lmb_radio.setChecked(SETTINGS["resize_mode"] == RESIZE_LEFT_CLICK)
        rmb_radio.setChecked(SETTINGS["resize_mode"] == RESIZE_RIGHT_CLICK)

        self.lmb_radio.toggled.connect(self._update_settings)

        radio_group = QButtonGroup()
        radio_group.addButton(self.lmb_radio)
        radio_group.addButton(rmb_radio)

        mouse_layout.addWidget(QLabel("Resize mode:"))
        mouse_layout.addWidget(self.lmb_radio)
        mouse_layout.addWidget(rmb_radio)

        # ----------------------------------

        self.emulator_command_input = QLineEdit(self)
        self.emulator_command_input.setPlaceholderText("Path to emulator")
        self.emulator_command_input.setText(SETTINGS["instaplay_emulator"])

        self.emulator_command_input.textChanged.connect(self._update_settings)

        self.emulator_path_button = QPushButton(icon("folder.svg"), "", self)
        self.emulator_path_button.pressed.connect(self._get_emulator_path)

        self.command_arguments_input = QLineEdit(self)
        self.command_arguments_input.setPlaceholderText("%f")
        self.command_arguments_input.setText(SETTINGS["instaplay_arguments"])

        self.command_arguments_input.textEdited.connect(self._update_settings)

        self.command_label = QLabel()

        command_box = QGroupBox("Emulator", self)
        command_layout = QVBoxLayout(command_box)

        command_layout.addWidget(QLabel('Emulator command or "path to exe":'))

        command_input_layout = QHBoxLayout()
        command_input_layout.addWidget(self.emulator_command_input)
        command_input_layout.addWidget(self.emulator_path_button)

        command_layout.addLayout(command_input_layout)
        command_layout.addWidget(QLabel("Command arguments (%f will be replaced with rom path):"))
        command_layout.addWidget(self.command_arguments_input)

        layout = QVBoxLayout(self)
        layout.addWidget(mouse_box)
        layout.addWidget(command_box)
        layout.addWidget(QLabel("Command used to play the rom:"))
        layout.addWidget(self.command_label)

        self.update()

    def update(self):
        self.command_label.setText(f" > {SETTINGS['instaplay_emulator']} {SETTINGS['instaplay_arguments']}")

    def _update_settings(self, _):
        SETTINGS["instaplay_emulator"] = self.emulator_command_input.text()
        SETTINGS["instaplay_arguments"] = self.command_arguments_input.text()

        if self.lmb_radio.isChecked():
            SETTINGS["resize_mode"] = RESIZE_LEFT_CLICK
        else:
            SETTINGS["resize_mode"] = RESIZE_RIGHT_CLICK

        self.update()

    def _get_emulator_path(self):
        path_to_emulator, _ = QFileDialog.getOpenFileName(self, caption="Select emulator executable")

        if not path_to_emulator:
            return

        self.emulator_command_input.setText(path_to_emulator)

    def on_exit(self):
        save_settings()

        super(SettingsDialog, self).on_exit()


def show_settings():
    SettingsDialog().exec_()
