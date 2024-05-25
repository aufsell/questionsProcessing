from pydantic import BaseModel, field_validator


class User(BaseModel):
    # Fields of the User model
    name: str
    last_name: str
    phone_number: str = ''
    username: str
    password: str = ''
    is_admin: bool
    is_active: bool
    is_banned: bool

    @field_validator('phone_number', pre=True)
    def validate_phone_number(cls, v):
        # Delete '+', ' ', '-'
        cleaned_number = v.replace('+', '').replace(' ', '').replace('-', '')

        # Check that the number has 11 digits
        if len(cleaned_number) != 11 or not cleaned_number.isdigit():
            raise ValueError(
                'Некорректный формат номера.'
                'Номера РФ состоят из 11 цифр'
                )

        # Check that the number starts with 7 or 8 and
        if cleaned_number[0] not in ['7', '8']:
            raise ValueError(
                'Некорректный формат номера.'
                'Номера РФ начинаются с +7 или 8'
                )

        return cleaned_number

    @field_validator('name', 'last_name', 'username')
    def validate_length(cls, v):
        # We check that the length does not exceed 31 characters
        if len(v) > 31:
            raise ValueError(
                'Длина имени, фамилии и username'
                'не должна превышать 63 символа'
                )
        return v
