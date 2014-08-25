from webapp2 import WSGIApplication, Route
import views

urls = [
    Route(
        r'/',
        handler=views.Home,
        name='Home'
    ),

    Route(
        r'/update',
        handler=views.Update,
        name='Update'
    ),

    Route(
        r'/remove',
        handler=views.Remove,
        name='Remove'
    ),

    Route(
        r'/save',
        handler=views.Save,
        name='Save'
    ),

    Route(
        r'/do',
        handler=views.Do,
        name='Do'
    ),

    Route(
        r'/add',
        handler=views.Add,
        name='Add'
    ),

    Route(
        r'/add_group',
        handler=views.AddGroup,
        name='AddGroup'
    ),

    Route(
        r'/order',
        handler=views.Order,
        name='Order'
    ),

    Route(
        r'/menu',
        handler=views.Menu,
        name='Menu'
    )
]

urls_admin = [
    Route(
        r'/admin/',
        handler=views.AdminConsole,
        name='AdminConsole'
    )
]

app = WSGIApplication(urls, debug=True)

app_admin = WSGIApplication(urls_admin, debug=True)