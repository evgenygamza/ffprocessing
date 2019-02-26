from django.shortcuts import render


def index(request):
    return render(request, 'mainApp/homePage.html')


def contacts(request):
    return render(request, 'mainApp/basic.html', {'values': ['Для связи можно использовать телефон или почту:',
                                                             '+7 926 886-18-55', 'evgeny.gamza@gmail.com']})


def news(request):
    return render(request, 'mainApp/basic.html', {'values': ['Here interesting news are expected to be']})
