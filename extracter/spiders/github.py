import requests
import pydash as py_
from bs4 import BeautifulSoup

URL = 'https://github.com/{}?tab=repositories'

class APIFailedExeption(Exception):
    "Unable to fetch data from github.com"
    pass

def fetchRepos(username):
    # use `public forked` and `public source` to find forked and user repos

    url = URL.format(username)
    session = requests.Session()
    response = session.get(url)

    if response.status_code != 200:
        raise APIFailedExeption

    soup = BeautifulSoup(response.content, 'html.parser')
    repos = soup.find_all('li', {'class': "col-12 d-flex flex-justify-between width-full py-4 border-bottom color-border-muted public source"}) or []

    return repos

def parseRepos(repos):
    parsed_repos = []
    for repo in repos:
        name = False
        link = False
        repo_soup = BeautifulSoup(str(repo), 'html.parser')
        repo_name_link = repo_soup.find('a', {'itemprop': 'name codeRepository'})
        descp = repo_soup.find('p', {'itemprop': 'description'})
        language_soup = repo_soup.find("span", {"itemprop": "programmingLanguage"})
        language = BeautifulSoup(str(language_soup), 'html.parser')

        if repo_name_link and repo_name_link.attrs and "href" in repo_name_link.attrs:
            link = repo_name_link.attrs["href"]

        if repo_name_link and repo_name_link.get_text():
            name = repo_name_link.get_text().strip()
        
        if language and language.get_text():
            language = language.get_text()
        else:
            language = False

        if descp and descp.get_text():
            descp = descp.get_text().strip()
        else:
            descp = False

        parsed_repos.append({"name": name, "description": descp, "link": "https:github.com" + link, "language": language})

    return parsed_repos

def fetch(username):
    if not username:
        return "Missing field:username"

    repos = fetchRepos(username)
    parsed_repos = parseRepos(repos)

    group_by_language = py_.group_by(parsed_repos, "language")
    group_by_language_count = {}

    for key in group_by_language:
        value = group_by_language[key]
        group_by_language_count[key] = {"count": len(value), "repos": value}
    
    return group_by_language_count