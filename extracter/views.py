from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .spiders import github as _github
from .helpers.fileextracter import extractTextFromPDFFile
from .helpers.gemini import analyseResumeText
import requests
import io

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

	# process file from request body url
	if request.body:
		data = json.loads(request.body)
	if "url" not in data:
		return JsonResponse({'error': 'URL not present.'}, status=403)

	file_response = requests.get(data['url'])
	if file_response.status_code not in [200, 201]:
		return JsonResponse({'error': 'Unable to fetch file from url, please try again with another url.'})

	resume = io.BytesIO(file_response.content)

	# process attached file in form data
	if request.FILES and request.FILES['file']:
		resume = request.FILES['file']

	resume_text = extractTextFromPDFFile(resume)
	result = analyseResumeText(resume_text)
	return JsonResponse({"result": result})