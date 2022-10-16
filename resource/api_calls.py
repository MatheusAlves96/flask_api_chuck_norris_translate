from flask import request
from flask_restful import Resource, reqparse
from deep_translator import GoogleTranslator
import requests

class Random_joker(Resource):
    def __init__(self):
        self.info = reqparse.RequestParser()
        #definir argumento pt_br tipo inteiro, default is False e location args, argumento utilizado
        #para definir se deseja traduçao da piada ou nao
        self.info.add_argument('pt_br', type=int, default=False, location='args')
    
    def random_joker(self):
        url = "https://api.chucknorris.io/jokes/random"
        
        #Get na url e tratativa do response retornando apenas o "value"
        response = requests.request("GET", url)
        if response.status_code == 200:
            response_dict = response.json()
            return response_dict['value']
        return False
    
    def get(self):
        info_dict = dict(self.info.parse_args())

        return_api = self.random_joker()
        if return_api: 
            if info_dict['pt_br'] == 1:
                #traduçao do value retornado pela função ramdom_joker caso o valor preenchido em pt_br seja 1
                translated = GoogleTranslator(source='en', target='portuguese').translate(return_api)
                return {'sucess' : True, 'joke_en' : return_api, 'joke_pt_br' : translated }, 200      
            return {'sucess' : True, 'joke_en' : return_api }, 200
        return {'sucess' : False, 'message' : 'Error on "https://api.chucknorris.io/" try later again' }, 202 
    
class All_categories(Resource):
    
    def all_categories(self):
        url = "https://api.chucknorris.io/jokes/categories"
        
        #get na api que retorna todas as categorias e retorna as categorias em forma de lista        
        response = requests.request("GET", url)
        if response.status_code == 200:
            response_dict = response.json()
            return response_dict
        return False
    
    def get(self):

        return_api = self.all_categories()
        if return_api:
            #envia o retorno da funçao para o cliente
            return {'sucess' : True, 'categories' : return_api }, 200
        return {'sucess' : False, 'message' : 'Error on "https://api.chucknorris.io/" try later again' }, 202 

class Random_joker_by_category(Resource):
    def __init__(self):
        self.info = reqparse.RequestParser()
        self.info.add_argument('pt_br', type=int, default=False, location='args')
        #request.host retorna o adress:port e adicionado a variavel seguinte para facilitar a leitura do cliente
        ip_address = request.host
        #variavel fora da função para edição caso necessario
        self.msg_not_found = f'No joke for category "_category_" found, send a GET to "http://{ip_address}/api/jokes/categories" to check available categories.'
    
    def random_joker_by_category(self, category):
        url = f"https://api.chucknorris.io/jokes/random?category={category}"
        
        
        #get no endpoint onde filtra as piadas por categorias retorna o value e o status code
        response = requests.request("GET", url)
        if response.status_code == 200:
            response_dict = response.json()
            return response_dict['value'], response.status_code
        elif response.status_code == 404:
            return self.msg_not_found.replace('_category_', category) , response.status_code
        return False
    
    def get(self, category):
        info_dict = dict(self.info.parse_args())

        return_api, return_code = self.random_joker_by_category(category)
        if return_api: 
            #retorno para o cliente o value e o return code já tratado pela api externa
            if info_dict['pt_br'] == 1:
                #adiciona a traduçao caso o cliente queira
                translated = GoogleTranslator(source='en', target='portuguese').translate(return_api)
                return {'sucess' : True, 'joke_en' : return_api, 'joke_pt_br' : translated }, return_code
            return {'sucess' : True, 'joke_en' : return_api }, return_code
        return {'sucess' : False , 'message' : 'Error on "https://api.chucknorris.io/" try later again' }, 202

class Joker_limited_query_txt(Resource):
    def __init__(self):
        self.info = reqparse.RequestParser()
        #define search e limit como parametro e ambos como obrigatorios, pt_br como opcional
        self.info.add_argument('search', type=str, required=True, location='args')
        self.info.add_argument('limit', type=int, required=True, location='args')
        self.info.add_argument('pt_br', type=int, default=False, location='args')
        #var fora da funcao para alteraçao caso necessario
        self.msg_not_found = f'No joke for query "_query_" found.'
    
    def joker_limited_query_txt(self, dict_info):
        url = f"https://api.chucknorris.io/jokes/search?query={dict_info['search']}"

        response = requests.request("GET", url)
        #define duas listas vazias
        list_en = []
        list_pt = []
        if response.status_code == 200:
            response_dict = response.json()
            #se o total de resultados ser 0 ja retorna a variavel definida em init e o codigo 404
            if int(response_dict['total']) == 0:
                return self.msg_not_found.replace('_query_', dict_info['search']), 404, list_pt
            #se o limite definido ser 0 ja retorna as listas vazias
            elif dict_info['limit'] == 0:
                return list_en , response.status_code, list_pt            
            elif response_dict['total'] > 0:
                #Inicia um loop com o limite de range
                for count in range(dict_info['limit']):
                    #adiciona a piada na lista definida anteriormente vazia
                    list_en.append(response_dict['result'][count]['value'])
                    if dict_info['pt_br'] == 1:
                        #adiciona a piada com a traduçao caso o cliente opte 
                        translated = GoogleTranslator(source='en', target='portuguese').translate(response_dict['result'][count]['value'])
                        list_pt.append(translated)
                    # quando count + 1 for maior ou igual ao total da um break para sair do loop e retorna o resultado
                    if (count + 1) >= response_dict['total']:
                        break
                return list_en , response.status_code, list_pt
        return False, 202, list_pt
    
    def get(self):
        info_dict = dict(self.info.parse_args())

        return_list_en, return_api_code, return_list_pt = self.joker_limited_query_txt(info_dict)
        if return_list_en is not False: 
            #envia o retorno da chamadada para o cliente
            if info_dict['pt_br'] == 1:
                #caso opte pela traducao adiciona mais um parametro no retorno
                return {'sucess' : True, 'jokes_en' : return_list_en, 'jokes_pt_br' : return_list_pt }, return_api_code
            return {'sucess' : True, 'jokes_en' : return_list_en }, return_api_code
        return {'sucess' : False, 'message' : 'Error on "https://api.chucknorris.io/" try later again' }, return_api_code