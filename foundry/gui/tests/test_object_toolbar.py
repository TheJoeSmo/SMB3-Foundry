from foundry.gui.ObjectToolBar import ObjectToolBar


def test_creation(qtbot):
    object_toolbar = ObjectToolBar()

    object_toolbar.set_object_set(1)

    object_toolbar.show()

    qtbot.addWidget(object_toolbar)
