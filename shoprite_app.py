import web, admin, controllers

urls = (
            '/?', 'controllers.MessageController',
            '/admin', admin.app_admin
            )

app = web.application(urls, globals())
application = app

if __name__ == "__main__": app.run()
