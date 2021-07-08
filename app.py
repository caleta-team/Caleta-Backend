from app import create_app
main_app = create_app()
main_app.run(host='0.0.0.0', port=5000, debug=True)

