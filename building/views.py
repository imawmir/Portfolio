from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Sum
from django.db.models.aggregates import Count, Max
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from openpyxl import Workbook
import urllib.parse

from .models import Building, Spent


# HOME
def home(request):
    buildings = Building.objects.all()

    # BUILDINGS COUNT
    building_count = Building.objects.aggregate(Count('id'))
    building_count = list(building_count.values())

    # WHOLE SPENTS
    total_price = Spent.objects.aggregate(total_price=Sum('price'))
    total_price = list(total_price.values())

    # WHOLE RECORDS
    total_records = Spent.objects.aggregate(total_records=Count('id'))
    total_records = list(total_records.values())

    # WHOLE AREA
    total_area = Building.objects.aggregate(total_area=Sum('area'))
    total_area = list(total_area.values())

    return render(request, 'home.html', {'buildings': buildings,
                                         'building_count': building_count[0],
                                         'total_price': total_price[0],
                                         'total_records': total_records[0],
                                         'total_area': total_area[0]})


# LOGIN
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(username=username, password=password)
#
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('home'))
#
#             else:
#                 return HttpResponse("ورود نامعتبر")
#         else:
#             print("Someone tried to login and failed")
#             print("Username: {} and password: {}".format(username, password))
#             return HttpResponse("کلمه عبور یا نام کاربری اشتباه است")
#     else:
#         return render((request, 'home.html'))
#
#
# # LOGOUT
# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('home'))


