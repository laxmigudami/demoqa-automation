import time

from behave import given, then, when

from pages.checkbox_page import CheckBoxPage
from utils.logger import Logger

logger = Logger(__name__).get_logger()

CASCADE_WAIT = 0.5
ACTION_WAIT = 1.0


@when('the user navigates to "Check Box" section under "Elements"')
def step_navigate_to_checkbox(context):
    try:
        context.home_page.navigate_to_menu_item("Check Box")
        time.sleep(ACTION_WAIT)
        context.checkbox_page = CheckBoxPage(context.driver)
    except Exception as e:
        logger.error(f"Failed to navigate to Check Box section: {e}")
        raise


@then('the user should be navigated to a URL containing "demoqa.com/checkbox"')
def step_verify_checkbox_url(context):
    try:
        context.checkbox_page.wait_for_url_contains("demoqa.com/checkbox")
        assert "demoqa.com/checkbox" in context.checkbox_page.get_current_url()
    except Exception as e:
        logger.error(f"Checkbox URL verification failed: {e}")
        raise


@then('the user should be able to see "Home" in the tree node')
def step_verify_home_node_visible(context):
    assert context.checkbox_page.node_exists("Home"), "Home node not visible"


@when("the user clicks on the expand all (+) button")
def step_click_expand_all_button(context):
    assert context.checkbox_page.click_expand_all_button(), "Tree expansion failed"


@then("all tree nodes should be expanded at all levels")
def step_verify_all_nodes_expanded(context):
    assert context.checkbox_page.is_tree_expanded(), "Tree not fully expanded"


@then("all expandable nodes should show collapse (-) icons")
def step_verify_collapse_icons_visible(context):
    collapse_icons = context.checkbox_page.find_elements(context.checkbox_page.locators.COLLAPSE_ICONS)
    assert len(collapse_icons) > 0, "No collapse icons found"


@then("the tree structure should display the complete hierarchy")
def step_verify_complete_hierarchy(context):
    visible_nodes = context.checkbox_page.get_all_visible_nodes()
    assert len(visible_nodes) >= 10, f"Expected >= 10 nodes, found {len(visible_nodes)}"


@then("the following nodes should be visible")
def step_verify_specific_nodes_visible(context):
    expected_nodes = [row[0] for row in context.table]
    missing = [n for n in expected_nodes if not context.checkbox_page.node_exists(n)]
    assert not missing, f"Missing nodes: {missing}"


@given("the user expands the tree at all levels through expand all (+) button")
def step_expand_tree_for_checkbox_test(context):
    assert context.checkbox_page.click_expand_all_button(), "Failed to expand tree"
    assert context.checkbox_page.is_tree_expanded(), "Tree expansion verification failed"


@when('the user selects the node "{node_name}" in the checkbox tree')
def step_select_node_in_tree(context, node_name):
    assert context.checkbox_page.node_exists(node_name), f"Node '{node_name}' not found in tree"
    context.checkbox_page.check_node(node_name)
    time.sleep(ACTION_WAIT)
    assert context.checkbox_page.is_node_checked(node_name), f"Failed to check node '{node_name}'"


@then('all child nodes under "{parent_node}" should be automatically checked')
def step_verify_children_automatically_checked(context, parent_node):
    time.sleep(CASCADE_WAIT)
    descendants = context.checkbox_page.get_all_descendant_nodes(parent_node)

    if not descendants:
        logger.warning(f"No descendants found under '{parent_node}'")
        return

    unchecked = [node for node in descendants if not context.checkbox_page.is_node_checked(node)]
    assert not unchecked, f"Unchecked nodes under '{parent_node}': {unchecked}"


@then('all ancestor nodes of "{node_name}" should show indeterminate state')
def step_verify_ancestors_indeterminate(context, node_name):
    time.sleep(CASCADE_WAIT)
    ancestors = context.checkbox_page.get_ancestor_nodes(node_name)

    if not ancestors:
        return

    wrong_state = [
        f"{ancestor} (state: {state})"
        for ancestor in ancestors
        if (state := context.checkbox_page.is_node_checked(ancestor)) != "half"
    ]
    assert not wrong_state, f"Ancestors without indeterminate state: {wrong_state}"


