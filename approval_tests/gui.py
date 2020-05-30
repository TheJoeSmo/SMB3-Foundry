from typing import Union

from PySide2.QtGui import QGuiApplication, QPixmap, Qt
from PySide2.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

image_source = Union[QPixmap, str]


def _get_pixmap_from_source(image: image_source) -> QPixmap:
    if isinstance(image, str):
        image = QPixmap(str)

    return image


class ApprovalDialog(QDialog):
    Ignore = QDialogButtonBox.Ignore

    def __init__(self, test_name: str, reference_image: QPixmap, generated_image: QPixmap):
        super(ApprovalDialog, self).__init__()

        self.setWindowTitle(test_name)

        main_layout = QVBoxLayout(self)

        ref_image = QLabel()
        ref_image.setPixmap(reference_image)

        gen_image = QLabel()
        gen_image.setPixmap(generated_image)

        scroll_area = QScrollArea()

        self.layout().addWidget(scroll_area)

        screen_width, screen_height = QGuiApplication.primaryScreen().size().toTuple()

        if reference_image.width() + gen_image.width() >= screen_width:
            self.image_layout = QVBoxLayout()
        else:
            self.image_layout = QHBoxLayout()

        self.image_layout.addStretch()
        self.image_layout.addWidget(ref_image)
        self.image_layout.addWidget(gen_image)
        self.image_layout.addStretch()

        scroll_area.setWidget(QWidget())
        scroll_area.setWidgetResizable(True)

        scroll_area.widget().setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        scroll_area.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        scroll_area.widget().setLayout(self.image_layout)

        def _sizeHint():
            orig_size = scroll_area.widget().sizeHint()

            orig_size.setHeight(orig_size.height() + 20)
            orig_size.setWidth(orig_size.width() + 20)

            if orig_size.width() > screen_width - 20:
                orig_size.setWidth(screen_width - 20)

            if orig_size.height() > screen_height - 20:
                orig_size.setHeight(screen_height - 20)

            return orig_size

        scroll_area.sizeHint = _sizeHint

        button_box = QDialogButtonBox()

        button_box.addButton("Reject", QDialogButtonBox.RejectRole).clicked.connect(self.reject)
        button_box.addButton(QDialogButtonBox.Ignore).clicked.connect(self._on_ignore)

        button_box.addButton("Accept as new Reference", QDialogButtonBox.ApplyRole).clicked.connect(self._on_overwrite)

        main_layout.addWidget(scroll_area)
        main_layout.addWidget(button_box, alignment=Qt.AlignCenter)

    def _on_overwrite(self):
        self.done(QDialogButtonBox.Apply)

    def _on_ignore(self):
        self.done(QDialogButtonBox.Ignore)

    @staticmethod
    def compare(test_name: str, reference_image: image_source, generated_image: image_source):
        reference_image = _get_pixmap_from_source(reference_image)
        generated_image = _get_pixmap_from_source(generated_image)

        if generated_image.toImage() == reference_image.toImage():
            return QDialog.Accepted

        dialog = ApprovalDialog(test_name, reference_image, generated_image)

        dialog.exec_()

        return dialog.result()
