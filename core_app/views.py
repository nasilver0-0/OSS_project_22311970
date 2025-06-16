from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Ingredient, MealRecord, Settings
from .forms import IngredientForm, LoginForm, MemberRegistrationForm, MealRecordForm, SettingsForm
from django.contrib.auth import logout, authenticate, login
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from collections import defaultdict
from core_app.models import Category

@login_required
def dashboard_view(request):
    settings, created = Settings.objects.get_or_create(member=request.user)
    today = timezone.localdate()

    qs = Ingredient.objects.filter(member=request.user)

    alert_expired_list = qs.filter(expiration_date__lt=today)
    alert_today_list = qs.filter(expiration_date=today)

    date_major = today + timedelta(days=settings.alert_day_major)
    alert_major_list = qs.filter(expiration_date=date_major)

    date_minor = today + timedelta(days=settings.alert_day_minor)
    alert_minor_list = qs.filter(expiration_date=date_minor)

    ingredients = qs.order_by('expiration_date')

    grouped_ingredients = defaultdict(list)
    for ing in ingredients:
        display_category = ing.get_category_display_text()
        grouped_ingredients[display_category].append(ing)

    return render(request, 'core_app/dashboard.html', {
        'settings': settings,
        'today': today,
        'alert_expired_list': alert_expired_list,
        'alert_today_list': alert_today_list,
        'date_major': date_major,
        'alert_major_list': alert_major_list,
        'date_minor': date_minor,
        'alert_minor_list': alert_minor_list,
        'grouped_ingredients': dict(grouped_ingredients),  
    })
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'core_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = MemberRegistrationForm()
    return render(request, 'core_app/register.html', {'form': form})


def add_ingredient_view(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ing = form.save(commit=False)
            ing.member = request.user

            category_name = form.cleaned_data['category']
            category, created = Category.objects.get_or_create(name=category_name)
            ing.category = category

            ing.save()
            return redirect('dashboard')
    else:
        form = IngredientForm()
    return render(request, 'core_app/add_ingredient.html', {'form': form})
def delete_ingredient_view(request, pk):
    ing = get_object_or_404(Ingredient, pk=pk, member=request.user)
    if request.method == 'POST':
        ing.delete()
        return redirect('dashboard')
    return render(request, 'core_app/confirm_delete.html', {'ingredient': ing})

def record_meal_view(request):
    if request.method == 'POST':
        form = MealRecordForm(request.POST)
        if form.is_valid():
            mr = form.save(commit=False)
            mr.member = request.user
            mr.save()
            return redirect('dashboard')
    else:
        form = MealRecordForm()
    return render(request, 'core_app/record_meal.html', {'form': form})


def meal_stats_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    settings_obj = Settings.objects.get(member=request.user)

    period = request.GET.get("range", "daily")
    trunc_func = {
        "daily": TruncDay,
        "weekly": TruncWeek,
        "monthly": TruncMonth
    }.get(period, TruncDay)

    today = date.today()
    current_month_start = today.replace(day=1)
    if today.month == 12:
        next_month_start = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month_start = today.replace(month=today.month + 1, day=1)

    base_qs = MealRecord.objects.filter(member=request.user)
    if period in ["daily", "weekly"]:
        base_qs = base_qs.filter(date__gte=current_month_start, date__lt=next_month_start)

    qs = (
        base_qs
        .annotate(period=trunc_func("date"))
        .values("period")
        .annotate(count=Count("id"))
        .order_by("period")
    )

    chart_data = [{"date": str(r["period"]), "count": r["count"]} for r in qs]

    return render(request, "core_app/meal_stats.html", {
        "events": chart_data,
        "range": period,
        "graph_color": settings_obj.graph_color,
    })

def settings_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    settings_obj, created = Settings.objects.get_or_create(member=request.user)

    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "알림 설정이 저장되었습니다.")
            return redirect('settings')
    else:
        form = SettingsForm(instance=settings_obj)

    return render(request, 'core_app/settings.html', {
        'form': form
    })

def meal_detail_view(request, ymd):
    from datetime import datetime
    date = datetime.strptime(ymd, '%Y-%m-%d').date()
    rec = MealRecord.objects.filter(member=request.user, date=date).first()
    return render(request, 'core_app/meal_detail.html', {
        'date': date,
        'record': rec
    })