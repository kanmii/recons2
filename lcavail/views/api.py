from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from lcavail.models import LCCoverMovement
from lcavail.serializers import LCCoverMovementSerializer
from lcavail.forms import LCCoverMovementForm
import json
from django.http import HttpResponse


class LCCoverMovementViewSet(ModelViewSet):
    queryset = LCCoverMovement.objects.all()
    serializer_class = LCCoverMovementSerializer

    @detail_route()
    def render_template(self, request, *args, **kwargs):
        return render(
            request,
            'lcavail/lc-cv-mvmt.html',
            {"form": LCCoverMovementForm()}
        )

    @detail_route(methods=['post'])
    def post_cover(self, request, *args, **kwargs):
        post_status = {}
        for pk in request.DATA:
            post_status[pk] = LCCoverMovement.objects.get(pk=pk).post()
        return HttpResponse(json.dumps(post_status))
