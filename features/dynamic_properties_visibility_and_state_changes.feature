Feature: Dynamic Properties Testing

  Background:
    Given the user has launched the DEMOQA application
    And the user clicks on "Elements" card
    Then the user should be navigated to a URL containing "demoqa.com/elements"
    And the menu list for "Elements" should be expanded
    And the menu list items for "Elements" should be
      | Items                  |
      | Text Box               |
      | Check Box              |
      | Radio Button           |
      | Web Tables             |
      | Buttons                |
      | Links                  |
      | Broken Links - Images  |
      | Upload and Download    |
      | Dynamic Properties     |
    When the user navigates to "Dynamic Properties" section under "Elements"
    Then the user should be navigated to a URL containing "demoqa.com/dynamic-properties"

  @smoke @functional @visibility-check
  Scenario: TC005 - Fluently wait for button with text "Visible after 5 seconds" to be displayed
    Given the user is on the Dynamic Properties page
    When the user loads the page
    Then the user waits fluently for the button with text "Visible After 5 Seconds" to be displayed
    And the button with text "Visible After 5 Seconds" should be visible on the page

  @smoke @functional @color-validation
  Scenario: TC006 - Verify that the Color Change button changes color after some time
    Given the user is on the Dynamic Properties page
    When the user loads the page
    And the user captures the initial color of the "Color Change" button
    And the user waits for the "Color Change" button color to change
    Then the "Color Change" button should have a different color than initially