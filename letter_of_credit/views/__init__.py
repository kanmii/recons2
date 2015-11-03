from django.shortcuts import render
from core_recons.views import CoreAppsView
from .lc import (
    LCStatusListCreateAPIView,
    LCStatusUpdateAPIView,
)

from .lc_register import (
    LetterOfCreditRegisterListCreateAPIView,
    LetterOfCreditRegisterUpdateAPIView,
    LCRegisterUploadView,
    ReleaseTelexView)

from .lc_issue import (
    LCIssueListCreateAPIView,
    LCIssueUpdateAPIView,
    LCIssueConcreteListCreateAPIView,
    LCIssueConcreteUpdateAPIView,
)

from .form_m import (
    FormMListCreateAPIView,
    FormMRetrieveUpdateDestroyAPIView,
    FormMCoverListCreateAPIView,
    FormMCoverRetrieveUpdateDestroyAPIView
)

from .lc_bid_request import LcBidRequestListCreateAPIView, LcBidRequestUpdateAPIView

from .download_bids import DownloadBidsView

from .uploaded_form_m import (
    UploadedFormMListCreateAPIView,
    UploadedFormMUpdateAPIView,
    UploadFromSingleWindowView
)


class AppHomeView(CoreAppsView):
    def get(self, request):
        context = {'urls': self.get_core_app_urls()}
        context.update(self.get_form_m_cover_types())
        return render(request, 'letter_of_credit/app/index.html', context)
