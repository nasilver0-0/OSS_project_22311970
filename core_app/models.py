from django.contrib.auth.models import AbstractUser,Group,Permission, User
from django.db import models
from django.utils import timezone

class Member(AbstractUser):
    name = models.CharField("이름", max_length=50)
    email = models.EmailField("이메일", unique=True)
   
    groups = models.ManyToManyField(
        Group,
        verbose_name="그룹",
        blank=True,
        related_name='+',   
        help_text="사용자가 속한 그룹"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="사용자 권한",
        blank=True,
        related_name='+',           
        help_text="사용자별 부여된 권한"
    )

    def __str__(self):
        return self.username

class Ingredient(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    name = models.CharField("식재료명", max_length=100)
    expiration_date = models.DateField("유통기한")
    CATEGORY_VEGETABLE   = 'vegetable'   
    CATEGORY_FRUIT       = 'fruit'       
    CATEGORY_MEAT        = 'meat'        
    CATEGORY_SEAFOOD     = 'seafood'     
    CATEGORY_DAIRY       = 'dairy'       
    CATEGORY_EGG         = 'egg'       
    CATEGORY_FROZEN      = 'frozen'      
    CATEGORY_SEASONING   = 'seasoning'   
    CATEGORY_BEVERAGE    = 'beverage'    
    CATEGORY_OTHER       = 'other'      

    CATEGORY_CHOICES = [
        (CATEGORY_VEGETABLE, "야채"),
        (CATEGORY_FRUIT,     "과일"),
        (CATEGORY_MEAT,      "정육(육류)"),
        (CATEGORY_SEAFOOD,   "해산물"),
        (CATEGORY_DAIRY,     "유제품"),
        (CATEGORY_EGG,       "계란"),
        (CATEGORY_FROZEN,    "냉동식품"),
        (CATEGORY_SEASONING, "양념·조미료"),
        (CATEGORY_BEVERAGE,  "음료"),
        (CATEGORY_OTHER,     "기타"),
    ]

    category = models.CharField(
        "카테고리",
        max_length=20,
        choices=CATEGORY_CHOICES,
        default=CATEGORY_VEGETABLE,
    )

    custom_category = models.CharField(
        "사용자 지정 카테고리",
        max_length=50,
        blank=True,
        help_text="기타를 선택한 경우 여기에 직접 입력하세요"
    )

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.category == self.CATEGORY_OTHER and not self.custom_category:
            raise ValidationError({
                'custom_category': "기타를 선택했으므로 사용자 지정 카테고리를 입력해야 합니다."
            })

    def get_category_display_text(self):
        if self.category == self.CATEGORY_OTHER:
            return self.custom_category
        return dict(self.CATEGORY_CHOICES).get(self.category, "알 수 없음")

    def __str__(self):
        return f"{self.name} ({self.get_category_display_text()})"

class MealRecord(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.DateField("날짜")

    breakfast = models.BooleanField("아침 집밥", default=False)
    lunch = models.BooleanField("점심 집밥", default=False)
    dinner = models.BooleanField("저녁 집밥", default=False)

    def get_meal_types(self):
        meals = []
        if self.breakfast:
            meals.append("아침")
        if self.lunch:
            meals.append("점심")
        if self.dinner:
            meals.append("저녁")
        return meals

    def __str__(self):
        return f"{self.member.username} - {self.date} ({', '.join(self.get_meal_types()) or '기록 없음'})"

class Settings(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name="settings")
    graph_color = models.CharField(max_length=7, default="#4bc0c0")

    push_expiry_alert = models.BooleanField(
        "알림 허용",
        default=True,
        help_text="유통기한 임박 알림을 받을지 설정합니다."
    )

    alert_day_major = models.PositiveSmallIntegerField(
        "첫 번째 알림(며칠 전)",
        default=3,
        help_text="유통기한 며칠 전에 첫 번째 알림을 받을지 설정하세요."
    )
    alert_day_minor = models.PositiveSmallIntegerField(
        "마지막 알림(며칠 전)",
        default=1,
        help_text="유통기한 며칠 전에 마지막 알림을 받을지 설정하세요."
    )

    def __str__(self):
        return f"{self.member.username} 설정"

    class Meta:
        verbose_name = "사용자 설정"
        verbose_name_plural = "사용자 설정들"

class Category(models.Model):  
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name