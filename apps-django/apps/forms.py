from django import forms


class UploadPDFForm(forms.Form):

    document = forms.FileField(
        label="Upload PDF",
        widget=forms.ClearableFileInput(
            attrs={
                "accept": ".pdf"
            }
        )
    )

    ratio = forms.FloatField(
        initial=0.27,
        min_value=0.10,
        max_value=0.50
    )