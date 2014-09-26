# coding=utf-8
from django.utils.translation import ugettext as _


# A tuple of standard large number to their converters
intword_converters = (
    (3, lambda number: _('%(value)dK')),
    (6, lambda number: _('%(value)dM')),
    (9, lambda number: _('%(value)dG')),
)


def intmin(value):
    """
    """
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    if value < 1000:
        return value

    for exponent, converter in intword_converters:
        large_number = 10 ** exponent
        if value < large_number * 1000:
            new_value = value / large_number
            tpl = "+%s" if value > large_number else "%s"
            return tpl % converter(new_value) % {'value': new_value}
    return value
