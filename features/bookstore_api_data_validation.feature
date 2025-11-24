Feature: Book Store Application - UI and API Data Validation

  Background:
    Given the user has launched the DEMOQA application
    And the user clicks on "Book Store Application" card
    Then the user should be navigated to a URL containing "demoqa.com/books"
    And the menu list for "Book Store Application" should be expanded
    And the menu list items for "Book Store Application" should be
      | Items          |
      | Login          |
      | Book Store     |
      | Profile        |
      | Book Store API |

  @smoke @critical @api-validation @positive
  Scenario: TC012 - Verify book catalog data consistency between UI and API
    When the user navigates to "Book Store" section under "Book Store Application"
    And the user waits for the book list table to be fully loaded
    And the user sends a GET request to endpoint "/BookStore/v1/Books"
    Then the API response should have HTTP status code 200
    And the API response should contain a "books" array
    And the number of books displayed on UI should match the API response count
    And for each book, the UI data should exactly match the API response data
      | Field     |
      | title     |
      | author    |
      | publisher |
    And all book images should be displayed with valid URLs from API

  @smoke @critical @api-validation @negative
  Scenario: TC013 - Verify search with non-existent book title shows no results
    When the user navigates to "Book Store" section under "Book Store Application"
    And the user waits for the book list table to be fully loaded
    And the user searches for "NonExistentBookTitle12345XYZ" on the Book Store page
    Then no books should be displayed in the results
    And the search result count should be 0
    And an appropriate "No rows found" message should be displayed