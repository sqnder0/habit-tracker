from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from . import models
from datetime import date, timedelta, datetime

import json

# Create your views here.
def index(request: HttpRequest):
    today = date.today()
    return render_day(request, today.year, today.month, today.day)

def render_day(request: HttpRequest, year: int, month: int, day: int):
    if request.user.is_authenticated:
        all_user_habits = models.Habit.objects.filter(user=request.user)
        habits_today = []
        
        request_date = date(year, month, day)
        
        if request_date == date.today() and request.path != reverse("index"):
            return redirect("index")
        
        if request_date > date.today():
            return HttpResponseBadRequest(request, "Cannot load future tasks!")
    
        for habit in all_user_habits:
            habit_today = models.Day.objects.get_or_create(day=request_date, habit=habit)
            habits_today.append(habit_today)
            
        sorted_habits_today = sort_daily_habits(habits_today)
        
        if request_date == date.today():
            next_day = "#"
        else:
            next_day = (request_date + timedelta(days=1)).strftime("%Y/%m/%d")
        
        prev_day = (request_date - timedelta(days=1)).strftime("%Y/%m/%d")
        
        readable_date = request_date.strftime("%d %b '%y") if request_date != date.today() else ""
        
        return render(request, "main/index.html", {"habits": sorted_habits_today, "date": readable_date, "previous_day": prev_day, "next_day": next_day})
    else:
        return redirect(reverse("login"))

def update_day(request: HttpRequest):
    if request.method != "POST":
        return HttpResponseForbidden()
    
    day_id = request.POST.get("day_id")
    notes = request.POST.get("notes", "") 
    
    day = get_object_or_404(models.Day, id=day_id)
    
    day.notes = notes
    
    if day.done:
        day.done = False
    else:
        day.done = True
        
    day.save()
    return redirect("index") 

def settings(request: HttpRequest):
    habits = models.Habit.objects.filter(user=request.user)
    statistics = []
    
    completed_habits = 0
    total_habits = 0
    
    for habit in habits:
        for day in models.Day.objects.filter(habit=habit):
            completed_habits += 1 if day.done else 0
            total_habits += 1
    
    
    percentage = round(( completed_habits/ total_habits) * 100) if total_habits != 0 else 0
    
    statistics.append({"name": "completed habits", "value": completed_habits})
    statistics.append({"name": "total habits passed", "value": total_habits})
    statistics.append({"name": "percentage", "value": f"{percentage}%"})
    statistics.append({"name": "streak", "value": f"{calc_total_streak(request.user)}"})
    
    return render(request, "main/settings.html", {"habits": habits, "stats": statistics})

def update_habit(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    
    if not request.method == "POST":
        return HttpResponseForbidden()
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    habit_id = str(data.get("habit_id"))
    habit_name = data.get("habit_name")
    timestamp = data.get("timestamp")
    habit_description = data.get("habit_description")
    
    if habit_id == None or not habit_id.isdigit():
        return JsonResponse({"error": "Invalid request, missing habit id"}, status=400)
    
    habit = models.Habit.objects.get(id=int(habit_id))
    
    if not request.user == habit.user:
        return HttpResponseForbidden()
    
    if not habit:
        return JsonResponse({"error": "Habit not found"}, status=404)
    
    habit.habit_name = habit_name
    habit.habit_description = habit_description
    
    try:
        valid_time = datetime.strptime(timestamp, "%H:%M").time()
        habit.timestamp = valid_time
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid timestamp format"}, status=400)
    
    habit.save()
    
    return JsonResponse({
        "success": "success"
    }, status=200)

def delete_habit(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    habit_id = str(data.get("habit_id"))
    
    if habit_id == None or not habit_id.isdigit():
        return JsonResponse({"error": "Invalid request, missing habit id"}, status=400)
    
    habit = models.Habit.objects.get(id=int(habit_id))
    
    if not habit.user == request.user:
        return HttpResponseForbidden()
    
    habit.delete()
    
    return JsonResponse({"success": "success"})
    
def calc_total_streak(user):
    habits = models.Habit.objects.filter(user=user)
    
    if not habits or len(habits) == 0:
        return 0
    
    shortest_streak = habits[0].habit_streak
    
    for habit in habits:
        if habit.habit_streak < shortest_streak:
            shortest_streak = habit.habit_streak
    
    return shortest_streak
    
def create_habit(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    habit_name = data.get("habit_name")
    timestamp = data.get("timestamp")
    habit_description = data.get("habit_description")
    user = request.user
    
    habit = models.Habit()
    habit.habit_name = habit_name
    habit.habit_description = habit_description
    habit.user = user
    
    try:
        valid_time = datetime.strptime(timestamp, "%H:%M").time()
        habit.timestamp = valid_time
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid timestamp format"}, status=400)
    
    habit.save()
    
    return JsonResponse({"success": "success", "habit_id": habit.pk})
    
    
# Some helper functions
def sort_daily_habits(habits):
    days_only = [habit[0] for habit in habits]
    sorted_days = sorted(days_only, key=lambda day: day.habit.timestamp)
    
    return sorted_days