from django.urls import path, re_path

urlpatterns = [
    path("foo/<int:bar>/", lambda: None, name="foo"),
    path("baz/<str:bar>/", lambda: None, name="baz"),
    path("qux/<username>/", lambda: None, name="qux"),
    re_path(r"zod/(?P<username>\w+)/$/", lambda: None, name="zod"),
]
