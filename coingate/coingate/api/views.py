from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.generic import DetailView, ListView, TemplateView
from django.shortcuts import get_object_or_404
import datetime
import secrets
from .models import Transaction
from django.http import HttpResponseRedirect, Http404
import requests
import json

User = get_user_model()
auth_token = 'ZJfMv-WzHZvm2ZVQ7MGYvyYGYPTsWtMZm-JqYdrx'  # set your token


class TransactionView(DetailView):
    template_name = 'transactions.html'

    def get_object(self):
        return get_object_or_404(User, username__iexact=self.request.user)

    def get_context_data(self, **kwargs):
        context = {}
        url = 'https://api-sandbox.coingate.com/v2/rates/merchant/'    #
        response = requests.get(url, params={'from': 'BTC', 'to': 'USD'},
                                headers={'Authorization': 'Token ' + auth_token})
        btc = float(response.text[1:-1])
        btc_min = round((1 / 1000 * btc), 4)
        context['btc'] = btc
        context['btc_min'] = btc_min
        return context


class ProceedView(TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            if request.method == "POST":
                value = request.POST.get("value")
                user = User.objects.get(username=request.user)
                created_date = datetime.datetime.now()
                order_id = str(request.user) + "_" + str(datetime.datetime.now())
                token = secrets.token_hex()
                rate_url = 'https://api-sandbox.coingate.com/v2/rates/merchant/'    #
                rate = requests.get(rate_url, params={'from': 'BTC', 'to': 'USD'},
                                    headers={'Authorization': 'Token ' + auth_token})
                rate = float(rate.text[1:-1])
                crypto_amount = float(value) / rate
                params = {
                    'order_id': order_id,
                    'price_amount': value,
                    'price_currency': 'USD',
                    'receive_currency': 'do_not_convert',
                    'title': 'Transaction value',
                    'description': 'description',
                    'callback_url': 'http://localhost:8000/callback/',  ###
                    'cancel_url': 'http://localhost:8000/cancel/',      ###
                    'success_url': 'http://localhost:8000/success/',    ###
                    'token': token

                }
                url = 'https://api-sandbox.coingate.com/v2/orders'
                response = requests.post(url, data=params, headers={'Authorization': 'Token ' + auth_token})
                result = json.loads(response.text)
                payment_instance = Transaction(user=request.user, token=token, purchase_id=result['id'],
                                               date=created_date,
                                               value=value,
                                               status=result['status'])
                payment_instance.save()

                return HttpResponseRedirect(result['payment_url'])
            else:
                raise Http404("request.method is not POST")
        except Exception as e:
            raise Http404(e)


class Transactions_list_View(ListView):
    template_name = 'transaction_list.html'
    def get_queryset(self):
        url = 'https://api-sandbox.coingate.com/v2/orders'     #
        response = requests.get(url=url, params={'per_page': 100, 'page': 100},
                                headers={'Authorization': 'Token ' + auth_token})
        response = json.loads(response.text)
        ts = Transaction.objects.all()
        for t in ts:
            for order in response['orders']:
                if int(t.purchase_id) == int(order['id']):
                    t.status = order['status']
                    t.save()
        qs = Transaction.objects.filter(user=self.request.user).order_by('-date')
        return qs


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'


class FailView(TemplateView):
    template_name = 'fail.html'


class CallBackView(TemplateView):
    template_name = 'callback.html'

    def post(self):
        return render(self.request, 'callback.html', self.request.data)
