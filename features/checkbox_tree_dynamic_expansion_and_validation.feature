Feature: Checkbox Tree Testing - Dynamic Expansion and Icon Validation

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
    When the user navigates to "Check Box" section under "Elements"
    Then the user should be navigated to a URL containing "demoqa.com/checkbox"
    And the user should be able to see "Home" in the tree node

  @smoke @functional @tree-expansion
  Scenario: TC001 - Dynamically expand the tree at all levels
    When the user clicks on the expand all (+) button
    Then all tree nodes should be expanded at all levels
    And all expandable nodes should show collapse (-) icons
    And the tree structure should display the complete hierarchy
    And the following nodes should be visible
      | Home      |
      | Desktop   |
      | Notes     |
      | Commands  |
      | Documents |
      | WorkSpace |
      | React     |
      | Angular   |
      | Veu       |
      | Office    |
      | Public    |
      | Private   |
      | Classified |
      | General   |
      | Downloads |
      | Word File.doc |
      | Excel File.doc |

  @smoke @functional @ui-validation @checkbox-behavior @cascading-selection
  Scenario: TC002 - Validate cascading checkbox selection for parent node with child hierarchy
    Given the user expands the tree at all levels through expand all (+) button
    When the user selects the node "WorkSpace" in the checkbox tree
    Then all child nodes under "WorkSpace" should be automatically checked
    And all ancestor nodes of "WorkSpace" should show indeterminate state
    And all sibling nodes of "WorkSpace" should remain unchecked
    And the selection result should display all items from "WorkSpace" branch

  @smoke @functional @checkbox-interaction @multiple-parent-selection
  Scenario: TC003 - Validate checkbox behavior when selecting multiple non-overlapping parent nodes
    Given the user expands the tree at all levels through expand all (+) button
    When the user selects the node "WorkSpace" in the checkbox tree
    And the user selects the node "Office" in the checkbox tree
    Then both selected nodes and all their children should be checked
    And the common parent node should show indeterminate state
    And unrelated nodes should remain unchecked
    And the selection result should include items from all selected branches

  @regression @edge-case @checkbox-deselection
  Scenario: TC004 - Validate checkbox deselection and state rollback behavior
    Given the user expands the tree at all levels through expand all (+) button
    When the user selects the node "WorkSpace" in the checkbox tree
    Then the node "WorkSpace" and all its children should be checked
    When the user deselects the node "WorkSpace" in the checkbox tree
    Then the node "WorkSpace" and all its children should be unchecked
    And all ancestor nodes should return to unchecked state
    And the selection result should be empty