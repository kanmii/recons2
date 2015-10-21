from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from adhocmodels.models import Customer, Currency
from letter_of_credit.models import LCRegister


class LCIssue(models.Model):
    text = models.CharField('Issue Text', max_length=300)

    class Meta:
        app_label = 'letter_of_credit'
        db_table = 'lc_issue'
        verbose_name = 'LC Issue'
        verbose_name_plural = 'LC Issue'

    def __unicode__(self):
        return self.text

    def save(self, *args, **kwargs):
        self.text = self.text.strip().upper()
        if not self.text.endswith(':ISSUE'):
            self.text = '%s:ISSUE' % self.text
        super(LCIssue, self).save(*args, **kwargs)


class FormM(models.Model):
    number = models.CharField('Number', max_length=13, unique=True)
    applicant = models.ForeignKey(Customer, verbose_name='Applicant')
    currency = models.ForeignKey(Currency, verbose_name='Currency')
    amount = models.DecimalField('Amount', max_digits=20, decimal_places=2)
    date_received = models.DateField('Date Received')
    lc = models.ForeignKey(LCRegister, null=True, blank=True, verbose_name='LC', related_name='form_m')
    goods_description = models.CharField('Goods Description', max_length=1000, blank=True, null=True)

    class Meta:
        app_label = 'letter_of_credit'
        db_table = 'form_m'
        verbose_name = 'Form M'
        verbose_name_plural = 'Form M'
        ordering = ('-date_received',)

    def __unicode__(self):
        return '[%s | %s%s | %s | %s]' % (
            self.number,
            self.currency.code,
            '{:,.2f}'.format(self.amount),
            self.applicant.name,
            self.goods_description and self.goods_description[:10] or ''
        )

    def save(self, *args, **kwargs):
        if self.lc and self.lc.applicant_obj != self.applicant:
            self.lc.applicant_obj = self.applicant
            self.lc.save()
        super(FormM, self).save(*args, **kwargs)

    def applicant_data(self):
        return self.applicant

    def currency_data(self):
        return self.currency

    def get_url(self):
        return reverse('formm-detail', kwargs={'pk': self.pk})

    @classmethod
    def search_filter(cls, qs, param):
        if not param:
            return qs

        return qs.filter(Q(number__icontains=param) | Q(applicant__name__icontains=param))

    @classmethod
    def lc_not_attached_filter(cls, qs, param):
        if not param:
            return qs

        param = True if param == 'true' else False

        return qs.filter(lc__isnull=param)

    def attach_lc(self, lc_number=None, lc=None):
        if self.lc:
            return
        if lc is None and lc_number is None:
            raise ValueError('You must either specify "LCRegister" object or lc number')
        if lc:
            self.lc = lc
        elif lc_number:
            self.lc = LCRegister.objects.get(lc_number=lc_number)
        self.save()

    def applicant_name(self):
        return self.applicant.name

    def lc_number(self):
        return self.lc and self.lc.lc_number or None


class LCIssueConcrete(models.Model):
    issue = models.ForeignKey(LCIssue, verbose_name='Issue')
    mf = models.ForeignKey(FormM, verbose_name='Related Form M', related_name='form_m_issues')
    created_at = models.DateField('Date Created', auto_now_add=True)
    closed_at = models.DateField('Date Closed', null=True, blank=True)

    class Meta:
        db_table = 'lc_issue_concrete'
        app_label = 'letter_of_credit'
        verbose_name = 'LC Issue Concrete'
        verbose_name_plural = 'LC Issue Concrete'

    def __unicode__(self):
        return '%s: %s' % (self.mf.number, self.issue.text)

    def save(self, *args, **kwargs):
        super(LCIssueConcrete, self).save(*args, **kwargs)

    def form_m_number(self):
        return self.mf.number

    def applicant(self):
        return self.mf.applicant

    def lc_number(self):
        return self.mf.lc and self.mf.lc.lc_number or None


class LcBidRequest(models.Model):
    mf = models.ForeignKey(FormM, verbose_name='Related Form M', related_name='bids')
    created_at = models.DateField('Date Created', auto_now_add=True)
    requested_at = models.DateField('Date Request To Treasury', blank=True, null=True)
    amount = models.DecimalField('Amount', max_digits=20, decimal_places=2)
    downloaded = models.BooleanField('Downloaded', default=False)

    class Meta:
        db_table = 'lc_bid_request'
        app_label = 'letter_of_credit'
        verbose_name = 'Lc Bid Request'
        verbose_name_plural = 'Lc Bid Request'

    def __unicode__(self):
        return '%s: %s%s' % (self.mf.number, self.mf.currency.code, '{:,.2f}'.format(self.amount))

    @classmethod
    def search_pending(cls, qs, param):
        if not param:
            return qs

        param = True if param == 'true' else False
        return qs.filter(requested_at__isnull=param)

    def form_m_number(self):
        return self.mf.number

    def applicant(self):
        return self.mf.applicant.name

    def goods_description(self):
        return self.mf.goods_description

    def currency(self):
        return self.mf.currency
