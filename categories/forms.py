from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        label="Category Name",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        label='Description',
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    slug = forms.CharField(
        label="Slug",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        label="Image",
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Category
        fields = ['name', 'description', 'slug', 'image']
    
    def clean_name(self):
        data = self.cleaned_data.get('name')
        if Category.objects.filter(name=data).exists():
            raise forms.ValidationError("A Category with this name already exists")
        
        return data
    
    def clean_slug(self):
        data = self.cleaned_data.get('slug')
        if Category.objects.filter(slug=data).exists():
            raise forms.ValidationError("A Category with this slug already exists")
        
        return data
    