#https://www.youtube.com/watch?v=BHAUJUuhiDw

from bottle import route, run, get, template, post

materias = {
    "Finan\u00e7as": {
        "materia": "Finan\u00e7as",
        "perguntas": {
            "Pergunta1": [
                "padr\u00e3o",
                "Infla\u00e7\u00e3o \u00e9 bom?",
                [
                    "nao",
                    "sim"
                ],
                "Sim"
            ],
            "Pergunta2": [
                "alternativa",
                "O que \u00e9 m\u00e9dia-padr\u00e3o?",
                [
                    {
                        "A": "Desvio da mediana.",
                        "B": "\u00c9 a medida natural de uma certa quantidade de fatos.",
                        "C": "\u00c9 o padr\u00e3o da m\u00e9dia com quem voc\u00ea anda"
                    }
                ],
                "A"
            ],
            "Pergunta3": [
                "dissertativa",
                "O que \u00e9 uma a\u00e7\u00e3o?",
                [],
                "A\u00e7\u00e3o \u00e9 um papel que uma empresa disponibiliza na bolsa para compra e venda por investidores, possibilitando a valoriza\u00e7\u00e3o e acumulo de capital da empresa."
            ]
        }
    },
    "Biomedicina": {
        "materia": "Biomedicina",
        "perguntas": {
            "Pergunta1": [
                "padr\u00e3o",
                "\u00c1tomo \u00e9 indivis\u00edvel?",
                [
                    "nao",
                    "sim"
                ],
                "N\u00e3o"
            ],
            "Pergunta2": [
                "alternativa",
                "O que \u00e9 \u00e1tomo?",
                [
                    {
                        "A": "Part\u00edcula",
                        "B": "Um elemento com outros elementos",
                        "C": "Pequeno e indivis\u00edvel"
                    }
                ],
                "B"
            ]
        }
    }
}

@get('/materias')
def obter_todas_materias():
	return {'materias':materias}

@get('/materias/<nome>')
def obter_uma_materia(nome):
	#materia = [materia for materia in materias if materias[nome] == nome]
	materia = materias[nome]
	return {'materia':materia}

@get('/materias/nomes')
def obter_nomes():
	nomes = [materia for materia in materias]
	return {'nomes':nomes}

@post('/materias')
def adicionar_uma_materia():
	#nova_materia = {'nome': {'materia':request.json.get('materia'), 'perguntas':request.json.get('perguntas')}}
	#materias[nova_materia] = nova_materia_specs
	return {'materias':materias}

run(host='localhost', port=8080, reloader=True, debug=True)
