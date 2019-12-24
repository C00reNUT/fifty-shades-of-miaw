from os.path import join
from typing import Union, Iterator

import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
from keras_preprocessing.image import array_to_img
from fifty_shades.image_processing import save_image_from_tensor


class NeuralStyleTransfer:
    def __init__(self):
        self.hub_module = hub.load("https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/1")

    def predict_and_save_all(
        self, content_tensors: Iterator[tf.Tensor], style_tensors: Iterator[tf.Tensor], save_directory_path: str
    ) -> None:
        for i, (content_tensor, style_tensor) in enumerate(zip(content_tensors, style_tensors)):
            self.predict_and_save(
                i, content_tensor, style_tensor, save_directory_path, is_saving_content=True, is_saving_style=True
            )

    def predict_single_style_and_save_all(
        self, content_tensors: Iterator[tf.Tensor], style_tensor: tf.Tensor, save_directory_path: str
    ) -> None:
        for i, content_tensor in enumerate(content_tensors):
            self.predict_and_save(i, content_tensor, style_tensor, save_directory_path, is_saving_content=True)
        save_image_from_tensor(save_directory_path, "style.jpg", style_tensor)

    def predict_single_content_and_save_all(
        self, content_tensor: tf.Tensor, style_tensors: Iterator[tf.Tensor], save_directory_path: str
    ) -> None:
        for i, style_tensor in enumerate(style_tensors):
            self.predict_and_save(i, content_tensor, style_tensor, save_directory_path, is_saving_style=True)
        save_image_from_tensor(save_directory_path, "content.jpg", content_tensor)

    def predict_and_save(
        self,
        image_id: Union[str, int],
        content_tensor: tf.Tensor,
        style_tensor: tf.Tensor,
        save_directory_path: str,
        is_saving_content: bool = False,
        is_saving_style: bool = False,
    ) -> None:
        predicted_image = self.predict(content_tensor, style_tensor)
        predicted_image.save(join(save_directory_path, f"{image_id}.jpg"))
        if is_saving_content:
            save_image_from_tensor(save_directory_path, f"{image_id}-content.jpg", content_tensor)
        if is_saving_style:
            save_image_from_tensor(save_directory_path, f"{image_id}-style.jpg", style_tensor)

    def predict(self, content_tensor: tf.Tensor, style_tensor: tf.Tensor) -> Image:
        predicted_tensor = self.hub_module(tf.constant(content_tensor), tf.constant(style_tensor))[0][0]
        predicted_image = array_to_img(predicted_tensor)
        return predicted_image
