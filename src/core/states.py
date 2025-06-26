from enum import Enum


class UserStates(str, Enum):
    # Состояния для создания тикета
    EMAIL_INPUT = "email_input"
    CODE_VERIFICATION = "code_verification"
    CATEGORY_SELECTION = "category_selection"
    SUBCATEGORY_SELECTION = "subcategory_selection"
    PROBLEM_DESCRIPTION = "problem_description"
    FILE_UPLOAD = "file_upload"

    # Состояния для дополнения тикета
    ADDITIONAL_INFO = "additional_info"




