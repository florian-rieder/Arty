import unittest

from api.Collection import Collection, CollectionImage

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
        self.assertNotIn(img2, [img1, img3])
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
        self.assertEqual(test_image1.to_reference(), expected_ref1)

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
        self.assertEqual(test_image2.to_reference(), expected_ref2)

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
        self.assertEqual(test_image3.to_reference(), expected_ref3)

class TestCollection(unittest.TestCase):
    def test_filter(self):
        test_image1 = CollectionImage(
                filename ="48224.jpg",
                artist="Leonard de Vinci",
                production_site="test",
                title="Mona Lisa (Joconde)",
                year="1503-1506",
                technique="Huile sur toile",
                conservation_site="Musée du Louvre, Paris",
                dimensions="77 x 53 cm"
            )
        test_image2 = CollectionImage(
                filename ="asjbd.jpg",
                artist="Leonard de Vinci",
                production_site="test",
                title="Salvator Mundi",
                year="1503-1506",
                technique="Huile sur bois",
                conservation_site="Musée du Louvre, Paris",
                dimensions="66 x 45 cm"
            )
        test_image3 = CollectionImage(
                filename ="4asdnkasjd.jpg",
                artist="Leonard Baldaquin",
                title="Portrait de Mona Rosa",
                technique="Huile sur toile",
            )
        # Let's define a collection to filter
        test_coll = Collection("test", "test", [
            test_image1, test_image2, test_image3
        ])

        self.assertEqual(
            [test_image1, test_image3], 
            test_coll.filter(technique="Huile sur toile")
        )
        self.assertEqual(
            [test_image1, test_image2, test_image3],
            test_coll.filter(artist="Leonard")
        )
        self.assertEqual(
            [test_image1, test_image2],
            test_coll.filter(artist="Leonard de Vinci")
        )
        self.assertEqual(
            [test_image1, test_image3],
            test_coll.filter(mode="all", artist="Leonard", title="Mona")
        )
        self.assertEqual(
            [test_image1, test_image2, test_image3],
            test_coll.filter(mode="any", artist="Leonard", title="Mona")
        )