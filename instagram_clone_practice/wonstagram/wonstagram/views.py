from django.shortcuts import render
from rest_framework.views import APIView


class Sub(APIView):
    def get(self, request):
        print("실행테스트")
        return render(request, "wonstagram/main.html")