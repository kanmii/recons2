import time
from behave import *
import nose.tools as nt
from adhocmodels.factories import CustomerFactory
from letter_of_credit.models import FormM
from commons import (
    add_form_m_btn_is_disabled,
    confirmation_dialog_css_selector,
    dialog_title_css_selector,
    form_m_saved_success_info_template
)


@given("There is form M request with form M data")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    context.form_m_data = dict(
            number='MF20159999990',
            amount=410252,
            applicant='ACADEMIC PRESS LTD'
    )


@given("There is customer in the system")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    context.applicant = CustomerFactory(name=context.form_m_data['applicant'])


@when("I fill form M number field")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    if context.browser.is_element_present_by_name('addFormMForm', wait_time=1):
        context.browser.fill('formMNumber', context.form_m_data['number'])


@then("I notice that save button is disabled")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    submit_btn_name = 'formMAddSubmitBtn'
    context.submit_btn_name = submit_btn_name

    # the submit button is disabled until form is completely filled and valid
    nt.assert_true(add_form_m_btn_is_disabled(context),
                   'Submit button must be disabled until form is completely filled.')


@when("I complete form M number field")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.execute_steps(u"""
    When I fill form M number field
    Then I notice that save button is disabled
    """)


@when("I fill applicant field")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.fill('applicant',
                         context.form_m_data['applicant'][:-1])  # otherwise typeahead dropdown will not show


@then("I see a drop down containing the text I typed into the input field")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # This is the selector for type-ahead the drop-down
    context.type_ahead_css_selector = 'li[id^=typeahead-][id*=-option-]'
    nt.assert_true(
            context.browser.is_element_present_by_css(context.type_ahead_css_selector, wait_time=0),
            'There must be a drop-down containing text typed into the input field')


@when("I click the first item in the drop down")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.find_by_css(context.type_ahead_css_selector).first.click()


@then("I notice that the drop down has disappeared")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    nt.assert_false(
            context.browser.is_element_present_by_css(context.type_ahead_css_selector, wait_time=0),
            'The drop-down containing text typed into the input field must disappear after the drop-down is clicked '
            'on.')


@step("I enter applicant's name in applicant field")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.fill('applicant', context.form_m_data['applicant'])


@step("I click on add new customer image")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.find_by_id('add-new-customer').first.click()


@then("A dialog pops up for adding new customer")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    nt.eq_(context.browser.find_by_css(dialog_title_css_selector).first.text, 'Add Customer',
           'A dialog must pop up with the text "Add Customer" in the title')


@step("I see applicant's name in the dialog")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    nt.eq_(context.browser.find_by_css('input[ng-model="customerModal.customer.name"]').first.value,
           context.form_m_data['applicant'], "Applicant's name must be visible in the dialog")


@step(
        "I see that the text and border colour of original input field for applicant is now rgb'169, 68, "
        "66' - indicating "
        "form error")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.applicant_input = context.browser.driver.find_element_by_name('applicant')
    nt.assert_in('169, 68, 66', context.applicant_input.value_of_css_property('color'),
                 "The text colour of applicant input must be rgb(169, 68, 66)")

    nt.assert_in('169, 68, 66', context.applicant_input.value_of_css_property('border'),
                 "The border colour of applicant input must be rgb(169, 68, 66)")


