
# Classe do agent PAA (Patient Analyzer Agent)
from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol

import connection
import pickle

class CompRequest(FipaRequestProtocol):
    """FIPA Request Behaviour of the PAA agent"""
    def __init__(self, agent):
        super(CompRequest, self).__init__(agent=agent, message=None, is_initiator=False)

    def handle_request(self, message):
        super(CompRequest, self).handle_request(message)
        display_message(self.agent.aid.localname, 'Possui novos pacientes?')
        
        situacaoPaciente = consultarGlycon(self)

        reply = message.create_reply()
        reply.set_performative(ACLMessage.INFORM)
        reply.set_content(situacaoPaciente)
        self.agent.send(reply)

class PAAgent(Agent):
    def __init__(self, aid):
        super(PAAgent, self).__init__(aid=aid, debug=False)
        self.comport_request = CompRequest(self)
        self.behaviours.append(self.comport_request)

def consultarGlycon(self):
        # consultando dados específicos do último paciente cadastrado
        document = connection.collection.find({}, {"_id": 0, "nome": 1, "glicemia.valorGlicemia": 1 }).sort("updateDate", -1).limit(1)
        
        # nome, quantidade de coletas e as glicemias
        paciente = document[0]["nome"]
        coletas = len(document[0]["glicemia"])
        glicemias = document[0]["glicemia"]
        
        # exibindo os dados coletados
        print('')
        print('Paciente encontrado:')
        print('Paciente: ', paciente)
        print('Quantidade de Coletas: ', coletas)
        print('Glicemias coletadas: ', glicemias)
        print('')

            
        ####### gerarRelatorioAvaliacao(self)
        if coletas == 1:
        #pega apenas o valor da glicemia coletada
            for x in glicemias[0].values():
                glicemia = int(x)

            # mostra a situação de acordo com a tabela
            if glicemia >= 0 and glicemia <= 49:
                situacao = 'hipoG'
            elif glicemia >=50 and glicemia <= 99:
                situacao = 'hipoL'
            elif glicemia >=100 and glicemia <= 200:
                situacao = 'gAlvo'
            elif glicemia >=201 and glicemia <= 250:
                situacao = 'hiperL'
            elif glicemia >=251 and glicemia <= 300:
                situacao = 'hiperG'
            elif glicemia >=301:
                situacao = 'hiperGG'
            else: print('glicemia inválida!')

        elif coletas > 1:
            #caso tenha mais de uma glicemia coletada
            # TODO calcular as probabilidades de hipo e hiper futuras
            print("calcular próxima glicemia, com base nos dados:")
            situacao = "a calcular..."
            
        #gerando o Relatório de Avaliação para enviar ao PTA
        #pickle.dumps converte o dict para str
        situacaoPaciente = pickle.dumps({'Paciente': paciente, 'Situacao':situacao})

        return situacaoPaciente