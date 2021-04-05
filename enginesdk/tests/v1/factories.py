from enginesdk.v1.services.predict import BasePredictor
from enginesdk.v1.schemas.url import ImageUrl


class SchemaFactory:
    @staticmethod
    def mock_input() -> ImageUrl:
        return ImageUrl(
            image_url="https://images.theconversation.com/files/274523/original/file-20190515-60557-1xbt1cb.jpg"
        )

    @staticmethod
    def mock_output() -> ImageUrl:
        return ImageUrl(
            image_url="https://images.theconversation.com/files/274523/original/file-20190515-60557-1xbt1cb.jpg"
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
        return ImageUrl(image_url="Test output")


class PredictFactory:
    @staticmethod
    def mock_predictor() -> Predictor:
        return Predictor(SchemaFactory)
