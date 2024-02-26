import os
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import FileResponse
from .serializers import AddressChangeSerializer
from .services.AddressCorrectionBot import AddressCorrectionBot
from django.core.files.storage import default_storage
from django.conf import settings
import zipfile
from rest_framework import status
from wsgiref.util import FileWrapper
import mimetypes

@api_view(['POST'])
def address_change(request):
    serializer = AddressChangeSerializer(data=request.data)
    if serializer.is_valid():
        cartonfile = request.FILES['cartonfile']
        fedexinvoice = request.FILES['fedexinvoice']
        
        # Save uploaded files temporarily
        cartonfile_path = default_storage.save('tmp_cartonfile.csv', cartonfile)
        fedexinvoice_path = default_storage.save('tmp_fedexinvoice.csv', fedexinvoice)
        
        # Instantiate and run your bot
        bot = AddressCorrectionBot(cartonfile_path, fedexinvoice_path)
        result_paths = bot.process_files()
        
        # Create a zip file to hold all the result files
        zip_filename = "result_files.zip"
        zip_filepath = os.path.join(settings.MEDIA_ROOT, zip_filename)
        with zipfile.ZipFile(zip_filepath, 'w') as zip_file:
            for path in result_paths:
                # Add file to the zip file
                zip_file.write(path, arcname=os.path.basename(path))
                
                # Optionally delete the file after adding it to the zip if you want to clean up
                os.remove(path)

        # Clean up the uploaded files
        default_storage.delete(cartonfile_path)
        default_storage.delete(fedexinvoice_path)

        # Prepare the zip file for download
        with open(zip_filepath, 'rb') as f:
            file_data = FileWrapper(f)
            content_type = mimetypes.guess_type(zip_filepath)[0]
            response = Response(file_data, content_type=content_type)
            response['Content-Length'] = os.path.getsize(zip_filepath)
            response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
            
            # Optionally delete the zip file after sending it if you want to clean up
            os.remove(zip_filepath)

        return response

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
