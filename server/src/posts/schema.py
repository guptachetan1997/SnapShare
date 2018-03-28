from graphene_django import DjangoObjectType
from graphene_django.fields import DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from graphene import ObjectType, Schema, relay
from posts.models import Post, Like, Comment
from django.contrib.auth.models import User


class PostNode(DjangoObjectType):

	class Meta:
		model = Post
		interfaces = (relay.Node, )
		filter_fields = {
			"user__username" : ["exact", ],
			"tags" : ["icontains", ]
		}


class UserNode(DjangoObjectType):

	class Meta:
		model = User
		interfaces = (relay.Node, )
		filter_fields = ["username", ]


class LikeNode(DjangoObjectType):

	class Meta:
		model = Like
		interfaces = (relay.Node, )
		filter_fields = ["post__uuid", "user__username"]


class CommentNode(DjangoObjectType):

	class Meta:
		model = Comment
		interfaces = (relay.Node, )
		filter_fields = ["post__uuid", "user__username"]


class Query(ObjectType):
	post = relay.Node.Field(PostNode)
	all_posts = DjangoFilterConnectionField(PostNode)
	user = relay.Node.Field(UserNode)
	all_users = DjangoFilterConnectionField(UserNode)
	like = relay.Node.Field(LikeNode)
	all_likes = DjangoFilterConnectionField(LikeNode)
	comment = relay.Node.Field(CommentNode)
	all_comments = DjangoFilterConnectionField(CommentNode)