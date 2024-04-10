from django import forms
from a_users.models import CustomProfile

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomProfile
        exclude = ["user"]
        labels = {
            "image": "Imagem de perfil",
            "nickname": "Apelido",
            "location": "Localização",
            "bio": "Biografia",
        }
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "nickname": forms.TextInput(attrs={"id": "form-nickname", "class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control"}),
        }
