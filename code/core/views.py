from django.shortcuts import render, HttpResponse

from core.models import Course, CourseContent, CourseMember, User

# Create your views here.
def index(request):
    return HttpResponse("<h1>Selamat datang di LMS KITA</h1>")

def testing(request):
    guru = User.objects.create_user(
        username="guru_1", email="guru_l@email.com",
        password="rahasia", first_name="Guru", last_name="Satu"
    )

    Course.objects.create(
        name="Pemrograman Python",
        description="Belajar Pemrograman Python",
        price=500000,
        teacher=guru
    )

    return HttpResponse("kosongan")