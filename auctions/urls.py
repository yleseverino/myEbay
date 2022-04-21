from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:product_id>", views.product, name="product"),
    path("addwhatlist/<int:product_id>", views.addwhatlist, name="addwhatlist"),
    path("rmwhatlist/<int:product_id>", views.rmwhatlist, name="rmwhatlist"),
    path("close_listing/<int:product_id>", views.close_listing, name="close_listing"),
    path("submit-bid", views.rmwhatlist, name="rmwhatlist"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("addwhatlist/<int:product_id>", views.comment_vw, name="comment")
]
