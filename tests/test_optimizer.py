import tempfile
import unittest
from pathlib import Path
from PIL import Image
from image_optimizer import optimize_image, main


class OptimizeTests(unittest.TestCase):
    def test_resize_and_unique_names(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            source = folder / "image.png"
            Image.new("RGB", (1600, 800), "red").save(source)
            out = folder / "output"
            first = optimize_image(source, out, 800, 500, 80)
            second = optimize_image(source, out, 800, 500, 80)
            self.assertIsNone(first.error)
            self.assertEqual(first.destination.name, "image_800x400.jpg")
            self.assertEqual(second.destination.name, "image_800x400_1.jpg")
            with Image.open(first.destination) as image:
                self.assertEqual(image.size, (800, 400))

    def test_alpha_composited_to_white(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            source = folder / "alpha.png"
            Image.new("RGBA", (20, 20), (255, 0, 0, 0)).save(source)
            result = optimize_image(source, folder / "out", 100, 100)
            with Image.open(result.destination) as image:
                self.assertGreater(min(image.getpixel((0, 0))), 245)

    def test_invalid_file_does_not_crash(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            source = folder / "broken.png"
            source.write_bytes(b"not an image")
            result = optimize_image(source, folder / "out", 500, 500)
            self.assertIsNotNone(result.error)

    def test_cli_validation(self):
        with self.assertRaises(SystemExit) as ctx:
            main(["--max-width", "0"])
        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
