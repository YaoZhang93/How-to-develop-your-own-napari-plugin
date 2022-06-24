# Develop your own napari plugin: a tutorial
This repo presents a tutorial on developing a napari plugin that can segment objects from an image by Otsu's thresholding.

![image](https://github.com/YaoZhang93/How-to-develop-your-own-napari-plugin/blob/main/figs/example.png)

## What is napari

* **napari** is a fast, interactive, multi-dimensional **image viewer** for Python. It’s designed for browsing, annotating, and analyzing large multi-dimensional images.
* It includes **critical viewer features out-of-the-box**, such as support for large multi-dimensional data, and layering and annotation.
* By integrating closely with the **Python ecosystem**, napari can be easily coupled to leading machine learning and image analysis tools (e.g. scikit-image, scikit-learn, TensorFlow, PyTorch), enabling more **user-friendly automated analysis**.

## What is a napari plugin

napari plugins are just **Python packages**. Minimally, they must:

* Include **a static plugin manifest file** that details the contributions contained in the plugin.
* Declare **a napari.manifest entry point** that allows napari to detect the plugin at runtime.

Plugins allow developers to customize and extend napari. This includes:

* Adding **file format support** with readers and writers
* Adding **custom widgets** and **user interface elements**
* Providing sample data
* Changing the look of napari with a color theme

## How to develop a napari plugin

* Step 0: Prepare the virtual enviroment
* Step 1: Initialize the plugin with Cookiecutter template
* Step 2: Implement the plugin
* Step 3: Install your plugin and try it out

### Step 0: Prepare the virtual enviroment

```shell
 $: conda create -y -n napari-env -c conda-forge python=3.9
 $: conda activate napari-env
 $: python -m pip install "napari[all]"
```

### Step1: Initialize the plugin with Cookiecutter template

```shell
 $: pip install cookiecutter
 $: cookiecutter https://github.com/napari/cookiecutter-napari-plugin
```

You will be asked for some information to customize the setup of your plugin. Each prompt gives the default value in square brackets (`[]`). The following is the answer to the plugin in this tutorial. 

```shell
full_name [Napari Developer]: Yao Zhang
email [yourname@example.com]: zhangyao215@mails.ucas.ac.cn
github_username_or_organization [githubuser]: YaoZhang93
# NOTE: for packages whose primary purpose is to be a napari plugin, we
# recommend using the 'napari-' prefix in the package name.
# If your package provides functionality outside of napari, you may
# choose to leave napari out of the name.
plugin_name [napari-foobar]: napari-otsu
Select github_repository_url:
1 - https://github.com/YaoZhang93/napari-otsu
2 - provide later
Choose from 1, 2 [1]:
module_name [growth_cone_finder]: napari_otsu
display_name [napari FooBar]: Otsu Segmentation Plugin
short_description [A simple plugin to use with napari]:
# you can select from various plugin template examples
include_reader_plugin [y]: n
include_writer_plugin [y]: n
include_sample_data_plugin [y]: n
include_dock_widget_plugin [y]: y
use_git_tags_for_versioning [n]: n
Select license:
1 - BSD-3
2 - MIT
3 - Mozilla Public License 2.0
4 - Apache Software License 2.0
5 - GNU LGPL v3.0
6 - GNU GPL v3.0
Choose from 1, 2, 3, 4, 5, 6 (1, 2, 3, 4, 5, 6) [1]:
```

Thereafter, the plugin directory will be organized as follows

```shell
.
├── LICENSE
├── MANIFEST.in
├── README.md
├── pyproject.toml
├── setup.cfg
├── src
│   └── napari_otsu
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-39.pyc
│       │   └── _widget.cpython-39.pyc
│       ├── _tests
│       │   ├── __init__.py
│       │   └── test_widget.py
│       ├── _widget.py
│       └── napari.yaml
└── tox.ini
```

### Step 2: Implement the plugin

`_widget.py` defines the function that performs Otsu segmentation, which takes the image data as the input and returns the segmentation result. The decorator `@magic_factory` tells napari to automatically generate a GUI.

```python
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
```

`napari.yaml` tells napari that the plugin contributes a command, the location of the function that executes the command, and the plugin contributes a widget, and that we’d like napari to **autogenerate** the widget from the command signature

```yaml
name: napari-otsu
display_name: napari otsu
contributions:
  commands:
    - id: napari-otsu.make_otsu_seg_widget
      python_name: napari_otsu._widget:otsu_seg_widget
      title: Make Otsu Segmentation
  widgets:
    - command: napari-otsu.make_otsu_seg_widget
      display_name: Otsu Segmentation
```

`setup.cfg` allows your plugin to be installed by pip. We add `napari` and `scikit-image` as the necessary requirements for this plugin.

```shell
[options]
packages = find:
install_requires =
    numpy
    magicgui
    qtpy
    napari
    scikit-image
```

`__init__.py` imports the function in `_widget.py`.

```python
__version__ = "0.0.1"
from ._widget import otsu_seg_widget

__all__ = (
    "otsu_seg_widget",
)
```

### Step 3: Install your plugin and try it out

```shell
 $: pip install -e .
 $: napari
```

![image](https://github.com/YaoZhang93/How-to-develop-your-own-napari-plugin/blob/main/figs/workflow.png)