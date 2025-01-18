# IMPORTS
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models.aggregates import Count
from django.urls import reverse
from .models import Course, Enroll
from .models import News

from openpyxl import Workbook
import urllib.parse


# COURSE VIEWS
def main(request):
    courses = Course.objects.all()
    news = News.objects.all()
    # COURSES COUNTS
    course_counts = Course.objects.aggregate(count=Count('id'))
    course_counts = list(course_counts.values())[0]
    # STUDENTS COUNTS
    student_counts = Enroll.objects.aggregate(count=Count('id'))
    student_counts = list(student_counts.values())[0]

    return render(request, 'main.html', {'courses': courses, 'news': news, 'course_counts': course_counts,
                                         'student_counts': student_counts})


def enroll(request, course_id):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        student_number = request.POST.get('student_number')
        phone = request.POST.get('phone')
        major = request.POST.get('major')
        course = request.POST.get('course')

        enroll = Enroll()

        enroll.firstname = firstname
        enroll.lastname = lastname
        enroll.student_number = student_number
        enroll.phone = phone
        enroll.major = major
        enroll.course = course

        enroll.save()
        print(course)

        message = 'شما با موفقیت ثبت نام شدید'
        messages.success(request, message)
        return redirect('university_main')

    course = get_object_or_404(Course, id=course_id)

    return render(request, 'enroll.html', {'course': course})


def add_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date = request.POST.get('start')
        end_date = request.POST.get('end')
        image = request.FILES.get('image')
        course = Course()

        course.title = title
        course.description = description
        course.start_date = start_date
        course.end_date = end_date
        course.image = image

        course.save()
        # course.id

    message = 'دوره با موفقیت اضافه شد'
    messages.success(request, message)

    courses = Course.objects.all()
    return redirect("university_main")


def students(request):
    course_students = Enroll.objects.all()
    return render(request, "students.html", {"students": course_students})


def courses(request):
    course = Course.objects.all()
    return render(request, "courses.html", {"courses": course})


def course_info(request, course_id):
    course = Course.objects.filter(id=course_id)
    course_name = Course.objects.filter(id=course_id).values_list('title', flat=True).first()
    course_students = Enroll.objects.filter(course=course_name)
    return render(request, "course_info.html", {"courses": course, "students": course_students})


def student_delete(request, enroll_id):
    student = Enroll(id=enroll_id)
    student.delete()

    message = 'دانشجو با موفقیت حذف شد'
    messages.success(request, message)
    return redirect('courses')


def student_update(request, enroll_id):
    course = Course.objects.all()
    student = get_object_or_404(Enroll, id=enroll_id)

    if request.method == 'POST':
        try:
            student.firstname = request.POST.get('firstname')
            student.lastname = request.POST.get('lastname')
            student.student_number = request.POST.get('student_number')
            student.phone = request.POST.get('phone')
            student.major = request.POST.get('major')

            student.save()

            message = 'اطلاعات دانشجو با موفقیت آپدیت شد'
            messages.success(request, message)
            return redirect('courses')
        except Exception as e:
            print(e)  # برای اشکال‌زدایی می‌توانید خطای رخ‌داده را چاپ کنید
            return redirect('courses')

    return render(request, 'courses.html', {'course': course})


def course_update(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        try:
            course.title = request.POST.get('title')
            course.description = request.POST.get('description')
            course.start_date = request.POST.get('start')
            course.end_date = request.POST.get('end')

            # اگر فایل جدیدی آپلود شده باشد، تصویر به‌روزرسانی می‌شود
            if 'image' in request.FILES:
                new_image = request.FILES['image']
                print(f"New image received: {new_image.name}")
                course.image = new_image
            else:
                print("No new image uploaded, keeping the existing image.")

            course.save()

            message = 'اطلاعات دوره با موفقیت آپدیت شد'
            messages.success(request, message)
            return redirect('courses')
        except Exception as e:
            print(e)  # برای اشکال‌زدایی می‌توانید خطای رخ‌داده را چاپ کنید
            return redirect('courses')

    return render(request, 'courses.html', {'course': course})


def course_delete(request, course_id):
    course = Course(id=course_id)
    course.delete()

    message = 'دوره با موفقیت حذف شد'
    messages.success(request, message)
    return redirect('courses')


# EXCEL
def generate_excel(request):
    if request.method == 'POST':
        course = request.POST.get('course_title')
        print("course title is: ", course)
    else:
        print("error")
    students = Enroll.objects.filter(course=course)

    wb = Workbook()
    ws = wb.active

    headers = ['دوره', 'نام', 'نام خانوادگی', 'شماره دانشجویی', 'شماره تلفن', 'رشته', 'تاریخ شرکت']
    ws.append(headers)

    for record in students:
        row = [record.course, record.firstname, record.lastname, record.student_number, record.phone, record.major,
               record.enrolled_at]
        ws.append(row)

    filename = f"{course}.xlsx"
    quoted_filename = urllib.parse.quote(filename)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{quoted_filename}'
    wb.save(response)

    return response


# News
def add_news(request):
    news = News()
    if request.method == 'POST':
        news.title = request.POST.get('news_title')
        news.content = request.POST.get('news_content')
        news.image = request.FILES.get('news_image')

        news.save()

    return redirect('university_main')


def news_info(request, id):
    news = News.objects.all()
    return render(request, "news_info.html", {"news": news})


def news_update(request, news_id):
    news = get_object_or_404(News, id=news_id)

    if request.method == 'POST':
        try:
            news.title = request.POST.get('title')
            news.content = request.POST.get('content')

            published_at_str = request.POST.get('published_at')
            try:
                # Parse the input date string to a datetime object
                published_at = datetime.strptime(published_at_str, "%b. %d, %Y, %I:%M %p")
                # Save the datetime object to the model
                news.published_at = published_at
            except ValueError:
                # Handle the case where the date format is not as expected
                print(f"Invalid date format: {published_at_str}")
                # You might want to handle this error more gracefully

            # اگر فایل جدیدی آپلود شده باشد، تصویر به‌روزرسانی می‌شود
            if 'image' in request.FILES:
                new_image = request.FILES['image']
                print(f"New image received: {new_image.name}")
                news.image = new_image
            else:
                print("No new image uploaded, keeping the existing image.")

            news.save()
            return redirect('news_info', news_id=news.id)
        except Exception as e:
            print(e)  # برای اشکال‌زدایی می‌توانید خطای رخ‌داده را چاپ کنید
            return redirect('news_info', news_id=news.id)

    return render(request, 'news_info.html', {'news': news})


def news_delete(request, news_id):
    news = News(id=news_id)
    news.delete()
    return redirect('course_list')
