Feature: List Form Ms
  As a user
  I should be able to see a list of form Ms in the system
  So I can pick anyone to see its details

  Background: There are form Ms in the system
    Given there are applicants in the system
    |name|_id|account_number|branch_code|

    And a number of form Ms
    |form_m_number|applicant|currency|amount|

  Scenario: # Enter scenario name here
    # Enter steps here
