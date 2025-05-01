from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

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

def allCourses(request):
    courses = Course.objects.all()
    data_resp = []
    for course in courses:
        record = {
            'id': course.id,
            'name': course.name,
            'price': course.price,
            'teacher': {
                'id': course.teacher.id,
                'username': course.teacher.username,
                'fullname': f"{course.teacher.first_name} {course.teacher.last_name}"
            }
        }  # Ensure this closing brace is correctly placed
        data_resp.append(record)

    return JsonResponse(data_resp, safe=False)

def userProfile(request, user_id):
    user = User.objects.get(pk=user_id)
    courses = Course.objects.filter(teacher=user)  
    
    data_resp = {
        'username': user.username,
        'email': user.email,
        'fullname': f"{user.first_name} {user.last_name}",
        'courses': []
    }
    
    for course in courses:
        course_data = {
            'id': course.id,
            'name': course.name,
            'description': course.description,
            'price': course.price
        }
        data_resp['courses'].append(course_data)

    return JsonResponse(data_resp, safe=False)

from django.db.models import Max, Min, Avg, Count
from django.core import serializers
def courseStat(request):
  courses = Course.objects.all()
  stats = courses.aggregate(max_price=Max('price'),
                              min_price=Min('price'),
                              avg_price=Avg('price'))
  cheapest = Course.objects.filter(price=stats['min_price'])
  expensive = Course.objects.filter(price=stats['max_price'])
  popular = Course.objects.annotate(member_count=Count('coursemember'))\
                          .order_by('-member_count')[:5]
  unpopular = Course.objects.annotate(member_count=Count('coursemember'))\
                          .order_by('member_count')[:5]

  result = {'course_count': len(courses), 'courses': stats,
            'cheapest': serializers.serialize('python', cheapest), 
            'expensive': serializers.serialize('python', expensive),
            'popular': serializers.serialize('python', popular), 
            'unpopular': serializers.serialize('python', unpopular)}
  return JsonResponse(result, safe=False) 