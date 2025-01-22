from pydantic import BaseModel


class PostProductRequest(BaseModel):
    artikul: int


class ProductSchema(BaseModel):
    name: str
    salePriceU: int
    reviewRating: float
    totalQuantity: int


class ProductsSchema(BaseModel):
    products: list[ProductSchema]


class DataSchema(BaseModel):
    data: ProductsSchema
