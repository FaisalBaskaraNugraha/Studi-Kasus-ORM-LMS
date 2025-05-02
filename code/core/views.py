from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.db.models import Max, Min, Avg, Count
from django.contrib.auth.models import User
from django.core import serializers
from core.models import Course, CourseMember, CourseContent 

# Welcome Page
def index(request):
    return HttpResponse("<h1>Selamat datang di LMS KITA</h1>")

# Sample Data Creation
def testing(request):
    guru, _ = User.objects.get_or_create(
        username="guru_1", email="guru_l@email.com",
        defaults={"password": "rahasia", "first_name": "Guru", "last_name": "Satu"}
    )

    Course.objects.get_or_create(
        name="Pemrograman Python",
        defaults={"description": "Belajar Pemrograman Python", "price": 500000, "teacher": guru}
    )

    return HttpResponse("Data contoh telah dibuat.")

# List All Courses with Teacher Information
def all_courses(request):
    courses = Course.objects.all().values(
        "id", "name", "price",
        "teacher__id", "teacher__username",
        "teacher__first_name", "teacher__last_name"
    )
    return JsonResponse(list(courses), safe=False)

# User Profile with Courses Created
def user_profile(request, user_id):
    user = User.objects.filter(pk=user_id).values("username", "email", "first_name", "last_name").first()
    if not user:
        return JsonResponse({"error": "User not found"}, status=404)

    courses = Course.objects.filter(teacher_id=user_id).values("id", "name", "description", "price")
    user["courses"] = list(courses)

    return JsonResponse(user)

# Course Statistics
def course_statistics(request):
    courses = Course.objects.all()
    stats = courses.aggregate(
        max_price=Max("price"),
        min_price=Min("price"),
        avg_price=Avg("price")
    )

    cheapest = Course.objects.filter(price=stats["min_price"])
    expensive = Course.objects.filter(price=stats["max_price"])
    popular = courses.annotate(member_count=Count("coursemember")).order_by("-member_count")[:5]
    unpopular = courses.annotate(member_count=Count("coursemember")).order_by("member_count")[:5]

    result = {
        "course_count": courses.count(),
        "course_stats": stats,
        "cheapest": serializers.serialize("python", cheapest),
        "expensive": serializers.serialize("python", expensive),
        "popular": serializers.serialize("python", popular),
        "unpopular": serializers.serialize("python", unpopular),
    }

    return JsonResponse(result, safe=False)

# User Enrollment Statistics
def enrollment_statistics(request):
    creators_count = User.objects.annotate(course_count=Count("course")).filter(course_count__gt=0).count()
    no_course_users = User.objects.annotate(course_count=Count("course")).filter(course_count=0).count()
    avg_courses_followed = CourseMember.objects.aggregate(avg_followed=Avg("user__coursemember"))["avg_followed"]

    most_active_user = User.objects.annotate(course_followed=Count("coursemember")).order_by("-course_followed").first()
    inactive_users = list(User.objects.filter(coursemember__isnull=True).values("id", "username"))

    result = {
        "jumlah_pembuat_course": creators_count,
        "jumlah_user_tidak_memiliki_course": no_course_users,
        "rata_rata_course_diikuti_user": avg_courses_followed,
        "user_teraktif": {
            "username": most_active_user.username if most_active_user else None,
            "jumlah_course_diikuti": most_active_user.course_followed if most_active_user else None,
        },
        "user_tidak_mengikuti_course_sama_sekali": inactive_users,
    }

    return JsonResponse(result)