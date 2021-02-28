from django import forms
from phonenumber_field.formfields import PhoneNumberField


class BuyTicketForm(forms.Form):
    error_css_class = 'is-invalid'

    name = forms.CharField(
        max_length=150,
        label="Имя и Фамилия",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Иван'}),
    )
    email = forms.CharField(
        required=True,
        label="Электронная почта",
        widget=forms.EmailInput(attrs={'placeholder': 'mail2@mail.ru'}),
    )
    phone_number = PhoneNumberField(
        required=True,
        label="Номер телефона",
        widget=forms.TextInput(attrs={'placeholder': '+79123456789'}),
    )

    def __init__(self, *args, **kwargs):
        super(BuyTicketForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
