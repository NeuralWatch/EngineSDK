import logging
import time


class BasePredictor:
    def __init__(self):
        self.model = self._load_model()

    def _load_model(self):
        """
        Returns the predictor object.
        """
        pass

    def _read_input(self, input):
        """
        Read input and implement pre processing steps.
        """
        pass

    def _predict(self, input):
        """
        Perform the inference.
        For example `self.model.predict(input)` or `self.model(input)`.
        """
        pass

    def _post_processing(self, model_input, prediction):
        """
        Implement post processing steps and returns the output. Examples:
        - combining images
        - uploading image/video to cloud storage
        """
        pass

    def run(self, input):
        # Read input
        begin = time.perf_counter()
        model_input = self._read_input(input)
        logging.info(f"Reading input time: {time.perf_counter() - begin:0.4f} seconds.")

        # Perform inference
        begin_inference = time.perf_counter()
        logging.info(f"Starting Inference...")
        prediction = self._predict(model_input)
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
