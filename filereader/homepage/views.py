from django.shortcuts import render, redirect

import json
from datetime import datetime
from homepage.models import DataTable


def upload(request):
    if request.method == "POST":
        errors = []
        db_list = []
        json_file = request.FILES.get("json_file")
        if not json_file:
            return render(
                request,
                "homepage/upload.html",
                {"errors": ["No file selected"]},
            )
        results = json.load(json_file)
        for i, dictionary in enumerate(results):
            if "name" not in dictionary or "date" not in dictionary:
                errors.append(f"wrong json form line {i}")
            elif len(dictionary["name"]) >= 50:
                errors.append(f"name field too long (50+ symbols) line {i}")
            else:
                try:
                    datetime.strptime(dictionary["date"], "%Y-%m-%d_%H:%M")
                except ValueError:
                    errors.append(f"wromg date field form line {i}")
                else:
                    db_list.append(dictionary)
        if errors:
            return render(request, "homepage/upload.html", {"errors": errors})
        else:
            for d in db_list:
                DataTable.objects.create(
                    name=d["name"],
                    date=d["date"],
                )
            return redirect("homepage:tableview")
    return render(request, "homepage/upload.html")


def tableview(request):
    items = DataTable.objects.all()
    return render(request, "homepage/datatable.html", {"items": items})
