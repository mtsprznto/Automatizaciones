from ia.consultas import agente_llm


input_file = "./data_scraping/bloques_extraidos.txt"

respuesta = agente_llm(input_file)

print(respuesta)