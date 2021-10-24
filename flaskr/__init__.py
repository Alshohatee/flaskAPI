from flask import Flask, jsonify, request
from models import setup_db, Plant
from flask_cors import CORS, cross_origin

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)
    #CORS(app, resources={r"*/api/*" : {origins: '*'}})
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
        return response

    #@cross_origin
    @app.route('/')
    def hello_world():
        return jsonify({'message':'HELLO, WORLD!'})
   
    @app.route('/plants', methods=['GET','POST'])
        #@cross_origin
    def get_plants():
        # Implement pagniation
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        plants = Plant.query.all()
        formatted_plants = [plant.format() for plant in plants]
        return jsonify({
            'success': True,
            'plants':formatted_plants[start:end],
            'total_plants': len(formatted_plants)
        })


    @app.route('/entrees/<int:entree_id>')
    def retrieve_entree(entree_id):
        return 'Entree %d' % entree_id
    return app