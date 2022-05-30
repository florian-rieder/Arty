import builtins
import csv
import re
from dataclasses import asdict

from unidecode import unidecode

from api.CollectionImage import CollectionImage

class CollectionUtils():
    """ Summary
        -------
        A static class regrouping a bunch of utility methods regarding
        Collections

        Methods
        -------
        filter(img_list, mode="any", **kwargs)
            Filters a list of CollectionImages based on metadata
        sort(img_list, attribute)
            Sorts the images in a list of CollectionImages
        
        Attributes
        ----------
        LEGEND_STYLES : dict
            List of available legend styles. Key is the style name and
            the value is the formattable string.

            Available tokens:
            artist, title, datation, production_site, technique,
            material, dimensions, conservation_site,
            production_site_if_no_artist

            Text modifiers:
            *** Not implemented yet ! ***
            [i][/i]: text between these tags will be rendered as italic
            [b][/b]: bold
    """

    AUTHORIZED_IMAGE_FORMATS = (
        ".jpg", ".jpeg", ".png", ".webp", ".tiff"
    )

    LEGEND_STYLES = {
        "SIMPLE": """
            {artist}{title_italic}{datation}
        """,
        "CHICAGO": """
            {artist}{title_italic}{production_site_if_no_artist}
            {datation}{material}{dimensions}{conservation_site}
        """,
    }

    @classmethod
    def filter(cls, img_list, mode="any", datation_min=-5000, datation_max=5000, **kwargs):
        """ Summary
            -------
            Filters a list of CollectionImages based on metadata

            Arguments
            ---------
            img_list : list(CollectionImage)
                A list of CollectionImages to filter.
            mode : str, default='any'
                Selection method for the filter. Either 'any' or 'all'.
                It's basically an OR/AND operator between the specified
                fields.
                (e.g. any: artist OR title must match; all: artist
                AND title must match)
            kwargs:
                Any attribute of CollectionImage (multiple allowed)

            Returns
            -------
            filtered_list : list(CollectionImages)
                List filtered according to the given parameters

            Examples
            --------
            filtered_collection = collection.filter(
                mode="all",
                title="Mona Lisa", artist="Leonard"
            )

            TODO
            ----
            Add a proper method for filtering by datation, such as "get
            all artworks in a range of dates (e.g. 1000-1200)"
        """
        # type check our list
        if not all(isinstance(i, CollectionImage) for i in img_list):
            raise TypeError(
                "All elements of img_list must be of type CollecitionImage"
            )

        # check that the mode chosen is valid
        if mode not in ("any", "all"):
            raise ValueError("mode must be either 'any' or 'all'")

        # check that the fields entered are valid CollectionImage fields
        for attr in kwargs:
            if not hasattr(CollectionImage, attr):
                raise ValueError("CollectionImage has no attribute %s" % attr)

        # pre-filter for datation
        img_list = [
            i for i in img_list if 
            datation_min <= cls._datation_to_numeric(i.datation) <= datation_max
        ]

        # for each image in the collection, retain if at least one of
        # the arguments matches (with the in keyword)
        # Here it is better for performance and readability to use a
        # list comprehension instead of filter()
        # ...but not for debugging though...
        return [
            # for each image in the collection
            image for image in img_list
            # this wizardry in the line below allows for using either
            # the 'any' or 'all' python builtins from name
            if getattr(builtins, mode)(
                # retain if any/all arguments matches
                # (with the in keyword)
                [
                    # check if the value we're looking for is in this
                    # image's attribute (accent and case insensitive)...
                    unidecode(value).lower() in unidecode(getattr(image, attr)).lower()
                    # ...but only if the attribute is filled in the
                    # current image
                    if getattr(image, attr) else False
                    # ...for each attribute we're filtering for...
                    for attr, value in kwargs.items()
                    # but only if we are actually filtering for that
                    # attribute
                    if value.strip()
                ]
            )
        ]


    @classmethod
    def sort(cls, img_list, attribute, reverse=False):
        """ Summary
            -------
            Sorts the images in a list of CollectionImages

            Arguments
            ---------
            img_list: list(CollectionImage)
                A list of CollectionImage
            attribute: str
                Any attribute of Collection image
            reverse: bool, default=False
                reverse the sorting

            Returns
            -------
            sorted_collection : list(CollectionImage)
                sorted collection

            Notes
            -----
            Does it make sense to sort by multiple arguments ? If so,
            how does one do it ?
        """
        # type check our list
        if not all(isinstance(i, CollectionImage) for i in img_list):
            raise TypeError(
                "All elements of img_list must be of type CollecitionImage"
            )

        # check that the argument is valid
        if not hasattr(CollectionImage, attribute):
            raise ValueError("CollectionImage has no attribute %s" % attribute)

        # special case with dates
        if attribute == "datation":
            # return the list sorted by estimated numeric value of
            # datation string
            return sorted(
                img_list,
                key=lambda i: cls._datation_to_numeric(getattr(i, attribute)),
                reverse=reverse
            )

        # return the list sorted by the chosen criterion
        return sorted(
            img_list,
            key=lambda i: getattr(i, attribute).lower(),
            reverse=reverse
        )


    @staticmethod
    def export_csv(image_list, output_file ,delimiter=","):
        """ Summary
            -------
            Export the collection to CSV and save to an output file
        """
        if not all(isinstance(i, CollectionImage) for i in image_list):
            raise TypeError()

        # get attributes names for csv headers
        attributes = asdict(image_list[0]).keys()

        with open(output_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=attributes, delimiter=delimiter)
            writer.writeheader()

            for image in image_list:
                dict_image = asdict(image)
                writer.writerow(dict_image)


    @classmethod
    def _datation_to_numeric(cls, datation_string):
        """ Summary
            -------
            Tries to estimate a numeric year value for datation strings
            for example:
            c. 1060 -> 1060
            IIè siècle av. j.-c. -> -200
            II-IIIè -> 100
            c. 1667-1668 -> 1667
            1666-8 -> 1666
            3-4ème siècle -> 200
            1667 -> 1667

            Notations:
            AP/AD can apply to all notations
            Estimated datation: 2 values given, centuries or years
                centuries: possible roman numerals
                    Note this little complication:
                           IIe s. AD -> 100
                           IIe s. AP -> -200
                year: no processing

            Returns
            -------
            int
                The estimated value of the input string. Returns 0 if
                nothing could be found

            Notes
            -----
            We could make it so that when we have two values, return the
            average of the two...

            TODO
            ----
            Implement management of quarter and half of century
            precisions:
                "2ème partie/moitié du IIème siècle" -> 150
                "3ème quart du XXème siècle" -> 1975
                "1er quart du 19ème siècle" -> 1800
                etc.
        """
        # detect AP/AD
        # NOTE: IN FRENCH !
        apad_regex = re.compile(
            r"((av\.?(ant)?)|(ap\.?(r[eè]s)?))\s?j\.?-?c\.?",
            flags=re.IGNORECASE
        )

        # detect numeric values (case sensitive)
        num_values = re.compile(r"\b[IVX]+|\b\d+")

        # detect if values are given in centuries
        century = re.compile(
            r"(\bsi[eè]cles?\b)|(\bs\.?\b)",
            flags=re.IGNORECASE
        )

        apad = 1

        # get AP/AD
        # AP -> negative number, AD -> positive number
        if re.search(apad_regex, datation_string):
            # check wether it is AP or AD
            apad = 1 if re.search(r"ap(?:r[eè]s)", datation_string) else -1

        values = list()

        # get all numeric values given in the string
        matches = re.findall(num_values, datation_string)
        if len(matches) > 0:
            # for each value
            for value in matches:
                # translate to int
                if re.match(r"[IVX]+", value):
                    values.append(cls._roman_to_int(value))
                else:
                    values.append(int(value))

        # check if the values are given in centuries
        if re.search(century, datation_string):
            # multiply each value by 100 (as each digit means a century)
            values = [i * 100 if apad == -1 else (i - 1) * 100 for i in values]

        # this is in case nothing was found
        if len(values) == 0:
            return 0

        # here we add the sign indicated by AP/AD
        return values[0] * apad


    @classmethod
    def _roman_to_int(cls, roman_numeral):
        """ Summary
            -------
            Converts roman numerals to int
            Entirely taken from :
            https://www.tutorialspoint.com/roman-to-integer-in-python

            Arguments
            ---------
            roman_numeral : str
                string of roman numerals (eg. 'XIII')

            Returns
            -------
            int
                decimal value of the roman numeral
        """
        roman = {
            'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000,'IV':4,
            'IX':9,'XL':40,'XC':90,'CD':400,'CM':900
        }

        i = 0
        num = 0
        while i < len(roman_numeral):
            if i+1<len(roman_numeral) and roman_numeral[i:i+2] in roman:
                num+=roman[roman_numeral[i:i+2]]
                i+=2
            else:
                num+=roman[roman_numeral[i]]
                i+=1
        return num
