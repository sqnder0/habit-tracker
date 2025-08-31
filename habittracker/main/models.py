from django.db import models
from django.conf import settings
import datetime

# Create your models here.
class Habit(models.Model):
    habit_name = models.CharField(max_length=64)
    habit_description = models.TextField(default="")
    timestamp = models.TimeField(default=datetime.time(12, 0))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return f"{self.user.username if self.user else 'unknown user'}: {self.habit_name}"
    
    @property
    def habit_streak(self):
        streak = 0
        today = datetime.date.today()
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        current_day = today
        
        start_habit = Day.objects.filter(habit=self, day=current_day).first()
        
        if not start_habit or not start_habit.done:
            current_day = yesterday
            start_habit = Day.objects.filter(habit=self, day=current_day).first()
            
            if not start_habit or not start_habit.done:
                return 0
            
        is_habit_done = start_habit.done
        
        while is_habit_done:
            streak += 1
            
            current_day -= datetime.timedelta(days=1)
            current_habit = Day.objects.filter(habit=self, day=current_day).first()
            
            if not current_habit:
                is_habit_done = False
                break
            
            is_habit_done = current_habit.done
        
        return streak
        

class Day(models.Model):
    day = models.DateField()
    notes = models.TextField(default="")
    done = models.BooleanField(default=False)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    