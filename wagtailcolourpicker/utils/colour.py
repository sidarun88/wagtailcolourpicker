from wagtail.admin.rich_text.editors.draftail import features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler

from wagtailcolourpicker.conf import get_setting


def get_colour_choices():
    choices = {name: prop['hex_code'] for name, prop in get_setting('COLOURS').items()}
    return tuple(choices.items())


def get_feature_name(name):
    feature = 'colour_%s' % name
    return feature


def get_feature_name_upper(name):
    return get_feature_name(name).upper()


def get_feature_name_list():
    return [get_feature_name_upper(name) for name in get_setting('COLOURS').keys()]


def register_color_feature(name, colour, css_class, features):
    feature_name = get_feature_name(name)
    type_ = get_feature_name_upper(name)
    tag = 'span'
    detection = '%s[class="%s"]' % (tag, css_class)

    control = {
        'type': type_,
        'icon': get_setting('ICON'),
        'description': colour,
        'style': {'color': colour}
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {detection: InlineStyleElementHandler(type_)},
        'to_database_format': {
            'style_map': {
                type_: {
                    'element': tag,
                    'props': {
                        'class': css_class,
                    }
                }
            }
        },
    })

    features.default_features.append(feature_name)


def register_all_colour_features(features):
    for name, colour_props in get_setting('COLOURS').items():
        colour = colour_props['hex_code']
        css_class = colour_props['css_class']
        register_color_feature(name, colour, css_class, features)


def get_list_colour_features_name():
    """
    Add list names into your
    models.py RichTextField(features=[get_list_features_name()]
    """
    list_features_name = list()

    for name, colour_props in get_setting('COLOURS').items():
        name_feature = get_feature_name(name)
        list_features_name.append(name_feature)
    return list_features_name
