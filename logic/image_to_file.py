from PIL import Image

class ImgToFile:

    @staticmethod
    def _open_image_and_extract_metadata(image_path):
        """
        Opens an image and extracts metadata.
        """
        image = Image.open(image_path)
        metadata = image.info
        original_file_name = metadata.get("OriginalFileName", "output")
        return image, original_file_name

    @staticmethod
    def _extract_hex_from_image(image):
        """
        Extracts pixel data from the image and converts it to a hex string.
        """
        pixels = image.load()
        image_size = image.size
        hex_data = ""

        for y in range(image_size[1]):
            for x in range(image_size[0]):
                r, g, b = pixels[x, y]
                hex_data += f"{r:02x}{g:02x}{b:02x}"  # Convert RGB values to hex

        return hex_data.rstrip("0")  # Remove padding

    @staticmethod
    def _convert_hex_to_file(hex_data, output_file_path):
        """
        Converts hex string back to bytes and saves it to a file.
        """
        file_bytes = bytes.fromhex(hex_data)
        with open(output_file_path, "wb") as f:
            f.write(file_bytes)

    @classmethod
    def process_image_to_file(cls, input_image_path):
        """
        Orchestrates the process of reading an image, extracting data, 
        and reconstructing the original file.
        """
        image, original_file_name = ImgToFile._open_image_and_extract_metadata(input_image_path)
        hex_data = ImgToFile._extract_hex_from_image(image)
        ImgToFile._convert_hex_to_file(hex_data, original_file_name)
        return original_file_name

