from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def test(request):
    person = {'name':'Dennis', 'age': 100}
    return Response(person)
