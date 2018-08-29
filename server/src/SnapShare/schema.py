from posts.schema import Query as PostQuery
from accounts.schema import Query as AccountQuery
# import cookbook.recipes.schema
import graphene

from graphene_django.debug import DjangoDebug


class Query(PostQuery, AccountQuery, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=Query)