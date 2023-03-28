from dataclasses import dataclass
import itertools
import multiprocessing as mp

import numpy as np
from tesserocr import PyTessBaseAPI, RIL
from PIL.Image import Image

# TODO: OCRProcessor should
#   1) be run on the eye_env_wrapper in that separate process to prevent GIL blocking
#   2) use the _Buffered class to minimize code duplication
class OCRProcessor:

    OCR_Threads = 4

    @dataclass
    class Result:
        text: list[str]
        confidence: list[float]
        boxes: list[tuple[int, int, int, int]]

    _image_queue: mp.Queue
    _result_queue: mp.Queue

    _image_lock: mp.Lock
    _result_lock: mp.Lock

    _process: mp.Process

    def __init__(self):
        self._process = mp.Process(target=self._loop, args=(self,), daemon=True)

    def start(self):
        self._process.start()

    def stop(self):
        if not self._process.is_alive():
            return
        self._process.join()

    def add_image(self, image):
        with self._images_lock:
            self._image_queue.put(image)

    def get_result(self):
        with self._result_lock:  # required to prevent sampling after .empty() but before .put()
            return self._result_queue.get()  # we want it to block until there is a result

    def _step(self):

        with self._images_lock:
            image = self._image_queue.get()
            self._image_queue.empty()

        image = Image(image.numpy().astype(np.uint8))

        with PyTessBaseAPI() as api:
            api.SetImage(image)
            boxes = api.GetComponentImages(RIL.TEXTLINE, True)

        # work in parallel
        box_splits = itertools.groupby(boxes, lambda x: x[0] % OCRProcessor.OCR_Threads)

        def process_split(i):
            with PyTessBaseAPI() as api:
                api.SetImage(image)
                result_i = OCRProcessor.Result([], [], [])
                for _, box, _, _ in box_splits[i]:
                    api.SetRectangle(box["x"], box["y"], box["w"], box["h"])
                    ocrResult = api.GetUTF8Text()
                    conf = api.MeanTextConf()  # confidence, 0-100

                    # append to result_i
                    result_i.text.append(ocrResult)
                    result_i.confidence.append(conf)
                    result_i.boxes.append((box["x"], box["y"], box["w"], box["h"]))
            return result_i

        with mp.Pool(OCRProcessor.OCR_Threads) as pool:
            result_is = pool.map(
                process_split, box_splits
            )  # waits for all threads to finish
        result = OCRProcessor.Result(
            text=sum(*[result_i.text for result_i in result_is]),
            confidence=sum(*[result_i.confidence for result_i in result_is]),
            boxes=sum(*[result_i.boxes for result_i in result_is]),
        )

        with self._results_lock:
            self.results.empty()
            self.results.put(result)

    def _loop(self):
        while not self._process.is_alive():
            self._step()
