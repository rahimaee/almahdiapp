from enum import Enum

class EnumMetaBuilder:
    """
    ساختار تولید متادیتا از Enum استاندارد
    Enum باید دارای value به شکل (key, label) باشد.
    """

    def __init__(self, enum_class: type[Enum], default_value: str = ''):
        self.enum_class = enum_class
        self.default_value = default_value

    @property
    def fields(self):
        """
        خروجی دیکشنری از key → {label, default}
        """
        return {f.value[0]: {'label': f.value[1], 'default': self.default_value} for f in self.enum_class}

    @property
    def choices(self):
        """
        خروجی لیست از (key, label)
        """
        return [(f.value[0], f.value[1]) for f in self.enum_class]

    @property
    def headers(self):
        """
        خروجی لیست از labelها
        """
        return [f.value[1] for f in self.enum_class]

    @property
    def defaults(self):
        """
        خروجی دیکشنری از key → default_value
        """
        return {f.value[0]: self.default_value for f in self.enum_class}

    @property
    def keys(self):
        """
        خروجی لیست از keyها
        """
        return [f.value[0] for f in self.enum_class]
