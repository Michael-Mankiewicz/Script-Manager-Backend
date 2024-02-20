import os
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import FileResponse

@api_view(['GET'])
def test(request):
    person = {'name':'Dennis', 'age': 100}
    return Response(person)


def report(request):
    pdf_path = os.path.join(os.path.dirname(__file__), 'test.pdf')
    response = FileResponse(open(pdf_path, 'rb'), as_attachment=True, content_type='application/pdf')
    return response

