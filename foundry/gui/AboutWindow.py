from PySide2.QtGui import QPixmap, Qt
from PySide2.QtWidgets import QBoxLayout, QFrame, QLabel

from foundry import data_dir, get_current_version_name
from foundry.gui.CustomDialog import CustomDialog

LINK_SMB3F = "https://github.com/mchlnix/SMB3-Foundry"
LINK_HUKKA = "http://hukka.ncn.fi/index.php?about"
LINK_SMB3WS = "https://www.romhacking.net/utilities/298/"
LINK_SOUTHBIRD = "https://github.com/captainsouthbird"
LINK_DISASM = "https://github.com/captainsouthbird/smb3"
LINK_BLUEFINCH = "https://www.twitch.tv/bluefinch3000"


class AboutDialog(CustomDialog):
    def __init__(self, parent):
        super(AboutDialog, self).__init__(parent, title="About SMB3Foundry")

        main_layout = QBoxLayout(QBoxLayout.LeftToRight, self)

        image = QPixmap(str(data_dir.joinpath("foundry.ico"))).scaled(200, 200)

        icon = QLabel(self)
        icon.setPixmap(image)

        main_layout.addWidget(icon)

        text_layout = QBoxLayout(QBoxLayout.TopToBottom)

        text_layout.addWidget(QLabel(f"SMB3 Foundry v{get_current_version_name()}", self))
        text_layout.addWidget(QHLine())
        text_layout.addWidget(LinkLabel(self, f'By <a href="{LINK_SMB3F}">Michael</a>'))
        text_layout.addWidget((QLabel("", self)))
        text_layout.addWidget(QLabel("With thanks to:", self))
        text_layout.addWidget(
            LinkLabel(self, f'<a href="{LINK_HUKKA}">Hukka</a> for <a href="{LINK_SMB3WS}">SMB3 Workshop</a>')
        )
        text_layout.addWidget(
            LinkLabel(
                self,
                f'<a href="{LINK_SOUTHBIRD}">Captain Southbird</a> for the <a href="{LINK_DISASM}">SMB3 Disassembly</a>',
            )
        )
        text_layout.addWidget(
            LinkLabel(
                self,
                f'<a href="{LINK_BLUEFINCH}">BlueFinch</a>, ZacMario and SKJyannick for testing and sanity checking',
            )
        )

        main_layout.addLayout(text_layout)


class LinkLabel(QLabel):
    def __init__(self, parent, text):
        super(LinkLabel, self).__init__(parent)

        self.setText(text)
        self.setTextFormat(Qt.RichText)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(True)


# taken from https://stackoverflow.com/a/41068447/4252230
class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
