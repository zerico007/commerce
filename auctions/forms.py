from django import forms
from django.forms import ModelForm
from .models import *

class ListingsForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ('title', 'description', 'starting_price', 'listing_photo', 'category')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'starting_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'listing_photo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'category': forms.Select(attrs={'class': 'form-control-check-input'})
        }

class BidsForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ('bid_price',)

        widgets = {
            'bid_price': forms.NumberInput(attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super(BidsForm, self).__init__(*args, **kwargs)
        self.fields['bid_price'].required = False

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('comment',)

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'cols': 10, 'rows': 5,})
        }
    def __init__(self, *args, **kwargs):
        super(CommentsForm, self).__init__(*args, **kwargs)
        self.fields['comment'].required = False

class ClosedForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ('closed',)
        widgets = {
            'closed': forms.CheckboxInput(attrs={'checked': 'checked'})
        }
    def __init__(self, *args, **kwargs):
        super(ClosedForm, self).__init__(*args, **kwargs)
        self.fields['closed'].required = False
