from rest_framework import generics, pagination, status
import django_filters
from rest_framework.response import Response
from letter_of_credit.models import FormM, LcBidRequest
from letter_of_credit.serializers import FormMSerializer, LcBidRequestSerializer, LCIssueConcreteSerializer

import logging

logger = logging.getLogger('recons_logger')


class FormMListPagination(pagination.PageNumberPagination):
    page_size = 20


class FormMFilter(django_filters.FilterSet):
    number = django_filters.CharFilter(lookup_type='icontains')
    applicant = django_filters.CharFilter(name='applicant__name', lookup_type='icontains')
    currency = django_filters.CharFilter(name='currency__code', lookup_type='iexact')
    lc_not_attached = django_filters.CharFilter(action=FormM.lc_not_attached_filter)
    filter = django_filters.CharFilter(action=FormM.search_filter)

    class Meta:
        model = FormM
        fields = ('number', 'applicant', 'currency', 'filter', 'lc_not_attached')


class FormIssueBidUtil:
    def __init__(self, request, form_m_url, log_prefix=None):
        self.request = request
        self.form_m_url = form_m_url
        self.log_prefix = log_prefix

    def create_bid(self, amount):
        logger.info('{} creating bid for amount "{:,.2f}"'.format(self.log_prefix, amount))

        serializer = LcBidRequestSerializer(data={'amount': amount, 'mf': self.form_m_url},
                                            context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def create_issues(self, issues):
        logger.info('{} creating form M issues: {:}'.format(self.log_prefix, issues))
        data = []
        for issue in issues:
            data.append({'issue': issue['url'], 'mf': self.form_m_url})

        serializer = LCIssueConcreteSerializer(data=data, context={'request': self.request}, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data


class FormMListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = FormMSerializer
    queryset = FormM.objects.all()
    pagination_class = FormMListPagination
    filter_class = FormMFilter

    def __init__(self, **kwargs):
        self.log_prefix = 'Creating new form M:'
        super(FormMListCreateAPIView, self).__init__(**kwargs)

    def create(self, request, *args, **kwargs):
        incoming_data = request.data
        logger.info('%s with incoming data = \n%r', self.log_prefix, incoming_data)

        serializer = self.get_serializer(data=incoming_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        form_m_data = serializer.data

        util = FormIssueBidUtil(request, form_m_data['url'], self.log_prefix)
        if 'bid' in incoming_data:
            form_m_data['bid'] = util.create_bid(incoming_data['bid']['amount'])

        if 'issues' in incoming_data:
            form_m_data['issues'] = util.create_issues(incoming_data['issues'])

        headers = self.get_success_headers(form_m_data)
        return Response(form_m_data, status=status.HTTP_201_CREATED, headers=headers)


class FormMUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FormM.objects.all()
    serializer_class = FormMSerializer

    def __init__(self, **kwargs):
        self.log_prefix = 'Updating form M:'
        super(FormMUpdateAPIView, self).__init__(**kwargs)

    def update(self, request, *args, **kwargs):
        incoming_data = request.data
        logger.info('%s with incoming data: \n%r', self.log_prefix, incoming_data)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=incoming_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        form_m_data = serializer.data

        util = FormIssueBidUtil(request, form_m_data['url'], self.log_prefix)
        if 'bid' in incoming_data:
            form_m_data['bid'] = util.create_bid(incoming_data['bid']['amount'])

        if 'issues' in incoming_data:
            form_m_data['issues'] = util.create_issues(incoming_data['issues'])

        return Response(form_m_data)