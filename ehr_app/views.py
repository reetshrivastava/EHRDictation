import re

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

category_titles = ["SUBJECTIVE", "OBJECTIVE", "ASSESSMENT AND PLAN", "ENDDOCUMENT"]

# Create your views here.
def string_contains_title(search_string, begin_title):
    if any(exclude in search_string and exclude != begin_title for exclude in category_titles):
        return True
    return False
	
def index(request):
    return render(request, 'webspeechdemo.html', {})
    
@csrf_exempt
def process_to_file(request):

    notes = request.POST.get('text').lower()

    categorized_dict = {}

    for begin_title in category_titles:
        for end_title in category_titles:
            if begin_title != end_title:
                regex_search_string = "{0}:?((.|\n)*?){1}".format(begin_title, end_title)
                m = re.search(regex_search_string, notes, re.IGNORECASE)
                if m:
                    if not string_contains_title(m.group(1), begin_title):
                        categorized_dict[begin_title] = m.group(1)
                      
    content = ''
		        
    #file = open('clean_op.txt', 'w')
    for section in categorized_dict:
        content += section + ':' + categorized_dict[section].replace("\n", " ")
        content += '\n\n'
    #file.close()
    
    if not content:
        content = request.POST.get('text')
    
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment;filename="ehr_file"'
    return response
