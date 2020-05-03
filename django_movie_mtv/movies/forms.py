from django import forms

from .models import Reviews


class ReviewForm(forms.ModelForm):
    """Forms of Review"""
    class Meta:
        model = Reviews
        fields = ("name", "email", "text")