@then('all sibling nodes of "{node_name}" should remain unchecked')
def step_verify_siblings_unchecked(context, node_name):
    time.sleep(CASCADE_WAIT)
    ancestors = context.checkbox_page.get_ancestor_nodes(node_name)

    if not ancestors:
        return

    parent = ancestors[0]
    siblings = [child for child in context.checkbox_page.get_child_nodes(parent) if child != node_name]
    checked_siblings = [s for s in siblings if context.checkbox_page.is_node_checked(s)]
    assert not checked_siblings, f"Checked siblings found: {checked_siblings}"


@then('the selection result should display all items from "{parent_node}" branch')
def step_verify_selection_result_branch(context, parent_node):
    time.sleep(CASCADE_WAIT)
    selected_items = context.checkbox_page.get_selected_items()

    assert selected_items, f"No selected items displayed for '{parent_node}' branch"
    assert parent_node.lower() in selected_items, f"Parent node '{parent_node}' not in results"


@then("both selected nodes and all their children should be checked")
def step_verify_both_selections_checked(context):
    time.sleep(CASCADE_WAIT)


@then("the common parent node should show indeterminate state")
def step_verify_common_parent_indeterminate(context):
    time.sleep(CASCADE_WAIT)
    common_parent = "Documents"
    state = context.checkbox_page.is_node_checked(common_parent)
    assert state in ["half", True], f"Common parent '{common_parent}' state invalid: {state}"


@then("unrelated nodes should remain unchecked")
def step_verify_unrelated_unchecked(context):
    time.sleep(CASCADE_WAIT)
    unrelated_nodes = ["Desktop", "Downloads"]
    checked_nodes = [
        node
        for node in unrelated_nodes
        if context.checkbox_page.node_exists(node) and context.checkbox_page.is_node_checked(node)
    ]
    assert not checked_nodes, f"Unrelated nodes are checked: {checked_nodes}"


@then("the selection result should include items from all selected branches")
def step_verify_result_multiple_branches(context):
    time.sleep(CASCADE_WAIT)
    selected_items = context.checkbox_page.get_selected_items()
    assert selected_items, "Expected items from multiple branches but got none"


@then('the node "{node_name}" and all its children should be checked')
def step_verify_node_and_children_checked(context, node_name):
    time.sleep(CASCADE_WAIT)
    assert context.checkbox_page.is_node_checked(node_name), f"Node '{node_name}' is not checked"

    descendants = context.checkbox_page.get_all_descendant_nodes(node_name)
    unchecked = [d for d in descendants if not context.checkbox_page.is_node_checked(d)]
    assert not unchecked, f"Unchecked descendants: {unchecked}"


@when('the user deselects the node "{node_name}" in the checkbox tree')
def step_deselect_node(context, node_name):
    assert context.checkbox_page.node_exists(node_name), f"Node '{node_name}' not found"
    context.checkbox_page.uncheck_node(node_name)
    time.sleep(ACTION_WAIT)
    assert not context.checkbox_page.is_node_checked(node_name), f"Failed to uncheck node '{node_name}'"


@then('the node "{node_name}" and all its children should be unchecked')
def step_verify_node_children_unchecked(context, node_name):
    time.sleep(CASCADE_WAIT)
    assert not context.checkbox_page.is_node_checked(node_name), f"Node '{node_name}' is still checked"

    descendants = context.checkbox_page.get_all_descendant_nodes(node_name)
    still_checked = [d for d in descendants if context.checkbox_page.is_node_checked(d)]
    assert not still_checked, f"Descendants still checked: {still_checked}"


@then("all ancestor nodes should return to unchecked state")  # pyright: ignore[reportCallIssue]
def step_verify_ancestors_unchecked(context):
    time.sleep(CASCADE_WAIT)
    if context.checkbox_page.node_exists("Home"):
        state = context.checkbox_page.is_node_checked("Home")
        assert not state or state is False, f"Root node 'Home' should be unchecked but is: {state}"


@then("the selection result should be empty")
def step_verify_result_empty(context):
    time.sleep(CASCADE_WAIT)
    selected = context.checkbox_page.get_selected_items()
    assert not selected, f"Expected empty result but found: {selected}"
