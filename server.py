import os, re
from datetime import date
from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__, static_folder='.')
TAVILY_KEY = os.getenv('TAVILY_API_KEY', '').strip()

@app.get('/')
def home():
    return send_from_directory('.', 'index.html')

@app.post('/api/opportunities/search')
def search_opportunities():
    if not TAVILY_KEY:
        return jsonify(error='Live search is not configured yet. Add a TAVILY_API_KEY to the server environment; see README.'), 503
    p = request.get_json(force=True) or {}
    age = int(p.get('age') or 0)
    gender = p.get('gender', '')
    state = p.get('state', '')
    education = p.get('education', '')
    field = p.get('field', '')
    year = p.get('year', '')
    income = p.get('income', '')
    interest = p.get('interest', 'All opportunities')
    keywords = p.get('keywords', '')
    q = f'''Find currently open or upcoming opportunities in India as of {date.today().isoformat()}: {interest}. Candidate: age {age}, gender {gender}, state {state}, education/status {education}, field {field}, year {year}, family income {income}, skills {keywords}. Include only opportunities whose published eligibility plausibly includes this profile. Exclude opportunities explicitly restricted to a different gender. Prioritize official government, university, company, foundation and organizer pages. Return current application deadlines and original source URLs. Do not include expired calls.'''
    try:
        res = requests.post('https://api.tavily.com/search', json={
            'api_key': TAVILY_KEY, 'query': q, 'search_depth': 'advanced',
            'topic': 'general', 'max_results': 12, 'include_answer': False,
            'include_raw_content': False
        }, timeout=35)
        res.raise_for_status()
        data = res.json()
    except requests.RequestException as exc:
        return jsonify(error='The live search provider could not be reached. Please try again.'), 502
    results=[]
    for item in data.get('results', []):
        title=item.get('title','').strip()
        url=item.get('url','')
        content=item.get('content','').strip()
        if not title or not url.startswith(('https://','http://')): continue
        # Do not label a listing eligible just because it appeared in search.
        text=(title+' '+content).lower()
        if gender.lower() == 'male' and re.search(r'\b(women[- ]only|female[- ]only|girls? (?:students?|candidates?)|women (?:students?|candidates?|founders?|entrepreneurs?)|female (?:students?|candidates?|founders?))\b', text):
            continue
        deadline_match=re.search(r'(?:deadline|last date|closes?|apply by)\s*[:\-]?\s*([^.;\n]{3,55})', content, re.I)
        deadline=deadline_match.group(1).strip() if deadline_match else 'Not stated in search excerpt — verify on official page'
        domain=re.sub(r'^www\.', '', requests.utils.urlparse(url).netloc)
        results.append({
            'title':title, 'organization':domain, 'domain':domain,
            'description':content[:700], 'url':url, 'deadline':deadline,
            'location':'India (confirm regional restrictions)',
            'type':'Opportunity',
            'match_note':'Potential relevance — verify full eligibility'
        })
    return jsonify(results=results, searched_at=date.today().isoformat())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT','8000')), debug=False)
