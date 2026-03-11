from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        label="Category Name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Category
        fields = ['name']
    
    def clean_name(self):
        data = self.cleaned_data.get('name')
        if Category.objects.filter(name=data).exists():
            raise forms.ValidationError("A Category with this name already exists")
        
        return data
    