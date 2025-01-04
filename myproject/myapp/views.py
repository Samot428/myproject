from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import CreateNewList
from .models import ToDoList

def HomePage(request):
    return render(request, 'HomePage.html')

def list_view(response):
    """
    User can view his ToDoLists.\n 
    He can create them and delete them with buttons (delete button won't show if none of the list is made).\n

    """
    if response.method == "POST":
        if response.POST.get("Delete"):
            for td in response.user.todolist.all():
                if response.POST.get(f"check{td.name}") == "clicked":
                    td.delete()
            return HttpResponseRedirect("/app/ToDoList/")
        elif response.POST.get("Create"):
            form = CreateNewList(response.POST)

            if form.is_valid():
                n = form.cleaned_data["name"]
                t = ToDoList(name=n)
                t.save()
                response.user.todolist.add(t)  # Use the related_name 'todolists'

            return HttpResponseRedirect("/app/ToDoList/")
        else:
            # Example of using the get method to retrieve a specific ToDoList instance
            try:
                todolist = ToDoList.objects.get(id=1)  # Replace with the appropriate filter
            except ToDoList.DoesNotExist:
                todolist = None

            return render(response, 'ToDoList.html', {'todolist': todolist})

    return render(response, "ToDoList.html", {"form": CreateNewList})

def items_view(response, id):
    """User sees the items of the list he has already made. \n
    He can mark them as completed or delete them.\n
    """
    ls = ToDoList.objects.get(id=id)

    if ls in response.user.todolist.all():
        if response.POST.get("save"):
            for item in ls.item_set.all():
                if response.POST.get("c"+str(item.id)) == "clicked":
                    item.completed = True
                else:
                    item.completed = False
                item.save()
                if response.POST.get("new-item"+str(item.id)+"-text") != item.text:
                    txt = response.POST.get("new-item"+str(item.id)+"-text")
                    item.text = txt
                    item.save()
        elif response.POST.get("Delete"):
            for item in ls.item_set.all():
                if response.POST.get("c"+str(item.id)) == "clicked":
                    item.delete()
        elif response.POST.get("newItem"):
            txt = response.POST.get("new")
            if len(txt) > 2:
                ls.item_set.create(text=txt, completed=False)
            else:
                print("invalid")
            return HttpResponseRedirect(f"/app/{ls.id}")
    return render(response, "TDLItem.html", {"ls":ls})