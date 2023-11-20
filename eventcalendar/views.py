from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.shortcuts import render
import httpx
import json
from calendarapp.models import Event
import os


class DashboardView(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    template_name = "calendarapp/dashboard.html"

    def get(self, request, *args, **kwargs):
        events = Event.objects.get_all_events(user=request.user)
        running_events = Event.objects.get_running_events(user=request.user)
        latest_events = Event.objects.filter(
            user=request.user).order_by("-id")[:10]
        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
        }
        return render(request, self.template_name, context)


def calendario_view(request):
    return render(request, 'calendario.html')


async def helpdesk_view(request):
    try:
        # Solicitar os dados dos helpdesks pela API
        async with httpx.AsyncClient(timeout=300) as client:
            resposta = await client.get('http://127.0.0.1:8000/static/arquivos/dados.json')

        # Verifica se a solicitação foi bem sucedida
        if resposta.status_code == 200:
            # Converter a resposta para json
            dados = resposta.json()

            # Passar os dados para o template
            return render(request, 'helpdesk.html', {'helpdesk': dados})
        else:
            return render(
                request, 'helpdesk.html',
                {'helpdesk': 'Erro ao carregar os dados da API'}
            )
    except Exception as e:
        return render(request, 'helpdesk.html', {'helpdesk': str(e)})


# async def helpdesk_view(request):
#     authorization = environ.get('AUTH_KEY')
#     api_key = environ.get('API_KEY')
#     try:
#         # Solicitar os dados dos helpdesks pela API
#         async with httpx.AsyncClient(timeout=300) as client:
#             resposta = await client.get(
#                 url=environ.get('URL_API') + '/recursos/consultaHelpDesk/',
#                 params={
#                     'chave': 'sim-isp.tins.com.br',
#                     "data_abertura": ["2023-11-17", "2023-11-16"]
#                 },
#                 headers={
#                     'Content-Type': 'application/json',
#                     'Authorization': f'Token {authorization}',
#                     'X-Custom-Api-Key': f'Token {api_key}'
#                 }
#             )

#         # Verifica se a solicitação foi bem sucedida
#         if resposta.status_code == 200:
#             # Converter a resposta para json
#             dados = resposta.json()

#             # Passar os dados para o template
#             return render(request, 'helpdesk.html', {'helpdesk': dados})
#         else:
#             return render(
#                 request, 'helpdesk.html',
#                 {'helpdesk': 'Erro ao carregar os dados da API'}
#             )
#     except Exception as e:
#         return render(request, 'helpdesk.html', {'helpdesk': str(e)})
