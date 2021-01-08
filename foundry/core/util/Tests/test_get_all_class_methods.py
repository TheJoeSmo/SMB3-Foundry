

from foundry.core.util.get_all_class_methods import get_all_class_methods


class TestClass:
    def method(self):
        pass


class BetterTestClass(TestClass):
    def super_mega_awesome_method(self):
        pass


def test_if_retrieving_methods():
    assert callable(get_all_class_methods(TestClass())[0])


def test_regular_class_counting():
    assert len(get_all_class_methods(TestClass())) == 1


def test_super_class_counting():
    assert len(get_all_class_methods((BetterTestClass()))) == 2
