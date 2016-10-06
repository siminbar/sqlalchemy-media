
import unittest
from os.path import dirname, abspath, join

from sqlalchemy_media.descriptors import AttachableDescriptor
from sqlalchemy_media.processors import ImageProcessor


class ImageProcessorTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.this_dir = abspath(dirname(__file__))
        cls.stuff_path = join(cls.this_dir, 'stuff')
        cls.cat_jpeg = join(cls.stuff_path, 'cat.jpg')
        cls.cat_png = join(cls.stuff_path, 'cat.png')
        cls.dog_jpg = join(cls.stuff_path, 'dog_213X160.jpg')

    def test_image_processor(self):
        # guess content types from extension

        with AttachableDescriptor(self.cat_png) as d:
            new_file, info = ImageProcessor(fmt='jpg', width=200).process(d, dict(
                length=100000,
                extension='.jpg',
            ))
            self.assertEqual(len(new_file.getvalue()), 11149)
            self.assertDictEqual(info, {
                'content_type': 'image/jpeg',
                'width': 200,
                'height': 150,
            })

        with AttachableDescriptor(self.cat_jpeg) as d:
            # Checking when not modifying stream.
            new_file, info = ImageProcessor().process(d, dict())
            self.assertIsNone(new_file)
            self.assertIsNone(info)

        with AttachableDescriptor(self.cat_jpeg) as d:
            # Checking when not modifying stream.
            new_file, info = ImageProcessor(fmt='jpeg').process(d, dict())
            self.assertIsNone(new_file)
            self.assertIsNone(info)

        with AttachableDescriptor(self.cat_jpeg) as d:
            # Checking when not modifying stream.
            new_file, info = ImageProcessor(fmt='jpeg', width=640).process(d, dict())
            self.assertIsNone(new_file)
            self.assertIsNone(info)

        with AttachableDescriptor(self.cat_jpeg) as d:
            # Checking when not modifying stream.
            new_file, info = ImageProcessor(height=480).process(d, dict())
            self.assertIsNone(new_file)
            self.assertIsNone(info)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()