"""
CorpStage Shared Configuration Framework - YAML Parser Module.

This module handles safe and deterministic parsing of YAML config files.
In order to be extremely resilient, it imports the standard 'yaml' package
(PyYAML), and provides a robust native lightweight parser fallback if the
external packages aren't available, logging warnings appropriately.
"""

import sys
import os
import re
import logging
from typing import Dict, Any

from corpstage.backend.shared.config.exceptions import (
    ConfigFileNotFoundError,
    YAMLValidationError
)

logger = logging.getLogger("CorpStage.Config.YAMLParser")

class YAMLParser:
    """
    Parses YAML configuration files. Handles nested structures, lists, 
    and general syntax validations.
    """

    @staticmethod
    def load_file(file_path: str) -> Dict[str, Any]:
        """
        Loads a YAML configuration file and parses it safely into a dictionary.
        
        Args:
            file_path: The filesystem path to the YAML file.
            
        Returns:
            Dict[str, Any]: Parsed configuration values.
            
        Raises:
            ConfigFileNotFoundError: If the file does not exist.
            YAMLValidationError: If there is a syntax or parsing error.
        """
        if not os.path.exists(file_path):
            raise ConfigFileNotFoundError(f"Configuration file not found at: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            raise YAMLValidationError(f"Failed to read file {file_path}: {str(e)}")

        # Try to use PyYAML first (standard production pattern)
        try:
            import yaml
            try:
                data = yaml.safe_load(content)
                if data is None:
                    return {}
                if not isinstance(data, dict):
                    raise YAMLValidationError("Root element of platform-config.yaml must be a dictionary/object.")
                return data
            except yaml.YAMLError as ex:
                raise YAMLValidationError(f"YAML Syntax Error in {file_path}: {str(ex)}")
        except ImportError:
            # High-resigned fallback parser if PyYAML is not present
            logger.warning(
                "PyYAML library not installed. Falling back to native lightweight parser. "
                "For production, please install pyyaml."
            )
            return YAMLParser._parse_native_yaml(content)

    @staticmethod
    def _parse_native_yaml(content: str) -> Dict[str, Any]:
        """
        Synthesizes standard YAML parsing using a native stack-based line parser
        to support nested objects, double quotes, and simple lists in case PyYAML is missing.
        """
        lines = content.splitlines()
        root: Dict[str, Any] = {}
        stack: list = [( -1, root )]  # Stack of (indentation_level, dict_ref)

        for line_num, line in enumerate(lines, 1):
            # Safe cleaning of comments
            # Matches comments starting with # unless inside a string
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('#'):
                continue
                
            # If line is a divider like =================== or -------------------
            if stripped_line.startswith('==') or stripped_line.startswith('--'):
                continue

            # Determine indentation
            indent_match = re.match(r"^(\s*)", line)
            indent = len(indent_match.group(1)) if indent_match else 0

            # Match standard key-value: "key: value" or "key:"
            # Handles quoted keys or values or lists
            match = re.match(r"^([\w_-]+)\s*:\s*(.*)$", stripped_line)
            if not match:
                # Let's check for list items: "- val"
                list_match = re.match(r"^-\s*(.*)$", stripped_line)
                if list_match:
                    val_str = list_match.group(1).strip()
                    # Resolve val_str
                    val = YAMLParser._parse_scalar(val_str)
                    # We need to append this to the current active array
                    # This fallback handles simple origin arrays or list of lists
                    parent_indent, parent_dict = stack[-1]
                    # Check if there is an active list for the parent
                    # For simpl_yaml we'll represent arrays as list in dict. 
                    # We can find the last inserted key
                    if parent_dict and isinstance(parent_dict, dict):
                        keys = list(parent_dict.keys())
                        if keys:
                            last_key = keys[-1]
                            if not isinstance(parent_dict[last_key], list):
                                parent_dict[last_key] = []
                            parent_dict[last_key].append(val)
                    continue
                else:
                    # Non-standard line
                    continue

            key = match.group(1).strip()
            rest = match.group(2).strip()

            # Strip comments that occur at the end of values
            if '#' in rest:
                # simplistic check - if # is not in quotes
                if not (rest.startswith('"') and rest.endswith('"')) and not (rest.startswith("'") and rest.endswith("'")):
                    rest = rest.split('#')[0].strip()

            value = YAMLParser._parse_scalar(rest)

            # Re-adjust stack according to indentation
            while len(stack) > 1 and indent <= stack[-1][0]:
                stack.pop()

            parent_indent, parent_dict = stack[-1]

            if value == "":  # Represents potential section or empty string/null
                new_dict: Dict[str, Any] = {}
                parent_dict[key] = new_dict
                stack.append((indent, new_dict))
            else:
                parent_dict[key] = value

        return root

    @staticmethod
    def _parse_scalar(val_str: str) -> Any:
        """Helper to parse a basic scalar YAML value into proper Python type."""
        if not val_str:
            return ""
        
        # Handle quoted strings
        if (val_str.startswith('"') and val_str.endswith('"')) or (val_str.startswith("'") and val_str.endswith("'")):
            return val_str[1:-1]
            
        # Boolean
        if val_str.lower() in ("true", "yes", "on"):
            return True
        if val_str.lower() in ("false", "no", "off"):
            return False
            
        # Null
        if val_str.lower() in ("null", "~", "none"):
            return None
            
        # Numeric values
        try:
            if "." in val_str:
                return float(val_str)
            return int(val_str)
        except ValueError:
            pass
            
        return val_str
