from django.shortcuts import render, HttpResponse

# Create your views here.

def prod(request):
    if request.method == "POST":
        number = request.POST["number"]
        test = search(number)
        return render(request, "sms/result.html", {"sms": test})
    else:
        return render(request, "sms/sms.html")

def search(phone_number):
    list1 = []
    n = 1
    with open(r"D:\nohup.out", "r", encoding='UTF-8') as f:
        t = f.readlines()
        sms = []
        for i in t:
            if phone_number in i:
                sms.append(i)
    for i in sms:
        dict1 = {}
        dict1.update({"index": n})
        dict1.update({"data": i[0:23]})
        dict1.update({"text": i[25:]})
        list1.append(dict1)
        n += 1
    return list1