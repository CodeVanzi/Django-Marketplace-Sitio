from django import forms
from a_users.models import CustomProfile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomProfile
        fields = ["image", "nickname", "email", "location", "bio"]
        labels = {
            "image": "Imagem de perfil",
            "nickname": "Apelido",
            "email": "E-mail",
            "location": "Localização",
            "bio": "Biografia",
        }
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "nickname": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control"}),
        }
