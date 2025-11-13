from enum import Enum

# ==========================
#  تعریف فیلدهای جایگاه سازمانی
# ==========================
class OrganizationalPositionField(Enum):
    POSITION_CODE = 'position_code', 'کد جایگاه'
    POSITION_GROUP = 'position_group', 'جایگاه سازمانی'
    POSITION_PARENT_GROUP = 'position_parent_group', 'سرگروه جایگاه'
    TITLE = 'title', 'عنوان جایگاه'
    DESCRIPTION = 'description', 'توضیحات'

    @property
    def key(self):
        return self.value[0]

    @property
    def label(self):
        return self.value[1]


ORGANIZATIONAL_POSITION_FIELDS = {
    f.key: {'label': f.label, 'default': ''} for f in OrganizationalPositionField
}

ORGANIZATIONAL_POSITION_CHOICES = [(f.key, f.label) for f in OrganizationalPositionField]
ORGANIZATIONAL_POSITION_HEADERS = [f.label for f in OrganizationalPositionField]
ORGANIZATIONAL_POSITION_DEFAULTS = {f.key: '' for f in OrganizationalPositionField}
ORGANIZATIONAL_POSITION_KEYS = [f.key for f in OrganizationalPositionField]


# ==========================
#  تعریف فیلدهای تخصیص سرباز به جایگاه
# ==========================
class OrganizationalPositionAssignEnum(Enum):
    POSITION_CODE = 'position_code', 'کد جایگاه'
    NATIONAL_CODE = 'national_code', 'کد ملی'

    @property
    def key(self):
        return self.value[0]

    @property
    def label(self):
        return self.value[1]
