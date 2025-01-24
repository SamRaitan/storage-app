from PIL import Image, PngImagePlugin
import os


class FileToImg:

    @staticmethod
    def _convert_bytes_to_hex(file_bytes):
        """
        Converts bytes to a hex string.
        """
        if not isinstance(file_bytes, bytes):
            raise ValueError("Expected file_bytes to be a bytes object.")
        return file_bytes.hex()

    @staticmethod
    def _create_image_from_hex(hex_data, output_image_path, metadata_dict):
        """
        Creates an image from hex data and embeds metadata.
        """
        # Calculate the image size (determine the width and height of the image)
        num_pixels = len(hex_data) // 6  # each pixel is represented by 6 hex characters (2 for each RGB)
        image_width = int(num_pixels ** 0.5)  # width as the square root of the pixel count
        image_height = (num_pixels // image_width) + (num_pixels % image_width > 0)  # calculate height to fit all pixels
        
        image = Image.new("RGB", (image_width, image_height), color="black")
        
        # Populate the image with pixel data
        pixels = image.load()
        index = 0
        for y in range(image_height):
            for x in range(image_width):
                if index + 5 >= len(hex_data):  # Ensure we don't exceed the hex data length
                    break
                r = int(hex_data[index:index + 2], 16)
                g = int(hex_data[index + 2:index + 4], 16)
                b = int(hex_data[index + 4:index + 6], 16)
                pixels[x, y] = (r, g, b)
                index += 6
        
        metadata = PngImagePlugin.PngInfo()
        for key, value in metadata_dict.items():
            metadata.add_text(key, value)

        image.save(f'{output_image_path}.png', "PNG", pnginfo=metadata)
        return f'{output_image_path}.png'

    @classmethod
    def process_file_to_image(cls, file_bytes, original_file_name):
        print(type(file_bytes))
        if not isinstance(file_bytes, bytes):
            raise ValueError("Expected file_bytes to be a bytes object.")

        hex_data = FileToImg._convert_bytes_to_hex(file_bytes)
        metadata_dict = {
            "OriginalFileName": os.path.splitext(original_file_name)[0],
            "Extension": os.path.splitext(original_file_name)[1],
            "CustomMessage": "hello" # user hash in the future
        }
        return FileToImg._create_image_from_hex(hex_data, os.path.splitext(original_file_name)[0], metadata_dict)