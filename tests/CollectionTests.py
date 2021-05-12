import unittest

from api.Collection import Collection, CollectionImage, CollectionUtils

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
            datation="1503-1506",
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
            datation="1503-1506",
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
            datation="1503-1506",
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
                datation="Xe siècle",
                title="Mona Lisa (Joconde)",
                technique="Huile sur toile",
            )
        test_image2 = CollectionImage(
                filename ="asjbd.jpg",
                artist="Leonard de Vinci",
                datation="1001",
                title="Salvator Mundi",
                technique="Huile sur bois",

            )
        test_image3 = CollectionImage(
                filename ="4asdnkasjd.jpg",
                artist="Leonard Baldaquin",
                datation="1525-1530",
                title="Portrait de Mona Rosa",
                technique="Huile sur toile",
            )

        # Let's define a collection to filter
        test_list = [test_image1, test_image2, test_image3]

        self.assertEqual(
            [test_image1, test_image3], 
            CollectionUtils.filter(test_list, technique="Huile sur toile")
        )
        self.assertEqual(
            [test_image1, test_image2, test_image3],
            CollectionUtils.filter(test_list, artist="Leonard")
        )
        self.assertEqual(
            [test_image1, test_image2],
            CollectionUtils.filter(test_list, artist="Leonard de Vinci")
        )
        self.assertEqual(
            [test_image1, test_image3],
            CollectionUtils.filter(test_list, mode="all", artist="Leonard", title="Mona")
        )
        self.assertEqual(
            [test_image1, test_image2, test_image3],
            CollectionUtils.filter(test_list, mode="any", artist="Leonard", title="Mona")
        )


    def test_datation_to_numeric(self):

        tests = {
            "III-IVe siècles": 200,
            "trucs": 0, # when no estimation is found
            "1620": 1620,
            "IIème siècle": 100,
            "IIème siècle av. j-c": -200,
            "100 av. JC": -100,
            "60 après JC": 60,
            "60 après J-C": 60,
            "60 après j.-C.": 60,
            "60 après J.c.": 60,
            "1620-1630": 1620,
            "c. 1600": 1600,
            "circa 320": 320,
            "XXème siècle": 1900,
            "XXIe s.": 2000,
            "2e s.": 100,
            "1668-9": 1668,
            "1512-1525": 1512,
            "Ve s. av. JC": -500,
            "après 1515": 1515,
            "vers l'an 200": 200,
            "entre 301 et 313": 301,
            #"1ère moitié du XVIème siècle": 1550 # not implemented yet
        }

        for key, value in tests.items():
            result = CollectionUtils._datation_to_numeric(key)
            self.assertEqual(result, value)


    def test_sort(self):
        test_image1 = CollectionImage(
            filename ="48224.jpg",
            artist="a",
            datation="1001",
            title="Mona Lisa (Joconde)",
            technique="Huile sur toile"
        )
        test_image2 = CollectionImage(
            filename ="asjbd.jpg",
            artist="c",
            datation="Xe siècle",
            title="Salvator Mundi",
            technique="Huile sur bois"
        )
        test_image3 = CollectionImage(
            filename ="4asdnkasjd.jpg",
            artist="b",
            datation="1525",
            title="Portrait de Mona Rosa",
            technique="Huile sur toile"
        )


        test_list = [test_image1, test_image2, test_image3]

        self.assertEqual(
            [test_image1, test_image3, test_image2],
            CollectionUtils.sort(test_list, "artist")
        )
        self.assertEqual(
            [test_image1, test_image3, test_image2],
            CollectionUtils.sort(test_list, "title")
        )
        self.assertEqual(
            [test_image2, test_image1, test_image3],
            CollectionUtils.sort(test_list, "datation")
        )
