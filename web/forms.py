"""Checkout form with validation matching the original Zod schema."""
import re
from django import forms
from .erp_services import ASSIUT_CENTERS


class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        min_length=3,
        max_length=100,
        error_messages={
            "required": "validation.nameRequired",
            "min_length": "validation.nameMin",
        },
    )
    phone = forms.CharField(
        max_length=20,
        error_messages={
            "required": "validation.phoneRequired",
        },
    )
    assiut_center = forms.ChoiceField(
        choices=[("", "---")] + [(c["value"], c["label"]["en"]) for c in ASSIUT_CENTERS],
        error_messages={
            "required": "validation.centerRequired",
        },
    )
    address_details = forms.CharField(
        min_length=10,
        max_length=500,
        widget=forms.Textarea(attrs={"rows": 3}),
        error_messages={
            "required": "validation.addressRequired",
            "min_length": "validation.addressMin",
        },
    )
    landmark = forms.CharField(max_length=200, required=False)
    notes = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
    )

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if not re.match(r"^01[0125]\d{8}$", phone):
            raise forms.ValidationError("validation.phoneInvalid")
        return phone
