import json
import logging
import os
import re

from endcord import peripherals, utils

EXT_NAME = "Textreplace"
EXT_VERSION = "0.1.0"
EXT_ENDCORD_VERSION = "1.5.0"
EXT_DESCRIPTION = "An extension that replaces message text with extended regex before its sent"
EXT_SOURCE = "https://github.com/sparklost/endcord-textreplace"
logger = logging.getLogger(__name__)


def fix_find_regex(regex_str):
    """Compile javascript-like regex string to python regex"""
    match = re.match(r"^/(.+?)/([gimsuyv]*)$", regex_str)
    if match:
        pattern, flags_str = match.groups()
        flag_map = {"i": re.IGNORECASE, "m": re.MULTILINE, "s": re.DOTALL}
        combined_flags = 0
        for char in set(flags_str):
            if char in flag_map:
                combined_flags |= flag_map[char]
    else:
        pattern = regex_str
        combined_flags = 0
    pattern = re.sub(r"\(\?\<([A-Za-z_]\w*)\>", r"(?P<\1>", pattern)
    return re.compile(pattern, combined_flags)


def fix_replace_regex(replace_str):
    """Convert javascript-like regex replacement to python-friendly one"""
    replace_str = replace_str.replace("\\n", "\n")
    replace_str = replace_str.replace("$&", r"\g<0>")   # entire match
    replace_str = re.sub(r"\$\<([A-Za-z_]\w*)\>", lambda m: f"\\g<{m.group(1)}>", replace_str)   # named groups
    return re.sub(r"\$(\d+)", lambda m: f"\\g<{m.group(1)}>", replace_str)   # numbered groups


class Extension:
    """Main extension class"""

    def __init__(self, app):
        self.app = app
        try:
            default_rules = [{"find": "", "replace": "", "includes": ""}]
            path = os.path.expanduser(os.path.join(peripherals.config_path, "textreplace_rules.json"))
            if not os.path.exists(path):
                utils.save_json(default_rules, "textreplace_rules.json")
                return default_rules
            with open(path, "r", encoding="utf-8") as f:
                rules = json.load(f)
        except Exception as e:
            logger.error(f"Error reading textreplace_rules.json: {e}")
            del type(self).on_message_send
        self.rules = []
        for idx, rule in enumerate(rules):
            if not (rule.get("find") or rule.get("find_re")) or "replace" not in rule:
                continue
            if "find_re" in rule:
                try:
                    self.rules.append((fix_find_regex(rule["find_re"]), fix_replace_regex(rule["replace"]), rule.get("includes"), True))
                except Exception as e:
                    logger.error(f"Error compiling regex {rule["find_re"]}: {e}")
            else:
                self.rules.append((rule["find"].replace("\\n", "\n"), rule["replace"].replace("\\n", "\n"), rule.get("includes"), False))


    def on_message_send(self, message_text):
        """Check if message is relevant or not"""
        for rule in self.rules:
            includes = rule[2]
            if includes and includes not in message_text:
                continue
            if rule[3]:
                message_text = re.sub(rule[0], rule[1], message_text)
            else:
                message_text = message_text.replace(rule[0], rule[1])
        return message_text
