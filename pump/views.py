from multiprocessing import context
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
import requests
import json
import pandas as pd
from django.contrib import messages

from .hp_table import hp_table
from .sub_table import sub_table


def main(request):
    return render(request, 'pump_main.html')

def menu(request):
    return render(request,'menu.html')

### SUBMERIBLE ### SUBMERIBLE 
def submersible_pipe_num(request):
    global sub_flow
    global sub_height
    global sub_well
    global sub_distance
    
    if request.method == "POST":
        sub_flow = int(request.POST.get('flow'))
        sub_height = int(request.POST.get('height'))
        sub_well = int(request.POST.get('well'))
        sub_distance = int(request.POST.get('distance'))
    return render(request, 'submersible_pipe_num.html')

def submersible_oft(request):
    global num_vars
    global pipe_num
    pipe_num = request.POST.get('pipe_num')
    num_vars = int(pipe_num)
    pipe_num = int(pipe_num) + 1
    pipe_num = range(1, pipe_num)

    return render(request, 'submersible_oft.html', {'pipe_num': pipe_num})

def submersible(request):
    if request.method == 'POST':
        try:
            global vars
            vars = [i for i in range(1, num_vars + 1)]

            global sub_hf
            global sub_diameter
            global sub_length
            global sub_area
            global sub_velocity

            sub_diameter = {}
            sub_year = {}
            sub_length = {}
            sub_heyzen = {}
            sub_c = {}
            sub_d = {}
            sub_hf = {}
            sub_area = []
            sub_velocity = []

            for i in vars:
                # DIAMETER
                diameter_var_name = f"sub_diameter_{i}"
                sub_diameter[diameter_var_name] = request.POST.get(f"pipe_diameter{i}")
                for diameter_var_name in sub_diameter:
                    sub_diameter[diameter_var_name] = int(sub_diameter[diameter_var_name])

                # YEAR
                year_var_name = f"sub_year_{i}"
                sub_year[year_var_name] = request.POST.get(f"pipe_age{i}")
                for year_var_name in sub_year:
                    sub_year[year_var_name] = int(sub_year[year_var_name])
                    if  sub_year[year_var_name] > 26 :
                        sub_year[year_var_name] = 26

                # LENGTH
                length_var_name = f"sub_length_{i}"
                sub_length[length_var_name] = request.POST.get(f"pipe_length{i}")
                for length_var_name in sub_length:
                    sub_length[length_var_name] = int(sub_length[length_var_name])

                try:
                    # HEYZEN
                    heyzen_var_name = f"sub_heyzen_{i}"
                    sub_heyzen[heyzen_var_name] = request.POST.get(f"pipe_heyzen{i}")
                    for heyzen_var_name in sub_heyzen:
                        sub_heyzen[heyzen_var_name] = int(sub_heyzen[heyzen_var_name])

                except:
                    # MATERIAL
                    material = request.POST.get(f"material{i}")

                    if material == 'polyethylene':
                        sub_heyzen[heyzen_var_name] = 135

                    elif material == 'steel':
                        sub_heyzen[heyzen_var_name] = 125

                    elif material == 'ductile_iron':
                        sub_heyzen[heyzen_var_name] = 140

                    elif material == 'asbestos':
                        sub_heyzen[heyzen_var_name] = 130

                    elif material == 'grp':
                        sub_heyzen[heyzen_var_name] = 115
                        
                if sub_heyzen[heyzen_var_name] > 140:
                    sub_heyzen[heyzen_var_name] = 140
                elif sub_heyzen[heyzen_var_name] < 90:
                    sub_heyzen[heyzen_var_name] = 90
                else:
                    pass

                ### CALCULATIONS
                # C
                sub_c_sum = sub_heyzen[heyzen_var_name] - (0.8 * sub_year[year_var_name])
                sub_c_sum = sub_c_sum ** 1.852
                c_var_name = f"sub_c_{i}"
                sub_c[c_var_name] = sub_c_sum
                # D
                sub_d_sum = (sub_diameter[diameter_var_name] / 1000) ** 4.868
                d_var_name = f"sub_d_{i}"
                sub_d[d_var_name] = sub_d_sum
                # HF
                sub_hf_sum = (10.68 * sub_length[length_var_name] * ((sub_flow / 1000) ** 1.852) / (sub_c[c_var_name] * sub_d[d_var_name])) * 1.1
                hf_var_name = f"sub_hf_{i}"
                sub_hf_sum = float(f"{sub_hf_sum:.2f}")
                # print('sub_hf_sum: ',sub_hf_sum)
                sub_hf[hf_var_name] = sub_hf_sum
                # HF SUM
                sub_hf_total = 0
                for i in vars:
                    sub_hf_total += sub_hf[hf_var_name]
                    # print('sub_hf_total: ',sub_hf_total)
            # AREA
            for i in vars:
                diameter_var_name = f"sub_diameter_{i}"
                area = (3.14 * (sub_diameter[diameter_var_name] ** 2)) / 400
                area = float(f"{area:.2f}")
                sub_area.append(area)
            # VELOCITY
            for i in vars:
                j = i
                j -= 1
                heyzen_var_name = f"sub_heyzen_{i}"
                diameter_var_name = f"sub_diameter_{i}"
                velocity = sub_flow / ((sub_area[j] / 10))  #تقسیم بر 10 میکنیم تا مساحت برحسب متر مربع بدست آید
                velocity = f"{velocity:.2f}"
                sub_velocity.append(velocity)


            return render(request, 'submersible.html', {'hf': sub_hf_total,
                                                         'debi': sub_flow,
                                                         'height': sub_height,
                                                         'well': sub_well,
                                                         'distance': sub_distance})
        except NameError:
            return render(request, 'submersible.html')
    else:
        return render(request, 'submersible.html')


