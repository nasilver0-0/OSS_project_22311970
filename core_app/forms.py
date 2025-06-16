from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Member, Ingredient, MealRecord, Settings

class MemberRegistrationForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    name = forms.CharField(label="이름", max_length=50)
    class Meta:
        model = Member
        fields = ["username", "name", "email", "password1", "password2"]

class LoginForm(forms.Form):
    username = forms.CharField(label="아이디")
    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput)

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "expiration_date", "category", "custom_category"]
        widgets = {
            "expiration_date": forms.DateInput(attrs={"type": "date"}),
            
            "category": forms.Select(attrs={"class": "form-select"}),
            "custom_category": forms.TextInput(attrs={
                "placeholder": "기타의 경우 직접 입력",
                "class": "form-control",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["custom_category"].required = False

class MealRecordForm(forms.ModelForm):
    class Meta:
        model = MealRecord
        fields = ["date", "breakfast", "lunch", "dinner"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = [
            "push_expiry_alert",
            "alert_day_major",
            "alert_day_minor",
            "graph_color"
        ]
        labels = {
            "push_expiry_alert": "유통기한 알림 전체 켜기",
            "alert_day_major": "유통기한 며칠 전에 첫 번째 알림?",
            "alert_day_minor": "유통기한 며칠 전에 두 번째 알림?",
            "graph_color": "그래프 색상"
        }
        help_texts = {
            "alert_day_major": "예: 3을 입력하면 오늘 기준 3일 후 만료식재료 알림.",
            "alert_day_minor": "예: 1을 입력하면 오늘 기준 1일 후 만료식재료 알림.",
            "graph_color": forms.TextInput(attrs={"type": "color"})
        }
        widgets = {
            "alert_day_major": forms.NumberInput(attrs={"min": 1, "style": "width:60px;"}),
            "alert_day_minor": forms.NumberInput(attrs={"min": 1, "style": "width:60px;"}),
            "graph_color": forms.TextInput(attrs={"type": "color"})
        }