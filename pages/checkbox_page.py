import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from pages.locators import CheckBoxPageLocators
from utils.logger import Logger

logger = Logger(__name__).get_logger()


class CheckBoxPage(BasePage):
    """Checkbox page class"""

    def __init__(self, driver):
        """Initialize checkbox page"""
        super().__init__(driver)
        self.locators = CheckBoxPageLocators()

    def click_expand_all_button(self):
        """Click expand all button and wait for tree to expand"""
        try:
            self.click_element(self.locators.EXPAND_ALL_BUTTON)
            logger.info("Clicked expand all button")

            # Wait for the collapse all button to appear (indicates expansion is complete)
            try:
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.locators.COLLAPSE_ALL_BUTTON))
                logger.info("Tree expansion completed - Collapse All button is now visible")

                # Wait for all nodes to be rendered
                WebDriverWait(self.driver, 10).until(lambda d: len(d.find_elements(*self.locators.TREE_NODES)) > 10)

                # Verify tree is expanded
                if self.is_tree_expanded():
                    logger.info("All tree nodes are expanded successfully")
                    return True
                else:
                    logger.warning("Collapse button appeared but tree may not be fully expanded")
                    return False

            except TimeoutException:
                logger.error("Timeout: Collapse All button did not appear after clicking Expand All")
                return False

        except Exception as e:
            logger.error(f"Error clicking expand all button: {e}")
            raise

    def click_collapse_all_button(self):
        """Click collapse all button and wait for tree to collapse"""
        try:
            self.click_element(self.locators.COLLAPSE_ALL_BUTTON)
            logger.info("Clicked collapse all button")

            # Wait for the expand all button to appear (indicates collapse is complete)
            try:
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.locators.EXPAND_ALL_BUTTON))
                logger.info("Tree collapse completed - Expand All button is now visible")
                return True

            except TimeoutException:
                logger.error("Timeout: Expand All button did not appear after clicking Collapse All")
                return False

        except Exception as e:
            logger.error(f"Error clicking collapse all button: {e}")
            raise

    def is_tree_expanded(self):
        """Check if tree is fully expanded"""
        try:
            collapse_button_present = self.is_element_present(self.locators.COLLAPSE_ALL_BUTTON)
            collapse_icons = self.find_elements(self.locators.COLLAPSE_ICONS)
            expand_icons = self.find_elements(self.locators.EXPAND_ICONS)

            is_expanded = collapse_button_present and len(collapse_icons) > 0 and len(expand_icons) == 0

            logger.info(
                f"Tree expanded: {is_expanded} "
                f"(collapse_button: {collapse_button_present}, "
                f"collapse_icons: {len(collapse_icons)}, expand_icons: {len(expand_icons)})"
            )

            return is_expanded

        except Exception as e:
            logger.error(f"Error checking tree expansion: {e}")
            return False

    def is_tree_collapsed(self):
        """Check if tree is fully collapsed by verifying Expand All button is present"""
        try:
            expand_button_present = self.is_element_present(self.locators.EXPAND_ALL_BUTTON)
            logger.info(f"Tree collapsed status: {expand_button_present}")
            return expand_button_present
        except Exception as e:
            logger.error(f"Error checking tree collapse: {e}")
            return False

    def get_all_visible_nodes(self):
        """Get all visible node names"""
        try:
            nodes = self.find_elements(self.locators.TREE_NODES)
            node_texts = [node.text for node in nodes if node.text.strip()]
            logger.info(f"Found {len(node_texts)} visible nodes")
            return node_texts
        except Exception as e:
            logger.error(f"Error getting visible nodes: {e}")
            return []

    def node_exists(self, node_name):
        """Check if node exists in tree"""
        try:
            locator = self.locators.get_node_by_name(node_name)
            return self.is_element_present(locator)
        except Exception as e:
            logger.error(f"Error checking node existence: {e}")
            return False

    def get_node_icon_state(self, node_name):
        """Get checkbox state for node"""
        try:
            parent_locator = self.locators.get_node_parent(node_name)
            parent = self.find_element(parent_locator)

            # Wait a moment for any animations to complete
            time.sleep(0.3)

            # Find the checkbox span element
            checkbox_spans = parent.find_elements(By.XPATH, ".//span[contains(@class, 'rct-checkbox')]")

            if not checkbox_spans:
                logger.warning(f"Node '{node_name}' - no checkbox element found")
                return "not-found"

            # Get all classes from the checkbox span
            checkbox_classes = checkbox_spans[0].get_attribute("class")
            logger.debug(f"Node '{node_name}' checkbox classes: {checkbox_classes}")

            # Check state based on classes
            if "rct-icon-check" in checkbox_classes and "rct-icon-half-check" not in checkbox_classes:
                logger.info(f"Node '{node_name}' is checked")
                return "checked"
            elif "rct-icon-half-check" in checkbox_classes:
                logger.info(f"Node '{node_name}' is half-checked")
                return "half-checked"
            elif "rct-icon-uncheck" in checkbox_classes:
                logger.info(f"Node '{node_name}' is unchecked")
                return "unchecked"
            else:
                logger.warning(f"Node '{node_name}' checkbox state unclear. Classes: {checkbox_classes}")
                return "unknown"

        except Exception as e:
            logger.error(f"Error getting node icon state for '{node_name}': {e}")
            return "error"

    def is_node_expandable(self, node_name):
        """Check if node is expandable"""
        try:
            parent_locator = self.locators.get_node_parent(node_name)
            parent = self.find_element(parent_locator)

            # Check for expand/collapse buttons
            toggle_button = parent.find_elements(
                By.XPATH, ".//button[contains(@class, 'rct-collapse') or contains(@class, 'rct-expand')]"
            )

            is_expandable = len(toggle_button) > 0
            logger.info(f"Node '{node_name}' expandable: {is_expandable}")
            return is_expandable
        except Exception as e:
            logger.error(f"Error checking if node is expandable: {e}")
            return False

    def check_node(self, node_name):
        """Check checkbox for node"""
        try:
            # Get current state before clicking
            current_state = self.is_node_checked(node_name)

            # Only click if not already checked
            if current_state is True:
                logger.info(f"Node '{node_name}' is already checked, skipping click")
                return

            checkbox_locator = self.locators.get_checkbox_for_node(node_name)
            self.click_element(checkbox_locator)
            logger.info(f"Clicked checkbox for node '{node_name}'")

            # Wait for state change with explicit wait
            try:
                WebDriverWait(self.driver, 5).until(lambda d: self.is_node_checked(node_name) is True)
                logger.info(f"Successfully checked node: {node_name}")
            except TimeoutException:
                logger.warning(f"Timeout waiting for node '{node_name}' to be checked")

        except Exception as e:
            logger.error(f"Error checking node '{node_name}': {e}")
            raise

    def uncheck_node(self, node_name):
        """Uncheck checkbox for node"""
        try:
            # Get current state before clicking
            current_state = self.is_node_checked(node_name)

            # Only click if not already unchecked
            if current_state is False:
                logger.info(f"Node '{node_name}' is already unchecked, skipping click")
                return

            checkbox_locator = self.locators.get_checkbox_for_node(node_name)
            self.click_element(checkbox_locator)
            logger.info(f"Clicked checkbox to uncheck node '{node_name}'")

            # Wait for state change with explicit wait
            try:
                WebDriverWait(self.driver, 5).until(lambda d: self.is_node_checked(node_name) is False)
                logger.info(f"Successfully unchecked node: {node_name}")
            except TimeoutException:
                logger.warning(f"Timeout waiting for node '{node_name}' to be unchecked")

        except Exception as e:
            logger.error(f"Error unchecking node '{node_name}': {e}")
            raise

    def is_node_checked(self, node_name):
        """
        Check node state using multiple detection methods:
        1. Check input element's checked and indeterminate state (most reliable)
        2. Check ARIA attributes (reliable fallback)
        3. Check icon classes (last resort)

        Returns:
            True: Node is fully checked
            False: Node is unchecked
            "half": Node is half-checked (indeterminate)
        """
        try:
            # Method 1: Check actual input element state (MOST RELIABLE)
            try:
                input_locator = self.locators.get_node_input(node_name)
                input_elem = self.find_element(input_locator)

                # Check if input is indeterminate (half-checked state) - must check first
                is_indeterminate = self.driver.execute_script("return arguments[0].indeterminate;", input_elem)

                if is_indeterminate:
                    logger.debug(f"Node '{node_name}' is half-checked (indeterminate)")
                    return "half"

                # Check if input is checked
                is_checked = input_elem.is_selected()
                logger.debug(f"Node '{node_name}' is {'checked' if is_checked else 'unchecked'}")
                return is_checked

            except (NoSuchElementException, TimeoutException):
                logger.debug(f"No input element found for '{node_name}', trying ARIA method")

            # Method 2: Check ARIA attributes (reliable fallback)
            checkbox = self.find_element(self.locators.get_checkbox_for_node(node_name))
            aria_checked = checkbox.get_attribute("aria-checked")

            if aria_checked:
                if aria_checked == "true":
                    logger.debug(f"Node '{node_name}' is checked (via ARIA)")
                    return True
                elif aria_checked == "false":
                    logger.debug(f"Node '{node_name}' is unchecked (via ARIA)")
                    return False
                elif aria_checked == "mixed":
                    logger.debug(f"Node '{node_name}' is half-checked (via ARIA)")
                    return "half"

            # Method 3: Check icon classes (last resort)
            icon_spans = checkbox.find_elements(By.XPATH, ".//span[contains(@class, 'rct-icon')]")
            if icon_spans:
                icon_classes = icon_spans[0].get_attribute("class")

                if "rct-icon-half-check" in icon_classes:
                    logger.debug(f"Node '{node_name}' is half-checked (via icon class)")
                    return "half"
                elif "rct-icon-check" in icon_classes:
                    logger.debug(f"Node '{node_name}' is checked (via icon class)")
                    return True
                elif "rct-icon-uncheck" in icon_classes:
                    logger.debug(f"Node '{node_name}' is unchecked (via icon class)")
                    return False

            # If all methods fail, return False as default
            logger.warning(f"Could not determine state for '{node_name}', defaulting to False")
            return False

        except Exception as e:
            logger.error(f"Error checking node '{node_name}' state: {e}")
            return False

    def get_child_nodes(self, parent_name):
        """Get all direct child nodes of parent"""
        try:
            parent_locator = self.locators.get_node_parent(parent_name)
            parent = self.find_element(parent_locator)

            # Find direct children only - immediate child ol element
            children_ol = parent.find_elements(By.XPATH, "./ol[@class='rct-node-children']")

            if not children_ol:
                logger.debug(f"No child nodes found for '{parent_name}'")
                return []

            # Get all direct li children
            children = children_ol[0].find_elements(By.XPATH, "./li")
            child_names = []

            for child in children:
                try:
                    child_text = child.find_element(By.XPATH, ".//span[@class='rct-title']").text
                    if child_text:  # Only add non-empty names
                        child_names.append(child_text)
                except Exception:
                    continue

            logger.debug(f"Found {len(child_names)} direct children for '{parent_name}': {child_names}")
            return child_names
        except Exception as e:
            logger.error(f"Error getting child nodes for '{parent_name}': {e}")
            return []

    def get_all_descendant_nodes(self, parent_name):
        """Get all descendants of parent node recursively (children, grandchildren, etc.)"""
        descendants = []

        def get_descendants_recursive(node_name):
            children = self.get_child_nodes(node_name)
            for child in children:
                descendants.append(child)
                get_descendants_recursive(child)  # Recurse into grandchildren

        get_descendants_recursive(parent_name)
        logger.debug(f"Found {len(descendants)} total descendants for '{parent_name}'")
        return descendants

    def get_ancestor_nodes(self, node_name):
        """Get all ancestor (parent) nodes of a given node, ordered from immediate parent to root"""
        ancestors = []

        try:
            current_locator = self.locators.get_node_parent(node_name)
            current_element = self.find_element(current_locator)

            # Traverse up the tree hierarchy
            max_iterations = 10  # Safety limit to prevent infinite loops
            iterations = 0

            while iterations < max_iterations:
                iterations += 1

                # Find parent ol element
                parent_ol = current_element.find_elements(By.XPATH, "./parent::ol[@class='rct-node-children']")
                if not parent_ol:
                    break

                # From ol, go to parent li
                parent_li = parent_ol[0].find_elements(By.XPATH, "./parent::li")
                if not parent_li:
                    break

                # Get the parent node name
                try:
                    parent_text = parent_li[0].find_element(By.XPATH, ".//span[@class='rct-title']").text
                    if parent_text:  # Only add non-empty names
                        ancestors.append(parent_text)
                        current_element = parent_li[0]
                    else:
                        break
                except Exception:
                    break

            logger.debug(f"Found {len(ancestors)} ancestors for '{node_name}': {ancestors}")
            return ancestors

        except Exception as e:
            logger.warning(f"Could not get ancestors for '{node_name}': {e}")
            return []

    def get_selected_items(self):
        """Get all selected items from result display"""
        try:
            result_text = self.get_text(self.locators.RESULT_TEXT)

            if not result_text or result_text.strip() == "":
                logger.debug("No result text found - selection is empty")
                return []

            logger.debug(f"Result text: {result_text}")

            if "You have selected" in result_text or "You have selected :" in result_text:
                # Extract the part after the colon
                items_text = result_text.split(":")[-1].strip()
                # Split by whitespace and filter empty strings, convert to lowercase
                items = [item.strip().lower() for item in items_text.split() if item.strip()]
                logger.debug(f"Selected items: {items}")
                return items

            return []
        except Exception as e:
            logger.error(f"Error getting selected items: {e}")
            return []
