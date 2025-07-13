from dataclasses import dataclass
from typing import Iterable

from django.template.loader import render_to_string
from django.urls import URLResolver, get_resolver

DJANGO_CONVERTER_NAME_TO_TYPESCRIPT_TYPE = {
    "StringConverter": "string",
    "IntConverter": "number",
    "UUIDConverter": "string",
    "SlugConverter": "string",
}


@dataclass
class Parameter:
    name: str
    typescript_type: str


@dataclass
class Route:
    name: str
    params: list[Parameter]
    template: str


def munge_template(raw_template: str, params: list[str]) -> str:
    text = raw_template
    for param in params:
        text = text.replace(f"%({param})s", "${{{}}}".format(param))
    return text


def extract_routes(resolver: URLResolver, denylist: list[str]) -> Iterable[Route]:
    # A lot of this approach is borrowed from `django-js-reverse`, just with a different
    # way of munging the final routes.
    keys = [key for key in resolver.reverse_dict.keys() if isinstance(key, str)]
    key_to_route = {key: resolver.reverse_dict.getlist(key)[0][0][0] for key in keys}
    for key in keys:
        path, parameter_keys = key_to_route[key]
        parameter_to_converter = resolver.reverse_dict.getlist(key)[0][3]
        params = []
        for parameter_key in parameter_keys:
            if parameter_key not in parameter_to_converter:
                typescript_type = "string"
            else:
                converter = parameter_to_converter[parameter_key]
                converter_class_name = converter.__class__.__name__
                typescript_type = DJANGO_CONVERTER_NAME_TO_TYPESCRIPT_TYPE.get(
                    converter_class_name, "string"
                )
            param = Parameter(name=parameter_key, typescript_type=typescript_type)
            params.append(param)
        yield Route(key, params, munge_template(path, parameter_keys))
    for key, (prefix, subresolver) in resolver.namespace_dict.items():
        if key in denylist:
            continue
        for route in extract_routes(subresolver, denylist):
            yield Route(
                f"{key}:{route.name}", route.params, f"{prefix}{route.template}"
            )


def generate_routes(urlconf: str, denylist: list[str]) -> str:
    resolver = get_resolver(urlconf)
    routes = extract_routes(resolver, denylist)
    rendered_string = render_to_string("urls.ts.template", {"routes": routes})
    # Remove all empty lines injected via the template.
    rendered_string = "\n".join(line for line in rendered_string.split("\n") if line.strip())
    return rendered_string.strip() + "\n"
