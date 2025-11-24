Feature: Practice Forms - Basic Functionality Testing

  Background:
    Given the user has launched the DEMOQA application
    And the user clicks on "Forms" card
    Then the user should be navigated to a URL containing "demoqa.com/forms"
    When the user navigates to "Practice Form" section under "Forms"
    Then the user should be navigated to a URL containing "demoqa.com/automation-practice-form"

  @smoke @critical
  Scenario: TC007 - Verify user not able to submit the form with empty fields
    When the user clicks on "Submit" button without filling any fields
    Then the field "First Name" should indicate error with red border
    And the field "Last Name" should indicate error with red border
    And the field "Gender" should indicate error with red border
    And the field "Mobile Number" should indicate error with red border

  @smoke @critical
  Scenario: TC008 - Verify form submission with valid required fields only
    When the user enters "Priyanka" in "First Name" field
    And the user enters "Chopra" in "Last Name" field
    And the user selects "Female" gender radio button
    And the user enters "9123456789" in "Mobile Number" field
    And the user enters "priyanka.chopra@bollywood.com" in "Email" field
    And the user enters "15 Jul 1982" in "Date of Birth" field
    And the user clicks on "Submit" button
    Then the form should be submitted successfully
    And the submission modal should display the following data
      | Label         | Value                         |
      | Student Name  | Priyanka Chopra               |
      | Student Email | priyanka.chopra@bollywood.com |
      | Gender        | Female                        |
      | Mobile        | 9123456789                    |
      | Date of Birth | 15 July,1982                  |

  @regression @validation
  Scenario Outline: TC009 - Validate Mobile Number field rejects invalid inputs
    When the user enters "Angelina" in "First Name" field
    And the user enters "Jolie" in "Last Name" field
    And the user selects "Female" gender radio button
    When the user enters "<mobile_number>" in "Mobile Number" field
    And the user clicks on "Submit" button
    Then the field "Mobile Number" should indicate error with red border

    Examples:
      | mobile_number     |
      | 98                |
      | hello world       |
      | 98@#$67890        |

  @regression @validation
  Scenario: TC010 - Validate Mobile Number field auto-limits to 10 digits maximum
    When the user enters "Angelina" in "First Name" field
    And the user enters "Jolie" in "Last Name" field
    And the user selects "Female" gender radio button
    When the user enters "987654321098765" in "Mobile Number" field
    Then verify if the "Mobile Number" field has accepted only "10" digits

  @regression @validation
  Scenario Outline: TC011 - Validate Email field rejects invalid formats
    When the user enters "Leonardo" in "First Name" field
    And the user enters "DiCaprio" in "Last Name" field
    And the user selects "Male" gender radio button
    And the user enters "8012345678" in "Mobile Number" field
    When the user enters "<email_address>" in "Email" field
    And the user clicks on "Submit" button
    Then the field "Email" should indicate error with red border

    Examples:
      | email_address       |
      | plaintext           |
      | user@               |
      | user@domain         |