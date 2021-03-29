import unittest

from api.CollectionImage import CollectionImage

class TestCollectionImage(unittest.TestCase):

    def test_eq(self):
        img1 = CollectionImage(filename="1")
        img2 = CollectionImage(filename="2")
        img3 = CollectionImage(filename="1")

        # we expect two CollectionImages that have the same filename to be
        # considered equal
        self.assertEqual(img1, img3)
        self.assertIn(img1, [img1, img2])
        self.assertIn(img3, [img1, img2])
        self.assertNotEqual(img1, img2)


    def test_to_reference(self):
        test_image1 = CollectionImage(
            filename ="48224.jpg",
            artist="Leonardo de Vinci",
            title="Mona Lisa (Joconde)",
            year="1503-1506",
            technique="Huile sur toile",
            conservation_site="Musée du Louvre, Paris",
            dimensions="77 x 53 cm"
            )
        expected_ref1 = "Leonardo de Vinci, Mona Lisa (Joconde), 1503-1506, Huile sur toile, 77 x 53 cm, Musée du Louvre, Paris"

        test_image2 = CollectionImage(
            filename ="48224.jpg",
            artist="Leonardo de Vinci",
            production_site="test",
            title="Mona Lisa (Joconde)",
            year="1503-1506",
            technique="Huile sur toile",
            conservation_site="Musée du Louvre, Paris",
            dimensions="77 x 53 cm"
            )
        expected_ref2 = "Leonardo de Vinci, Mona Lisa (Joconde), 1503-1506, Huile sur toile, 77 x 53 cm, Musée du Louvre, Paris"

        test_image3 = CollectionImage(
            filename ="48224.jpg",
            artist=None,
            production_site="test",
            title="Mona Lisa (Joconde)",
            year="1503-1506",
            technique="Huile sur toile",
            conservation_site="Musée du Louvre, Paris",
            dimensions="77 x 53 cm"
            )
        expected_ref3 = "Mona Lisa (Joconde), test, 1503-1506, Huile sur toile, 77 x 53 cm, Musée du Louvre, Paris"

        self.assertEqual(test_image1.to_reference(), expected_ref1)
        self.assertEqual(test_image2.to_reference(), expected_ref2)
        self.assertEqual(test_image3.to_reference(), expected_ref3)


if __name__ == '__main__':
    unittest.main()