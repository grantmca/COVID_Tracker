from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Case, Person, Test
from .forms import PersonModelForm, TestFormset, CaseFormset, CloseFormset, ManagerFormset
from django.contrib import messages




def index(request):
    persons = Person.objects.all()
    context = {
        'persons': persons,
    }
    return render(request, 'index.html', context)

def display_all(request):
    # test = Person.objects.all()
    # items = Case.objects.all()
    persons = Person.objects.all()
    context = {
        'persons' : persons,
    }
    return render(request, 'index.html', context)


def add_case(request):
    template_name = 'add_case.html'
    if request.method == "GET":
        personform = PersonModelForm(request.GET or None)
        caseformset = CaseFormset(queryset=Case.objects.none(), prefix="case")
        testformset = TestFormset(queryset=Test.objects.none(), prefix="test")
        closeformset = CloseFormset(queryset=Person.objects.none())
        managerformset= ManagerFormset(queryset=Person.objects.none() ,prefix="manager")
    elif request.method == 'POST':
        personform = PersonModelForm(request.POST)
        caseformset = CaseFormset(request.POST, prefix="case")
        testformset = TestFormset(request.POST, prefix="test")
        closeformset = CloseFormset(request.POST)
        managerformset = ManagerFormset(request.POST, prefix="manager")
        print('This is intreresting')
        if personform.is_valid() and caseformset.is_valid() and testformset.is_valid() and managerformset.is_valid():
            print("Just anothe test")
            for form in testformset:
                test = form.save()
                print("the test was saved")
                print(test)
            for form in caseformset:
                case = form.save()
                print("The case")
                print(case)
                case.Test_Case.add(test)
                case.save()

            for form in managerformset:
                print("Thsi si the name things" + form.cleaned_data['name'])
                if Person.objects.filter(name=form.cleaned_data['name']).exists():
                    print("It is equal!")
                    case.manager = Person.objects.get(name=form.cleaned_data['name'])
                    case.save()
                else:
                    print("YEP YEP YEP")
                    manager = form.save()
                    case.manager = manager
                    case.save()


            if closeformset.is_valid():
                print("closeformset is valid")
                for form in closeformset:
                    print("Thsi si the name things" + form.cleaned_data['name'])
                    if Person.objects.filter(name=form.cleaned_data['name']).exists():
                        print("It is equal!")
                        case.close_contact.add(Person.objects.get(name=form.cleaned_data['name']))
                        case.save()
                    else:
                        print("YEP YEP YEP")
                        close = form.save()
                        case.close_contact.add(close)
                        case.save()
            else:
                print(closeformset.errors)


            if Person.objects.filter(name=personform.cleaned_data['name']).exists():
                case.team_member = Person.objects.get(name=personform.cleaned_data['name'])
                case.save()
            else:
                person = personform.save()
                person.Team_Member.add(case)
                person.save()
            return redirect('index')

        else:
            print(personform.errors)
            print(caseformset.errors)
            print(testformset.errors)
            print(managerformset.errors)
            print("Error Reached")
            return redirect('index')


    return render(request, template_name, {
        'personform' : personform,
        'caseformset' : caseformset,
        'testformset': testformset,
        'closeformset': closeformset,
        'managerformset': managerformset,
        })


# def add_person(request):
#     if request.method == "POST":
#         form = PersonForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#             return redirect('add_case')
#
#
#     else:
#         form = PersonForm()
#         return render(request, 'add_person.html', {'form' : form})
#
#
# def add_test(request):
#     if request.method == "POST":
#         form = TestForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#             return redirect('add_case')
#
#
#     else:
#         form = TestForm()
#         return render(request, 'add_person.html', {'form' : form})