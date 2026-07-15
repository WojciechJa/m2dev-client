import re
import unittest
from collections import Counter
from pathlib import Path


ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
ATTACH_GROUP_DECL_RE = re.compile(r"\bGroup\s+AttachData\b", re.IGNORECASE)
ATTACH_GROUP_RE = re.compile(
    r"\bGroup\s+AttachData\s*\{(?P<body>[^{}]*)\}",
    re.IGNORECASE | re.DOTALL,
)
INTEGER_FIELD_TEMPLATE = r"^\s*{name}\s+(-?\d+)\s*$"
ATTACH_FILE_RE = re.compile(r'^\s*AttachFile\s+"([^"]*)"\s*$', re.MULTILINE | re.IGNORECASE)

FLY_ATTACH_EFFECT = 1
FLY_ATTACH_OBJECT = 2
KNOWN_ATTACH_TYPES = {0, FLY_ATTACH_EFFECT, FLY_ATTACH_OBJECT}
KNOWN_FLY_TYPES = set(range(5))


def integer_field(body, name, path, group_index):
    matches = re.findall(
        INTEGER_FIELD_TEMPLATE.format(name=re.escape(name)),
        body,
        re.MULTILINE | re.IGNORECASE,
    )
    if len(matches) != 1:
        raise AssertionError(
            f"{path}: AttachData {group_index} must contain exactly one {name}; "
            f"found {len(matches)}"
        )
    return int(matches[0])


def parse_attach_groups(path):
    text = path.read_text(encoding="utf-8-sig")
    declaration_count = len(ATTACH_GROUP_DECL_RE.findall(text))
    groups = []

    for group_index, match in enumerate(ATTACH_GROUP_RE.finditer(text)):
        body = match.group("body")
        attach_files = ATTACH_FILE_RE.findall(body)
        if len(attach_files) != 1:
            raise AssertionError(
                f"{path}: AttachData {group_index} must contain exactly one AttachFile; "
                f"found {len(attach_files)}"
            )

        groups.append(
            {
                "type": integer_field(body, "Type", path, group_index),
                "fly_type": integer_field(body, "FlyType", path, group_index),
                "attach_file": attach_files[0],
            }
        )

    if len(groups) != declaration_count:
        raise AssertionError(
            f"{path}: malformed AttachData group; "
            f"declared {declaration_count}, parsed {len(groups)}"
        )
    return groups


class FlyingAssetsTest(unittest.TestCase):
    def test_msf_attachments_use_supported_runtime_types(self):
        paths = sorted(
            path for path in ASSETS_DIR.rglob("*") if path.is_file() and path.suffix.lower() == ".msf"
        )
        self.assertTrue(paths, "no .msf flying assets found")

        type_counts = Counter()
        unsupported = []
        for path in paths:
            groups = parse_attach_groups(path)
            self.assertTrue(groups, f"{path}: no AttachData groups found")
            for group_index, group in enumerate(groups):
                attach_type = group["type"]
                fly_type = group["fly_type"]
                type_counts[attach_type] += 1

                self.assertIn(
                    attach_type,
                    KNOWN_ATTACH_TYPES,
                    f"{path}: AttachData {group_index} has unknown Type {attach_type}",
                )
                self.assertIn(
                    fly_type,
                    KNOWN_FLY_TYPES,
                    f"{path}: AttachData {group_index} has unknown FlyType {fly_type}",
                )
                if group["attach_file"]:
                    self.assertEqual(
                        Path(group["attach_file"]).suffix.lower(),
                        ".mse",
                        f"{path}: AttachData {group_index} effect must reference .mse",
                    )
                if attach_type != FLY_ATTACH_EFFECT:
                    unsupported.append(
                        f"{path}: AttachData {group_index} Type {attach_type} "
                        f"(FLY_ATTACH_OBJECT={FLY_ATTACH_OBJECT})"
                    )

        self.assertFalse(
            unsupported,
            "unsupported flying attachment types would reach FlyingInstance.cpp:\n"
            + "\n".join(unsupported),
        )
        self.assertEqual(
            set(type_counts),
            {FLY_ATTACH_EFFECT},
            "checked-in flying assets must remain on the implemented effect path",
        )


if __name__ == "__main__":
    unittest.main()
