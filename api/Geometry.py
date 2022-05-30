"""
    Regrouping reusable geometry math
"""

class Geometry():
    @staticmethod
    def fit_to_container(content_original_size : tuple, container_size : tuple, padding=0):
        """ Summary
            -------
            Computes the desired size of the content, in function of the
            ratio of the content and the size of the container

            This function is unit agnostic, but all input values must be
            expressed in the same unit.

            Arguments
            ---------
            content_original_size: tuple
                tuple containing the original x and y size of the
                content to fit (for example size of the image in pixels).
                Units don't matter, only the ratio between x and y.
            container_size: tuple
                tuple containg the x and y size of the container.
            padding: int
                Optional padding between content and
                container. Defaults to 0.

            Returns
            -------
            fitted_content_size : tuple
                bi-dimensional tuple containing the x and y size of the
                fitted content, in the units used for container_size.
        """
        # size content in function of the container size

        # assign the x and y to different variables for ease of reading
        content_width, content_height = content_original_size
        container_width, container_height = container_size

        content_ratio = content_width / content_height
        container_ratio = container_width / container_height

        # size content based on content ratio and container ratio
        if content_ratio < container_ratio:
            # size by height
            height = container_height - padding
            width = height * content_ratio
        else:
            # size by width
            width = container_width - padding
            height = width / content_ratio

        fitted_content_size = (width, height)

        return fitted_content_size
