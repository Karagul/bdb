from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import CommentForm, SearchForm, LoginForm, UploadForm
from .models import BondIssue, Country, Currency, Comment


RECORDS_ON_PAGE = 6 


def bonds_list(request):
    records = BondIssue.active.all()

    paginator = Paginator(records, RECORDS_ON_PAGE) # Число записей на странице
    page = request.GET.get('page')
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)

    return render(request, 'core/list.html', {'records': records, 'page': page})


def bonds_detail(request, isin):
    record = get_object_or_404(BondIssue, ISIN=isin)
    comments = record.comments.filter(active=True) # использует related field 'comments'

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Добавить привязку к user, чтобы не приходилось вводить имя
            new_comment = comment_form.save(commit=False)
            new_comment.record = record
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    return render(request, 'core/detail.html', {'record': record,
                                                'comments': comments,
                                                'new_comment': new_comment,
                                                'comment_form': comment_form })

def bonds_search(request):
    search_string = request.GET.get('search_string')
    ordered_by = request.GET.get('ordered_by')
    descending = request.GET.get('descending')
    
    if search_string:
        
        search_results = BondIssue.active.filter(
            IssuerCompany__icontains=search_string).order_by('-'*int(descending=='on') + ordered_by)
        search_form = SearchForm()

        paginator = Paginator(search_results, RECORDS_ON_PAGE) # Число записей на странице
        page = request.GET.get('page')
        try:
            search_results = paginator.page(page)
        except PageNotAnInteger:
            search_results = paginator.page(1)
        except EmptyPage:
            search_results = paginator.page(paginator.num_pages)
        search_done = True    
        

    else: # Если поиск не запускался
        search_form = SearchForm()
        search_done = search_results = page = None
        search_string = None

    return render(request, 'core/search.html', {'search_form': search_form,
                                                'search_string': search_string,
                                                'search_done': search_done,
                                                'search_results': search_results,
                                                'page': page,
                                                'ordered_by': ordered_by,
                                                'descending': descending,
                                                })


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    logged_status = 'Авторизация успешна'
                    form = LoginForm()
                    return render(request, 'core/login.html', {'form': form, 'logged_status': logged_status})
                else:
                    logged_status = 'Аккаунт не активирован'
                    return render(request, 'core/login.html', {'form': form, 'logged_status': logged_status})
            else:
                logged_status = 'Неверный логин/пароль'
                return render(request, 'core/login.html', {'form': form, 'logged_status': logged_status})

    else: # Перед авторизацией
        form = LoginForm()
        logged_status = None
    return render(request, 'core/login.html', {'form': form, 'logged_status': logged_status})

def user_logout(request):
    logout(request)
    return redirect('/')


def data_loader(request):
    if request.method == 'POST':
        upload_form = UploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            file_uploaded = True
            if handle_uploaded_file(request.FILES['file_']):
                database_response = "Загружено в базу"
            else:
                database_response = "Загрузка в базу не удалась"
            return render(request, 'core/loader.html', {'upload_form': upload_form,
                                                        'file_uploaded': file_uploaded,
                                                        'database_response': database_response})

    else:
        upload_form = UploadForm()
        file_uploaded = False
        return render(request, 'core/loader.html', {'upload_form': upload_form, 'file_uploaded': file_uploaded})

def handle_uploaded_file(fh):
    # Временный файл
    with open('temporary_upload.csv', 'wb+') as destination:
        for chunk in fh.chunks():
            destination.write(chunk)
    date_transform = lambda x: '-'.join(x.split('.')[::-1])
    float_transform = lambda x: 0 if not x else float(x)
    
    # Обработка csv и загрузка в базу
    infile = open('temporary_upload.csv','r')
    # outfile = open('loader_log.txt', 'w')
    
    for line in infile:
        data = line.strip().split(";")
        
        # try:
        new_record = BondIssue( ISIN=data[0],
                                IssuerCompany=data[1],
                                Ticker=data[2],
                                Coupon=data[3],
                                Maturity=date_transform(data[4]), 
                                MaturityType=data[5],
                                Currency=Currency.objects.get(abbr=data[6]),
                                Source=data[7],
                                Moody=data[8],
                                Sp=data[9],
                                Fitch=data[10],
                                BloombergCompositeRating=data[11],
                                Announce=date_transform(data[12]),
                                CollateralType=data[13],
                                Country=Country.objects.get(abbr=data[14]),
                                IssueDate=date_transform(data[15]),
                                OutstandingAmount =data[16],
                                IssuedAmount=data[17],
                                Underwriter=data[18],
                                MinimumPiece=data[19],
                                BidPrice=float_transform(data[20]),
                                BidYTM=float_transform(data[21]),
                                BidMDuration=float_transform(data[22]),
                                Archived=False
                            )
        new_record.save()
        # except Exception:
        #   print("...", file=outfile)
        #    return False

    infile.close()
    # Удалить временный
    # outfile.close()

    return True
