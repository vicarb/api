import graphene
from graphene_django import DjangoObjectType
from .models import Category, Negocios, Contact, Competencia, Producto, Token, PurchaseData, Cart, ECCategoria, ECNegocios, ECProducto, ECContact, ProductoImage
from ninja import Schema, ModelSchema


#EC SCHEMAS
class ECContactSchema(ModelSchema):
    class Config:
        model = ECContact
        model_fields = '__all__'

class ECProductoSchema(ModelSchema):
    class Config:
        model = ECProducto
        model_fields = '__all__'

class ECNegociosSchema(ModelSchema):
    class Config:
        model = ECNegocios
        model_fields = '__all__'

class ECCategoriaSchema(ModelSchema):
    class Config:
        model = ECCategoria
        model_fields = '__all__'
###

class ContactSchema(ModelSchema):
    class Config:
        model = Contact
        model_fields = '__all__'

class CartSchema(ModelSchema):
    class Config:
        model = Cart
        model_fields = '__all__'

class CompetenciaSchema(Schema):
    id: int
    title: str
    description: str
    image: str


class NegocioSchema(Schema):
    id: int
    name: str
    cat_name: str
    image: str
    description: str

class ProductoSchema(ModelSchema):
    class Config:
        model = Producto
        model_fields = '__all__'

class ProductoImageSchema(ModelSchema):
    class Config:
        model = ProductoImage
        model_fields = '__all__'

class TokenSchema(ModelSchema):
    class Config:
        model = Token
        model_fields = '__all__'

class PurchaseDataSchema(ModelSchema):
    class Config:
        model = PurchaseData
        model_fields = '__all__'
        arbitrary_types_allowed = True


class NotFoundSchema(Schema):
    message: str

class CategoryType(DjangoObjectType):
    class Meta: 
        model = Category
        fields = ('id','title')

class CompetenciaType(DjangoObjectType):
    class Meta:
        model = Competencia
        fields= ('id', 'title', 'description', 'image', 'date_created')

class NegocioType(DjangoObjectType):
    class Meta:
        model = Negocios
        fields = (
        'id',
        'name',
        'cat_name',
        'image',
        'description',
        'date_created',
        )

class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType)
    negocios = graphene.List(NegocioType)
    negocio = graphene.Field(NegocioType, id=graphene.String())
    competencias = graphene.List(CompetenciaType)
    competencia = graphene.List(CompetenciaType, id=graphene.String())


    def resolve_negocios(root, info, **kwargs):
        return Negocios.objects.all()
    
    def resolve_negocio(root, info, id):
        return Negocios.objects.get(pk=id)

    def resolve_competencias(root, info, **kwargs):
        return Competencia.objects.all()

    def resolve_negocio(root, info, id):
        return Competencia.objects.get(pk=id)


    def resolve_categories(root, info, **kwargs):
        # Querying a list
        return Category.objects.all()

class UpdateCategory(graphene.Mutation):
    class Arguments:
        # Mutation to update a category 
        title = graphene.String(required=True)
        id = graphene.ID()


    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, title, id):
        category = Category.objects.get(pk=id)
        category.title = title
        category.save()
        
        return UpdateCategory(category=category)

class CreateCategory(graphene.Mutation):
    class Arguments:
        # Mutation to create a category
        title = graphene.String(required=True)

    # Class attributes define the response of the mutation
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, title):
        category = Category()
        category.title = title
        category.save()
        
        return CreateCategory(category=category)

class NegocioInput(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()

class CreateNegocio(graphene.Mutation):
    class Arguments:
        input = NegocioInput(required=True)

    negocio = graphene.Field(NegocioType)
    
    @classmethod
    def mutate(cls, root, info, input):
        negocio = Negocios()
        negocio.name = input.name
        negocio.description = input.description
        negocio.save()
        return CreateNegocio(negocio=negocio)

class UpdateNegocio(graphene.Mutation):
    class Arguments:
        input = NegocioInput(required=True)
        id = graphene.ID()

    negocio = graphene.Field(NegocioType)
    
    @classmethod
    def mutate(cls, root, info, input, id):
        negocio = Negocios.objects.get(pk=id)
        negocio.name = input.name
        negocio.description = input.description
        negocio.save()
        return UpdateNegocio(negocio=negocio)

class Mutation(graphene.ObjectType):
    update_category = UpdateCategory.Field()
    create_category = CreateCategory.Field()
    create_negocio = CreateNegocio.Field()
    update_negocio = UpdateNegocio.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
