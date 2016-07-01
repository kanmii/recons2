from rest_framework import serializers

from letter_of_credit.models import LcBidRequest


class LcBidRequestSerializer(serializers.HyperlinkedModelSerializer):
    currency = serializers.ReadOnlyField(source='mf.currency.code')
    form_m_number = serializers.ReadOnlyField(source='mf.number')
    applicant = serializers.ReadOnlyField(source='mf.applicant.name')
    goods_description = serializers.ReadOnlyField(source='mf.goods_description')

    class Meta:
        model = LcBidRequest
        fields = (
            'id',
            'url',
            'currency',
            'created_at',
            'requested_at',
            'deleted_at',
            'amount',
            'mf',
            'form_m_number',
            'applicant',
            'goods_description',
            'rate',
            'bid_letter',
            'credit_approval',
            'docs_complete',
            'comment',
            'downloaded',
            'maturity',
            'ct_id',
            'ct_url',
            'allocations',
            'sum_allocations',
            'sum_utilizations',
            'unallocated',
        )
