import os
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import CommentForm, SearchForm, LoginForm, UploadForm
from .models import BondIssue, Country, Currency, Comment


DEFAULT_RECORDS_ON_PAGE = 25
MOODY_RATINGS_RANKS = ('Aaa', 'Aa1', 'Aa2', 'Aa3', 'A1', 'A2', 'A3', 
                        'Baa1', 'Baa2', 'Baa3', 'Ba1', 'Ba2', 'Ba3', 'B1', 'B2', 'B3',
                        'Caa1', 'Caa2', 'Caa3', 'Ca', 'C')

###### Представления, связанные с выпусками
# Список
def bonds_list(request):
    RECORDS_ON_PAGE = request.GET.get('records_on_page') or DEFAULT_RECORDS_ON_PAGE
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

# Индивидуальный выпуск и комментарии к нему
def bonds_detail(request, isin):
    record = get_object_or_404(BondIssue, ISIN=isin)
    comments = record.comments.filter(active=True) # использует related field 'comments'

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid() and comment_form.cleaned_data['body']:
            new_comment = comment_form.save(commit=False)
            new_comment.record = record
            new_comment.save()
            
            # Привязка к user, автоматически подставляющая имя и почту
            comment_form = CommentForm(data={'name': request.user.username,
                                            'email': request.user.email or request.user.username + "@mail.com"})
    else:
        # Привязка к user, автоматически подставляющая имя и почту
        if request.user.is_authenticated:
            comment_form = CommentForm(data={'name': request.user.username,
                                             'email': request.user.email or request.user.username + "@mail.com"})
        else:
            comment_form = CommentForm()

    return render(request, 'core/detail.html', {'record': record,
                                                'comments': comments,
                                                'new_comment': new_comment,
                                                'comment_form': comment_form })

# Поиск выпусков
def bonds_search(request):
    search_params = {'search_string': request.GET.get('search_string'),
                    'ordered_by': request.GET.get('ordered_by'),
                    'descending': request.GET.get('descending'),
                    'maturity_start': request.GET.get('maturity_start'),
                    'maturity_end': request.GET.get('maturity_end'),
                    'coupon_min': request.GET.get('coupon_min'),
                    'coupon_max': request.GET.get('coupon_max'),
                    'search_currency': request.GET.get('search_currency'),
                    'rating_min': request.GET.get('rating_min'),
                    'rating_max': request.GET.get('rating_max'),
                    'records_on_page': request.GET.get('records_on_page')
                    }
    RECORDS_ON_PAGE = search_params['records_on_page'] or DEFAULT_RECORDS_ON_PAGE
    
    # Если поиск запускался
    if search_params['search_string'] or search_params['maturity_end']:

        # Группы валют
        if search_params['search_currency'] == "AUD":
            currency_group = ('AUD', 'NZD')
        elif search_params['search_currency'] == "HKD":
            currency_group = ('HKD', 'SGD')
        elif search_params['search_currency'] == "SEK":
            currency_group = ('SEK', 'NOK')
        elif search_params['search_currency'] == "ARS":
            currency_group = ('ARS', 'CLP', 'COP', 'MXN', 'PEN', 'PHP', 'UYU')
        elif search_params['search_currency'] == "ITL":
            currency_group = ('DEM', 'FRF', 'CZK', 'HRK', 'HUF', 'PLN', 'RON', 'ITL', 'SKK')
        elif search_params['search_currency'] == "KRW":
            currency_group = ('KRW', 'INR', 'MYR', 'IDR', 'GEL', 'KZT', 'TWD', 'TRY', 'ZAR')
        else:
            currency_group = (search_params['search_currency'],)
        
        # Группы рейтинга
        min_index = MOODY_RATINGS_RANKS.index(search_params['rating_min'])
        max_index = MOODY_RATINGS_RANKS.index(search_params['rating_max'])
        ratings_group = list(MOODY_RATINGS_RANKS[max_index:min_index+1])
        for rtng in tuple(ratings_group):
            ratings_group.append(rtng+" *-")
            ratings_group.append(rtng+" *+")
            
        # Фильтрация выдачи поиска
        search_results = BondIssue.active.filter(
            IssuerCompany__icontains=search_params['search_string']            
        ).filter(
            Maturity__range=(search_params['maturity_start'], search_params['maturity_end'])
        ).filter(
            Coupon__range=(search_params['coupon_min'], search_params['coupon_max'])
        ).filter(
            Currency__in=currency_group
        ).filter(
            Moody__in=ratings_group
        ).order_by('-'*int(search_params['descending']=='on') + search_params['ordered_by'])

        paginator = Paginator(search_results, RECORDS_ON_PAGE) # Число записей на странице
        page = request.GET.get('page')
        try:
            search_results = paginator.page(page)
        except PageNotAnInteger:
            search_results = paginator.page(1)
        except EmptyPage:
            search_results = paginator.page(paginator.num_pages)
        search_done = True
        search_form = SearchForm()

    else: # Если поиск не запускался
        search_form = SearchForm()
        search_done = search_results = page = None
        search_params = {}

    return render(request, 'core/search.html', {'search_form': search_form,
                                                'search_done': search_done,
                                                'search_results': search_results,
                                                'page': page,
                                                'search_params': search_params,
                                                })


##### Представления, связанные с авторизацией
# Логин
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

# Логаут
def user_logout(request):
    logout(request)
    return redirect('/')


##### Представления, связанные с загрузчиком
# Фронт загрузчика
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

# Бэк загрузчика
def handle_uploaded_file(fh):
    with open('temporary_upload.csv', 'wb+') as destination:
        for chunk in fh.chunks():
            destination.write(chunk)
    date_transform = lambda x: '-'.join(x.split('.')[::-1])
    float_transform = lambda x: 0 if not x else float(x)
    
    # Обработка csv и загрузка в базу
    infile = open('temporary_upload.csv','r')
    # outfile = open('loader_log.txt', 'w')
    
    for line in infile:
        data = line.strip().split("|")
        
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
    os.remove('temporary_upload.csv')
    # outfile.close()
    return True


##### Представления, связанные со статьями
# Список статей
# Индивидуальная статья








##### Представления, связанные с новостями
# Список новостей
# Индивидуальная новость
