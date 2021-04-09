from os import remove
from urllib.request import urlretrieve
from enginesdk.v1.services.predict import BasePredictor
from enginesdk.v1.schemas.url import ImageUrl
from enginesdk.v1.services.uploader import upload


class SchemaFactory:
    @staticmethod
    def mock_input() -> ImageUrl:
        return ImageUrl(
            image_url="https://res.cloudinary.com/trouni/image/upload/c_thumb,w_200,g_face/v1617982889/kaepler/engines/kaepler-engine/test_image.jpg"
        )

    @staticmethod
    def mock_output() -> ImageUrl:
        return ImageUrl(
            image_url="https://res.cloudinary.com/trouni/image/upload/c_thumb,w_200,g_face/v1617982889/kaepler/engines/kaepler-engine/test_image.jpg"
        )


class Predictor(BasePredictor):
    def _load_model(self):
        """
        Returns the predictor object.
        """
        return lambda x: x

    def _read_input(self, input):
        """
        Read input and implement pre processing steps.
        """
        urlretrieve(input.image_url, "temp.jpg")
        return input

    def _predict(self, model, input):
        """
        Perform the inference.
        For example `model.predict(input)` or `model(input)`.
        """
        return model(input)

    def _post_processing(self, model_input, prediction):
        """
        Implement post processing steps and returns the output. Examples:
        - combining images
        - uploading image/video to cloud storage
        """
        # Testing uploader service
        upload(
            "temp.jpg",
            public_id="test_image",
            overwrite=True,
        )
        remove("temp.jpg")
        return ImageUrl(image_url="Test output")


class PredictFactory:
    @staticmethod
    def mock_predictor() -> Predictor:
        return Predictor(SchemaFactory)
