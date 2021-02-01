
# Classe do agent PAA (Patient Analyzer Agent)

from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from agents.behaviours import CompRequest2
from agents.behaviours import ComportTemporal

import agents.connection
import pickle

class PatientAnalyzerAgent(Agent): 
    def __init__(self, aid, pta_agent_name, dataHora, paciente, glicemia, situacaoPaciente):
        super(PatientAnalyzerAgent, self).__init__(aid=aid)

        self.dataHora = dataHora
        self.paciente = paciente
        self.glicemia = glicemia
        self.situacaoPaciente = situacaoPaciente

        # mensagem que requisita algo ao agente PTA
        message = ACLMessage(ACLMessage.REQUEST) #cria a mensagem por meio da classe ACLMessage
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL) #seta o protocolo da msg
        message.add_receiver(AID(name=pta_agent_name)) #adiciona pra quem a mensagem vai

        situacaoPaciente = gerarRelatorioAvaliacao()
        message.set_content(situacaoPaciente) #seta o conteúdo

        # executa o que está implementado no CompRequest2 a cada 10 segundos
        self.comport_request = CompRequest2(self, message) #instancia o comportamento de request
        self.comport_temp = ComportTemporal(self, 10.0, message) #instanciando a classe ComportTemporal

        #adiciona os comportamentos a variável behaviours
        self.behaviours.append(self.comport_request)
        self.behaviours.append(self.comport_temp)




    def consultarGlycon(self):
        print('Novo paciente encontrado. Coletando os dados...')
        print('')
        #consultando dados específicos do último paciente cadastrado
        document = connection.collection.find({}, {"_id": 0, "nome": 1, "glicemia.valorGlicemia": 1 }).sort("updateDate", -1).limit(1)
        
        # nome, quantidade de coletas e as glicemias
        paciente = document[0]["nome"]
        coletas = len(document[0]["glicemia"])
        glicemias = document[0]["glicemia"]
        
        # exibindo os dados coletados
        print('Paciente: ', paciente)
        print('Quantidade de Coletas: ', coletas)
        print('Glicemias coletadas: ', glicemias)
        print('')



    def gerarRelatorioAvaliacao(self, document, paciente, coletas, glicemias):

        if coletas == 1:
        #pega apenas o valor da glicemia coletada
            for x in glicemias[0].values():
                glicemia = int(x)

            # mostra a situação de acordo com a tabela
            if glicemia >= 0 and glicemia <= 49:
                situacao = 'hypoS'
            elif glicemia >=50 and glicemia <= 99:
                situacao = 'hypoM'
            elif glicemia >=100 and glicemia <= 200:
                situacao = 'normalBG'
            elif glicemia >=201 and glicemia <= 250:
                situacao = 'hyperM'
            elif glicemia >=251 and glicemia <= 300:
                situacao = 'hyperS'
            elif glicemia >=301:
                situacao = 'hyperVS'
            else: print('glicemia inválida!')

        elif coletas > 1:
            #caso tenha mais de uma glicemia coletada
            for x in document:
                #TODO calcular as probabilidades de hipo e hiper futuras
                print("calcular próxima glicemia, com base nos dados:")
                print(x)

        #gerando o Relatório de Avaliação para enviar ao PTA
        self.situacaoPaciente = {'Paciente': paciente, 'Situacao':situacao}
        print(self.situacaoPaciente)

        return self.situacaoPaciente
        
