from freedebtapp import create_app

app_func = create_app()

if __name__ == '__main__':
    app_func.run(debug = True)
