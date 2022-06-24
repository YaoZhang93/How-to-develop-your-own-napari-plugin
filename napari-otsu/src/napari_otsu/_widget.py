"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

from magicgui import magic_factory

if TYPE_CHECKING:
    import napari

from skimage.filters import threshold_otsu
from skimage.measure import label

@magic_factory
def otsu_seg_widget(img_layer: "napari.layers.Image") -> "napari.types.LayerDataTuple":

    threshold_seg = threshold_otsu(img_layer.data)
    binary_seg = img_layer.data > threshold_seg
    instance_seg = label(binary_seg)

    seg_layer = (instance_seg, {"name": f"{img_layer.name}_seg"}, "labels")

    return seg_layer