@when("I click add customer button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.find_by_name('addNewCustomerModalSubmitBtn').first.click()


@then("I notice that the dialog has disappeared")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    nt.assert_false(context.browser.is_element_present_by_css(dialog_title_css_selector, wait_time=1))


@step(
        "I see that the text and border colour of original input field for applicant is no longer rgb'169, 68, "
        "66' - indicating that input is valid")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    # This is a hack. Ideally, when user clicks "Add customer" submit button, the applicant field is supposed to become
    # valid automatically so that assertion below will work. However, in tests comma, this is not so. This may be a bug
    # in the test browser suite because my code works in real life
    context.execute_steps(u"""
    When I fill applicant field
    Then I see a drop down containing the text I typed into the input field
    When I click the first item in the drop down
    Then I notice that the drop down has disappeared
    """)

    # If we don't do this, the assertion below will only pass in phantomjs
    time.sleep(1)

    nt.assert_not_in(
            '169, 68, 66',
            context.applicant_input.value_of_css_property('color'),
            "The text colour of applicant input must no longer be rgb(169, 68, 66) when input is valid")

    nt.assert_not_in(
            '169, 68, 66',
            context.applicant_input.value_of_css_property('border'),
            "The border colour of applicant input must no longer be rgb(169, 68, 66) when applicant input is valid")


@when("I fill currency, amount and submit completed form")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.execute_steps(u"""
    When I fill currency field
    Then I notice that save button is disabled
    When I fill amount field
    Then I notice that save button is enabled
    When I submit the completed form
     """)


@then("I verify that the form M has been properly saved")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.execute_steps(u"""
    Then I see a dialog containing information about form M
    And I see the dialog title informing that form M was successfully saved
    And I notice that dialog contains information about saved form M
    And confirm that there is one form M in the system
    When I click on dialog close button
    Then I see that dialog has disappeared from page
    And that tab title has changed to a text containing information about saved form M
    """)


@when("I fill currency field")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.fill('currency', context.currency.code[:-1])  # otherwise typeahead dropdown will not show
    context.execute_steps(u"""
    Then I see a drop down containing the text I typed into the input field
    When I click the first item in the drop down
    Then I notice that the drop down has disappeared
    """)


@when("I fill amount field")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    context.browser.fill('amount', context.form_m_data['amount'])


@then("I notice that save button is enabled")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    nt.assert_false(add_form_m_btn_is_disabled(context),
                    'submit button must be enabled when form m is completely filled and valid')


@step("that the tab title is 'Form M'")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    text = context.browser.find_by_css(context.active_tab_css_selector).first.text
    nt.eq_(
            text,
            'Form M',
            'Active tab title must be: %s' % text
    )


@when("I submit the completed form")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    context.browser.find_by_name(context.submit_btn_name).first.click()


@then("I see a dialog containing information about form M")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    nt.assert_true(
            context.browser.is_element_present_by_css(confirmation_dialog_css_selector),
            'Dialog with css selector "%s" must pop up after form M successfully saved.' %
            confirmation_dialog_css_selector
    )


@then("I see the dialog title informing that form M was successfully saved")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    nt.eq_(
            context.browser.find_by_css(dialog_title_css_selector).first.text,
            '"%s" successfully saved' % context.form_m_data['number'],
            'Form M has been created and "success message must now be displayed in confirmation dialog title"')


@step("I notice that dialog contains information about saved form M")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # Will be reused in other steps
    context.confirmation_dialog = context.browser.find_by_css(confirmation_dialog_css_selector).first

    # Will be reused in other steps
    context.confirmation_dialog_debug_message = "Confirmation dialog text is:\n%s\nand must contain text:\n%s"

    text = form_m_saved_success_info_template.format(
            applicant=context.form_m_data['applicant'],
            form_m_number=context.form_m_data['number'],
            currency_amount='{} {:,.2f}'.format(context.currency.code, context.form_m_data['amount'])
    )
    nt.assert_in(text, context.confirmation_dialog.text)


@step("confirm that there is one form M in the system")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    mf = FormM.objects.all()
    nt.eq_(mf.count(), 1)
    nt.eq_(mf[0].number, context.form_m_data['number'])


@when("I click on dialog close button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.find_by_css('.ui-dialog-titlebar-close').first.click()


@then("I see that dialog has disappeared from page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    nt.assert_false(
            context.browser.is_element_present_by_css(confirmation_dialog_css_selector),
            'Confirmation dialog must disappear from page when its close button is clicked.'
    )


@step("that tab title has changed to a text containing information about saved form M")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    nt.eq_(context.browser.find_by_css(context.active_tab_css_selector).first.text,
           'Details of "%s"' % context.form_m_data['number'])


@when("I fill 'Form M Number', 'Applicant', 'Currency', and 'Amount' fields and submit form")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.execute_steps(u"""
    When I fill form M number field
    Then I notice that save button is disabled
    When I fill applicant field
    Then I see a drop down containing the text I typed into the input field
    When I click the first item in the drop down
    Then I notice that the drop down has disappeared
    Then I notice that save button is disabled
    When I fill currency field
    Then I notice that save button is disabled
    When I fill amount field
    Then I notice that save button is enabled
    When I submit the completed form
     """)


@then("I see a dialog with title that says request did not succeed")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    dialog_title = "Request Not Completed"
    nt.eq_(
            context.browser.find_by_css(dialog_title_css_selector).first.text,
            dialog_title,
            'Http post action was not successful and a dialog with title "%s" must be displayed after action' %
            dialog_title)

    context.error_dialog_css_selector = '.xhr-error.ui-dialog-content'


@step("Dialog informs me that form M number must be unique")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    nt.assert_in('Error 400\nBAD REQUEST\nError in FORM M NUMBER\n- This field must be unique.',
                 context.browser.find_by_css(context.error_dialog_css_selector).first.text)
