from tkinter import *
import json
import requests


class APP_CNAE_Info:

    def __init__(self):

        self.dicionario_de_conjuntos_temporario = None
        self.dicionario_de_ids = None
        self.dicionario_de_descricoes = None
        self.dicionario_de_observacoes = None

        self.conteudo_da_lista_principal = None

        self.endereco_subclasses = "https://servicodados.ibge.gov.br/api/v2/cnae/subclasses"
        self.endereco_classes = "https://servicodados.ibge.gov.br/api/v2/cnae/classes"
        self.endereco_grupos = "https://servicodados.ibge.gov.br/api/v2/cnae/grupos/"
        self.endereco_divisoes = "https://servicodados.ibge.gov.br/api/v2/cnae/divisoes/"
        self.endereco_sessoes = "https://servicodados.ibge.gov.br/api/v2/cnae/secoes"

        self.window = Tk()
        self.window.config(bg="grey90")
        self.window.title("CNAE (Classificação Nacional de Atividades Econômicas)")
        self.window.geometry("+500+200")

        self.menu = Menu(self.window)
        self.window.config(menu=self.menu)

        self.menu_iniciar = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Menu de listas de Atividades Economicas por >>", menu=self.menu_iniciar)

        self.menu_iniciar.add_command(label="Subclasses",
                                      command=self.criar_lista_por_subclasse_de_atividade)

        self.menu_iniciar.add_command(label="Classes",
                                      command=self.criar_lista_por_classe_de_atividade)

        self.menu_iniciar.add_command(label="Grupos",
                                      command=self.criar_lista_por_grupo_de_atividade)

        self.menu_iniciar.add_command(label="Divisoes",
                                      command=self.criar_lista_por_divisao_de_atividade)

        self.menu_iniciar.add_command(label="Secoes",
                                      command=self.criar_lista_por_secao_de_atividade)

        self.frame = Frame(self.window, bd=8, bg="grey90")
        self.frame.pack()

        self.botao = Button(self.window, text="Mostrar Informacoes", font="Arial 7",
                            command=self.executar_informacoes_sobre_item_selecionado)
        self.botao.pack()

        self.texto = Text(self.window, bd=8)
        self.texto.pack(fill="x")

        self.sub_frame_esquerdo = Frame(self.frame, bd=3)
        self.sub_frame_esquerdo.pack(side="left")

        self.sub_frame_direito = Frame(self.frame, bd=3)
        self.sub_frame_direito.pack(side="right")

        self.listbox_de_informacoes = Listbox(self.sub_frame_direito, width=40, bd=0, bg="grey90",
                                              font="Consolas 8 ")
        self.listbox_de_informacoes.pack(fill="y")

        self.label_listbox_principal = Label(self.sub_frame_esquerdo, bd=1,
                                             text=f"Lista de Atividades Economicas:(...)")
        self.label_listbox_principal.pack()

        self.listbox_principal = Listbox(self.sub_frame_esquerdo, width=90, bd=2)
        self.listbox_principal.pack()

        self.window.mainloop()

    def executar_informacoes_sobre_item_selecionado(self):
        self._mostrar_observacoes()
        self._mostrar_detalhes()

    def _mostrar_detalhes(self):
        try:
            self.listbox_de_informacoes.delete(0, END)
            self.listbox_de_informacoes.insert(END, f"* Outros Detalhes:")

            string_de_id = self.dicionario_de_ids[self.listbox_principal.get(ANCHOR)]
            string_de_descricao = self.dicionario_de_descricoes[self.listbox_principal.get(ANCHOR)]
            string_de_conjunto = self.dicionario_de_conjuntos_temporario[self.listbox_principal.get(ANCHOR)]

            self.listbox_de_informacoes.insert(END, f'id: {string_de_id}')
            self.listbox_de_informacoes.insert(END, f'descricao: {string_de_descricao}')
            self.listbox_de_informacoes.insert(END, f'{string_de_conjunto}')
        except:
            self.listbox_de_informacoes.insert(END, "#$%  ErR0r  %#$")
            self.texto.insert(END, "Selecione um item na lista acima")

    def _mostrar_observacoes(self):
        try:
            self.texto.delete(1.0, END)
            self.texto.insert(END, f"* Observacoes Sobre: \n(({self.listbox_principal.get(ANCHOR)}))\n\n\n")

            lista_de_observacoes = self.dicionario_de_observacoes[self.listbox_principal.get(ANCHOR)]

            cont = 1
            for i in lista_de_observacoes:
                self.texto.insert(END, f"OBSERVACAO {cont}:   {i}")
                self.texto.insert(END, f"\n{'-' * 80} \n\n\n\n")
                cont += 1
        except:
            self.listbox_principal.insert(END, f"Adicione uma lista clicando em Menu de Atividades Economicas")

    def criar_lista_por_subclasse_de_atividade(self):
        self.label_listbox_principal.config(text=f"Lista de Atividades Economicas:(subclasses)")
        self._criar_e_organizar_conteudo_da_lista_principal(self.endereco_subclasses)

    def criar_lista_por_classe_de_atividade(self):
        self.label_listbox_principal.config(text=f"Lista de Atividades Economicas:(classes)")
        self._criar_e_organizar_conteudo_da_lista_principal(self.endereco_classes)

    def criar_lista_por_grupo_de_atividade(self):
        self.label_listbox_principal.config(text=f"Lista de Atividades Economicas:(grupos)")
        self._criar_e_organizar_conteudo_da_lista_principal(self.endereco_grupos)

    def criar_lista_por_divisao_de_atividade(self):
        self.label_listbox_principal.config(text=f"Lista de Atividades Economicas:(divisoes)")
        self._criar_e_organizar_conteudo_da_lista_principal(self.endereco_divisoes)

    def criar_lista_por_secao_de_atividade(self):
        self.label_listbox_principal.config(text=f"Lista de Atividades Economicas:(sessoes)")
        self._criar_e_organizar_conteudo_da_lista_principal(self.endereco_sessoes)

    def _criar_e_organizar_conteudo_da_lista_principal(self, endereco):
        try:
            self.listbox_principal.delete(0, END)

            self.dicionario_de_ids = None
            self.dicionario_de_descricoes = None
            self.dicionario_de_conjuntos_temporario = None
            self.dicionario_de_observacoes = None

            self.conteudo_da_lista_principal = None

            self.dicionario_de_ids = dict()
            self.dicionario_de_descricoes = dict()
            self.dicionario_de_conjuntos_temporario = dict()
            self.dicionario_de_observacoes = dict()

            self.conteudo_da_lista_principal = set()

            request = requests.get(endereco)
            dicionario = json.loads(request.text)

            for i in dicionario:
                string_de_id_temporaria = i["id"]
                self.dicionario_de_ids[f'{i["descricao"]}'] = string_de_id_temporaria

                string_de_descricao_temporaria = i["descricao"]
                self.dicionario_de_descricoes[f'{i["descricao"]}'] = string_de_descricao_temporaria

                conjunto_temporario = set(i)
                if 'classe' in conjunto_temporario:
                    string_temporaria = f'classe: {i["classe"]["descricao"]}'
                    self.dicionario_de_conjuntos_temporario[f'{i["descricao"]}'] = string_temporaria
                elif 'grupo' in conjunto_temporario:
                    string_temporaria = f'grupo: {i["grupo"]["descricao"]}'
                    self.dicionario_de_conjuntos_temporario[f'{i["descricao"]}'] = string_temporaria
                elif 'divisao' in conjunto_temporario:
                    string_temporaria = f'divisao: {i["divisao"]["descricao"]}'
                    self.dicionario_de_conjuntos_temporario[f'{i["descricao"]}'] = string_temporaria
                elif 'secao' in conjunto_temporario:
                    string_temporaria = f'secao: {i["secao"]["descricao"]}'
                    self.dicionario_de_conjuntos_temporario[f'{i["descricao"]}'] = string_temporaria
                else:
                    self.dicionario_de_conjuntos_temporario[f'{i["descricao"]}'] = ""

                lista_de_observacoes_temporaria = i["observacoes"]
                self.dicionario_de_observacoes[f'{i["descricao"]}'] = lista_de_observacoes_temporaria

                self.conteudo_da_lista_principal.add(f'{i["descricao"]}')

            for i in self.conteudo_da_lista_principal:
                self.listbox_principal.insert(END, f'{i}')

        except:
            self.texto.insert(END, "Selecione um item na lista acima")

APP_CNAE_Info()
