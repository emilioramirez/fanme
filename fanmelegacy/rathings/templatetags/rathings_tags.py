from django import template
from django.utils.encoding import smart_text
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from rathings.models import Like, Dislike

register = template.Library()


class BaseRatingNode(template.Node):

    @classmethod
    def token_handler(cls, parser, token):
        # This version uses a regular expression to parse tag contents.
        try:
            # Splitting by None == splitting by spaces.
            tag_name, arg = token.contents.split(None, 1)
        except ValueError:
            raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
        
        words = arg.strip().split(" ")
        
        if len(words) == 2:
            if words[0] != "for":
                print "no es for"
                raise template.TemplateSyntaxError("{} tag had invalid arguments: {}".format(tag_name, words[0]))
            object_expr = words[1]
            return cls(
                object_expr=parser.compile_filter(object_expr))
        elif len(words) == 4:
            print "es 4"
            if words[0] != "for":
                raise template.TemplateSyntaxError("{} tag had invalid arguments: {}".format(tag_name, words[0]))
            if words[2] != "as":
                raise template.TemplateSyntaxError("{} tag had invalid arguments: {}".format(tag_name, words[2]))
            object_expr, var_name = words[1], words[3]
            return cls(
                var_name=var_name,
                object_expr=parser.compile_filter(object_expr))
        else:
            raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)

    def __init__(self, var_name="", object_expr=None):
        if object_expr is None:
            raise template.TemplateSyntaxError("Rating nodes must be given either a literal object or a ctype and object pk.")
        
        self.rating_model = Like
        self.var_name = var_name
        self.object_expr = object_expr

    def get_target_ctype_pk(self, context):
        try:
            obj = self.object_expr.resolve(context)
        except template.VariableDoesNotExist:
            return None, None
        return ContentType.objects.get_for_model(obj), obj.pk

    def get_queryset(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        
        if not object_pk:
            return self.rating_model.objects.none()

        qs = self.rating_model.objects.filter(
            content_type = ctype,
            object_id = smart_text(object_pk),
            user = context['user']
        )
        return qs

    def get_context_value_from_queryset(self, context, qs):
        """Subclasses should override this"""
        raise NotImplementedError('subclasses of BaseRatingNode must provide a get_context_value_from_queryset method')

    def render(self, context):
        """
        The result of this tag are in var_name on the template context
        """
        qs = self.get_queryset(context)
        context[self.var_name] = self.get_context_value_from_queryset(context, qs)
        return ''


class LikeNode(BaseRatingNode):
    def get_context_value_from_queryset(self, context, qs):
        """Subclasses should override this."""
        return qs.count()


@register.tag
def count_likes(parser, token):
    """"""
    return LikeNode.token_handler(parser, token)


class LikeLinkNode(BaseRatingNode):
    
    def render(self, context):
        content_type, object_id = self.get_target_ctype_pk(context)
        url = "#"
        try:
            Like.objects.get(content_type=content_type, object_id=object_id, user=context['user'])
        except Like.DoesNotExist:
            url = reverse("rathings.views.like", args=[object_id])
        
        return render_to_string("rathings/like.html", {"url": url, "content_type": content_type})


@register.tag
def get_like_link(parser, token):
    return LikeLinkNode.token_handler(parser, token)


class DislikeNode(BaseRatingNode):

    def __init__(self, var_name="", object_expr=None):
        if object_expr is None:
            raise template.TemplateSyntaxError("Rating nodes must be given either a literal object or a ctype and object pk.")
        
        self.rating_model = Dislike
        self.var_name = var_name
        self.object_expr = object_expr

    def get_context_value_from_queryset(self, context, qs):
        """Subclasses should override this."""
        return qs.count()


@register.tag
def count_dislikes(parser, token):
    """"""
    return DislikeNode.token_handler(parser, token)


class DislikeLinkNode(DislikeNode):
    
    def render(self, context):
        content_type, object_id = self.get_target_ctype_pk(context)
        url = "#"
        try:
            Dislike.objects.get(content_type=content_type, object_id=object_id, user=context['user'])
        except Dislike.DoesNotExist:
            url = reverse("rathings.views.dislike", args=[object_id])

        return render_to_string("rathings/dislike.html",{"url": url, "content_type": content_type})


@register.tag
def get_dislike_link(parser, token):
    return DislikeLinkNode.token_handler(parser, token)
