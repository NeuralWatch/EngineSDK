import logging
import time


class BasePredictor:
    def __init__(self, schema_factory):
        """
        Initializes the predictor with a SchemaFactory object.
        """
        self._initialize()
        self.factory = schema_factory
        self.Input = type(schema_factory.mock_input())
        self.Output = type(schema_factory.mock_output())
        self.model = self._load_model()

    def _initialize(self):
        """
        Executes optional logic before loading the model.
        """
        pass

    def _load_model(self):
        """
        Returns the predictor object.
        """
        raise NotImplementedError()

    def _read_input(self, input):
        """
        Read input and implement pre processing steps.
        """
        raise NotImplementedError()

    def _predict(self, model, input):
        """
        Perform the inference.
        For example `model.predict(input)` or `model(input)`.
        """
        raise NotImplementedError()

    def _post_processing(self, model_input, prediction):
        """
        Implement post processing steps and returns the output. Examples:
        - combining images
        - uploading image/video to cloud storage
        """
        raise NotImplementedError()

    def run(self, input):
        # Read input
        begin = time.perf_counter()
        model_input = self._read_input(input)
        logging.info(f"Reading input time: {time.perf_counter() - begin:0.4f} seconds.")

        # Perform inference
        begin_inference = time.perf_counter()
        logging.info(f"Starting Inference...")
        prediction = self._predict(self.model, model_input)
        logging.info(
            f"Inference time: {time.perf_counter() - begin_inference:0.4f} seconds."
        )

        # Post processing
        begin_post_processing = time.perf_counter()
        output = self._post_processing(model_input, prediction)
        logging.info(
            f"Post-processing time: {time.perf_counter() - begin_post_processing:0.4f} seconds."
        )

        logging.info(f"Total time: {time.perf_counter() - begin:0.4f} seconds.")
        return output
