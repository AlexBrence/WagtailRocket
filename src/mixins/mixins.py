from django.shortcuts import render

from home.models import HomePage


class BreadcrumbMixin:
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        homepage = HomePage.objects.first()
        # Add current page data to items
        items = [ { "title": self.title, "url": self.url } ]

        if self.is_child_of(homepage):
            context["breadcrumbs"] = items
            return context

        # Fill ancestors' data
        ancestors = self.get_ancestors().specific()
        for page in ancestors.reverse():
            data = {
                "title": page.title,
                "url": page.url
            }
            items.insert(0, data)

            if page.is_child_of(homepage):
                break

        context["breadcrumbs"] = items
        return context


class HtmxMixin:
    partials_template = None # add partials, e.g. products/partials/_products.html

    def serve(self, request, *args, **kwargs):
        """ Handle HTMX request """
        if request.META.get("HTTP_HX_REQUEST") == "true":
            context = self.get_context(request)
            return render(request, self.partials_template, context) 
        return super().serve(request, args, kwargs)