from typing import Dict, List, Union, TypedDict


class FlattenedItemText(TypedDict):
    type: str
    content: str


class FlattenedItemVariable(TypedDict):
    type: str
    content: str
    description: str


class FlattenedItemParagraph(TypedDict):
    type: str


FlattenedItem = Union[FlattenedItemText, FlattenedItemVariable, FlattenedItemParagraph]


class VersionData(TypedDict):
    text: str
    parts: List[FlattenedItem]


Prompts = Dict[str, Dict[str, Union[str, Dict[int, VersionData]]]]

TemplateObject = Dict[str, str]


class GeneratedPrompt(TypedDict):
    prompt: str
    metadata: Dict[str, Union[str, int, TemplateObject]]
