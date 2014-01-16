from webapp2 import WSGIApplication, Route
import views as v

urls = [
    Route(
        r'/',
        handler=v.Home,
        name='Home'
    ),

    Route(
        r'/update',
        handler=v.Update,
        name='Update'
    ),

    Route(
        r'/remove',
        handler=v.Remove,
        name='Remove'
    ),

    Route(
        r'/save',
        handler=v.Save,
        name='Save'
    ),

    Route(
        r'/do',
        handler=v.Do,
        name='Do'
    ),

    Route(
        r'/add',
        handler=v.Add,
        name='Add'
    )
]

app = WSGIApplication(urls, debug=True)




    # Route(
    #     r'/loyalties',
    #     handler=v.Loyalties,
    #     name='Loyalties'
    # ),