from pdfminer.high_level import extract_text
import pydash as _
from io import BytesIO
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
	resume = resume.read()
	text = extract_text(pdf_file=BytesIO(resume))

	return JsonResponse({"result": _.compact(text.split('\n'))})
	