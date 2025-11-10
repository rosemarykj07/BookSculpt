from django.urls import path
from . import views
urlpatterns = [
    path('',views.index),
    path('register/',views.register),
    path('login/',views.login),
    path('Users/',views.users),
    path('edit',views.edit),
    path('delete',views.delete),
    path('Add/',views.addbook),
    path('View/',views.viewbook),
    path('Userview/', views.userview, name='userview'),
    # path('userview/', views.viewbook, name='userview'),
    path('read/<int:book_id>/', views.readbook, name='readbook'),
    path("delete_book/<int:idl>/", views.delete_book, name="delete_book"),
    path('search/', views.search_books, name='search_books'),
    path("login1/", views.login_view, name="login"),
    path('recommend/', views.recommend_books, name='recommend_books'),
    path('userHome/',views.userHome, name="userHome"),
    path('adminHome/',views.adminHome),
    path('Admpro/',views.admin_profile, name="admin_profile"),
    path("adminedit", views.edit_admin_profile, name="edit_admin_profile"),
    
    path("reading-list/remove/<int:book_id>/", views.remove_from_reading_list, name="remove_from_reading_list"),
    path('contact',views.contact),
    path('collections/',views.collections),
    path('plans_manage/', views.manage_plans, name="manage_plans"),
    ###admin###
    path("plans/add/", views.add_plan, name="add_plan"),
    path("plans/edit/<int:plan_id>/", views.edit_plan, name="edit_plan"),
    path("plans/delete/<int:plan_id>/", views.delete_plan, name="delete_plan"),

    path("viewplans/", views.view_plans, name="view_plans"),
    path("subscribe/<int:plan_id>/", views.subscribe, name="subscribe"),
    path("mysubscription/", views.my_subscription, name="my_subscription"),
    path('book/<int:book_id>/', views.access_book, name='access_book'),
    # path("payment/<int:plan_id>/", views.payment, name="payment"),
    path('new/',views.new_arrivals, name="new_arrivals"),
    path("user_pro/", views.user_profile, name="user_profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path('trend',views.trending,name="trending"),
    path('admin_view/',views.admin_view_collections),

    # Show all reading lists for logged-in user
    path("my_reading_list/", views.my_reading_list, name="my_reading_list"),
    path("read/<int:book_id>/", views.read_book, name="read_book"),  
    ###
    path("boks/", views.book_list, name="book_Lists"),
    path("add_to_reading_list/<int:idn>/", views.add_to_reading_list, name="add_to_reading_list"),
    path("remove/<int:book_id>/", views.remove_from_reading_list, name="remove_from_reading_list"),
    path('mybooks/',views.mybooks),
    path("available_books/", views.available_books, name="available_books"),
    path("adminhome/subscriptions/", views.admin_subscriptions, name="admin_subscriptions"),
    path("adminhome/subscriptions/delete/<int:sub_id>/", views.delete_subscription, name="delete_subscription"),
    path('media/',views.media),
    # path("rl/add/<int:idn>/",views.readingList, name="reading_list"),
    # path("bk/<int:book_id>/", views.access_book, name="access_book"),
    
]