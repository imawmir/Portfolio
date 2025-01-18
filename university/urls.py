from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="university_main"),
    path("enroll/<int:course_id>/", views.enroll, name="enroll"),
    path("add_course/", views.add_course, name="add_course"),
    path("students/", views.students, name="students"),
    path("courses/", views.courses, name="courses"),
    path("course_info/<int:course_id>/", views.course_info, name="course_info"),
    path("course_update/<int:course_id>", views.course_update, name="course_update"),
    path("course_delete/<int:course_id>", views.course_delete, name="course_delete"),
    path("student_delete/<int:enroll_id>", views.student_delete, name="student_delete"),
    path("student_update/<int:enroll_id>", views.student_update, name="student_update"),
    path("excel/", views.generate_excel, name="excel"),
    path("add_news", views.add_news, name="add_news"),
    path("news_info/<int:id>/", views.news_info, name="news_info"),
    path("news_update/<int:news_id>", views.news_update, name="news_update"),
    path("news_delete/<int:news_id>/", views.news_delete, name="news_delete"),

]