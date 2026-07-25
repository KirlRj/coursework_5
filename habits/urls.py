from django.urls import path

from .views import (HabitListCreateView, HabitRetrieveUpdateDestroyView,
                    PublicHabitListView)

app_name = "habits"

urlpatterns = [
    path("", HabitListCreateView.as_view(), name="habit_list_create"),
    path("<int:pk>/", HabitRetrieveUpdateDestroyView.as_view(), name="habit_detail"),
    path("public/", PublicHabitListView.as_view(), name="habit_public"),
]
