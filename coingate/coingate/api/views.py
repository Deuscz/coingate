from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, FormView
import datetime
import secrets
from .models import Transaction
from django.http import HttpResponseRedirect, HttpResponse
import requests
import json
from .forms import TransactionForm
from django.contrib import messages

auth_token = 'ZJfMv-WzHZvm2ZVQ7MGYvyYGYPTsWtMZm-JqYdrx'  # set your token



class TransactionView(FormView):
    template_name = 'transaction.html'
    form_class = TransactionForm
    def get(self, request, *args, **kwargs):
        context = {}
        url = 'https://api-sandbox.coingate.com/v2/rates/merchant/'    #
        response = requests.get(url, params={'from': 'BTC', 'to': 'USD'},
                                headers={'Authorization': 'Token ' + auth_token})
        btc = float(response.text[1:-1])
        context['btc'] = btc
        context['form'] = TransactionForm
        return render(request, 'transaction.html', context)

    def form_valid(self, form):
        try:
            if form.is_valid():
                form = form.cleaned_data
                value = form['value']
                order_id = str(value) + "_" + str(datetime.datetime.now())
                token = secrets.token_hex()
                Transaction.objects.create(**form,
                                           date = datetime.datetime.now(),
                                           order_id = str(value) + "_" + str(datetime.datetime.now()),
                                           token = token,
                                           status = 'new')
            else:
                messages.add_message(self.request, messages.INFO, 'Your transaction has incorrect values!')
            params = {
                'order_id': order_id,
                'price_amount': value,
                'price_currency': form['currency'],
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
            t = get_object_or_404(Transaction, token=result['token'])
            t.coin_id = result['id']
            t.status = result['status']
            t.save()
            return HttpResponseRedirect(result['payment_url'])
        except Exception as e:
            print(e)
            return HttpResponseRedirect('fail')

class Transactions_list_View(ListView):
    template_name = 'transaction_list.html'
    def get_queryset(self):
        url = 'https://api-sandbox.coingate.com/v2/orders/'     #
        ts = Transaction.objects.all()
        for t in ts:
            try:
                response = requests.get(url=url+str(t.coin_id),
                                        headers={'Authorization': 'Token ' + auth_token})
                response = json.loads(response.text)
                t.status = response['status']
                t.save()
            except:
                t.status = 'failed'
                t.save()
        qs = Transaction.objects.all().order_by('-date')
        return qs


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'


class FailView(TemplateView):
    template_name = 'fail.html'


def callback(request):
    print(request)
    return HttpResponse(status=200)
