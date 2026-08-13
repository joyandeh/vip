# custom validators with Persian messages
# these override the default Django password validators to show Persian error messages

from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator as BaseSimilarityValidator,
    MinimumLengthValidator as BaseMinLengthValidator,
    CommonPasswordValidator as BaseCommonValidator,
    NumericPasswordValidator as BaseNumericValidator,
)


class UserAttributeSimilarityValidator(BaseSimilarityValidator):
    def get_help_text(self):
        return "رمز عبور شما نمی‌تواند شباهت زیادی به سایر اطلاعات شخصی شما داشته باشد."

    def get_error_message(self):
        return "رمز عبور شما بیش از حد به اطلاعات شخصی شما شباهت دارد."


class MinimumLengthValidator(BaseMinLengthValidator):
    def __init__(self, min_length=8):
        super().__init__(min_length)
        self.min_length = min_length

    def get_help_text(self):
        return f"رمز عبور شما باید حداقل {self.min_length} کاراکتر داشته باشد."

    def get_error_message(self):
        return f"رمز عبور شما باید حداقل {self.min_length} کاراکتر داشته باشد. (تعداد کاراکترهای فعلی: )"


class CommonPasswordValidator(BaseCommonValidator):
    def get_help_text(self):
        return "رمز عبور شما نمی‌تواند یک رمز عبور رایج و ساده باشد."

    def get_error_message(self):
        return "این رمز عبور بسیار رایج و ساده است. لطفاً یک رمز عبور پیچیده‌تر انتخاب کنید."


class NumericPasswordValidator(BaseNumericValidator):
    def get_help_text(self):
        return "رمز عبور شما نمی‌تواند تماماً عددی باشد."

    def get_error_message(self):
        return "رمز عبور شما نمی‌تواند تماماً از اعداد تشکیل شده باشد."