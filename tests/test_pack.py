import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


PACK_SCRIPT = Path(__file__).resolve().parents[1] / "assets" / "pack.py"
SPEC = importlib.util.spec_from_file_location("m2dev_pack", PACK_SCRIPT)
pack = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pack)


class PackScriptTest(unittest.TestCase):
    def test_discover_pack_folders_excludes_hidden_and_tool_directories(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            assets_dir = Path(temporary_directory)
            for name in ("root", "locale", ".claude", "tools", "__pycache__", "zz_ignore_old"):
                (assets_dir / name).mkdir()

            names = [path.name for path in pack.discover_pack_folders(assets_dir)]

        self.assertEqual(["locale", "root"], names)

    def test_pack_folder_reports_missing_input(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            base_dir = Path(temporary_directory)
            pack_maker = base_dir / "PackMaker.exe"
            pack_maker.touch()

            with mock.patch.object(pack.subprocess, "run") as run:
                result = pack.pack_folder(base_dir / "missing", pack_maker, base_dir / "pack")

        self.assertFalse(result)
        run.assert_not_called()

    def test_pack_folder_propagates_packmaker_failure(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            base_dir = Path(temporary_directory)
            input_dir = base_dir / "root"
            input_dir.mkdir()
            pack_maker = base_dir / "PackMaker.exe"
            pack_maker.touch()

            with mock.patch.object(
                pack.subprocess,
                "run",
                side_effect=subprocess.CalledProcessError(7, "PackMaker.exe"),
            ):
                result = pack.pack_folder(input_dir, pack_maker, base_dir / "pack")

        self.assertFalse(result)

    def test_pack_folder_uses_input_parent_as_working_directory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            base_dir = Path(temporary_directory)
            input_dir = base_dir / "root"
            input_dir.mkdir()
            pack_maker = base_dir / "PackMaker.exe"
            pack_maker.touch()
            output_dir = base_dir / "pack"

            with mock.patch.object(pack.subprocess, "run") as run:
                result = pack.pack_folder(input_dir, pack_maker, output_dir)

        self.assertTrue(result)
        run.assert_called_once_with(
            [
                str(pack_maker.resolve()),
                "--input",
                "root",
                "--output",
                str(output_dir.resolve()),
            ],
            check=True,
            cwd=input_dir.resolve().parent,
        )

    def test_pack_all_consumes_worker_results(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            assets_dir = Path(temporary_directory)
            (assets_dir / "good").mkdir()
            (assets_dir / "bad").mkdir()

            with mock.patch.object(pack, "pack_folder", side_effect=[False, True]) as worker:
                result = pack.pack_all_folders(assets_dir)

        self.assertFalse(result)
        self.assertEqual(2, worker.call_count)

    def test_main_returns_failure_when_pack_fails(self):
        with mock.patch.object(pack, "pack_folder", return_value=False):
            self.assertEqual(1, pack.main(["root"]))


if __name__ == "__main__":
    unittest.main()
