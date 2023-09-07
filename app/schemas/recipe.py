from typing import Sequence

from pydantic import BaseModel, HttpUrl, Field


class GetRecipe(BaseModel):
    class Config:
        orm_mode = True

    id: int
    label: str
    source: str
    url: HttpUrl
    submitter_id: int


class CreateRecipe(BaseModel):
    label: str
    source: str
    url: HttpUrl


class UpdateRecipe(CreateRecipe):
    pass


class SearchRecipe(BaseModel):
    total_results: int
    results: Sequence[GetRecipe]


class RandomRecipe(BaseModel):
    class Config:
        allow_population_by_field_name = True

    title: str = Field(..., alias="label")
    sourceName: str = Field(..., alias="source")
    sourceUrl: HttpUrl = Field(..., alias="url")
