import decimal
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.db.models.functions import Round
from django.shortcuts import render
from django.template.loader import get_template

from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views, forms as auth_forms
from django.db.models import Sum
from .serializers import CustomerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.urls import reverse,reverse_lazy
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import CustomUser
from django.views import generic
from django.conf import settings
from django.http import HttpResponse
from twilio.rest import Client
from io import BytesIO
from xhtml2pdf import pisa

now = timezone.now()
def home(request):
   return render(request, 'portfolio/home.html',
                 {'portfolio': home})

@login_required
def customer_list(request):
    customer = Customer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'portfolio/customer_list.html',
                 {'customers': customer})

@login_required
def customer_edit(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   if request.method == "POST":
       # update
       form = CustomerForm(request.POST, instance=customer)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.updated_date = timezone.now()
           customer.save()
           return redirect('portfolio:customer_list')
   else:
        # edit
       form = CustomerForm(instance=customer)
   return render(request, 'portfolio/customer_edit.html', {'form': form})

@login_required
def customer_delete(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   customer.delete()
   return redirect('portfolio:customer_list')

@login_required
def stock_list(request):
   #stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
   stocks = Stock.objects.all()
   return render(request, 'portfolio/stock_list.html', {'stocks': stocks})

@login_required
def stock_edit(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   if request.method == "POST":
       form = StockForm(request.POST, instance=stock)
       if form.is_valid():
           stock = form.save()
           # stock.customer = stock.id
           stock.updated_date = timezone.now()
           stock.save()
           return redirect('portfolio:stock_list')
   else:
       # print("else")
       form = StockForm(instance=stock)
   return render(request, 'portfolio/stock_edit.html', {'form': form})

@login_required
def stock_delete(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   stock.delete()
   return redirect('portfolio:stock_list')

@login_required
def investment_list(request):
    investments = Investment.objects.all()
    return render(request, 'portfolio/investment_list.html', {'investments': investments})


@login_required
def investment_new(request):
    if request.method == "POST":
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.created_date = timezone.now()
            investment.save()
            return redirect('portfolio:investment_list')
    else:
        form = InvestmentForm()
        # print("Else")
    return render(request, 'portfolio/investment_new.html', {'form': form})

@login_required
def investment_edit(request, pk):
    investment = get_object_or_404(Investment, pk=pk)
    if request.method == "POST":
        form = InvestmentForm(request.POST, instance=investment)
        if form.is_valid():
            investment = form.save()
            investment.updated_date = timezone.now()
            investment.save()
            return redirect('portfolio:investment_list')
    else:
        # print("else")
        form = InvestmentForm(instance=investment)
    return render(request, 'portfolio/investment_edit.html', {'form': form})

@login_required
def investment_delete(request, pk):
   investment = get_object_or_404(Investment, pk=pk)
   investment.delete()
   return redirect('portfolio:investment_list')

@login_required
def stock_new(request):
   if request.method == "POST":
       form = StockForm(request.POST)
       if form.is_valid():
           stock = form.save(commit=False)
           stock.created_date = timezone.now()
           stock.save()
           stocks = Stock.objects.all()
           return render(request, 'portfolio/stock_list.html',
                         {'stocks': stocks})
   else:
       form = StockForm()
       # print("Else")
   return render(request, 'portfolio/stock_new.html', {'form': form})

@login_required
def customer_new(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_date = timezone.now()
            customer.save()
            customer = Customer.objects.all()
            #context= {'customers': customer}
            return redirect('portfolio:customer_list')
            #return redirect(reverse('portfolio:customer_list'),context)
            #return HttpResponseRedirect(reverse('portfolio:customer_list'), context)
    else:
        form = CustomerForm()
    return render(request, 'portfolio/customer_new.html', {'form': form})

@login_required
def portfolio(request,pk):
   customer = get_object_or_404(Customer, pk=pk)
   customers = Customer.objects.filter(created_date__lte=timezone.now())
   investments =Investment.objects.filter(customer=pk)
   stocks = Stock.objects.filter(customer=pk)
   sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
   sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
   #overall_investment_results = sum_recent_value-sum_acquired_value
   # Initialize the value of the stocks
   sum_current_stocks_value = 0.00
   sum_of_initial_stock_value = 0.00
   customer_phoneNumber = customer.cell_phone
   indianrupee_value = customer.indianrupee()
   gbp_value = customer.gbp()

   # Loop through each stock and add the value to the total
   for stock in stocks:
        currentvalue = float(stock.current_stock_price()) * float(stock.shares)
        sum_current_stocks_value += round(currentvalue,2)
        sum_of_initial_stock_value += round(float(stock.initial_stock_value()), 2)
        stock.current_stock_value = round(decimal.Decimal(stock.current_stock_price()) * decimal.Decimal(stock.shares),2)
        stock.result = round(decimal.Decimal(stock.current_stock_value) - decimal.Decimal(stock.initial_stock_value()), 2)
        stock.result_indianrupee = round((decimal.Decimal(stock.current_stock_value) - decimal.Decimal(stock.initial_stock_value())) * decimal.Decimal(indianrupee_value), 2)
        stock.result_gbp = round((decimal.Decimal(stock.current_stock_value) - decimal.Decimal(stock.initial_stock_value())) * decimal.Decimal(gbp_value), 2)

   sum_of_initial_investment_value = 0.00
   sum_current_investment_value = 0.00

   for investment in investments:
        sum_of_initial_investment_value += round(float(investment.acquired_value), 2)
        sum_current_investment_value += round(float(investment.recent_value), 2)
        investment.result = round(decimal.Decimal(investment.recent_value) - decimal.Decimal(investment.acquired_value), 2)
        investment.result_indianrupee = round((decimal.Decimal(investment.recent_value) - decimal.Decimal(investment.acquired_value)) * decimal.Decimal(indianrupee_value), 2)
        investment.result_gbp = round((decimal.Decimal(investment.recent_value) - decimal.Decimal(investment.acquired_value)) * decimal.Decimal(gbp_value), 2)


   sum_of_result_of_stock_value = round(decimal.Decimal(sum_current_stocks_value) - decimal.Decimal(sum_of_initial_stock_value), 2)
   sum_of_result_of_investment_value = round(decimal.Decimal(sum_current_investment_value) - decimal.Decimal(sum_of_initial_investment_value), 2)


   return render(request, 'portfolio/portfolio.html', {'customers': customers,
                                                       'investments': investments,
                                                       'stocks': stocks,
                                                       'sum_acquired_value': sum_acquired_value,
                                                       'sum_recent_value': sum_recent_value,
                                                        'sum_current_stocks_value': sum_current_stocks_value,
                                                        'sum_of_initial_stock_value': sum_of_initial_stock_value,
                                                        'sum_of_result_of_stock_value': sum_of_result_of_stock_value,
                                                       'sum_current_investment_value': sum_current_investment_value,
                                                       'sum_of_initial_investment_value': sum_of_initial_investment_value,
                                                       'sum_of_result_of_investment_value': sum_of_result_of_investment_value,
                                                       'customerid': pk,
                                                       'customer_phoneNumber': customer_phoneNumber})

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'portfolio/signup.html'

class PasswordResetView(auth_views.PasswordResetView):
    form_class = auth_forms.PasswordResetForm
    template_name = 'portfolio/reset_password.html'
    email_template_name = 'portfolio/reset_password_email.html'
    success_url = reverse_lazy('portfolio:reset_password_done')

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    form_class = auth_forms.PasswordResetForm
    template_name = 'portfolio/reset_password_done.html'
    #success_url = reverse_lazy('reset_password_done')

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = auth_forms.SetPasswordForm
    template_name = 'portfolio/reset_password_confirm.html'
    success_url = reverse_lazy('portfolio:reset_password_complete')

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    form_class = auth_forms.PasswordResetForm
    template_name = 'portfolio/reset_password_complete.html'
    #success_url = reverse_lazy('login.html')

class ChangePasswordResetDoneView(auth_views.PasswordChangeView):
    form_class = auth_forms.PasswordChangeForm
    template_name = 'portfolio/change_password.html'
    success_url = reverse_lazy('portfolio:change_password_done')

class ChangePasswordResetDoneSuccessView(auth_views.PasswordChangeView):
    form_class = auth_forms.PasswordChangeForm
    template_name = 'portfolio/change_password_done.html'


def broadcast_sms(request,pk,phonenumber,initalstock,currentstock,initalinvestment,currentinvestment):
    message_to_broadcast = ("Your current portfolio\n"
                            "Sock Information \n"
                            "Initial Stock: " + str(initalstock) + "\n" +
                            "Current Stock: " + str(currentstock) + "\n" +
                            "Investment Information \n"
                            "Acquired Investment: " + str(initalinvestment) +  "\n" +
                            "Recent Stock: " + str(currentinvestment) + "\n"
                            )
    client = Client('ACf54c9ea27d3d03a97ddcd27caba158d9', '879b786f58af5cccedddd7a5b6b24ecb')
    if phonenumber:
        client.messages.create(to=phonenumber,
                               from_='7064508598',
                               body=message_to_broadcast)
    return redirect('portfolio:portfolio',pk=pk)

def account_profile(request):
    print("User:" + str(request.user))
    print("Request-Get" + str(request.GET))
    print("Request-POST" + str(request.POST))
    print(request.path)
    print(request.user.id)
    customuser = CustomUser.objects.get(pk=request.user.id)
    print("customuser details",customuser)
    return render(request, 'portfolio/accountprofile.html', {'customuser': customuser})


def account_profile_edit(request, pk):
    customuser = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=customuser)
        if form.is_valid():
            customuser = form.save(commit=False)
            customuser.updated_date = timezone.now()
            customuser.save()
            customuser = CustomUser.objects.get(pk=pk)
            return render(request,'portfolio/accountprofile.html', {'customuser': customuser})
    else:
        # edit
        form = CustomUserChangeForm(instance=customuser)
    return render(request, 'portfolio/accountprofile_edit.html', {'form': form})

def sendpdfEmail(request,pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments = Investment.objects.filter(customer=pk)
    stocks = Stock.objects.filter(customer=pk)
    sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
    sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
    # overall_investment_results = sum_recent_value-sum_acquired_value
    # Initialize the value of the stocks
    sum_current_stocks_value = 0
    sum_of_initial_stock_value = 0
    customer_phoneNumber = customer.cell_phone

    # Loop through each stock and add the value to the total
    for stock in stocks:
        sum_current_stocks_value += round(decimal.Decimal(stock.current_stock_price()) * decimal.Decimal(stock.shares),
                                          2)
        sum_of_initial_stock_value += stock.initial_stock_value()
        stock.current_stock_value = round(decimal.Decimal(stock.current_stock_price()) * decimal.Decimal(stock.shares),
                                          2)
        stock.result = round(decimal.Decimal(stock.current_stock_value) - decimal.Decimal(stock.initial_stock_value()),
                             2)

    sum_of_initial_investment_value = 0
    sum_current_investment_value = 0

    for investment in investments:
        sum_of_initial_investment_value += investment.acquired_value
        sum_current_investment_value += investment.recent_value
        investment.result = round(decimal.Decimal(investment.recent_value) - decimal.Decimal(investment.acquired_value),2)

    sum_of_result_of_stock_value = round(decimal.Decimal(sum_current_stocks_value) - decimal.Decimal(sum_of_initial_stock_value), 2)
    sum_of_result_of_investment_value = round(decimal.Decimal(sum_current_investment_value) - decimal.Decimal(sum_of_initial_investment_value), 2)

    pdfbytes = render_to_pdf('portfolio/sendemail.html', {'customers': customers,
                                                        'investments': investments,
                                                        'stocks': stocks,
                                                        'sum_acquired_value': sum_acquired_value,
                                                        'sum_recent_value': sum_recent_value,
                                                        'sum_current_stocks_value': sum_current_stocks_value,
                                                        'sum_of_initial_stock_value': sum_of_initial_stock_value,
                                                        'sum_of_result_of_stock_value': sum_of_result_of_stock_value,
                                                        'sum_current_investment_value': sum_current_investment_value,
                                                        'sum_of_initial_investment_value': sum_of_initial_investment_value,
                                                        'sum_of_result_of_investment_value': sum_of_result_of_investment_value,
                                                        'customerid': pk,
                                                        'customer_phoneNumber': customer_phoneNumber})
    if pdfbytes:
        email= customer.email
        print(email)
        print(settings.EMAIL_HOST_USER)
        subject = "Customer Portfolio"
        from_email = settings.EMAIL_HOST_USER
        email = EmailMultiAlternatives(subject=subject, body="Customer Portfolio", from_email=from_email, to=[email])
        email.attach(filename='portfolio.pdf', content=pdfbytes, mimetype='application/pdf')
        email.send()
        return redirect('portfolio:portfolio',pk=pk)

def downloadPDF(request,pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments = Investment.objects.filter(customer=pk)
    stocks = Stock.objects.filter(customer=pk)
    sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
    sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
    # overall_investment_results = sum_recent_value-sum_acquired_value
    # Initialize the value of the stocks
    sum_current_stocks_value = 0
    sum_of_initial_stock_value = 0
    customer_phoneNumber = customer.cell_phone

    # Loop through each stock and add the value to the total
    for stock in stocks:
        sum_current_stocks_value += round(decimal.Decimal(stock.current_stock_price()) * decimal.Decimal(stock.shares),
                                          2)
        sum_of_initial_stock_value += stock.initial_stock_value()
        stock.current_stock_value = round(decimal.Decimal(stock.current_stock_price()) * decimal.Decimal(stock.shares),
                                          2)
        stock.result = round(decimal.Decimal(stock.current_stock_value) - decimal.Decimal(stock.initial_stock_value()),
                             2)

    sum_of_initial_investment_value = 0
    sum_current_investment_value = 0

    for investment in investments:
        sum_of_initial_investment_value += investment.acquired_value
        sum_current_investment_value += investment.recent_value
        investment.result = round(decimal.Decimal(investment.recent_value) - decimal.Decimal(investment.acquired_value),
                                  2)

    sum_of_result_of_stock_value = round(
        decimal.Decimal(sum_current_stocks_value) - decimal.Decimal(sum_of_initial_stock_value), 2)
    sum_of_result_of_investment_value = round(
        decimal.Decimal(sum_current_investment_value) - decimal.Decimal(sum_of_initial_investment_value), 2)

    pdfbytes = render_to_pdf('portfolio/sendemail.html', {'customers': customers,
                                                        'investments': investments,
                                                        'stocks': stocks,
                                                        'sum_acquired_value': sum_acquired_value,
                                                        'sum_recent_value': sum_recent_value,
                                                        'sum_current_stocks_value': sum_current_stocks_value,
                                                        'sum_of_initial_stock_value': sum_of_initial_stock_value,
                                                        'sum_of_result_of_stock_value': sum_of_result_of_stock_value,
                                                        'sum_current_investment_value': sum_current_investment_value,
                                                        'sum_of_initial_investment_value': sum_of_initial_investment_value,
                                                        'sum_of_result_of_investment_value': sum_of_result_of_investment_value,
                                                        'customerid': pk,
                                                        'customer_phoneNumber': customer_phoneNumber})
    if pdfbytes:
        response = HttpResponse(pdfbytes, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s' % 'ClientVisits.pdf'
        return response
    return redirect('portfolio:portfolio',pk=pk)

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.replace(u'\ufeff', '').encode("latin-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None

class CustomerList(APIView):
    def get(self, request):
        customers_json = Customer.objects.all()
        serializer = CustomerSerializer(customers_json, many=True)
        return Response(serializer.data)

class CustomerByNumber(APIView):
    def get(self, request, pk, format=None):
        try:
            person = Customer.objects.get(cust_number=pk)
            serializer = CustomerSerializer(person)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)