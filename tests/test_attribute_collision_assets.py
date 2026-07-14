import struct
import unittest
from collections import Counter
from pathlib import Path


ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
ATTRIBUTE_HEADER = b"AttributeData\x00"
DIMENSION_BYTES = {
    0: 2 * 4,  # PLANE
    1: 3 * 4,  # BOX - parsed by the loader, unsupported by collision instances
    2: 1 * 4,  # SPHERE
    3: 2 * 4,  # CYLINDER
    4: 3 * 4,  # AABB
    5: 3 * 4,  # OBB
}
UNSUPPORTED_RUNTIME_TYPES = {1: "BOX"}


def require_bytes(data, offset, size, path, field):
    if offset + size > len(data):
        raise AssertionError(
            f"{path}: truncated {field} at offset {offset}; "
            f"need {size} bytes, have {len(data) - offset}"
        )


def parse_collision_types(path):
    data = path.read_bytes()
    if not data.startswith(ATTRIBUTE_HEADER):
        raise AssertionError(f"{path}: invalid AttributeData header")

    offset = len(ATTRIBUTE_HEADER)
    require_bytes(data, offset, 8, path, "record counts")
    collision_count, height_count = struct.unpack_from("<II", data, offset)
    offset += 8
    collision_types = []

    for collision_index in range(collision_count):
        require_bytes(data, offset, 48, path, f"collision {collision_index} prefix")
        collision_type = struct.unpack_from("<I", data, offset)[0]
        offset += 48  # type + name[32] + position[3]
        if collision_type not in DIMENSION_BYTES:
            raise AssertionError(
                f"{path}: collision {collision_index} has unknown type {collision_type}"
            )
        payload_size = DIMENSION_BYTES[collision_type] + 16  # dimensions + quaternion
        require_bytes(data, offset, payload_size, path, f"collision {collision_index} payload")
        offset += payload_size
        collision_types.append(collision_type)

    for height_index in range(height_count):
        require_bytes(data, offset, 36, path, f"height {height_index} prefix")
        primitive_count = struct.unpack_from("<I", data, offset + 32)[0]
        offset += 36
        vertices_size = primitive_count * 12
        require_bytes(data, offset, vertices_size, path, f"height {height_index} vertices")
        offset += vertices_size

    if offset != len(data):
        raise AssertionError(f"{path}: {len(data) - offset} unparsed trailing bytes")

    return collision_types


class AttributeCollisionAssetsTest(unittest.TestCase):
    def test_mdatr_files_use_supported_runtime_collision_types(self):
        paths = sorted(ASSETS_DIR.rglob("*.mdatr"))
        self.assertTrue(paths, "no .mdatr AttributeData assets found")

        type_counts = Counter()
        unsupported = []
        for path in paths:
            collision_types = parse_collision_types(path)
            type_counts.update(collision_types)
            for collision_type in collision_types:
                if collision_type in UNSUPPORTED_RUNTIME_TYPES:
                    unsupported.append(
                        f"{path}: {UNSUPPORTED_RUNTIME_TYPES[collision_type]} ({collision_type})"
                    )

        self.assertFalse(
            unsupported,
            "unsupported collision types would reach CollisionData.cpp:\n"
            + "\n".join(unsupported),
        )
        self.assertTrue(type_counts, "AttributeData corpus contains no collision records")


if __name__ == "__main__":
    unittest.main()
