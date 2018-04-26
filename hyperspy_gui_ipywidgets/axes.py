import ipywidgets

from hyperspy_gui_ipywidgets.utils import (
    labelme, register_ipy_widget, add_display_arg)
from link_traits import link


@register_ipy_widget(toolkey="navigation_sliders")
@add_display_arg
def ipy_navigation_sliders(obj, **kwargs):
    continuous_update = ipywidgets.Checkbox(True,
                                            description="Continous update")
    wdict = {}
    wdict["continuous_update"] = continuous_update
    widgets = []
    for i, axis in enumerate(obj):
        axis_dict = {}
        wdict["axis{}".format(i)] = axis_dict
        iwidget = ipywidgets.IntSlider(
            min=0,
            max=axis.size - 1,
            readout=True,
            description="index"
        )
        link((continuous_update, "value"),
             (iwidget, "continuous_update"))
        link((axis, "index"), (iwidget, "value"))
        vwidget = ipywidgets.BoundedFloatText(
            min=axis.low_value,
            max=axis.high_value,
            step=axis.scale,
            description="value"
            # readout_format=".lf"
        )
        link((continuous_update, "value"),
             (vwidget, "continuous_update"))
        link((axis, "value"), (vwidget, "value"))
        link((axis, "high_value"), (vwidget, "max"))
        link((axis, "low_value"), (vwidget, "min"))
        link((axis, "scale"), (vwidget, "step"))
        name = ipywidgets.Label(str(axis),
                                layout=ipywidgets.Layout(width="15%"))
        units = ipywidgets.Label(layout=ipywidgets.Layout(width="5%"),
                                 disabled=True)
        link((axis, "name"), (name, "value"))
        link((axis, "units"), (units, "value"))
        bothw = ipywidgets.HBox([name, iwidget, vwidget, units])
        # labeled_widget = labelme(str(axis), bothw)
        widgets.append(bothw)
        axis_dict["value"] = vwidget
        axis_dict["index"] = iwidget
        axis_dict["units"] = units
    widgets.append(continuous_update)
    box = ipywidgets.VBox(widgets)
    return {"widget": box, "wdict": wdict}


@register_ipy_widget(toolkey="DataAxis")
@add_display_arg
def _get_axis_widgets(obj):
    widgets = []
    wd = {}
    name = ipywidgets.Text()
    widgets.append(labelme(ipywidgets.Label("Name"), name))
    link((obj, "name"), (name, "value"))
    wd["name"] = name

    size = ipywidgets.IntText(disabled=True)
    widgets.append(labelme("Size", size))
    link((obj, "size"), (size, "value"))
    wd["size"] = size

    index_in_array = ipywidgets.IntText(disabled=True)
    widgets.append(labelme("Index in array", index_in_array))
    link((obj, "index_in_array"), (index_in_array, "value"))
    wd["index_in_array"] = index_in_array
    if obj.navigate:
        index = ipywidgets.IntSlider(min=0, max=obj.size - 1)
        widgets.append(labelme("Index", index))
        link((obj, "index"), (index, "value"))
        wd["index"] = index

        value = ipywidgets.FloatSlider(
            min=obj.low_value,
            max=obj.high_value,
        )
        wd["value"] = value
        widgets.append(labelme("Value", value))
        link((obj, "value"), (value, "value"))
        link((obj, "high_value"), (value, "max"))
        link((obj, "low_value"), (value, "min"))
        link((obj, "scale"), (value, "step"))

    units = ipywidgets.Text()
    widgets.append(labelme("Units", units))
    link((obj, "units"), (units, "value"))
    wd["units"] = units

    scale = ipywidgets.FloatText()
    widgets.append(labelme("Scale", scale))
    link((obj, "scale"), (scale, "value"))
    wd["scale"] = scale

    offset = ipywidgets.FloatText()
    widgets.append(labelme("Offset", offset))
    link((obj, "offset"), (offset, "value"))
    wd["offset"] = offset

    return {
        "widget": ipywidgets.VBox(widgets),
        "wdict": wd
    }


@register_ipy_widget(toolkey="AxesManager")
@add_display_arg
def ipy_axes_gui(obj, **kwargs):
    wdict = {}
    nav_widgets = []
    sig_widgets = []
    for i, axis in enumerate(obj.navigation_axes):
        wd = _get_axis_widgets(axis, display=False)
        accord = ipywidgets.Accordion([wd["widget"]])
        accord.set_title(0, "Axis {}".format(i))
        nav_widgets.append(accord)
        wdict["axis{}".format(i)] = wd["wdict"]
    for j, axis in enumerate(obj.signal_axes):
        wd = _get_axis_widgets(axis, display=False)
        accord = ipywidgets.Accordion([wd["widget"]])
        accord.set_title(0, "Axis {}".format(i + j + 1))
        sig_widgets.append(accord)
        wdict["axis{}".format(i + j + 1)] = wd["wdict"]
    nav_accordion = ipywidgets.VBox(nav_widgets)
    sig_accordion = ipywidgets.VBox(sig_widgets)
    tabs = ipywidgets.HBox([nav_accordion, sig_accordion])
    return {
        "widget": tabs,
        "wdict": wdict,
    }
