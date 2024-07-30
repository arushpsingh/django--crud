from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
import io
from rest_framework.parsers import JSONParser
from .models import Student
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from rest_framework.exceptions import ParseError
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt
def student_api(request):
    if request.method == 'GET':
        id = request.GET.get('id', None)
        if id is not None:
            try:
                student = Student.objects.get(id=id)
                serializer = StudentSerializer(student)
                return JsonResponse(serializer.data, safe=False)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Student not found'}, status=404)
        else:
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
        except ValueError:
            return HttpResponseBadRequest('Invalid JSON')

        serializer = StudentSerializer(data=json_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({ 'msg': 'Data created'}, status=201)

        return JsonResponse(serializer.errors, status=400)

    if request.method == 'PUT':
        try:
            json_data = json.loads(request.body)
        except ValueError:
            return HttpResponseBadRequest('Invalid JSON')

        id = json_data.get('id')
        if not id:
            return HttpResponseBadRequest('ID is required')

        try:
            student = Student.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse({ 'error': 'Student not found'}, status=404)

        serializer = StudentSerializer(student, data=json_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({ 'msg': 'Data updated' }, status=200)

        return JsonResponse(serializer.errors, status=400)

    if request.method == 'DELETE':
        try:
            json_data = json.loads(request.body)
        except ValueError:
            return HttpResponseBadRequest('Invalid JSON')

        id = json_data.get('id')
        if not id:
            return HttpResponseBadRequest('ID is required')

        try:
            student = Student.objects.get(id=id)
            student.delete()
            return JsonResponse({'msg': 'Data deleted'})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)

    return JsonResponse({'error': 'Method not allowed'}, status=405)