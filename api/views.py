import os
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import FileResponse, JsonResponse
from .serializers import MyFormSerializer, ScriptSerializer
from .models import Script
from rest_framework import status

@api_view(['GET'])
def test(request):
    person = {'name':'Dennis', 'age': 100}
    return Response(person)


def report(request):
    pdf_path = os.path.join(os.path.dirname(__file__), 'test.pdf')
    response = FileResponse(open(pdf_path, 'rb'), as_attachment=True, content_type='application/pdf')
    return response

@api_view(['POST'])
def string(request):
    string1 = request.data["string1"]
    string2 = request.data["string2"]
    string3 = string1 + string2
    print(request.data)
    return Response(string3)

@api_view(['POST'])
def settings(request):
    serializer = MyFormSerializer(data = request.data)
    if serializer.is_valid():
        file = request.data["file"]
        if request.data["username"] == "chinkin" and request.data["password"] == "password":
            return Response("you gave me this file: " + file.name + ". it has a size of: " + str(file.size))
        else:
            return Response("womp womp")
    else:
        return Response(serializer.errors, status=400)
    
@api_view(['GET','POST'])
def script_list(request):
    if request.method == 'GET':
        scripts = Script.objects.all()
        serializer = ScriptSerializer(scripts, many=True)
        return JsonResponse({"scripts": serializer.data})
    if request.method == 'POST':
        serializer = ScriptSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
