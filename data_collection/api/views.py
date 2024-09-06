from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def submit_data(request):
    if request.method == "POST":
        try:
            # 解析请求体中的 JSON 数据
            data = json.loads(request.body)
            print("收到的数据:", data)
            # 处理数据（例如保存到数据库）
            return JsonResponse({"message": "数据已成功提交！"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "无效的数据格式"}, status=400)
    return JsonResponse({"error": "仅支持POST请求"}, status=405)