# BUILDING LIST
def buildings(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        address = request.POST.get('address')
        area = request.POST.get('area')
        floor = request.POST.get('floor')
        licence = request.POST.get('licence')

        building = Building()

        building.title = title
        building.address = address
        building.area = area
        building.floor = floor
        building.licence = licence

        building.save()
        building.id
        
        return redirect('buildings')

    buildings = Building.objects.all()

    return render(request, 'buildings.html', {'buildings': list(buildings)})


# BUILDING INFO
def building_info(request, pk):
    buildings = Building.objects.all()

    buildings_pk = Building.objects.get(pk=pk)
    spent_pk = Spent.objects.filter(building=buildings_pk)

    total_price = Spent.objects.filter(building=buildings_pk).aggregate(total_price=Sum('price'))
    total_price = list(total_price.values())[0]

    return render(request, 'building_info.html', {'building': buildings_pk,
                                                  'building_spent': list(spent_pk),
                                                  'total_price': total_price,
                                                  'buildings': buildings,
                                                  'building_name': buildings_pk})


# SPENT LIST
# def spent(request):

#     if request.method == 'POST':
#         try:

#             category = request.POST.get('category')
#             subject = request.POST.get('subject')
#             building = request.POST.get('building')
#             date = request.POST.get('date')
#             payer = request.POST.get('payer')
#             price = request.POST.get('price')

#             spent = Spent()

#             spent.category = category
#             spent.subject = subject
#             spent.building = building
#             spent.date = date
#             spent.payer = payer
#             spent.price = price

#             spent.save()
#             spent.id

#         except:
#             try:
#                 delete_id = request.POST.get('delete_id')
#                 spent = Spent(pk=delete_id)
#                 spent.delete()

#             except:
#                 pass

#     queryset = Spent.objects.all()
#     building_name = Building.objects.all()

#     total_price = Spent.objects.aggregate(total_price=Sum('price'))
#     total_price = list(total_price.values())
#     try:
#         total_price = f"{total_price[0]:,}"
#     except:
#         pass

#     return render(request, 'spent.html', {'spent': list(queryset), 'building': list(building_name), 'total_price': total_price})

# SPENT INFO
def spent_info(request, pk):
    buildings = Building.objects.all()

    spent = Spent.objects.get(pk=pk)
    return render(request, 'spent_info.html', {'spent': spent, 'buildings': buildings})


# SPENT UPDATE
def spent_update(request):
    buildings = Building.objects.all()
    
    try:
        try:
            if request.method == 'POST':

                spent_id = request.POST.get('spent_id')
                spent = Spent(pk=spent_id)
                    
                spent.category = request.POST.get('category')
                spent.subject = request.POST.get('subject')
                spent.building = request.POST.get('building')
                spent.date = request.POST.get('date')
                spent.payer = request.POST.get('payer')
                spent.price = request.POST.get('price')
                    
                spent.save()
        
        except:
            category = request.POST.get('category')
            subject = request.POST.get('subject')
            building = request.POST.get('building')
            date = request.POST.get('date')
            payer = request.POST.get('payer')
            price = request.POST.get('price')
                    
            spent = Spent()
            
            spent.category = category
            spent.subject = subject
            spent.building = building
            spent.date = date
            spent.payer = payer
            spent.price = price
                    
            spent.save()
            spent.id
        
    except:
        try:
            delete_id = request.POST.get('delete_id')
            spent = Spent(pk=delete_id)
            spent.delete()
                
        except:
            pass
                
        
    queryset = Spent.objects.all()

    return redirect('building_main')



# SORTED SPENT
def sorted_spent(request):
    buildings = Building.objects.all()

    if request.method == 'POST':
        category = request.POST.get('options')
        building = request.POST.get('building_name')

        if category == 'دستمزد':
            queryset = Spent.objects.filter(category="دستمزد", building=building)
            total_price = Spent.objects.filter(category="دستمزد", building=building).aggregate(total_price=Sum('price'))
            total_price = list(total_price.values())
            try:
                total_price = f"{total_price[0]:,}"
            except:
                pass
        elif category == 'خرید':
            queryset = Spent.objects.filter(category="خرید", building=building)
            total_price = Spent.objects.filter(category="خرید", building=building).aggregate(total_price=Sum('price'))
            total_price = list(total_price.values())
            try:
                total_price = f"{total_price[0]:,}"
            except:
                pass
        elif category == 'نظام مهندسی':
            queryset = Spent.objects.filter(category="نظام مهندسی", building=building)
            total_price = Spent.objects.filter(category="نظام مهندسی", building=building).aggregate(
                total_price=Sum('price'))
            total_price = list(total_price.values())
            try:
                total_price = f"{total_price[0]:,}"
            except:
                pass
        elif category == 'شهرداری':
            queryset = Spent.objects.filter(category="شهرداری", building=building)
            total_price = Spent.objects.filter(category="شهرداری", building=building).aggregate(
                total_price=Sum('price'))
            total_price = list(total_price.values())
            try:
                total_price = f"{total_price[0]:,}"
            except:
                pass
        else:
            queryset = Spent.objects.filter(category="بیمه", building=building)
            total_price = Spent.objects.filter(category="بیمه", building=building).aggregate(total_price=Sum('price'))
            total_price = list(total_price.values())
            try:
                total_price = f"{total_price[0]:,}"
            except:
                pass

    return render(request, 'sorted_spent.html',
                  {'sorted_spent': list(queryset), 'total_price': total_price, 'buildings': buildings})


# SEARCH SPENT
def search_spent(request):
    try:
        buildings = Building.objects.all()            
        building = request.POST.get('building_name')

        if request.method == 'POST':
            search = request.POST.get('search')
            queryset = Spent.objects.filter(subject__icontains=search, building=building)

            total_price = Spent.objects.filter(subject__icontains=search, building=building).aggregate(
                total_price=Sum('price'))
            total_price = list(total_price.values())
            total_price = f"{total_price[0]:,}"

        return render(request, 'search_spent.html',
                    {'search_spent': list(queryset), 'total_price': total_price, 'buildings': buildings})
        
    except:
        raise Http404("رکوردی با این نام وجود ندارد")


# EXCEL GENERATE
def generate_excel(request):
    if request.method == 'POST':
        building = request.POST.get('building_name')

    spent = Spent.objects.filter(building=building)

    wb = Workbook()
    ws = wb.active

    headers = ['ID', 'دسته بندی', 'عنوان', 'ساختمان', 'تاریخ', 'پرداخت کننده', 'قیمت']
    ws.append(headers)

    for record in spent:
        row = [record.id, record.category, record.subject, record.building, record.date, record.payer, record.price]
        ws.append(row)

    filename = f"{building}.xlsx"
    quoted_filename = urllib.parse.quote(filename)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{quoted_filename}'
    wb.save(response)

    return response

