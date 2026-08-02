import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
import hashlib
from typing import Sequence, OrderedDict

import jinja2
import requests

swagger_to_py = {
    ('integer', None): 'int',
    ('integer', 'int64'): 'int',
    ('boolean', None): 'bool',
    ('string', None): 'str',
    ('string', 'date-time'): 'str',
    ('number', 'float'): 'float'
}


@dataclass
class Field:
    name: str
    type_: str
    format: str | None
    description: str | None
    items: str | None


@dataclass
class Ref:
    url: str
    name: str
    description: str | None


@dataclass
class Class:
    name: str
    parent: str | None
    fields: Sequence[Field]


@dataclass
class Enum:
    name: str
    type_: str
    members: list[str]
    description: str

@dataclass
class Array:
    name: str
    fixed_items: int | None
    type_: str
    format: str
    description: str


_refs: dict[str, dict] = {}

_classes: OrderedDict[str, Class | Enum | Array] = OrderedDict()

def _get(url: str) -> dict:
    if 'HOME' in os.environ and os.path.isdir(syscachedir := (Path(os.environ['HOME']) / '.cache')):
        cachedir = syscachedir / 'swagger_to_python'
        if not os.path.isdir(cachedir):
            os.mkdir(cachedir)
        file = hashlib.md5(url.encode()).hexdigest() + '.json'
        cachepath = cachedir / file
        if os.path.isfile(cachepath):
            with open(cachepath, 'r') as f:
                return json.load(f)
        data = requests.get(url=url).json()
        with open(cachepath, 'w') as f:
            json.dump(data, f)
        return data
    return requests.get(url=url).json()

def _lookup_ref(url: str, name: str) -> dict:
    global _refs
    if url not in _refs:
        _refs[url] = _get(url)
    return {name: _refs[url][name]}

def _ref_from_dct(ref: dict) -> Ref:
    url, name = ref['$ref'].split('#/')
    return Ref(url, name, ref.get('description'))


def _convert(input: dict) -> None:
    global _classes
    for k, v in input.items():
        class_name = k
        if class_name in _classes:
            continue
        fields: list[Field] = []
        parent_class = None
        if 'allOf' in v:
            parent_ref = _ref_from_dct(v['allOf'][0])
            _convert(_lookup_ref(parent_ref.url, parent_ref.name))
            parent_class = parent_ref.name
            properties = v['allOf'][1]['properties']
        elif 'enum' in v:
            if v['type'] != 'string':
                raise RuntimeError('Unknown enum type for %s' % class_name)
            _classes[class_name] = Enum(
                name=class_name,
                type_='StrEnum',
                members=[choice for choice in v['enum']],
                description=v.get('description', '')
            )
            continue
        elif v.get('type') == 'array':
            _classes[class_name] = Array(
                name=class_name,
                fixed_items=int(v['minItems']) if v.get('minItems') and v['minItems'] == v.get('maxItems') else None,
                type_=v['items']['type'],
                format=v['items']['format'],
                description=v.get('description', '')
            )
            continue
        else:
            try:
                properties = v['properties']
            except KeyError:
                print(k)
                raise
        for field_name, props in properties.items():
            items = None

            if '$ref' in props:
                ref = _ref_from_dct(props)
                _convert(_lookup_ref(ref.url, ref.name))
                fields.append(
                    Field(
                        name=field_name,
                        type_='object',
                        format=ref.name,
                        description=ref.description,
                        items=None
                    )
                )
            else:
                if props.get('type') == 'array':
                    items_ref = _ref_from_dct(props['items'])
                    _convert(_lookup_ref(items_ref.url, items_ref.name))
                    items = items_ref.name

                fields.append(
                    Field(
                        name=field_name,
                        type_=props['type'],
                        format=props.get('format', None),
                        description=props.get('description', None),
                        items=items
                    )
                )
        _classes[class_name] = Class(
            name=class_name,
            parent=parent_class,
            fields=fields,
        )

def main():
    arg = sys.argv[1]
    if arg.startswith('http:') or arg.startswith('https:'):
        data = _get(arg)
    else:
        with open(arg, 'r') as f:
            data = json.load(f)
    _convert(data)
    classes: list[dict] = []
    enums: list[dict] = []
    typedefs: list[dict] = []
    for class_ in _classes.values():
        if isinstance(class_, Enum):
            enums.append({
                'name': class_.name,
                'type': class_.type_,
                'members': class_.members,
                'description': class_.description,
            })
            continue
        elif isinstance(class_, Array):
            if class_.fixed_items > 0:
                type_ = 'tuple[%s]' % ', '.join((swagger_to_py[(class_.type_, class_.format)] for _ in range(0, class_.fixed_items)))
            else:
                type_ = 'Sequence[%s]' % swagger_to_py[(class_.type_, class_.format)]
            typedefs.append({
                'name': class_.name,
                'type': type_,
                'description': class_.description,
            })
            continue
        fields: list[dict] = []
        for field_ in class_.fields:
            if field_.type_ == 'array':
                python_type = 'Sequence[%s]' % field_.items
            elif field_.type_ == 'object':
                python_type = field_.format
            else:
                python_type = swagger_to_py[(field_.type_, field_.format)]
            fields.append({
                'name': field_.name,
                'type': python_type,
                'description': field_.description
            })
        classes.append({
            'parent': class_.parent or 'Protocol',
            'fields': fields,
            'name': class_.name,

        })
    with open(Path(os.path.dirname(__file__)) / 'swagger_to_python.py.j2', 'r') as f:
        template = jinja2.Template(f.read())

    print(template.render(
        classes=classes,
        typedefs=typedefs,
        enums=enums,
    ))

if __name__ == '__main__':
    main()
