from PyQt5.QtCore import Qt

DICT_PROJECT = "project"
DICT_INITIATOR = "initiator"
DICT_USER = "user"
DICT_PRIORITY = "priority"

COLOR_PRIORITY_LOW = 0xff5EF045
COLOR_PRIORITY_MEDIUM = 0xffFFFF40
COLOR_PRIORITY_HIGH = 0xffFF7B7C

COLOR_DEADLINE_LOW = 0xff5EF045
COLOR_DEADLINE_MEDIUM = 0xffFFFF40
COLOR_DEADLINE_HIGH = 0xffFF7B7C

COLOR_PERCENT_100 = 0xffF5F6D1

COLOR_STRICT_DATE = 0xffFF7B00

RoleNodeId = Qt.UserRole + 1
RoleUser = RoleNodeId + 1
RoleInit = RoleUser + 1
RoleProject = RoleInit + 1
RoleDateBegin = RoleProject + 1
RoleDateEnd = RoleDateBegin+ 1
RoleActive = RoleDateEnd + 1
RoleStrict = RoleActive + 1
RolePercent = RoleStrict + 1
RoleFilterData = RolePercent + 1
