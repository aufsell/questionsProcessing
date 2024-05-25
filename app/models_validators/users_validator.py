from pydantic import BaseModel, Field, field_validator


class UserValidator(BaseModel):
    # Fields of the User model
    name: str = Field(..., max_length=31)
    last_name: str = Field(..., max_length=31)
    phone_number: str = Field(default='', max_length=11)
    username: str = Field(..., max_length=31)
    password: str = Field(default='', max_length=127)
    is_admin: bool = Field(default=False)
    is_active: bool = Field(default=True)
    is_banned: bool = Field(default=False)

    @field_validator('phone_number', mode='before')
    def validate_phone_number(cls, v):
        # Delete '+', ' ', '-'
        cleaned_number = v.replace('+', '').replace(' ', '').replace('-', '')

        # Check that the number has 11 digits
        if len(cleaned_number) != 11 or not cleaned_number.isdigit():
            raise ValueError(
                'Некорректный формат номера. Номера РФ состоят из 11 цифр'
            )

        # Check that the number starts with 7 or 8
        if cleaned_number[0] not in ['7', '8']:
            raise ValueError(
                'Некорректный формат номера. Номера РФ начинаются с +7 или 8'
            )

        return cleaned_number

    @field_validator('name', 'last_name', 'username')
    def validate_length(cls, v, field):
        # We check that the length does not exceed the max length
        # defined in the field
        if len(v) > 63:
            raise ValueError(
                f'Длина {field.name} не должна превышать {63} символа'
            )
        return v
