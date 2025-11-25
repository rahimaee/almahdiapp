from dataclasses import dataclass

@dataclass
class StatItem:
    title: str
    value: int


class StatBase:
    base_queryset = None  # اگر None باشد، باید get_queryset override شود

    def __init__(self, parent=None):
        if parent:
            # استفاده از queryset والد، بدون وابستگی
            self.queryset = parent.queryset
        elif self.base_queryset is not None:
            self.queryset = self.base_queryset
        else:
            self.queryset = self.get_queryset()

    def get_queryset(self):
        raise NotImplementedError("هر کلاس فرزند باید get_queryset را پیاده کند یا base_queryset داشته باشد.")

    def count(self):
        return self.get_queryset().count()
