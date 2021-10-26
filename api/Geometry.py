

class Geometry():
    def fit_to_container(content_original_size, container_size, padding=0):
        """ Summary
            -------
            Computes the desired size of the content, in function of the
            ratio of the content and the size of the container

            This function is 
            All input values must be in the same unit.

            Returns
            -------
            modal_size : tuple
                bi-dimensional tuple containing the x and y size of the
                modal.
            window_width : int
            window_height : int
        """
        # size content in function of the container size

        # assign the x and y to different variables for ease of reading
        content_width, content_height = content_original_size
        container_width, container_height = container_size

        content_ratio = content_width / content_height
        container_ratio = container_width / container_height

        # size content based on content ratio and container size
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