from django import forms


class CommentForm(forms.Form):
    # get the author of the form, name shouldnt be longer than 60 chars
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your Name"
        })
    )
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Leave a Comment!"
        })
    )
