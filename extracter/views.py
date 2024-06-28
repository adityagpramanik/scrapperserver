from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .spiders import github as _github

@csrf_exempt
def github(request):
	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			if not data['username']:
				return JsonResponse({'error': 'Invalid username'}, status=400)
			return JsonResponse(_github.fetch(data['username']))
		except json.JSONDecodeError as e:
			return JsonResponse({'error': 'Invalid JSON'}, status=400)
	elif request.method == 'GET':
		try:
			username = request.GET['username']
			if not username:
				return JsonResponse({'error': 'Invalid username'}, status=400)
			
			result = _github.fetch(username)
			return JsonResponse(result)
		except:
			return JsonResponse({'error': 'Invalid JSON'}, status=400)
	else:
		return JsonResponse({'error': 'Only POST method allowed'}, status=405)