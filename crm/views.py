from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from .utils import render_to_pdf
from django.core.mail import send_mail, EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


now = timezone.now()


def home(request):
    return render(request, 'crm/home.html', {'crm': home})


@login_required
def customer_list(request):
    customer_list = Customer.objects.filter(created_date__lte=timezone.now())
    paginator = Paginator(customer_list, 2)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        customer = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        customer = paginator.page(paginator.num_pages)
    return render(request, 'crm/customer_list.html', {'customers': customer, 'page': page})


@login_required
def customer_list_order(request, orderby):
    order = request.GET.get('orderby')
    order_name = 'cust_name'
    if order == 'cust_name':
        order_name = 'cust_name'
    elif order == 'email':
        order_name = 'email'

    customer_list = Customer.objects.order_by(order_name)
    paginator = Paginator(customer_list, 2)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        customer = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        customer = paginator.page(paginator.num_pages)
    return render(request, 'crm/customer_list.html', {'customers': customer, 'page': page})



@login_required
def customer_new(request):
    form = CustomerForm(request.POST or None)
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
           customer = form.save(commit=False)
           customer.created_date = timezone.now()
           customer.save()
           customers = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/customer_list.html', {'customers': customers})
    else:
        form = CustomerForm()
       # print("Else")
    return render(request, 'crm/customer_new.html', {'form': form})




@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None)
    if request.method == "POST":
        # update
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.updated_date = timezone.now()
            customer.save()
            customer = Customer.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/customer_list.html', {'customers': customer})
        else:
            # edit
            form = CustomerForm(instance=customer)
    return render(request, 'crm/customer_edit.html', {'form': form})


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('crm:customer_list')


@login_required
def service_list(request):
    services = Service.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/service_list.html', {'services': services})


@login_required
def service_new(request):
    form = ServiceForm(request.POST or None)
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
           service = form.save(commit=False)
           service.created_date = timezone.now()
           service.save()
           services = Service.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/service_list.html',
                         {'services': services})
    else:
        form = ServiceForm()
       # print("Else")
    return render(request, 'crm/service_new.html', {'form': form})


@login_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    form = ServiceForm(request.POST or None)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            service = form.save()
            # service.customer = service.id
            service.updated_date = timezone.now()
            service.save()
            services = Service.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/service_list.html', {'services': services})
        else:
            # print("else")
            form = ServiceForm(instance=service)
    return render(request, 'crm/service_edit.html', {'form': form})


@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    return redirect('crm:service_list')


@login_required
def product_list(request):
    products = Product.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/product_list.html', {'products': products})


@login_required
def product_new(request):
    form = (request.POST or None)
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
           product = form.save(commit=False)
           product.created_date = timezone.now()
           product.save()
           products = Product.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/product_list.html',
                         {'products': products})
    else:
        form = ProductForm()
       # print("Else")
    return render(request, 'crm/product_new.html', {'form': form})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            # service.customer = service.id
            product.updated_date = timezone.now()
            product.save()
            products = Product.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/product_list.html', {'products': products})
        else:
            # print("else")
            form = ProductForm(instance=product)
    return render(request, 'crm/product_edit.html', {'form': form})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Service, pk=pk)
    product.delete()
    return redirect('crm:product_list')


@login_required
def summary(request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customers = Customer.objects.filter(created_date__lte=timezone.now())
        services = Service.objects.filter(cust_name=pk)
        products = Product.objects.filter(cust_name=pk)
        sum_service_charge = Service.objects.filter(cust_name=pk).aggregate(Sum('service_charge'))
        sum_product_charge = Product.objects.filter(cust_name=pk).aggregate(Sum('charge'))
        return render(request, 'crm/summary.html', {'customers': customers,
                                                    'customer': customer,
                                                    'products': products,
                                                'services': services,
                                                'sum_service_charge': sum_service_charge,
                                                'sum_product_charge': sum_product_charge, })


def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('crm:home')
    return render(request, 'registration/login_form.html', {'form': form, 'title': title})


def register_view(request):
    title = 'Register'
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('crm:home')

    context = {
        "form": form,
        "title": title
    }
    return render(request, "registration/login_form.html", context)


def logout_view(request):
    logout(request)
    return redirect('crm:home')



def admin_summary_pdf(request, pk):
    # Task to send an e-mail notification when an order is successfully created.
    customer = get_object_or_404(Customer, pk=pk)
    subject = 'Order nr. {}'.format(customer.cust_name)
    message = 'Dear {},\n\nYou have successfully placed an order.\
               Find the attached order invoice.'

    subject = 'Order Confirmation : ' + str(customer.cust_name)

    # mail_sent = send_mail(subject, message,'mavstaruno@gmail.com', [order.email]) #mavstaruno/@mavstar123
    print("Before generating PDF")
    summarypdf = generate_summary_pdf(request, pk)
    summaryFileName = 'Summary_' + str(customer.cust_name) + '.pdf'
    msg = EmailMessage(subject, message, from_email="mavstaruno@gmail.com", to=['manushah@unomaha.edu'])
    msg.attach(summaryFileName, summarypdf, 'application/pdf')
    # msg.content_subtype = "html"
    msg.send()
    print("After sending PDF")
    # return mail_sent
    return redirect('crm:home')


def generate_summary_pdf(request, pk):
    print(pk)
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    services = Service.objects.filter(cust_name=pk)
    products = Product.objects.filter(cust_name=pk)
    sum_service_charge = Service.objects.filter(cust_name=pk).aggregate(Sum('service_charge'))
    sum_product_charge = Product.objects.filter(cust_name=pk).aggregate(Sum('charge'))

    template = get_template('crm/pdf.html')
    context = {'customers': customers, 'products': products, 'customer': customer,
               'services': services,
               'sum_service_charge': sum_service_charge,
               'sum_product_charge': sum_product_charge, }
    html = template.render(context)
    pdf = render_to_pdf('crm/pdf.html', context)
    if pdf:
        response=  HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename= "order_{}.pdf"'.format(customer.cust_name)
        #return response
        #return HttpResponse(pdf, content_type='application/octet-stream')
        return pdf
    return HttpResponse("Not Found")

