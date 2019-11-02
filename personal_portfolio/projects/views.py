from django.shortcuts import render
from projects.models import Project
import socket
import geoip2.database
# Create your views here.

def visitor_ip_address(request):
    x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip=x_forwarded_for.split(',')[0]
        print("for",x_forwarded_for)
    else:
        ip=request.META.get('REMOTE_ADDR')
        print("remote",ip)
    return ip


def locate(request):
    
    ip=visitor_ip_address(request)
    print(ip)
    latitude=0
    longitude=0
    try:
        socket.inet_aton(ip)
        ip_valid=True
    except socket.error:
        ip_valid=False

    if ip_valid:
        reader=geoip2.database.Reader('projects/GeoLite2-City_20191029/GeoLite2-City.mmdb')
        print(ip)
        try:
            response=reader.city(ip)
            latitude=int(response.location.latitude)
            longitude=int(response.location.longitude)

        except :
            print("error occured")
            

    return {'latitude':latitude,'longitude':longitude}

def project_index(request):
    projects=Project.objects.all()
    obj=locate(request)
    context={'projects':projects,'latitude':obj['latitude'],'longitude':obj['longitude']}
    return render(request,'project_index.html',context)

def project_detail(request,pk):
    project=Project.objects.get(pk=pk)
    context={
        'project':project
    }
    return render(request,'project_detail.html',context)

def attend(request):
    return render(request,'attendance_record.html')