from dataclasses import dataclass

@dataclass
class StatItem:
    title: str
    value: int
    access:bool


class StatBase:
    base_queryset = None  # اگر None باشد، باید get_queryset override شود
    label = '',
    def __init__(self, parent=None):
        if isinstance(parent, StatBase):
            # parent یک StatBase است، از queryset آن استفاده کن
            self.queryset = parent.queryset
        elif hasattr(parent, "all") and callable(parent.all):
            # parent یک QuerySet است
            self.queryset = parent
        elif self.base_queryset is not None:
            # از base_queryset استفاده کن
            self.queryset = self.base_queryset
        else:
            # باید get_queryset override شود
            self.queryset = self.get_queryset()

    def get_queryset(self):
        raise NotImplementedError("هر کلاس فرزند باید get_queryset را پیاده کند یا base_queryset داشته باشد.")

    def count(self):
        return self.get_queryset().count()
