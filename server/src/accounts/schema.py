from graphene_django import DjangoObjectType
from graphene_django.fields import DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from graphene import ObjectType, Schema, relay
from accounts.models import Connection
from django.contrib.auth.models import User
from accounts.models import Connection


class ConnectionNode(DjangoObjectType):

	class Meta:
		model = Connection
		interfaces = (relay.Node, )
		filter_fields = ["from_user__username" , "to_user__username"]


# class UserNode(DjangoObjectType):

# 	class Meta:
# 		model = User
# 		interfaces = (relay.Node, )


class Query(ObjectType):
	connection = relay.Node.Field(ConnectionNode)
	all_connections = DjangoFilterConnectionField(ConnectionNode)
	# user = relay.Node.Field(UserNode)
	# all_users = DjangoConnectionField(UserNode)