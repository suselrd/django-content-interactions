# coding=utf-8


def visit_handler(instance, **kwargs):
    return instance, kwargs.get('user', None)