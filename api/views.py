import os
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import FileResponse
from .serializers import AddressChangeSerializer
from .services.AddressCorrectionBot import AddressCorrectionBot
from .services.simple_csv_reader import SimpleCSVReader
from django.core.files.storage import default_storage
from django.conf import settings
import zipfile
from rest_framework import status
from wsgiref.util import FileWrapper
import mimetypes

class FileCleanupResponse(FileResponse):
    def __init__(self, *args, cleanup_files=[], **kwargs):
        super().__init__(*args, **kwargs)
        self.cleanup_files = cleanup_files

    def close(self):
        super().close()
        for filepath in self.cleanup_files:
            os.remove(filepath)

@api_view(['POST'])
def address_change(request):
    serializer = AddressChangeSerializer(data=request.data)
    if serializer.is_valid():
        cartonfile = request.data['cartonfile']
        fedexinvoice = request.data['fedexinvoice']
        
        cartonfile_path = default_storage.save('tmp_cartonfile.csv', cartonfile)
        fedexinvoice_path = default_storage.save('tmp_fedexinvoice.csv', fedexinvoice)

        bot = AddressCorrectionBot.AddressCorrectionBot(cartonfile_path, fedexinvoice_path)
        result_paths = bot.process_files()
        
        zip_filename = "result_files.zip"
        zip_filepath = os.path.join(settings.MEDIA_ROOT, zip_filename)

        with zipfile.ZipFile(zip_filepath, 'w') as zip_file:
            for path in result_paths:
                zip_file.write(path, arcname=os.path.basename(path))
                os.remove(path)

        default_storage.delete(cartonfile_path)
        default_storage.delete(fedexinvoice_path)

        # Open the file without a `with` statement
        f = open(zip_filepath, 'rb')
        response = FileCleanupResponse(f, as_attachment=True, filename=zip_filename, cleanup_files=[zip_filepath])

        return response

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
