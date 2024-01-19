from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .model.functions import predict_image_from_base64
import json

@csrf_exempt
@require_POST
def analyze_image(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        image_data = data.get('image')

        # Здесь вызывайте функцию из вашего модуля, передавая ей image_data и model
        result = predict_image_from_base64(image_data)

        return JsonResponse(result, safe = False)
    except Exception as e:
        # Обработка ошибок с выводом подробной информации
        import traceback
        traceback_str = traceback.format_exc()
        print(f"Error in analyze_image: {e}\n{traceback_str}")
        return JsonResponse({'error': f"Internal Server Error: {e}"}, status=500)