def submersible_calculation(request):
    
    sub_diameter_list = list(sub_diameter.values())
    sub_length_list = list(sub_length.values())
    sub_hf_list = list(sub_hf.values())

    if request.method == 'POST':
        sub_flow = int(request.POST.get('flow'))
        sub_height = int(request.POST.get('height'))
        sub_loss = float(request.POST.get('loss'))
    else:
        print('something went wrong!')

    final_flow = sub_flow * 3.6
    final_height = sub_height + sub_loss + sub_well
    
    print("Flow: ", final_flow)
    print("Height: ", final_height)
    
    
    # try:
    final_flow = sub_table(sub_flow, final_height)[0]
    pumping_height = sub_table(sub_flow, final_height)[1]
    stage = sub_table(sub_flow, final_height)[2]
    nominal_power = sub_table(sub_flow, final_height)[3]
    pump_name = sub_table(sub_flow, final_height)[4]
    # except:
    #     messages.info(request, "Entries are invalid. Please try again!")
    #     return redirect("submersible")

    return render(request, 'pump.html', {'vars': vars,
                           'diameter': sub_diameter_list,
                           'area': sub_area,
                           'length': sub_length_list,
                           'velocity': sub_velocity,
                           'hf': sub_hf_list,
                           'final_debi': final_flow,
                           'final_height': final_height,
                           'name': pump_name,
                           'flow': final_flow,
                           'height': pumping_height,
                           'stage': stage,
                           'power': nominal_power})

### HIGHPRESSURE ### HIGHPRESSURE
def highpressure_pipe_num(request):
    global high_debi
    global high_height
    if request.method == "POST":
        high_debi = int(request.POST.get('debi'))
        high_height = int(request.POST.get('height'))
    return render(request, 'highpressure_pipe_num.html')

def highpressure_oft(request):
    global num_vars
    global pipe_num
    pipe_num = request.POST.get('pipe_num')
    num_vars = int(pipe_num)
    pipe_num = int(pipe_num) + 1
    pipe_num = range(1, pipe_num)

    return render(request, 'highpressure_oft.html', {'pipe_num': pipe_num})

