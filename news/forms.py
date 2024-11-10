from django import forms
from .models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image', 'category']

    # Şəkilsiz xəbər qəbul edilə bilər amma həm mətinsiz həm də şəkilsiz xəbər daxil edilməsin
    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        image = cleaned_data.get("image")
        
        if not content and not image:
            raise forms.ValidationError("Şəkilsiz xəbər mətn daxil edilməlidir.")
        return cleaned_data
