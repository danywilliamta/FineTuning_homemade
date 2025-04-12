
from pydantic import BaseModel, Field


class Product(BaseModel):

    """
    Représente un produit.

    Attributs:
        name (str | None): Le nom du produit (par exemple, "Disque de frein").
        reference (str | None): La reference alphanumérique du produit (par exemple, "BG425Z", "90503").
        quantite (int | None): La quantité du produit.
        marque (str | None): La marque du produit.
    """
    name: str | None = Field(default=None)
    reference: str | None = Field(default=None)
    quantite: int | None = Field(default=None)
    marque: str | None = Field(default=None)

class DevisTool(BaseModel):
    produits: list[Product] | None = Field(description="List of products")
    client: str | None = Field(description="client")


class OrderTool(BaseModel):
    produits: list[Product] | None = Field(description="List of products")
    emplacement: str | None = Field(default=None, description="Emplacement")
    liste_prix: str | None = Field(default=None, description="Liste de prix")
    fournisseur: str | None = Field(description="fournisseur")


class StockTool(BaseModel):
    produits: list[Product] | None = Field(description="List of products")
