from django import forms
from .models import InventoryItem

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['title', 'code', 'count', 'new_count', 'type_of_change', 'notes', 'picture']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter code'}),
            'count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter current count'}),
            'new_count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter new count'}),
            'type_of_change': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter type of change'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter notes', 'rows': 4}),
            'picture': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'})
        } 