def highpressure(request):
    if request.method == 'POST':
        try:
            global vars
            vars = [i for i in range(1, num_vars + 1)]

            global high_hf
            global high_diameter
            global high_length
            global high_area
            global high_velocity

            high_diameter = {}
            high_year = {}
            high_length = {}
            high_heyzen = {}
            high_c = {}
            high_d = {}
            high_hf = {}
            high_area = []
            high_velocity = []

            for i in vars:
                # DIAMETER
                diameter_var_name = f"high_diameter_{i}"
                high_diameter[diameter_var_name] = request.POST.get(f"high_diameter{i}")
                for diameter_var_name in high_diameter:
                    high_diameter[diameter_var_name] = int(high_diameter[diameter_var_name])

                # YEAR
                year_var_name = f"high_year_{i}"
                high_year[year_var_name] = request.POST.get(f"high_year{i}")
                for year_var_name in high_year:
                    high_year[year_var_name] = int(high_year[year_var_name])
                    if  high_year[year_var_name] > 26 :
                        high_year[year_var_name] = 26

                # LENGTH
                length_var_name = f"high_length_{i}"
                high_length[length_var_name] = request.POST.get(f"high_length{i}")
                for length_var_name in high_length:
                    high_length[length_var_name] = int(high_length[length_var_name])

                try:
                    # HEYZEN
                    heyzen_var_name = f"high_heyzen_{i}"
                    high_heyzen[heyzen_var_name] = request.POST.get(f"high_heyzen{i}")
                    for heyzen_var_name in high_heyzen:
                        high_heyzen[heyzen_var_name] = int(high_heyzen[heyzen_var_name])

                except:
                    # MATERIAL
                    material = request.POST.get(f"material{i}")

                    if material == 'polyethylene':
                        high_heyzen[heyzen_var_name] = 135

                    elif material == 'steel':
                        high_heyzen[heyzen_var_name] = 125

                    elif material == 'ductile_iron':
                        high_heyzen[heyzen_var_name] = 140

                    elif material == 'asbestos':
                        high_heyzen[heyzen_var_name] = 130

                    elif material == 'grp':
                        high_heyzen[heyzen_var_name] = 115
                        
                if high_heyzen[heyzen_var_name] > 140:
                    high_heyzen[heyzen_var_name] = 140
                elif high_heyzen[heyzen_var_name] < 90:
                    high_heyzen[heyzen_var_name] = 90
                else:
                    pass

                ### CALCULATIONS
                # C
                high_c_sum = high_heyzen[heyzen_var_name] - (0.8 * high_year[year_var_name])
                high_c_sum = high_c_sum ** 1.852
                c_var_name = f"high_c_{i}"
                high_c[c_var_name] = high_c_sum
                # D
                high_d_sum = (high_diameter[diameter_var_name] / 1000) ** 4.868
                d_var_name = f"high_d_{i}"
                high_d[d_var_name] = high_d_sum
                # HF
                high_hf_sum = (10.68 * high_length[length_var_name] * ((high_debi / 1000) ** 1.852) / (high_c[c_var_name] * high_d[d_var_name])) * 1.1
                hf_var_name = f"high_hf_{i}"
                high_hf_sum = float(f"{high_hf_sum:.2f}")
                # print('high_hf_sum: ',high_hf_sum)
                high_hf[hf_var_name] = high_hf_sum
                # HF SUM
                high_hf_total = 0
                for i in vars:
                    high_hf_total += high_hf[hf_var_name]
                    # print('high_hf_total: ',high_hf_total)
            # AREA
            for i in vars:
                diameter_var_name = f"high_diameter_{i}"
                area = (3.14 * (high_diameter[diameter_var_name] ** 2)) / 400
                area = float(f"{area:.2f}")
                high_area.append(area)
            # VELOCITY
            for i in vars:
                j = i
                j -= 1
                heyzen_var_name = f"high_heyzen_{i}"
                diameter_var_name = f"high_diameter_{i}"
                velocity = high_debi / ((high_area[j] / 10))  #تقسیم بر 10 میکنیم تا مساحت برحسب متر مربع بدست آید
                velocity = f"{velocity:.2f}"
                high_velocity.append(velocity)


            return render(request, 'highpressure.html', {'hf': high_hf_total,
                                                         'debi': high_debi,
                                                         'height': high_height})
        except NameError:
            return render(request, 'highpressure.html')
    else:
        return render(request, 'highpressure.html')

# def pump(request):
#     return render(request, 'pump.html')

def highpressure_calculation(request):
    high_diameter_list = list(high_diameter.values())
    high_length_list = list(high_length.values())
    high_hf_list = list(high_hf.values())

    if request.method == 'POST':
        high_debi = int(request.POST.get('debi'))
        high_height = int(request.POST.get('height'))
        high_motor_rpm = int(request.POST.get('motor'))
        high_oft = float(request.POST.get('oft'))
    else:
        print('something went wrong!')

    final_debi = high_debi * 3.6
    final_height = high_height + high_oft
    
    # print("Flow: ", high_debi)
    # print("Height: ", final_height)
    
    # print(hp_table(high_motor_rpm, high_debi, final_height))
    
    try:
        final_flow = hp_table(high_motor_rpm, high_debi, final_height)[0]
        pumping_height = hp_table(high_motor_rpm, high_debi, final_height)[1]
        stage = hp_table(high_motor_rpm, high_debi, final_height)[2]
        nominal_power = hp_table(high_motor_rpm, high_debi, final_height)[3]
        pump_name = hp_table(high_motor_rpm, high_debi, final_height)[4]
    except:
        messages.info(request, "Entries are invalid. Please try again!")
        return redirect("highpressure")

    return render(request, 'pump.html', {'vars': vars,
                           'diameter': high_diameter_list,
                           'area': high_area,
                           'length': high_length_list,
                           'velocity': high_velocity,
                           'hf': high_hf_list,
                           'final_debi': final_debi,
                           'final_height': final_height,
                           'name': pump_name,
                           'flow': final_flow,
                           'height': pumping_height,
                           'stage': stage,
                           'power': nominal_power})


