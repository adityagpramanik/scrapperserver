from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .spiders import github as _github
from .helpers.fileextracter import extractTextFromPDFFile

@csrf_exempt
def github(request):
	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			if not data['username']:
				return JsonResponse({'error': 'Invalid username'}, status=403)
			return JsonResponse(_github.fetch(data['username']))
		except json.JSONDecodeError:
			return JsonResponse({'error': 'Invalid JSON'}, status=403)
	elif request.method == 'GET':
		try:
			username = request.GET['username']
			if not username:
				return JsonResponse({'error': 'Invalid username'}, status=403)
			
			result = _github.fetch(username)
			return JsonResponse(result)
		except:
			return JsonResponse({'error': 'Invalid JSON'}, status=403)
	else:
		return JsonResponse({'error': 'Method not allowed for this endpoint'}, status=405)

@csrf_exempt
def extractResume(request):
	if request.method !=  'POST':
		return JsonResponse({'error': 'Method not allowed for this endpoint'}, status=405)

	resume = request.FILES['file']
	return JsonResponse({"result": extractTextFromPDFFile(resume)})