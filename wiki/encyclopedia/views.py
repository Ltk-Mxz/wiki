from django.shortcuts import render, redirect
from . import util
import markdown2
import random


def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(content)
    })


def search(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()
    if query in entries:
        return redirect('entry', title=query)
    
    results = [entry for entry in entries if query.lower() in entry.lower()]
    
    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "results": results
    })


def new_page(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        if util.get_entry(title):
            return render(request, "encyclopedia/new_page.html", {
                "error": "An entry with this title already exists."
            })
        util.save_entry(title, content)
        return redirect('entry', title=title)
    return render(request, "encyclopedia/new_page.html")


def edit_page(request, title):
    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(title, content)  # Sauvegarde les modifications
        return redirect('entry', title=title)
    
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content
    })


def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)

    return redirect('entry', title=title)