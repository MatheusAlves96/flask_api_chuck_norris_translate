from flask import Flask
from flask_restful import Api
from resource.api_voxus_recruiter import Random_joker, Random_joker_by_category, All_categories, Joker_limited_query_txt

app = Flask(__name__)

#app config para retornar a falta de parametros individualmente na chamada da api
app.config['BUNDLE_ERRORS'] = True
api = Api(app)

#endpoint que retorna uma piada aleatoria
api.add_resource(Random_joker, '/api/jokes/random')

#endpoint que retorna uma piada por categoria
api.add_resource(Random_joker_by_category, '/api/jokes/category/<string:category>')

#endpoint que retorna piadas com limite definido pelo usuario e filtro de texto
api.add_resource(Joker_limited_query_txt, '/api/jokes/filter')

#endpoint que retorna todas as categorias
api.add_resource(All_categories, '/api/jokes/category')


if __name__ == '__main__':
    #iniciar servidor em localhost e porta 8080
    app.run(host='localhost', port=8080 , debug=True)