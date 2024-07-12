from django.shortcuts import render
import io
from rest_framework.parsers import JSONParser
from .models import Student
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from rest_framework.exceptions import ParseError

# Create your views here.

def student_api(request):
    if not request.body:
            return JsonResponse({'error': 'Request body is empty'}, status=400)
        
    try:
        stream = io.BytesIO(request.body)
        python_data = JSONParser().parse(stream)
    except ParseError as e:
        return JsonResponse({'error': str(e)}, status=400)
    
    if request.method == 'GET':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)

        id = python_data.get('id', None)
        if id is not None:
            student = Student.objects.get(id = id)
            serializer = StudentSerializer(student)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')
        
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')
