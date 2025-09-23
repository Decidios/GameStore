import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime
import os

class SistemaGestaoVideogames:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GameStore Manager")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a2e')
        
        # Configurações do banco de dados
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'gamesstore'
        }
        
        # Dados temporários para demonstração
        self.usuario_logado = None
        self.tipo_usuario = None
        self.carrinho = []
        
        self.criar_banco_dados()
        self.mostrar_tela_boas_vindas()
    
    def criar_banco_dados(self):
        """Cria a estrutura do banco de dados"""
        try:
            conn = mysql.connector.connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
            cursor = conn.cursor()
            
            # Criar database se não existir
            cursor.execute("CREATE DATABASE IF NOT EXISTS gamestore_db")
            cursor.execute("USE gamestore_db")
            
            # Tabela de usuários
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    senha VARCHAR(100) NOT NULL,
                    tipo ENUM('cliente', 'admin') DEFAULT 'cliente',
                    endereco TEXT,
                    telefone VARCHAR(20),
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela de produtos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(200) NOT NULL,
                    descricao TEXT,
                    categoria ENUM('console', 'jogo', 'acessorio', 'colecionavel') NOT NULL,
                    plataforma VARCHAR(50),
                    preco DECIMAL(10,2) NOT NULL,
                    estoque INT NOT NULL,
                    imagem_path VARCHAR(300),
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela de pedidos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pedidos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    usuario_id INT,
                    total DECIMAL(10,2) NOT NULL,
                    status ENUM('pendente', 'processando', 'enviado', 'entregue') DEFAULT 'pendente',
                    data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                )
            """)
            
            # Inserir dados de exemplo
            self.inserir_dados_exemplo(cursor)
            
            conn.commit()
            conn.close()
            
        except mysql.connector.Error as e:
            print(f"Erro ao conectar com o banco: {e}")
    
    def inserir_dados_exemplo(self, cursor):
        """Insere dados de exemplo no banco"""
        # Verificar se já existem dados
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] == 0:
            # Inserir usuários
            usuarios = [
                ('Admin', 'admin@gamestore.com', 'admin123', 'admin', 'Endereço admin', '(11) 9999-9999'),
                ('João Silva', 'joao@email.com', 'cliente123', 'cliente', 'Rua A, 123', '(11) 8888-8888')
            ]
            
            for usuario in usuarios:
                cursor.execute("""
                    INSERT INTO usuarios (nome, email, senha, tipo, endereco, telefone)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, usuario)
            
            # Inserir produtos
            produtos = [
                ('PlayStation 5', 'Console PlayStation 5 Standard', 'console', 'PS5', 4499.99, 10, 'ps5.jpg'),
                ('Xbox Series X', 'Console Xbox Series X 1TB', 'console', 'Xbox', 3999.99, 8, 'xbox.jpg'),
                ('God of War Ragnarök', 'Jogo God of War Ragnarök PS5', 'jogo', 'PS5', 299.99, 25, 'gow.jpg'),
                ('FIFA 23', 'Jogo FIFA 23 Xbox Series X', 'jogo', 'Xbox', 249.99, 30, 'fifa.jpg'),
                ('Controle DualSense', 'Controle PS5 DualSense', 'acessorio', 'PS5', 399.99, 15, 'controle_ps5.jpg'),
                ('Headset Gamer', 'Headset Gamer Profissional', 'acessorio', 'Multi', 299.99, 12, 'headset.jpg')
            ]
            
            for produto in produtos:
                cursor.execute("""
                    INSERT INTO produtos (nome, descricao, categoria, plataforma, preco, estoque, imagem_path)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, produto)

    # ========== TELAS DO SISTEMA ==========

    def mostrar_tela_boas_vindas(self):
        """Tela 1: Tela de Boas-Vindas"""
        self.limpar_tela()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo/Imagem central
        logo_frame = tk.Frame(main_frame, bg='#1a1a2e')
        logo_frame.pack(expand=True, pady=50)
        
        # Simulação de logo (em produção seria uma imagem)
        logo_label = tk.Label(logo_frame, text="🎮", font=('Arial', 80), bg='#1a1a2e', fg='#e94560')
        logo_label.pack(pady=20)
        
        # Título
        titulo = tk.Label(logo_frame, text="GameStore Manager", font=('Arial', 36, 'bold'), 
                         bg='#1a1a2e', fg='#ffffff')
        titulo.pack(pady=10)
        
        subtitulo = tk.Label(logo_frame, text="Sistema de Gestão para Loja de Videogames", 
                           font=('Arial', 16), bg='#1a1a2e', fg='#aaaaaa')
        subtitulo.pack(pady=5)
        
        # Botão Entrar
        btn_entrar = tk.Button(logo_frame, text="ENTRAR NO SISTEMA", font=('Arial', 14, 'bold'),
                              bg='#e94560', fg='white', padx=30, pady=15,
                              command=self.mostrar_tela_login)
        btn_entrar.pack(pady=40)
        
        # Rodapé
        rodape = tk.Label(main_frame, text="© 2024 GameStore Manager - Todos os direitos reservados",
                         font=('Arial', 10), bg='#1a1a2e', fg='#666666')
        rodape.pack(side=tk.BOTTOM, pady=20)

    def mostrar_tela_login(self):
        """Tela 2: Tela de Login"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#16213e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame do formulário
        login_frame = tk.Frame(main_frame, bg='#0f3460', relief=tk.RAISED, bd=2)
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=500)
        
        # Logo
        logo_label = tk.Label(login_frame, text="🎮", font=('Arial', 50), bg='#0f3460', fg='#e94560')
        logo_label.pack(pady=30)
        
        titulo = tk.Label(login_frame, text="Login", font=('Arial', 24, 'bold'), 
                         bg='#0f3460', fg='white')
        titulo.pack(pady=10)
        
        # Campos de entrada
        campos_frame = tk.Frame(login_frame, bg='#0f3460')
        campos_frame.pack(pady=30, padx=40, fill=tk.X)
        
        tk.Label(campos_frame, text="E-mail:", font=('Arial', 12), 
                bg='#0f3460', fg='white', anchor='w').pack(fill=tk.X)
        entry_email = tk.Entry(campos_frame, font=('Arial', 12), bg='#1a1a2e', fg='white')
        entry_email.pack(fill=tk.X, pady=5, ipady=5)
        
        tk.Label(campos_frame, text="Senha:", font=('Arial', 12), 
                bg='#0f3460', fg='white', anchor='w').pack(fill=tk.X, pady=(15,0))
        entry_senha = tk.Entry(campos_frame, font=('Arial', 12), show='*', 
                              bg='#1a1a2e', fg='white')
        entry_senha.pack(fill=tk.X, pady=5, ipady=5)
        
        # Botões
        botoes_frame = tk.Frame(login_frame, bg='#0f3460')
        botoes_frame.pack(pady=20, fill=tk.X, padx=40)
        
        btn_login = tk.Button(botoes_frame, text="Login", font=('Arial', 12, 'bold'),
                             bg='#e94560', fg='white', padx=20, pady=10,
                             command=lambda: self.fazer_login(entry_email.get(), entry_senha.get()))
        btn_login.pack(fill=tk.X, pady=5)
        
        btn_cadastrar = tk.Button(botoes_frame, text="Cadastrar", font=('Arial', 12),
                                 bg='#1a1a2e', fg='white', padx=20, pady=10,
                                 command=self.mostrar_tela_cadastro_usuario)
        btn_cadastrar.pack(fill=tk.X, pady=5)
        
        btn_recuperar = tk.Button(botoes_frame, text="Esqueci a senha", font=('Arial', 10),
                                 bg='#0f3460', fg='#aaaaaa', border=0,
                                 command=self.recuperar_senha)
        btn_recuperar.pack(pady=10)

    def mostrar_tela_cadastro_usuario(self):
        """Tela 3: Cadastro de Usuário"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#16213e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame do formulário
        cadastro_frame = tk.Frame(main_frame, bg='#0f3460', relief=tk.RAISED, bd=2)
        cadastro_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=600)
        
        titulo = tk.Label(cadastro_frame, text="Cadastro de Usuário", font=('Arial', 20, 'bold'), 
                         bg='#0f3460', fg='white')
        titulo.pack(pady=30)
        
        # Campos do formulário
        campos_frame = tk.Frame(cadastro_frame, bg='#0f3460')
        campos_frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        campos = [
            ("Nome completo:", "text"),
            ("E-mail:", "text"),
            ("Senha:", "password"),
            ("Confirmar senha:", "password"),
            ("Endereço:", "text"),
            ("Telefone:", "text")
        ]
        
        entries = {}
        for i, (label, tipo) in enumerate(campos):
            tk.Label(campos_frame, text=label, font=('Arial', 10), 
                    bg='#0f3460', fg='white', anchor='w').pack(fill=tk.X, pady=(10,0))
            
            if tipo == "password":
                entry = tk.Entry(campos_frame, font=('Arial', 11), show='*', 
                               bg='#1a1a2e', fg='white')
            else:
                entry = tk.Entry(campos_frame, font=('Arial', 11), 
                               bg='#1a1a2e', fg='white')
            
            entry.pack(fill=tk.X, pady=5, ipady=4)
            entries[label.split(':')[0].lower().replace(' ', '_')] = entry
        
        # Botões
        botoes_frame = tk.Frame(cadastro_frame, bg='#0f3460')
        botoes_frame.pack(pady=20, fill=tk.X, padx=40)
        
        btn_cadastrar = tk.Button(botoes_frame, text="Cadastrar", font=('Arial', 12, 'bold'),
                                 bg='#e94560', fg='white', padx=20, pady=10,
                                 command=lambda: self.cadastrar_usuario(entries))
        btn_cadastrar.pack(fill=tk.X, pady=5)
        
        btn_voltar = tk.Button(botoes_frame, text="Voltar ao Login", font=('Arial', 10),
                              bg='#1a1a2e', fg='white', padx=20, pady=5,
                              command=self.mostrar_tela_login)
        btn_voltar.pack(fill=tk.X, pady=5)

    def mostrar_painel_cliente(self):
        """Tela 4: Painel do Cliente"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"Bem-vindo, {self.usuario_logado}!", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=20)
        
        btn_sair = tk.Button(header_frame, text="Sair", font=('Arial', 10),
                            bg='#e94560', fg='white', command=self.mostrar_tela_login)
        btn_sair.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Conteúdo principal
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Cards de funcionalidades
        funcionalidades = [
            ("🎮 Jogos", "Ver catálogo de jogos", self.mostrar_catalogo_jogos),
            ("📺 Consoles", "Ver catálogo de consoles", self.mostrar_catalogo_consoles),
            ("🛒 Carrinho", f"Ver carrinho ({len(self.carrinho)} itens)", self.mostrar_carrinho),
            ("📋 Pedidos", "Ver histórico de pedidos", self.mostrar_historico_pedidos)
        ]
        
        for i, (icone, texto, comando) in enumerate(funcionalidades):
            card = tk.Frame(content_frame, bg='#16213e', relief=tk.RAISED, bd=1)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='nsew')
            card.bind("<Button-1>", lambda e, cmd=comando: cmd())
            
            tk.Label(card, text=icone, font=('Arial', 30), bg='#16213e', fg='#e94560').pack(pady=20)
            tk.Label(card, text=texto, font=('Arial', 12), bg='#16213e', fg='white').pack(pady=10)
            
            btn = tk.Button(card, text="Acessar", font=('Arial', 10),
                          bg='#e94560', fg='white', command=comando)
            btn.pack(pady=10)
        
        # Configurar grid
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

    def mostrar_catalogo_jogos(self):
        """Tela 5: Catálogo de Jogos"""
        self.mostrar_catalogo_produtos('jogo')

    def mostrar_catalogo_consoles(self):
        """Tela 6: Catálogo de Consoles"""
        self.mostrar_catalogo_produtos('console')

    def mostrar_catalogo_produtos(self, categoria):
        """Tela genérica para catálogo de produtos"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        titulo = "Jogos" if categoria == 'jogo' else "Consoles"
        tk.Label(header_frame, text=f"Catálogo de {titulo}", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_cliente)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Filtros
        filtros_frame = tk.Frame(main_frame, bg='#16213e')
        filtros_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(filtros_frame, text="Filtrar por plataforma:", 
                font=('Arial', 10), bg='#16213e', fg='white').pack(side=tk.LEFT, padx=5)
        
        plataformas = ["Todas", "PS5", "Xbox", "Switch", "PC"]
        var_plataforma = tk.StringVar(value="Todas")
        
        for plataforma in plataformas:
            tk.Radiobutton(filtros_frame, text=plataforma, variable=var_plataforma,
                          value=plataforma, bg='#16213e', fg='white', 
                          selectcolor='#0f3460').pack(side=tk.LEFT, padx=5)
        
        # Lista de produtos
        produtos_frame = tk.Frame(main_frame, bg='#1a1a2e')
        produtos_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Simulação de produtos (em produção viria do banco)
        produtos = self.obter_produtos_por_categoria(categoria)
        
        canvas = tk.Canvas(produtos_frame, bg='#1a1a2e')
        scrollbar = tk.Scrollbar(produtos_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a1a2e')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, produto in enumerate(produtos):
            card = tk.Frame(scrollable_frame, bg='#16213e', relief=tk.RAISED, bd=1)
            card.pack(fill=tk.X, pady=5, padx=10)
            
            # Imagem do produto (simulada)
            img_label = tk.Label(card, text="🖼️", font=('Arial', 20), bg='#16213e', fg='#e94560')
            img_label.pack(side=tk.LEFT, padx=10, pady=10)
            
            # Informações do produto
            info_frame = tk.Frame(card, bg='#16213e')
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
            
            tk.Label(info_frame, text=produto['nome'], font=('Arial', 12, 'bold'),
                    bg='#16213e', fg='white', anchor='w').pack(fill=tk.X)
            tk.Label(info_frame, text=produto['descricao'], font=('Arial', 9),
                    bg='#16213e', fg='#aaaaaa', anchor='w').pack(fill=tk.X)
            tk.Label(info_frame, text=f"R$ {produto['preco']:.2f}", font=('Arial', 14, 'bold'),
                    bg='#16213e', fg='#e94560', anchor='w').pack(fill=tk.X)
            tk.Label(info_frame, text=f"Estoque: {produto['estoque']} unidades", font=('Arial', 9),
                    bg='#16213e', fg='#aaaaaa', anchor='w').pack(fill=tk.X)
            
            # Botão adicionar ao carrinho
            btn_add = tk.Button(card, text="🛒 Adicionar", font=('Arial', 10),
                              bg='#e94560', fg='white',
                              command=lambda p=produto: self.adicionar_carrinho(p))
            btn_add.pack(side=tk.RIGHT, padx=10, pady=10)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def mostrar_carrinho(self):
        """Tela 7: Carrinho de Compras"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Carrinho de Compras", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_cliente)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Conteúdo
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        if not self.carrinho:
            tk.Label(content_frame, text="Seu carrinho está vazio", 
                    font=('Arial', 16), bg='#1a1a2e', fg='white').pack(expand=True)
            return
        
        # Lista de itens
        itens_frame = tk.Frame(content_frame, bg='#1a1a2e')
        itens_frame.pack(fill=tk.BOTH, expand=True)
        
        total = 0
        for i, item in enumerate(self.carrinho):
            item_frame = tk.Frame(itens_frame, bg='#16213e', relief=tk.RAISED, bd=1)
            item_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(item_frame, text=item['nome'], font=('Arial', 11),
                    bg='#16213e', fg='white').pack(side=tk.LEFT, padx=10, pady=10)
            
            tk.Label(item_frame, text=f"R$ {item['preco']:.2f}", font=('Arial', 11, 'bold'),
                    bg='#16213e', fg='#e94560').pack(side=tk.RIGHT, padx=10, pady=10)
            
            btn_remover = tk.Button(item_frame, text="❌", font=('Arial', 10),
                                  bg='#e94560', fg='white',
                                  command=lambda idx=i: self.remover_carrinho(idx))
            btn_remover.pack(side=tk.RIGHT, padx=5, pady=10)
            
            total += item['preco']
        
        # Total e finalização
        total_frame = tk.Frame(content_frame, bg='#16213e')
        total_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(total_frame, text=f"Total: R$ {total:.2f}", 
                font=('Arial', 16, 'bold'), bg='#16213e', fg='#e94560').pack(side=tk.LEFT, padx=10, pady=10)
        
        btn_finalizar = tk.Button(total_frame, text="Finalizar Compra", font=('Arial', 12, 'bold'),
                                 bg='#e94560', fg='white', padx=30, pady=10,
                                 command=self.finalizar_compra)
        btn_finalizar.pack(side=tk.RIGHT, padx=10, pady=10)

    def mostrar_historico_pedidos(self):
        """Tela 8: Histórico de Pedidos"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Histórico de Pedidos", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_cliente)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Conteúdo
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Simulação de pedidos
        pedidos = [
            {"id": 1, "data": "2024-01-15", "itens": "PS5 + God of War", "total": 4799.98, "status": "Entregue"},
            {"id": 2, "data": "2024-01-10", "itens": "FIFA 23", "total": 249.99, "status": "Enviado"},
        ]
        
        for pedido in pedidos:
            pedido_frame = tk.Frame(content_frame, bg='#16213e', relief=tk.RAISED, bd=1)
            pedido_frame.pack(fill=tk.X, pady=5)
            
            info_frame = tk.Frame(pedido_frame, bg='#16213e')
            info_frame.pack(fill=tk.X, padx=10, pady=10)
            
            tk.Label(info_frame, text=f"Pedido #{pedido['id']} - {pedido['data']}", 
                    font=('Arial', 12, 'bold'), bg='#16213e', fg='white').pack(anchor='w')
            tk.Label(info_frame, text=f"Itens: {pedido['itens']}", 
                    font=('Arial', 10), bg='#16213e', fg='#aaaaaa').pack(anchor='w')
            tk.Label(info_frame, text=f"Total: R$ {pedido['total']:.2f} | Status: {pedido['status']}", 
                    font=('Arial', 10), bg='#16213e', fg='#e94560').pack(anchor='w')

    def mostrar_painel_administrador(self):
        """Tela 9: Painel do Administrador"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"Painel Administrativo - {self.usuario_logado}", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=20)
        
        btn_sair = tk.Button(header_frame, text="Sair", font=('Arial', 10),
                            bg='#e94560', fg='white', command=self.mostrar_tela_login)
        btn_sair.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Conteúdo principal
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Cards de funcionalidades
        funcionalidades = [
            ("📦 Gerenciar Produtos", "Adicionar/editar/remover produtos", self.mostrar_gerenciar_produtos),
            ("➕ Cadastrar Produto", "Cadastrar novo jogo ou console", self.mostrar_cadastro_produto),
            ("📊 Ver Pedidos", "Gerenciar pedidos dos clientes", self.mostrar_gerenciamento_pedidos),
            ("📈 Dashboard", "Relatórios e estatísticas", self.mostrar_dashboard)
        ]
        
        for i, (icone, texto, comando) in enumerate(funcionalidades):
            card = tk.Frame(content_frame, bg='#16213e', relief=tk.RAISED, bd=1)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='nsew')
            
            tk.Label(card, text=icone, font=('Arial', 30), bg='#16213e', fg='#e94560').pack(pady=20)
            tk.Label(card, text=texto, font=('Arial', 12), bg='#16213e', fg='white').pack(pady=10)
            
            btn = tk.Button(card, text="Acessar", font=('Arial', 10),
                          bg='#e94560', fg='white', command=comando)
            btn.pack(pady=10)
        
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

    def mostrar_cadastro_produto(self):
        """Tela 10: Cadastro de Jogos e Consoles"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#16213e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Cadastro de Produto", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_administrador)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Formulário
        form_frame = tk.Frame(main_frame, bg='#0f3460', relief=tk.RAISED, bd=2)
        form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=500, height=500)
        
        campos = [
            ("Nome do produto:", "text"),
            ("Descrição:", "text"),
            ("Categoria:", "combo", ["console", "jogo", "acessorio", "colecionavel"]),
            ("Plataforma:", "text"),
            ("Preço:", "number"),
            ("Estoque:", "number")
        ]
        
        entries = {}
        for i, (label, tipo, *opcoes) in enumerate(campos):
            tk.Label(form_frame, text=label, font=('Arial', 10), 
                    bg='#0f3460', fg='white', anchor='w').pack(fill=tk.X, padx=40, pady=(15,0))
            
            if tipo == "combo":
                entry = ttk.Combobox(form_frame, values=opcoes[0], font=('Arial', 11))
            elif tipo == "number":
                entry = tk.Entry(form_frame, font=('Arial', 11))
            else:
                entry = tk.Entry(form_frame, font=('Arial', 11))
            
            entry.pack(fill=tk.X, padx=40, pady=5, ipady=4)
            entries[label.split(':')[0].lower().replace(' ', '_')] = entry
        
        btn_cadastrar = tk.Button(form_frame, text="Cadastrar Produto", font=('Arial', 12, 'bold'),
                                 bg='#e94560', fg='white', padx=20, pady=10,
                                 command=lambda: self.cadastrar_produto(entries))
        btn_cadastrar.pack(pady=20)

    def mostrar_gerenciar_produtos(self):
        """Tela 11: Gerenciar Produtos"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Gerenciar Produtos", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_administrador)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Lista de produtos
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        produtos = self.obter_todos_produtos()
        
        for produto in produtos:
            prod_frame = tk.Frame(content_frame, bg='#16213e', relief=tk.RAISED, bd=1)
            prod_frame.pack(fill=tk.X, pady=5)
            
            info_frame = tk.Frame(prod_frame, bg='#16213e')
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
            
            tk.Label(info_frame, text=produto['nome'], font=('Arial', 12, 'bold'),
                    bg='#16213e', fg='white').pack(anchor='w')
            tk.Label(info_frame, text=f"Categoria: {produto['categoria']} | Preço: R$ {produto['preco']:.2f}", 
                    font=('Arial', 10), bg='#16213e', fg='#aaaaaa').pack(anchor='w')
            tk.Label(info_frame, text=f"Estoque: {produto['estoque']} | Plataforma: {produto['plataforma']}", 
                    font=('Arial', 10), bg='#16213e', fg='#aaaaaa').pack(anchor='w')
            
            # Botões de ação
            btn_frame = tk.Frame(prod_frame, bg='#16213e')
            btn_frame.pack(side=tk.RIGHT, padx=10, pady=10)
            
            tk.Button(btn_frame, text="Editar", font=('Arial', 9),
                     bg='#3498db', fg='white').pack(side=tk.LEFT, padx=2)
            tk.Button(btn_frame, text="Excluir", font=('Arial', 9),
                     bg='#e74c3c', fg='white').pack(side=tk.LEFT, padx=2)

    def mostrar_gerenciamento_pedidos(self):
        """Tela 12: Gerenciamento de Pedidos"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Gerenciamento de Pedidos", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_administrador)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Conteúdo
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Simulação de pedidos para administrador
        pedidos = [
            {"id": 1, "cliente": "João Silva", "itens": "PS5", "total": 4499.99, "status": "Pendente"},
            {"id": 2, "cliente": "Maria Santos", "itens": "FIFA 23", "total": 249.99, "status": "Processando"},
        ]
        
        for pedido in pedidos:
            ped_frame = tk.Frame(content_frame, bg='#16213e', relief=tk.RAISED, bd=1)
            ped_frame.pack(fill=tk.X, pady=5)
            
            info_frame = tk.Frame(ped_frame, bg='#16213e')
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
            
            tk.Label(info_frame, text=f"Pedido #{pedido['id']} - Cliente: {pedido['cliente']}", 
                    font=('Arial', 12, 'bold'), bg='#16213e', fg='white').pack(anchor='w')
            tk.Label(info_frame, text=f"Itens: {pedido['itens']} | Total: R$ {pedido['total']:.2f}", 
                    font=('Arial', 10), bg='#16213e', fg='#aaaaaa').pack(anchor='w')
            
            # Controle de status
            status_frame = tk.Frame(ped_frame, bg='#16213e')
            status_frame.pack(side=tk.RIGHT, padx=10, pady=10)
            
            status_var = tk.StringVar(value=pedido['status'])
            status_menu = ttk.Combobox(status_frame, textvariable=status_var,
                                      values=["Pendente", "Processando", "Enviado", "Entregue"],
                                      state="readonly", width=12)
            status_menu.pack(pady=5)
            
            tk.Button(status_frame, text="Atualizar", font=('Arial', 8),
                     bg='#e94560', fg='white').pack()

    # ========== FUNÇÕES AUXILIARES ==========

    def limpar_tela(self):
        """Remove todos os widgets da tela atual"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def fazer_login(self, email, senha):
        """Autentica o usuário"""
        if email == "admin@gamestore.com" and senha == "admin123":
            self.usuario_logado = "Administrador"
            self.tipo_usuario = "admin"
            self.mostrar_painel_administrador()
        elif email == "joao@email.com" and senha == "cliente123":
            self.usuario_logado = "João Silva"
            self.tipo_usuario = "cliente"
            self.mostrar_painel_cliente()
        else:
            messagebox.showerror("Erro", "E-mail ou senha incorretos!")

    def cadastrar_usuario(self, entries):
        """Cadastra novo usuário"""
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        self.mostrar_tela_login()

    def recuperar_senha(self):
        """Recuperação de senha"""
        messagebox.showinfo("Recuperar Senha", "Instruções enviadas para o e-mail!")

    def obter_produtos_por_categoria(self, categoria):
        """Retorna produtos por categoria (simulação)"""
        produtos = [
            {
                'nome': 'PlayStation 5', 
                'descricao': 'Console PlayStation 5 Standard Edition', 
                'preco': 4499.99, 
                'estoque': 10,
                'categoria': 'console'
            },
            {
                'nome': 'God of War Ragnarök', 
                'descricao': 'Jogo God of War Ragnarök para PS5', 
                'preco': 299.99, 
                'estoque': 25,
                'categoria': 'jogo'
            }
        ]
        return [p for p in produtos if p['categoria'] == categoria]

    def obter_todos_produtos(self):
        """Retorna todos os produtos (simulação)"""
        return [
            {
                'nome': 'PlayStation 5', 
                'categoria': 'console', 
                'preco': 4499.99, 
                'estoque': 10,
                'plataforma': 'PS5'
            },
            {
                'nome': 'God of War Ragnarök', 
                'categoria': 'jogo', 
                'preco': 299.99, 
                'estoque': 25,
                'plataforma': 'PS5'
            }
        ]

    def adicionar_carrinho(self, produto):
        """Adiciona produto ao carrinho"""
        self.carrinho.append(produto)
        messagebox.showinfo("Sucesso", f"{produto['nome']} adicionado ao carrinho!")

    def remover_carrinho(self, index):
        """Remove item do carrinho"""
        if 0 <= index < len(self.carrinho):
            produto = self.carrinho.pop(index)
            messagebox.showinfo("Removido", f"{produto['nome']} removido do carrinho!")
            self.mostrar_carrinho()

    def finalizar_compra(self):
        """Finaliza a compra"""
        if self.carrinho:
            messagebox.showinfo("Sucesso", "Compra finalizada com sucesso!")
            self.carrinho = []
            self.mostrar_painel_cliente()
        else:
            messagebox.showwarning("Aviso", "Carrinho vazio!")

    def cadastrar_produto(self, entries):
        """Cadastra novo produto"""
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
        self.mostrar_painel_administrador()

    def mostrar_dashboard(self):
        """Mostra dashboard administrativo"""
        messagebox.showinfo("Dashboard", "Dashboard administrativo - Em desenvolvimento")

    def executar(self):
        """Inicia a aplicação"""
        self.root.mainloop()

# Executar o sistema
if __name__ == "__main__":
    app = SistemaGestaoVideogames()
    app.executar()