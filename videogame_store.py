import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import hashlib

class SistemaGestaoVideogames:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GameStore Manager - Sistema Completo")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        self.center_window()
        
        # Dados da sessão
        self.usuario_logado = None
        self.tipo_usuario = None
        self.usuario_id = None
        self.carrinho = []
        
        # Dados em memória
        self.produtos = []
        self.usuarios = []
        self.pedidos = []
        
        # Variáveis para filtros
        self.var_plataforma = None
        self.categoria_atual = None
        
        self.inicializar_dados()
        self.mostrar_tela_boas_vindas()
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def inicializar_dados(self):
        """Inicializa dados de exemplo"""
        # Usuários de exemplo
        self.usuarios = [
            {'id': 1, 'nome': 'Admin Sistema', 'email': 'admin@gamestore.com', 
             'senha': self.hash_password('admin123'), 'tipo': 'admin', 
             'endereco': 'Av. Principal, 123', 'telefone': '(11) 9999-9999', 'data_cadastro': '2024-01-01'},
            {'id': 2, 'nome': 'João Silva', 'email': 'joao@email.com', 
             'senha': self.hash_password('cliente123'), 'tipo': 'cliente',
             'endereco': 'Rua A, 456', 'telefone': '(11) 8888-8888', 'data_cadastro': '2024-01-15'},
            {'id': 3, 'nome': 'Maria Santos', 'email': 'maria@email.com', 
             'senha': self.hash_password('cliente123'), 'tipo': 'cliente',
             'endereco': 'Rua B, 789', 'telefone': '(11) 7777-7777', 'data_cadastro': '2024-01-20'}
        ]
        
        # Produtos de exemplo
        self.produtos = [
            {'id': 1, 'nome': 'PlayStation 5', 'descricao': 'Console PlayStation 5 Standard Edition', 
             'categoria': 'console', 'plataforma': 'PS5', 'preco': 4499.99, 'estoque': 10, 'imagem': '🎮'},
            {'id': 2, 'nome': 'Xbox Series X', 'descricao': 'Console Xbox Series X 1TB', 
             'categoria': 'console', 'plataforma': 'Xbox', 'preco': 3999.99, 'estoque': 8, 'imagem': '🎮'},
            {'id': 3, 'nome': 'Nintendo Switch', 'descricao': 'Console Nintendo Switch OLED', 
             'categoria': 'console', 'plataforma': 'Switch', 'preco': 1999.99, 'estoque': 15, 'imagem': '🎮'},
            {'id': 4, 'nome': 'God of War Ragnarök', 'descricao': 'Jogo God of War Ragnarök para PS5', 
             'categoria': 'jogo', 'plataforma': 'PS5', 'preco': 299.99, 'estoque': 25, 'imagem': '🎯'},
            {'id': 5, 'nome': 'FIFA 23', 'descricao': 'Jogo FIFA 23 Xbox Series X', 
             'categoria': 'jogo', 'plataforma': 'Xbox', 'preco': 249.99, 'estoque': 30, 'imagem': '⚽'},
            {'id': 6, 'nome': 'The Legend of Zelda', 'descricao': 'Jogo Zelda Tears of the Kingdom', 
             'categoria': 'jogo', 'plataforma': 'Switch', 'preco': 299.99, 'estoque': 20, 'imagem': '🛡️'},
            {'id': 7, 'nome': 'Controle DualSense PS5', 'descricao': 'Controle Wireless PS5 DualSense', 
             'categoria': 'acessorio', 'plataforma': 'PS5', 'preco': 399.99, 'estoque': 15, 'imagem': '🎮'},
            {'id': 8, 'nome': 'Headset Gamer Profissional', 'descricao': 'Headset 7.1 Surround Sound', 
             'categoria': 'acessorio', 'plataforma': 'Multi', 'preco': 299.99, 'estoque': 12, 'imagem': '🎧'},
            {'id': 9, 'nome': 'Cadeira Gamer RGB', 'descricao': 'Cadeira Gamer Ergonômica com LED', 
             'categoria': 'acessorio', 'plataforma': 'Multi', 'preco': 899.99, 'estoque': 5, 'imagem': '💺'}
        ]
        
        # Pedidos de exemplo
        self.pedidos = [
            {'id': 1, 'usuario_id': 2, 'itens': [{'produto_id': 1, 'quantidade': 1, 'preco': 4499.99}], 
             'total': 4499.99, 'status': 'entregue', 'data': '2024-01-16'},
            {'id': 2, 'usuario_id': 3, 'itens': [{'produto_id': 4, 'quantidade': 1, 'preco': 299.99}], 
             'total': 299.99, 'status': 'enviado', 'data': '2024-01-21'}
        ]
    
    def hash_password(self, password):
        """Cria hash da senha para segurança"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verificar_senha(self, password, hashed):
        """Verifica se a senha corresponde ao hash"""
        return self.hash_password(password) == hashed

    # ========== TELAS PRINCIPAIS ==========

    def mostrar_tela_boas_vindas(self):
        """Tela 1: Tela de Boas-Vindas"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        logo_frame = tk.Frame(main_frame, bg='#1a1a2e')
        logo_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        logo_label = tk.Label(logo_frame, text="🎮", font=('Arial', 80), bg='#1a1a2e', fg='#e94560')
        logo_label.pack(pady=20)
        
        titulo = tk.Label(logo_frame, text="GameStore Manager", font=('Arial', 36, 'bold'), 
                         bg='#1a1a2e', fg='#ffffff')
        titulo.pack(pady=10)
        
        subtitulo = tk.Label(logo_frame, text="Sistema de Gestão para Loja de Videogames", 
                           font=('Arial', 16), bg='#1a1a2e', fg='#aaaaaa')
        subtitulo.pack(pady=5)
        
        btn_entrar = tk.Button(logo_frame, text="ENTRAR NO SISTEMA", font=('Arial', 14, 'bold'),
                              bg='#e94560', fg='white', padx=30, pady=15,
                              command=self.mostrar_tela_login)
        btn_entrar.pack(pady=40)
        
        rodape = tk.Label(main_frame, text="© 2024 GameStore Manager - Todos os direitos reservados",
                         font=('Arial', 10), bg='#1a1a2e', fg='#666666')
        rodape.pack(side=tk.BOTTOM, pady=20)

    def mostrar_tela_login(self):
        """Tela 2: Tela de Login"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#16213e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame principal centralizado
        login_container = tk.Frame(main_frame, bg='#16213e')
        login_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Notebook para abas
        notebook = ttk.Notebook(login_container)
        notebook.pack(padx=20, pady=20)
        
        # Aba de Login
        login_frame = ttk.Frame(notebook, width=400, height=400)
        notebook.add(login_frame, text="Login")
        
        # Conteúdo do Login
        login_content = tk.Frame(login_frame, bg='#0f3460')
        login_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(login_content, text="🎮", font=('Arial', 50), bg='#0f3460', fg='#e94560').pack(pady=20)
        tk.Label(login_content, text="Login", font=('Arial', 24, 'bold'), bg='#0f3460', fg='white').pack(pady=10)
        
        # Campos login
        campos_frame = tk.Frame(login_content, bg='#0f3460')
        campos_frame.pack(pady=30, fill=tk.X)
        
        tk.Label(campos_frame, text="E-mail:", font=('Arial', 12), bg='#0f3460', fg='white').pack(anchor='w')
        self.login_email = tk.Entry(campos_frame, font=('Arial', 12), bg='#1a1a2e', fg='white', width=30)
        self.login_email.pack(fill=tk.X, pady=5, ipady=5)
        self.login_email.insert(0, "admin@gamestore.com")
        
        tk.Label(campos_frame, text="Senha:", font=('Arial', 12), bg='#0f3460', fg='white').pack(anchor='w', pady=(10,0))
        self.login_senha = tk.Entry(campos_frame, font=('Arial', 12), show='*', bg='#1a1a2e', fg='white', width=30)
        self.login_senha.pack(fill=tk.X, pady=5, ipady=5)
        self.login_senha.insert(0, "admin123")
        
        # Botões login
        botoes_frame = tk.Frame(login_content, bg='#0f3460')
        botoes_frame.pack(pady=20)
        
        btn_login = tk.Button(botoes_frame, text="Entrar", font=('Arial', 12, 'bold'),
                             bg='#e94560', fg='white', padx=30, pady=10,
                             command=self.fazer_login)
        btn_login.pack(fill=tk.X, pady=5)
        
        btn_recuperar = tk.Button(botoes_frame, text="Esqueci a senha", font=('Arial', 10),
                                 bg='#0f3460', fg='#aaaaaa', border=0,
                                 command=self.recuperar_senha)
        btn_recuperar.pack(pady=10)
        
        # Aba de Cadastro
        cadastro_frame = ttk.Frame(notebook, width=400, height=500)
        notebook.add(cadastro_frame, text="Cadastrar")
        
        # Conteúdo do Cadastro
        cadastro_content = tk.Frame(cadastro_frame, bg='#0f3460')
        cadastro_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Canvas com scrollbar para cadastro
        canvas = tk.Canvas(cadastro_content, bg='#0f3460', highlightthickness=0, height=400)
        scrollbar = ttk.Scrollbar(cadastro_content, orient=tk.VERTICAL, command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg='#0f3460')
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        tk.Label(scroll_frame, text="👤", font=('Arial', 40), bg='#0f3460', fg='#e94560').pack(pady=10)
        tk.Label(scroll_frame, text="Criar Nova Conta", font=('Arial', 20, 'bold'), 
                bg='#0f3460', fg='white').pack(pady=10)
        
        campos = [
            ("Nome completo:", "text"),
            ("E-mail:", "text"),
            ("Senha:", "password"),
            ("Confirmar senha:", "password"),
            ("Endereço:", "text"),
            ("Telefone:", "text")
        ]
        
        self.cadastro_entries = {}
        for i, (label, tipo) in enumerate(campos):
            linha = tk.Frame(scroll_frame, bg='#0f3460')
            linha.pack(fill=tk.X, pady=10, padx=10)
            
            tk.Label(linha, text=label, font=('Arial', 11), 
                    bg='#0f3460', fg='white', width=15, anchor='w').pack(side=tk.LEFT)
            
            if tipo == "password":
                entry = tk.Entry(linha, font=('Arial', 11), show='*', 
                               bg='#1a1a2e', fg='white', width=25)
            else:
                entry = tk.Entry(linha, font=('Arial', 11), 
                               bg='#1a1a2e', fg='white', width=25)
            
            entry.pack(side=tk.LEFT, padx=5, ipady=3)
            self.cadastro_entries[label.split(':')[0].lower().replace(' ', '_')] = entry
        
        btn_cadastrar = tk.Button(scroll_frame, text="Cadastrar", font=('Arial', 12, 'bold'),
                                 bg='#e94560', fg='white', padx=20, pady=10,
                                 command=self.cadastrar_usuario)
        btn_cadastrar.pack(pady=20)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar tamanho das abas
        login_frame.pack_propagate(False)
        cadastro_frame.pack_propagate(False)
        
        # Bind Enter para fazer login
        self.root.bind('<Return>', lambda event: self.fazer_login())

    def mostrar_painel_cliente(self):
        """Tela 4: Painel do Cliente"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"🎮 Bem-vindo, {self.usuario_logado}!", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=20)
        
        btn_sair = tk.Button(header_frame, text="🚪 Sair", font=('Arial', 10),
                            bg='#e94560', fg='white', command=self.logout)
        btn_sair.pack(side=tk.RIGHT, padx=20, pady=20)
        
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        funcionalidades = [
            ("🎮 Jogos", "Ver catálogo de jogos", self.mostrar_catalogo_jogos),
            ("📺 Consoles", "Ver catálogo de consoles", self.mostrar_catalogo_consoles),
            ("🎧 Acessórios", "Ver acessórios disponíveis", self.mostrar_catalogo_acessorios),
            ("🛒 Carrinho", f"Ver carrinho ({len(self.carrinho)} itens)", self.mostrar_carrinho),
            ("📋 Meus Pedidos", "Ver histórico de pedidos", self.mostrar_historico_pedidos),
            ("👤 Meus Dados", "Meus dados cadastrais", self.mostrar_meus_dados)
        ]
        
        for i, (icone, texto, comando) in enumerate(funcionalidades):
            card = tk.Frame(content_frame, bg='#16213e', relief=tk.RAISED, bd=1)
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky='nsew')
            
            tk.Label(card, text=icone, font=('Arial', 30), bg='#16213e', fg='#e94560').pack(pady=20)
            tk.Label(card, text=texto, font=('Arial', 12), bg='#16213e', fg='white', wraplength=150).pack(pady=10)
            
            btn = tk.Button(card, text="Acessar", font=('Arial', 10),
                          bg='#e94560', fg='white', command=comando)
            btn.pack(pady=10)
        
        for i in range(2):
            content_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            content_frame.grid_columnconfigure(i, weight=1)

    def mostrar_catalogo_jogos(self):
        self.mostrar_catalogo_produtos('jogo')

    def mostrar_catalogo_consoles(self):
        self.mostrar_catalogo_produtos('console')

    def mostrar_catalogo_acessorios(self):
        self.mostrar_catalogo_produtos('acessorio')

    def mostrar_catalogo_produtos(self, categoria):
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        titulo = "Jogos" if categoria == 'jogo' else "Consoles" if categoria == 'console' else "Acessórios"
        tk.Label(header_frame, text=f"🛍️ Catálogo de {titulo}", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="← Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_cliente)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        filtros_frame = tk.Frame(main_frame, bg='#16213e')
        filtros_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(filtros_frame, text="Filtrar por plataforma:", 
                font=('Arial', 10), bg='#16213e', fg='white').pack(side=tk.LEFT, padx=5)
        
        plataformas = ["Todas", "PS5", "Xbox", "Switch", "PC", "Multi"]
        self.var_plataforma = tk.StringVar(value="Todas")
        
        for plataforma in plataformas:
            tk.Radiobutton(filtros_frame, text=plataforma, variable=self.var_plataforma,
                          value=plataforma, bg='#16213e', fg='white', 
                          selectcolor='#0f3460', command=self.filtrar_produtos).pack(side=tk.LEFT, padx=5)
        
        produtos_frame = tk.Frame(main_frame, bg='#1a1a2e')
        produtos_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.canvas_catalogo = tk.Canvas(produtos_frame, bg='#1a1a2e')
        scrollbar = ttk.Scrollbar(produtos_frame, orient=tk.VERTICAL, command=self.canvas_catalogo.yview)
        self.scrollable_frame = tk.Frame(self.canvas_catalogo, bg='#1a1a2e')
        
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas_catalogo.configure(scrollregion=self.canvas_catalogo.bbox("all")))
        self.canvas_catalogo.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas_catalogo.configure(yscrollcommand=scrollbar.set)
        
        self.categoria_atual = categoria
        self.atualizar_lista_produtos()
        
        self.canvas_catalogo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def atualizar_lista_produtos(self):
        # Limpar produtos atuais
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        plataforma_filtro = self.var_plataforma.get() if self.var_plataforma else "Todas"
        produtos_filtrados = [p for p in self.produtos if p['categoria'] == self.categoria_atual]
        
        if plataforma_filtro != "Todas":
            produtos_filtrados = [p for p in produtos_filtrados if p['plataforma'] == plataforma_filtro]
        
        if not produtos_filtrados:
            tk.Label(self.scrollable_frame, text="Nenhum produto encontrado", 
                    font=('Arial', 14), bg='#1a1a2e', fg='white').pack(pady=50)
            return
        
        for produto in produtos_filtrados:
            card = tk.Frame(self.scrollable_frame, bg='#16213e', relief=tk.RAISED, bd=1)
            card.pack(fill=tk.X, pady=5, padx=10)
            
            img_label = tk.Label(card, text=produto['imagem'], font=('Arial', 24), bg='#16213e', fg='#e94560')
            img_label.pack(side=tk.LEFT, padx=15, pady=15)
            
            info_frame = tk.Frame(card, bg='#16213e')
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
            
            tk.Label(info_frame, text=produto['nome'], font=('Arial', 12, 'bold'),
                    bg='#16213e', fg='white', anchor='w').pack(fill=tk.X)
            tk.Label(info_frame, text=produto['descricao'], font=('Arial', 9),
                    bg='#16213e', fg='#aaaaaa', anchor='w').pack(fill=tk.X)
            tk.Label(info_frame, text=f"R$ {produto['preco']:.2f}", font=('Arial', 14, 'bold'),
                    bg='#16213e', fg='#e94560', anchor='w').pack(fill=tk.X)
            tk.Label(info_frame, text=f"Plataforma: {produto['plataforma']} | Estoque: {produto['estoque']} unidades", 
                    font=('Arial', 9), bg='#16213e', fg='#aaaaaa', anchor='w').pack(fill=tk.X)
            
            btn_add = tk.Button(card, text="🛒 Adicionar ao Carrinho", font=('Arial', 10),
                              bg='#e94560', fg='white', padx=15,
                              command=lambda p=produto: self.adicionar_carrinho(p))
            btn_add.pack(side=tk.RIGHT, padx=10, pady=10)

    def filtrar_produtos(self):
        self.atualizar_lista_produtos()

    def mostrar_carrinho(self):
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🛒 Carrinho de Compras", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="← Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_cliente)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        if not self.carrinho:
            empty_frame = tk.Frame(content_frame, bg='#1a1a2e')
            empty_frame.pack(expand=True)
            
            tk.Label(empty_frame, text="🛒", font=('Arial', 80), bg='#1a1a2e', fg='#666666').pack(pady=20)
            tk.Label(empty_frame, text="Seu carrinho está vazio", font=('Arial', 16), 
                    bg='#1a1a2e', fg='white').pack()
            tk.Label(empty_frame, text="Navegue pelo catálogo e adicione produtos!", font=('Arial', 12), 
                    bg='#1a1a2e', fg='#aaaaaa').pack(pady=10)
            return
        
        itens_frame = tk.Frame(content_frame, bg='#1a1a2e')
        itens_frame.pack(fill=tk.BOTH, expand=True)
        
        total = 0
        for i, item in enumerate(self.carrinho):
            item_frame = tk.Frame(itens_frame, bg='#16213e', relief=tk.RAISED, bd=1)
            item_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(item_frame, text=item['imagem'], font=('Arial', 20), 
                    bg='#16213e', fg='#e94560').pack(side=tk.LEFT, padx=15, pady=10)
            
            info_frame = tk.Frame(item_frame, bg='#16213e')
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
            
            tk.Label(info_frame, text=item['nome'], font=('Arial', 11, 'bold'),
                    bg='#16213e', fg='white').pack(anchor='w')
            tk.Label(info_frame, text=f"R$ {item['preco']:.2f}", font=('Arial', 11),
                    bg='#16213e', fg='#e94560').pack(anchor='w')
            tk.Label(info_frame, text=f"Plataforma: {item['plataforma']}", font=('Arial', 9),
                    bg='#16213e', fg='#aaaaaa').pack(anchor='w')
            
            btn_remover = tk.Button(item_frame, text="❌ Remover", font=('Arial', 9),
                                  bg='#e94560', fg='white',
                                  command=lambda idx=i: self.remover_carrinho(idx))
            btn_remover.pack(side=tk.RIGHT, padx=10, pady=10)
            
            total += item['preco']
        
        total_frame = tk.Frame(content_frame, bg='#16213e', relief=tk.RAISED, bd=2)
        total_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(total_frame, text=f"💰 Total: R$ {total:.2f}", 
                font=('Arial', 16, 'bold'), bg='#16213e', fg='#e94560').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_finalizar = tk.Button(total_frame, text="✅ Finalizar Compra", font=('Arial', 12, 'bold'),
                                 bg='#2ecc71', fg='white', padx=30, pady=10,
                                 command=self.finalizar_compra)
        btn_finalizar.pack(side=tk.RIGHT, padx=20, pady=10)
        
        btn_limpar = tk.Button(total_frame, text="🗑️ Limpar Carrinho", font=('Arial', 10),
                              bg='#e74c3c', fg='white', padx=15, pady=5,
                              command=self.limpar_carrinho)
        btn_limpar.pack(side=tk.RIGHT, padx=10, pady=10)

    def mostrar_historico_pedidos(self):
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📋 Meus Pedidos", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="← Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_cliente)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        pedidos_usuario = [p for p in self.pedidos if p['usuario_id'] == self.usuario_id]
        
        if not pedidos_usuario:
            empty_frame = tk.Frame(content_frame, bg='#1a1a2e')
            empty_frame.pack(expand=True)
            
            tk.Label(empty_frame, text="📦", font=('Arial', 80), bg='#1a1a2e', fg='#666666').pack(pady=20)
            tk.Label(empty_frame, text="Nenhum pedido realizado", font=('Arial', 16), 
                    bg='#1a1a2e', fg='white').pack()
            tk.Label(empty_frame, text="Seus pedidos aparecerão aqui!", font=('Arial', 12), 
                    bg='#1a1a2e', fg='#aaaaaa').pack(pady=10)
            return
        
        # Frame com scrollbar para os pedidos
        canvas_frame = tk.Frame(content_frame, bg='#1a1a2e')
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(canvas_frame, bg='#1a1a2e')
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a1a2e')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for pedido in pedidos_usuario:
            pedido_frame = tk.Frame(scrollable_frame, bg='#16213e', relief=tk.RAISED, bd=1)
            pedido_frame.pack(fill=tk.X, pady=10, padx=10)
            
            header_pedido = tk.Frame(pedido_frame, bg='#0f3460')
            header_pedido.pack(fill=tk.X)
            
            tk.Label(header_pedido, text=f"Pedido #{pedido['id']}", font=('Arial', 12, 'bold'),
                    bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=15, pady=10)
            
            status_color = {'pendente': '#f39c12', 'enviado': '#3498db', 'entregue': '#2ecc71', 'cancelado': '#e74c3c'}
            tk.Label(header_pedido, text=pedido['status'].upper(), font=('Arial', 10, 'bold'),
                    bg=status_color.get(pedido['status'], '#666666'), fg='white',
                    padx=10, pady=5).pack(side=tk.RIGHT, padx=15, pady=10)
            
            info_pedido = tk.Frame(pedido_frame, bg='#16213e')
            info_pedido.pack(fill=tk.X, padx=15, pady=10)
            
            tk.Label(info_pedido, text=f"Data: {pedido['data']}", font=('Arial', 10),
                    bg='#16213e', fg='#aaaaaa').pack(anchor='w')
            
            itens_text = ", ".join([self.obter_nome_produto(item['produto_id']) for item in pedido['itens']])
            tk.Label(info_pedido, text=f"Itens: {itens_text}", font=('Arial', 10),
                    bg='#16213e', fg='white', wraplength=500).pack(anchor='w', pady=5)
            
            tk.Label(info_pedido, text=f"Total: R$ {pedido['total']:.2f}", font=('Arial', 12, 'bold'),
                    bg='#16213e', fg='#e94560').pack(anchor='w')
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def mostrar_meus_dados(self):
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="👤 Meus Dados", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="← Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_cliente)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        usuario = next((u for u in self.usuarios if u['id'] == self.usuario_id), None)
        if not usuario:
            messagebox.showerror("Erro", "Usuário não encontrado!")
            return
        
        dados_frame = tk.Frame(content_frame, bg='#16213e', relief=tk.RAISED, bd=2)
        dados_frame.pack(fill=tk.X, padx=50, pady=20)
        
        tk.Label(dados_frame, text="👤", font=('Arial', 50), bg='#16213e', fg='#e94560').pack(pady=20)
        
        dados = [
            ("Nome:", usuario['nome']),
            ("E-mail:", usuario['email']),
            ("Tipo:", usuario['tipo'].title()),
            ("Endereço:", usuario['endereco']),
            ("Telefone:", usuario['telefone']),
            ("Data de Cadastro:", usuario['data_cadastro'])
        ]
        
        for campo, valor in dados:
            linha = tk.Frame(dados_frame, bg='#16213e')
            linha.pack(fill=tk.X, padx=30, pady=15)
            
            tk.Label(linha, text=campo, font=('Arial', 12, 'bold'), 
                    bg='#16213e', fg='#e94560', width=18, anchor='w').pack(side=tk.LEFT)
            tk.Label(linha, text=valor, font=('Arial', 12), 
                    bg='#16213e', fg='white', anchor='w').pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        botoes_frame = tk.Frame(dados_frame, bg='#16213e')
        botoes_frame.pack(fill=tk.X, pady=20)
        
        btn_editar = tk.Button(botoes_frame, text="✏️ Editar Dados", font=('Arial', 11),
                              bg='#3498db', fg='white', padx=20, pady=10,
                              command=self.editar_dados_usuario)
        btn_editar.pack(side=tk.LEFT, padx=15)
        
        btn_senha = tk.Button(botoes_frame, text="🔒 Alterar Senha", font=('Arial', 11),
                             bg='#f39c12', fg='white', padx=20, pady=10,
                             command=self.alterar_senha)
        btn_senha.pack(side=tk.LEFT, padx=15)

    def mostrar_painel_administrador(self):
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"⚙️ Painel Administrativo - {self.usuario_logado}", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=20)
        
        btn_sair = tk.Button(header_frame, text="🚪 Sair", font=('Arial', 10),
                            bg='#e94560', fg='white', command=self.logout)
        btn_sair.pack(side=tk.RIGHT, padx=20, pady=20)
        
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        funcionalidades = [
            ("📦 Gerenciar Produtos", "Adicionar/editar/remover produtos", self.mostrar_gerenciar_produtos),
            ("➕ Cadastrar Produto", "Cadastrar novo produto", self.mostrar_cadastro_produto),
            ("📊 Gerenciar Pedidos", "Visualizar e atualizar pedidos", self.mostrar_gerenciamento_pedidos),
            ("👥 Usuários Cadastrados", "Visualizar todos os usuários", self.mostrar_tabela_usuarios),
            ("📈 Relatórios", "Relatórios e estatísticas", self.mostrar_relatorios),
            ("💰 Dashboard", "Indicadores de desempenho", self.mostrar_dashboard)
        ]
        
        for i, (titulo, descricao, comando) in enumerate(funcionalidades):
            card = tk.Frame(content_frame, bg='#16213e', relief=tk.RAISED, bd=1)
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky='nsew')
            
            # Extrair emoji do título
            emoji = titulo.split()[0]
            texto = titulo[len(emoji):].strip()
            
            tk.Label(card, text=emoji, font=('Arial', 30), bg='#16213e', fg='#e94560').pack(pady=20)
            tk.Label(card, text=texto, font=('Arial', 12, 'bold'), bg='#16213e', fg='white').pack(pady=5)
            tk.Label(card, text=descricao, font=('Arial', 10), bg='#16213e', fg='#aaaaaa', wraplength=150).pack(pady=10)
            
            btn = tk.Button(card, text="Acessar", font=('Arial', 10),
                          bg='#e94560', fg='white', command=comando)
            btn.pack(pady=10)
        
        for i in range(2):
            content_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            content_frame.grid_columnconfigure(i, weight=1)

    # ========== FUNÇÕES DO ADMINISTRADOR ==========

    def mostrar_gerenciar_produtos(self):
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📦 Gerenciar Produtos", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="← Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_administrador)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        btn_add = tk.Button(header_frame, text="➕ Novo Produto", font=('Arial', 10),
                           bg='#2ecc71', fg='white', command=self.mostrar_cadastro_produto)
        btn_add.pack(side=tk.RIGHT, padx=10, pady=15)
        
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tabela de produtos
        columns = ('ID', 'Nome', 'Categoria', 'Plataforma', 'Preço', 'Estoque')
        self.tree_produtos = ttk.Treeview(content_frame, columns=columns, show='headings', height=15)
        
        # Configurar colunas
        widths = {'ID': 50, 'Nome': 200, 'Categoria': 100, 'Plataforma': 100, 'Preço': 100, 'Estoque': 80}
        for col in columns:
            self.tree_produtos.heading(col, text=col)
            self.tree_produtos.column(col, width=widths.get(col, 120))
        
        # Scrollbar
        scrollbar_produtos = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=self.tree_produtos.yview)
        self.tree_produtos.configure(yscrollcommand=scrollbar_produtos.set)
        
        # Preencher dados
        self.atualizar_tabela_produtos()
        
        # Botões de ação
        botoes_frame = tk.Frame(content_frame, bg='#1a1a2e')
        botoes_frame.pack(fill=tk.X, pady=10)
        
        btn_editar = tk.Button(botoes_frame, text="✏️ Editar", font=('Arial', 10),
                              bg='#3498db', fg='white', padx=20, pady=5,
                              command=self.editar_produto)
        btn_editar.pack(side=tk.LEFT, padx=5)
        
        btn_deletar = tk.Button(botoes_frame, text="🗑️ Deletar", font=('Arial', 10),
                               bg='#e74c3c', fg='white', padx=20, pady=5,
                               command=self.deletar_produto)
        btn_deletar.pack(side=tk.LEFT, padx=5)
        
        btn_atualizar = tk.Button(botoes_frame, text="🔄 Atualizar", font=('Arial', 10),
                                 bg='#f39c12', fg='white', padx=20, pady=5,
                                 command=self.atualizar_tabela_produtos)
        btn_atualizar.pack(side=tk.LEFT, padx=5)
        
        self.tree_produtos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_produtos.pack(side=tk.RIGHT, fill=tk.Y)

    def mostrar_cadastro_produto(self):
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="➕ Cadastrar Produto", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="← Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_gerenciar_produtos)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        form_frame = tk.Frame(content_frame, bg='#16213e', relief=tk.RAISED, bd=2)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        tk.Label(form_frame, text="📦 Novo Produto", font=('Arial', 20, 'bold'),
                bg='#16213e', fg='#e94560').pack(pady=20)
        
        # Campos do formulário
        campos = [
            ("Nome:", "text"),
            ("Descrição:", "text"),
            ("Categoria:", "combo"),
            ("Plataforma:", "combo"),
            ("Preço:", "number"),
            ("Estoque:", "number"),
            ("Ícone:", "text")
        ]
        
        self.produto_entries = {}
        
        for campo, tipo in campos:
            linha = tk.Frame(form_frame, bg='#16213e')
            linha.pack(fill=tk.X, padx=30, pady=10)
            
            tk.Label(linha, text=campo, font=('Arial', 12, 'bold'),
                    bg='#16213e', fg='white', width=12, anchor='w').pack(side=tk.LEFT)
            
            if tipo == "combo" and campo == "Categoria:":
                widget = ttk.Combobox(linha, values=['console', 'jogo', 'acessorio'], 
                                    font=('Arial', 11), width=25, state='readonly')
            elif tipo == "combo" and campo == "Plataforma:":
                widget = ttk.Combobox(linha, values=['PS5', 'Xbox', 'Switch', 'PC', 'Multi'], 
                                    font=('Arial', 11), width=25, state='readonly')
            else:
                widget = tk.Entry(linha, font=('Arial', 11), bg='#1a1a2e', fg='white', width=28)
                if campo == "Ícone:":
                    widget.insert(0, "🎮")
            
            widget.pack(side=tk.LEFT, padx=10, ipady=3)
            self.produto_entries[campo.rstrip(':')] = widget
        
        botoes_frame = tk.Frame(form_frame, bg='#16213e')
        botoes_frame.pack(pady=30)
        
        btn_salvar = tk.Button(botoes_frame, text="💾 Salvar Produto", font=('Arial', 12, 'bold'),
                              bg='#2ecc71', fg='white', padx=30, pady=10,
                              command=self.salvar_produto)
        btn_salvar.pack(side=tk.LEFT, padx=10)
        
        btn_limpar = tk.Button(botoes_frame, text="🗑️ Limpar", font=('Arial', 10),
                              bg='#e74c3c', fg='white', padx=20, pady=10,
                              command=self.limpar_formulario_produto)
        btn_limpar.pack(side=tk.LEFT, padx=10)

    def mostrar_gerenciamento_pedidos(self):
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📊 Gerenciamento de Pedidos", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="← Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_administrador)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        if not self.pedidos:
            empty_frame = tk.Frame(content_frame, bg='#1a1a2e')
            empty_frame.pack(expand=True)
            
            tk.Label(empty_frame, text="📊", font=('Arial', 80), bg='#1a1a2e', fg='#666666').pack(pady=20)
            tk.Label(empty_frame, text="Nenhum pedido encontrado", font=('Arial', 16), 
                    bg='#1a1a2e', fg='white').pack()
            return
        
        # Tabela de pedidos
        columns = ('ID', 'Usuario', 'Data', 'Total', 'Status')
        self.tree_pedidos = ttk.Treeview(content_frame, columns=columns, show='headings', height=15)
        
        # Configurar colunas
        widths = {'ID': 60, 'Usuario': 150, 'Data': 100, 'Total': 100, 'Status': 100}
        for col in columns:
            self.tree_pedidos.heading(col, text=col)
            self.tree_pedidos.column(col, width=widths.get(col, 120))
        
        # Scrollbar
        scrollbar_pedidos = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=self.tree_pedidos.yview)
        self.tree_pedidos.configure(yscrollcommand=scrollbar_pedidos.set)
        
        # Preencher dados
        self.atualizar_tabela_pedidos()
        
        # Botões de ação
        botoes_frame = tk.Frame(content_frame, bg='#1a1a2e')
        botoes_frame.pack(fill=tk.X, pady=10)
        
        btn_detalhes = tk.Button(botoes_frame, text="👁️ Ver Detalhes", font=('Arial', 10),
                                bg='#3498db', fg='white', padx=20, pady=5,
                                command=self.ver_detalhes_pedido)
        btn_detalhes.pack(side=tk.LEFT, padx=5)
        
        btn_status = tk.Button(botoes_frame, text="🔄 Alterar Status", font=('Arial', 10),
                              bg='#f39c12', fg='white', padx=20, pady=5,
                              command=self.alterar_status_pedido)
        btn_status.pack(side=tk.LEFT, padx=5)
        
        btn_atualizar = tk.Button(botoes_frame, text="🔄 Atualizar", font=('Arial', 10),
                                 bg='#2ecc71', fg='white', padx=20, pady=5,
                                 command=self.atualizar_tabela_pedidos)
        btn_atualizar.pack(side=tk.LEFT, padx=5)
        
        self.tree_pedidos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_pedidos.pack(side=tk.RIGHT, fill=tk.Y)

    def mostrar_tabela_usuarios(self):
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="👥 Usuários Cadastrados", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="← Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_administrador)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tabela de usuários
        columns = ('ID', 'Nome', 'Email', 'Tipo', 'Telefone', 'Data Cadastro')
        tree_usuarios = ttk.Treeview(content_frame, columns=columns, show='headings', height=15)
        
        # Configurar colunas
        widths = {'ID': 50, 'Nome': 180, 'Email': 200, 'Tipo': 80, 'Telefone': 120, 'Data Cadastro': 100}
        for col in columns:
            tree_usuarios.heading(col, text=col)
            tree_usuarios.column(col, width=widths.get(col, 120))
        
        # Scrollbar
        scrollbar_usuarios = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=tree_usuarios.yview)
        tree_usuarios.configure(yscrollcommand=scrollbar_usuarios.set)
        
        # Preencher dados
        for usuario in self.usuarios:
            tree_usuarios.insert('', tk.END, values=(
                usuario['id'],
                usuario['nome'],
                usuario['email'],
                usuario['tipo'].title(),
                usuario['telefone'],
                usuario['data_cadastro']
            ))
        
        tree_usuarios.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_usuarios.pack(side=tk.RIGHT, fill=tk.Y)

    def mostrar_relatorios(self):
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📈 Relatórios e Estatísticas", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="← Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_administrador)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Calcular estatísticas
        total_usuarios = len([u for u in self.usuarios if u['tipo'] == 'cliente'])
        total_produtos = len(self.produtos)
        total_pedidos = len(self.pedidos)
        total_vendas = sum(p['total'] for p in self.pedidos)
        ticket_medio = total_vendas / total_pedidos if total_pedidos > 0 else 0
        
        # Produtos mais vendidos
        vendas_por_produto = {}
        for pedido in self.pedidos:
            for item in pedido['itens']:
                produto_id = item['produto_id']
                quantidade = item['quantidade']
                if produto_id in vendas_por_produto:
                    vendas_por_produto[produto_id] += quantidade
                else:
                    vendas_por_produto[produto_id] = quantidade
        
        # Grid de estatísticas
        stats_frame = tk.Frame(content_frame, bg='#1a1a2e')
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Estatísticas gerais
        estatisticas = [
            ("👥 Clientes Cadastrados", f"{total_usuarios}"),
            ("📦 Produtos no Estoque", f"{total_produtos}"),
            ("📋 Total de Pedidos", f"{total_pedidos}"),
            ("💰 Total em Vendas", f"R$ {total_vendas:.2f}"),
            ("📊 Ticket Médio", f"R$ {ticket_medio:.2f}"),
            ("🏆 Produto Mais Vendido", self.obter_produto_mais_vendido(vendas_por_produto))
        ]
        
        for i, (titulo, valor) in enumerate(estatisticas):
            card = tk.Frame(stats_frame, bg='#16213e', relief=tk.RAISED, bd=1)
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky='nsew')
            
            # Extrair emoji do título
            emoji = titulo.split()[0]
            texto = titulo[len(emoji):].strip()
            
            tk.Label(card, text=emoji, font=('Arial', 30), bg='#16213e', fg='#e94560').pack(pady=15)
            tk.Label(card, text=texto, font=('Arial', 10, 'bold'), bg='#16213e', fg='white').pack(pady=5)
            tk.Label(card, text=valor, font=('Arial', 12, 'bold'), bg='#16213e', fg='#e94560').pack(pady=10)
        
        for i in range(2):
            stats_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            stats_frame.grid_columnconfigure(i, weight=1)

    def mostrar_dashboard(self):
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="💰 Dashboard", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="← Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_administrador)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Indicadores principais
        kpis_frame = tk.Frame(content_frame, bg='#1a1a2e')
        kpis_frame.pack(fill=tk.X, pady=20)
        
        # Calcular KPIs
        vendas_hoje = len([p for p in self.pedidos if p['data'] == datetime.now().strftime("%Y-%m-%d")])
        produtos_baixo_estoque = len([p for p in self.produtos if p['estoque'] < 5])
        pedidos_pendentes = len([p for p in self.pedidos if p['status'] == 'pendente'])
        
        kpis = [
            ("💰", "Vendas Hoje", f"{vendas_hoje}", "#2ecc71"),
            ("📦", "Estoque Baixo", f"{produtos_baixo_estoque}", "#e74c3c"),
            ("⏳", "Pedidos Pendentes", f"{pedidos_pendentes}", "#f39c12"),
            ("📊", "Total Produtos", f"{len(self.produtos)}", "#3498db")
        ]
        
        for i, (emoji, titulo, valor, cor) in enumerate(kpis):
            kpi_card = tk.Frame(kpis_frame, bg=cor, relief=tk.RAISED, bd=2)
            kpi_card.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
            
            tk.Label(kpi_card, text=emoji, font=('Arial', 24), bg=cor, fg='white').pack(pady=10)
            tk.Label(kpi_card, text=valor, font=('Arial', 20, 'bold'), bg=cor, fg='white').pack()
            tk.Label(kpi_card, text=titulo, font=('Arial', 10), bg=cor, fg='white').pack(pady=5)
        
        for i in range(4):
            kpis_frame.grid_columnconfigure(i, weight=1)
        
        # Lista de produtos com baixo estoque
        if produtos_baixo_estoque > 0:
            baixo_estoque_frame = tk.Frame(content_frame, bg='#16213e', relief=tk.RAISED, bd=2)
            baixo_estoque_frame.pack(fill=tk.X, pady=20)
            
            tk.Label(baixo_estoque_frame, text="⚠️ Produtos com Baixo Estoque", 
                    font=('Arial', 14, 'bold'), bg='#16213e', fg='#e74c3c').pack(pady=10)
            
            for produto in [p for p in self.produtos if p['estoque'] < 5]:
                item_frame = tk.Frame(baixo_estoque_frame, bg='#16213e')
                item_frame.pack(fill=tk.X, padx=20, pady=5)
                
                tk.Label(item_frame, text=f"{produto['nome']}", font=('Arial', 10),
                        bg='#16213e', fg='white').pack(side=tk.LEFT)
                tk.Label(item_frame, text=f"Estoque: {produto['estoque']}", font=('Arial', 10, 'bold'),
                        bg='#16213e', fg='#e74c3c').pack(side=tk.RIGHT)

    # ========== FUNÇÕES DE AÇÃO ==========

    def fazer_login(self):
        """Função de login"""
        email = self.login_email.get().strip()
        senha = self.login_senha.get().strip()
        
        if not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        usuario = next((u for u in self.usuarios if u['email'] == email), None)
        
        if usuario and self.verificar_senha(senha, usuario['senha']):
            self.usuario_logado = usuario['nome']
            self.tipo_usuario = usuario['tipo']
            self.usuario_id = usuario['id']
            
            if usuario['tipo'] == 'admin':
                self.mostrar_painel_administrador()
            else:
                self.mostrar_painel_cliente()
        else:
            messagebox.showerror("Erro", "E-mail ou senha incorretos!")

    def cadastrar_usuario(self):
        """Cadastra novo usuário"""
        try:
            dados = {}
            
            # Validar campos obrigatórios
            campos_obrigatorios = ['nome_completo', 'e-mail', 'senha', 'confirmar_senha']
            for campo in campos_obrigatorios:
                if campo not in self.cadastro_entries:
                    messagebox.showerror("Erro", f"Campo {campo} não encontrado!")
                    return
                
                valor = self.cadastro_entries[campo].get().strip()
                if not valor:
                    messagebox.showerror("Erro", f"Preencha o campo: {campo.replace('_', ' ').title()}")
                    return
                dados[campo] = valor
            
            # Validar senhas
            if dados['senha'] != dados['confirmar_senha']:
                messagebox.showerror("Erro", "As senhas não coincidem!")
                return
            
            if len(dados['senha']) < 6:
                messagebox.showerror("Erro", "A senha deve ter pelo menos 6 caracteres!")
                return
            
            # Verificar email único
            if any(u['email'] == dados['e-mail'] for u in self.usuarios):
                messagebox.showerror("Erro", "Este e-mail já está cadastrado!")
                return
            
            # Criar novo usuário
            novo_id = max([u['id'] for u in self.usuarios]) + 1 if self.usuarios else 1
            novo_usuario = {
                'id': novo_id,
                'nome': dados['nome_completo'],
                'email': dados['e-mail'],
                'senha': self.hash_password(dados['senha']),
                'tipo': 'cliente',
                'endereco': self.cadastro_entries.get('endereço', tk.Entry()).get().strip() or 'Não informado',
                'telefone': self.cadastro_entries.get('telefone', tk.Entry()).get().strip() or 'Não informado',
                'data_cadastro': datetime.now().strftime("%Y-%m-%d")
            }
            
            self.usuarios.append(novo_usuario)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!\n\nFaça login para continuar.")
            
            # Limpar formulário
            for entry in self.cadastro_entries.values():
                entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {str(e)}")

    def adicionar_carrinho(self, produto):
        """Adiciona produto ao carrinho"""
        if produto['estoque'] <= 0:
            messagebox.showwarning("Estoque", "Produto sem estoque disponível!")
            return
        
        # Verificar se produto já está no carrinho
        produto_existente = next((item for item in self.carrinho if item['id'] == produto['id']), None)
        if produto_existente:
            messagebox.showinfo("Carrinho", f"✅ {produto['nome']} já está no carrinho!")
        else:
            self.carrinho.append(produto.copy())
            messagebox.showinfo("Sucesso", f"✅ {produto['nome']} adicionado ao carrinho!")

    def remover_carrinho(self, index):
        """Remove produto do carrinho"""
        if 0 <= index < len(self.carrinho):
            produto = self.carrinho.pop(index)
            messagebox.showinfo("Removido", f"❌ {produto['nome']} removido do carrinho!")
            self.mostrar_carrinho()

    def limpar_carrinho(self):
        """Limpa todo o carrinho"""
        if self.carrinho:
            resposta = messagebox.askyesno("Confirmar", "Deseja realmente limpar todo o carrinho?")
            if resposta:
                self.carrinho.clear()
                messagebox.showinfo("Carrinho", "🛒 Carrinho limpo!")
                self.mostrar_carrinho()

    def finalizar_compra(self):
        """Finaliza a compra"""
        if not self.carrinho:
            messagebox.showwarning("Carrinho", "Carrinho vazio!")
            return
        
        # Verificar estoque
        for item in self.carrinho:
            produto = next((p for p in self.produtos if p['id'] == item['id']), None)
            if not produto or produto['estoque'] <= 0:
                messagebox.showerror("Erro", f"Produto {item['nome']} não está mais disponível!")
                return
        
        # Calcular total
        total = sum(item['preco'] for item in self.carrinho)
        
        # Confirmar compra
        resposta = messagebox.askyesno("Confirmar Compra", 
                                     f"Confirmar compra no valor de R$ {total:.2f}?")
        if not resposta:
            return
        
        # Criar pedido
        novo_id = max([p['id'] for p in self.pedidos]) + 1 if self.pedidos else 1
        novo_pedido = {
            'id': novo_id,
            'usuario_id': self.usuario_id,
            'itens': [{'produto_id': item['id'], 'quantidade': 1, 'preco': item['preco']} 
                     for item in self.carrinho],
            'total': total,
            'status': 'pendente',
            'data': datetime.now().strftime("%Y-%m-%d")
        }
        
        # Atualizar estoque
        for item in self.carrinho:
            produto = next((p for p in self.produtos if p['id'] == item['id']), None)
            if produto:
                produto['estoque'] -= 1
        
        self.pedidos.append(novo_pedido)
        self.carrinho.clear()
        
        messagebox.showinfo("Sucesso", f"✅ Compra finalizada com sucesso!\n\nPedido #{novo_id}\nTotal: R$ {total:.2f}")
        self.mostrar_painel_cliente()

    def obter_nome_produto(self, produto_id):
        """Retorna o nome do produto pelo ID"""
        produto = next((p for p in self.produtos if p['id'] == produto_id), None)
        return produto['nome'] if produto else f"Produto #{produto_id}"

    def obter_produto_mais_vendido(self, vendas_por_produto):
        """Retorna o nome do produto mais vendido"""
        if not vendas_por_produto:
            return "Nenhum"
        
        produto_id = max(vendas_por_produto, key=vendas_por_produto.get)
        return self.obter_nome_produto(produto_id)

    def obter_nome_usuario(self, usuario_id):
        """Retorna o nome do usuário pelo ID"""
        usuario = next((u for u in self.usuarios if u['id'] == usuario_id), None)
        return usuario['nome'] if usuario else f"Usuário #{usuario_id}"

    def logout(self):
        """Faz logout do usuário"""
        self.usuario_logado = None
        self.tipo_usuario = None
        self.usuario_id = None
        self.carrinho.clear()
        self.mostrar_tela_login()

    def recuperar_senha(self):
        """Funcionalidade de recuperação de senha"""
        email = self.login_email.get().strip()
        if not email:
            messagebox.showinfo("Recuperar Senha", "Digite seu e-mail no campo de login primeiro.")
            return
        
        usuario = next((u for u in self.usuarios if u['email'] == email), None)
        if usuario:
            messagebox.showinfo("Recuperar Senha", 
                              f"Instruções de recuperação enviadas para: {email}\n\n" +
                              "Para demonstração, suas credenciais são:\n" +
                              f"E-mail: {email}\n" +
                              "Senha: [Entre em contato com o administrador]")
        else:
            messagebox.showerror("Erro", "E-mail não encontrado no sistema!")

    def editar_dados_usuario(self):
        """Editar dados do usuário logado"""
        usuario = next((u for u in self.usuarios if u['id'] == self.usuario_id), None)
        if not usuario:
            messagebox.showerror("Erro", "Usuário não encontrado!")
            return
        
        # Criar janela de edição
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Editar Dados")
        edit_window.geometry("400x500")
        edit_window.configure(bg='#16213e')
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Centralizar janela
        edit_window.update_idletasks()
        x = (edit_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (edit_window.winfo_screenheight() // 2) - (500 // 2)
        edit_window.geometry(f"400x500+{x}+{y}")
        
        tk.Label(edit_window, text="✏️ Editar Dados", font=('Arial', 16, 'bold'),
                bg='#16213e', fg='#e94560').pack(pady=20)
        
        # Campos editáveis
        campos = [
            ("Nome:", usuario['nome']),
            ("E-mail:", usuario['email']),
            ("Endereço:", usuario['endereco']),
            ("Telefone:", usuario['telefone'])
        ]
        
        entries = {}
        for campo, valor_atual in campos:
            frame = tk.Frame(edit_window, bg='#16213e')
            frame.pack(fill=tk.X, padx=30, pady=10)
            
            tk.Label(frame, text=campo, font=('Arial', 11, 'bold'),
                    bg='#16213e', fg='white', width=10, anchor='w').pack(side=tk.LEFT)
            
            entry = tk.Entry(frame, font=('Arial', 11), bg='#1a1a2e', fg='white', width=25)
            entry.insert(0, valor_atual)
            entry.pack(side=tk.LEFT, padx=10, ipady=3)
            
            entries[campo.rstrip(':')] = entry
        
        def salvar_edicao():
            try:
                # Validar e salvar
                usuario['nome'] = entries['Nome'].get().strip() or usuario['nome']
                novo_email = entries['E-mail'].get().strip()
                
                # Verificar email único (exceto o próprio)
                if novo_email != usuario['email']:
                    if any(u['email'] == novo_email for u in self.usuarios if u['id'] != self.usuario_id):
                        messagebox.showerror("Erro", "Este e-mail já está em uso!")
                        return
                    usuario['email'] = novo_email
                
                usuario['endereco'] = entries['Endereço'].get().strip() or usuario['endereco']
                usuario['telefone'] = entries['Telefone'].get().strip() or usuario['telefone']
                
                messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
                edit_window.destroy()
                self.mostrar_meus_dados()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
        
        # Botões
        botoes_frame = tk.Frame(edit_window, bg='#16213e')
        botoes_frame.pack(pady=30)
        
        tk.Button(botoes_frame, text="💾 Salvar", font=('Arial', 11, 'bold'),
                 bg='#2ecc71', fg='white', padx=20, pady=10,
                 command=salvar_edicao).pack(side=tk.LEFT, padx=10)
        
        tk.Button(botoes_frame, text="❌ Cancelar", font=('Arial', 11),
                 bg='#e74c3c', fg='white', padx=20, pady=10,
                 command=edit_window.destroy).pack(side=tk.LEFT, padx=10)

    def alterar_senha(self):
        """Alterar senha do usuário"""
        # Criar janela de alteração de senha
        senha_window = tk.Toplevel(self.root)
        senha_window.title("Alterar Senha")
        senha_window.geometry("350x300")
        senha_window.configure(bg='#16213e')
        senha_window.transient(self.root)
        senha_window.grab_set()
        
        # Centralizar janela
        senha_window.update_idletasks()
        x = (senha_window.winfo_screenwidth() // 2) - (350 // 2)
        y = (senha_window.winfo_screenheight() // 2) - (300 // 2)
        senha_window.geometry(f"350x300+{x}+{y}")
        
        tk.Label(senha_window, text="🔒 Alterar Senha", font=('Arial', 16, 'bold'),
                bg='#16213e', fg='#e94560').pack(pady=20)
        
        # Campos de senha
        campos_frame = tk.Frame(senha_window, bg='#16213e')
        campos_frame.pack(pady=20)
        
        tk.Label(campos_frame, text="Senha Atual:", font=('Arial', 11),
                bg='#16213e', fg='white').pack(anchor='w', pady=(0,5))
        senha_atual = tk.Entry(campos_frame, font=('Arial', 11), show='*',
                              bg='#1a1a2e', fg='white', width=30)
        senha_atual.pack(pady=(0,15), ipady=3)
        
        tk.Label(campos_frame, text="Nova Senha:", font=('Arial', 11),
                bg='#16213e', fg='white').pack(anchor='w', pady=(0,5))
        nova_senha = tk.Entry(campos_frame, font=('Arial', 11), show='*',
                             bg='#1a1a2e', fg='white', width=30)
        nova_senha.pack(pady=(0,15), ipady=3)
        
        tk.Label(campos_frame, text="Confirmar Nova Senha:", font=('Arial', 11),
                bg='#16213e', fg='white').pack(anchor='w', pady=(0,5))
        confirmar_senha = tk.Entry(campos_frame, font=('Arial', 11), show='*',
                                  bg='#1a1a2e', fg='white', width=30)
        confirmar_senha.pack(ipady=3)
        
        def salvar_senha():
            try:
                usuario = next((u for u in self.usuarios if u['id'] == self.usuario_id), None)
                if not usuario:
                    messagebox.showerror("Erro", "Usuário não encontrado!")
                    return
                
                # Validações
                if not self.verificar_senha(senha_atual.get(), usuario['senha']):
                    messagebox.showerror("Erro", "Senha atual incorreta!")
                    return
                
                if len(nova_senha.get()) < 6:
                    messagebox.showerror("Erro", "Nova senha deve ter pelo menos 6 caracteres!")
                    return
                
                if nova_senha.get() != confirmar_senha.get():
                    messagebox.showerror("Erro", "Confirmação de senha não confere!")
                    return
                
                # Salvar nova senha
                usuario['senha'] = self.hash_password(nova_senha.get())
                messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")
                senha_window.destroy()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao alterar senha: {str(e)}")
        
        # Botões
        botoes_frame = tk.Frame(senha_window, bg='#16213e')
        botoes_frame.pack(pady=20)
        
        tk.Button(botoes_frame, text="💾 Salvar", font=('Arial', 11, 'bold'),
                 bg='#2ecc71', fg='white', padx=20, pady=8,
                 command=salvar_senha).pack(side=tk.LEFT, padx=10)
        
        tk.Button(botoes_frame, text="❌ Cancelar", font=('Arial', 11),
                 bg='#e74c3c', fg='white', padx=20, pady=8,
                 command=senha_window.destroy).pack(side=tk.LEFT, padx=10)

    # ========== FUNÇÕES ADMINISTRATIVAS ==========

    def atualizar_tabela_produtos(self):
        """Atualiza a tabela de produtos na tela administrativa"""
        if hasattr(self, 'tree_produtos'):
            # Limpar dados atuais
            for item in self.tree_produtos.get_children():
                self.tree_produtos.delete(item)
            
            # Adicionar produtos atualizados
            for produto in self.produtos:
                self.tree_produtos.insert('', tk.END, values=(
                    produto['id'],
                    produto['nome'],
                    produto['categoria'].title(),
                    produto['plataforma'],
                    f"R$ {produto['preco']:.2f}",
                    produto['estoque']
                ))

    def atualizar_tabela_pedidos(self):
        """Atualiza a tabela de pedidos na tela administrativa"""
        if hasattr(self, 'tree_pedidos'):
            # Limpar dados atuais
            for item in self.tree_pedidos.get_children():
                self.tree_pedidos.delete(item)
            
            # Adicionar pedidos atualizados
            for pedido in self.pedidos:
                nome_usuario = self.obter_nome_usuario(pedido['usuario_id'])
                self.tree_pedidos.insert('', tk.END, values=(
                    pedido['id'],
                    nome_usuario,
                    pedido['data'],
                    f"R$ {pedido['total']:.2f}",
                    pedido['status'].title()
                ))

    def salvar_produto(self):
        """Salva novo produto no sistema"""
        try:
            # Coletar dados do formulário
            nome = self.produto_entries['Nome'].get().strip()
            descricao = self.produto_entries['Descrição'].get().strip()
            categoria = self.produto_entries['Categoria'].get()
            plataforma = self.produto_entries['Plataforma'].get()
            preco_str = self.produto_entries['Preço'].get().strip()
            estoque_str = self.produto_entries['Estoque'].get().strip()
            icone = self.produto_entries['Ícone'].get().strip()
            
            # Validações
            if not all([nome, descricao, categoria, plataforma, preco_str, estoque_str]):
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return
            
            try:
                preco = float(preco_str.replace(',', '.'))
                estoque = int(estoque_str)
            except ValueError:
                messagebox.showerror("Erro", "Preço deve ser um número válido e estoque deve ser um inteiro!")
                return
            
            if preco <= 0 or estoque < 0:
                messagebox.showerror("Erro", "Preço deve ser maior que zero e estoque não pode ser negativo!")
                return
            
            # Criar novo produto
            novo_id = max([p['id'] for p in self.produtos]) + 1 if self.produtos else 1
            novo_produto = {
                'id': novo_id,
                'nome': nome,
                'descricao': descricao,
                'categoria': categoria.lower(),
                'plataforma': plataforma,
                'preco': preco,
                'estoque': estoque,
                'imagem': icone or '🎮'
            }
            
            self.produtos.append(novo_produto)
            messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado com sucesso!")
            self.limpar_formulario_produto()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar produto: {str(e)}")

    def limpar_formulario_produto(self):
        """Limpa o formulário de cadastro de produto"""
        for key, widget in self.produto_entries.items():
            if hasattr(widget, 'delete'):
                widget.delete(0, tk.END)
                if key == 'Ícone':
                    widget.insert(0, '🎮')
            elif hasattr(widget, 'set'):
                widget.set('')

    def editar_produto(self):
        """Edita produto selecionado"""
        if not hasattr(self, 'tree_produtos'):
            return
            
        selection = self.tree_produtos.selection()
        if not selection:
            messagebox.showwarning("Seleção", "Selecione um produto para editar!")
            return
        
        item = self.tree_produtos.item(selection[0])
        produto_id = int(item['values'][0])
        produto = next((p for p in self.produtos if p['id'] == produto_id), None)
        
        if not produto:
            messagebox.showerror("Erro", "Produto não encontrado!")
            return
        
        # Criar janela de edição
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Editar Produto - {produto['nome']}")
        edit_window.geometry("500x600")
        edit_window.configure(bg='#16213e')
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Centralizar janela
        edit_window.update_idletasks()
        x = (edit_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (edit_window.winfo_screenheight() // 2) - (600 // 2)
        edit_window.geometry(f"500x600+{x}+{y}")
        
        tk.Label(edit_window, text=f"✏️ Editando: {produto['nome']}", font=('Arial', 14, 'bold'),
                bg='#16213e', fg='#e94560').pack(pady=15)
        
        # Campos de edição
        campos = [
            ("Nome:", produto['nome'], "text"),
            ("Descrição:", produto['descricao'], "text"),
            ("Categoria:", produto['categoria'], "combo"),
            ("Plataforma:", produto['plataforma'], "combo"),
            ("Preço:", str(produto['preco']), "number"),
            ("Estoque:", str(produto['estoque']), "number"),
            ("Ícone:", produto['imagem'], "text")
        ]
        
        edit_entries = {}
        for campo, valor_atual, tipo in campos:
            frame = tk.Frame(edit_window, bg='#16213e')
            frame.pack(fill=tk.X, padx=30, pady=10)
            
            tk.Label(frame, text=campo, font=('Arial', 11, 'bold'),
                    bg='#16213e', fg='white', width=12, anchor='w').pack(side=tk.LEFT)
            
            if tipo == "combo" and campo == "Categoria:":
                widget = ttk.Combobox(frame, values=['console', 'jogo', 'acessorio'], 
                                    font=('Arial', 11), width=25, state='readonly')
                widget.set(valor_atual)
            elif tipo == "combo" and campo == "Plataforma:":
                widget = ttk.Combobox(frame, values=['PS5', 'Xbox', 'Switch', 'PC', 'Multi'], 
                                    font=('Arial', 11), width=25, state='readonly')
                widget.set(valor_atual)
            else:
                widget = tk.Entry(frame, font=('Arial', 11), bg='#1a1a2e', fg='white', width=28)
                widget.insert(0, valor_atual)
            
            widget.pack(side=tk.LEFT, padx=10, ipady=3)
            edit_entries[campo.rstrip(':')] = widget
        
        def salvar_edicao_produto():
            try:
                # Validar e salvar
                nome = edit_entries['Nome'].get().strip()
                descricao = edit_entries['Descrição'].get().strip()
                categoria = edit_entries['Categoria'].get()
                plataforma = edit_entries['Plataforma'].get()
                preco_str = edit_entries['Preço'].get().strip()
                estoque_str = edit_entries['Estoque'].get().strip()
                icone = edit_entries['Ícone'].get().strip()
                
                if not all([nome, descricao, categoria, plataforma, preco_str, estoque_str]):
                    messagebox.showerror("Erro", "Preencha todos os campos!")
                    return
                
                try:
                    preco = float(preco_str.replace(',', '.'))
                    estoque = int(estoque_str)
                except ValueError:
                    messagebox.showerror("Erro", "Valores inválidos para preço ou estoque!")
                    return
                
                if preco <= 0 or estoque < 0:
                    messagebox.showerror("Erro", "Preço deve ser maior que zero e estoque não pode ser negativo!")
                    return
                
                # Atualizar produto
                produto['nome'] = nome
                produto['descricao'] = descricao
                produto['categoria'] = categoria.lower()
                produto['plataforma'] = plataforma
                produto['preco'] = preco
                produto['estoque'] = estoque
                produto['imagem'] = icone or '🎮'
                
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
                edit_window.destroy()
                self.atualizar_tabela_produtos()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
        
        # Botões
        botoes_frame = tk.Frame(edit_window, bg='#16213e')
        botoes_frame.pack(pady=20)
        
        tk.Button(botoes_frame, text="💾 Salvar", font=('Arial', 11, 'bold'),
                 bg='#2ecc71', fg='white', padx=20, pady=10,
                 command=salvar_edicao_produto).pack(side=tk.LEFT, padx=10)
        
        tk.Button(botoes_frame, text="❌ Cancelar", font=('Arial', 11),
                 bg='#e74c3c', fg='white', padx=20, pady=10,
                 command=edit_window.destroy).pack(side=tk.LEFT, padx=10)

    def deletar_produto(self):
        """Deleta produto selecionado"""
        if not hasattr(self, 'tree_produtos'):
            return
            
        selection = self.tree_produtos.selection()
        if not selection:
            messagebox.showwarning("Seleção", "Selecione um produto para deletar!")
            return
        
        item = self.tree_produtos.item(selection[0])
        produto_id = int(item['values'][0])
        produto = next((p for p in self.produtos if p['id'] == produto_id), None)
        
        if not produto:
            messagebox.showerror("Erro", "Produto não encontrado!")
            return
        
        # Verificar se produto está em algum pedido
        produto_em_pedidos = any(
            any(item['produto_id'] == produto_id for item in pedido['itens']) 
            for pedido in self.pedidos
        )
        
        if produto_em_pedidos:
            messagebox.showwarning("Aviso", 
                                 f"O produto '{produto['nome']}' não pode ser deletado pois está presente em pedidos!\n\n" +
                                 "Você pode apenas zerar o estoque para não permitir novas vendas.")
            return
        
        # Confirmar exclusão
        resposta = messagebox.askyesno("Confirmar Exclusão", 
                                     f"Tem certeza que deseja deletar o produto:\n\n'{produto['nome']}'?\n\n" +
                                     "Esta ação não pode ser desfeita!")
        
        if resposta:
            self.produtos.remove(produto)
            messagebox.showinfo("Sucesso", f"Produto '{produto['nome']}' deletado com sucesso!")
            self.atualizar_tabela_produtos()

    def ver_detalhes_pedido(self):
        """Mostra detalhes do pedido selecionado"""
        if not hasattr(self, 'tree_pedidos'):
            return
            
        selection = self.tree_pedidos.selection()
        if not selection:
            messagebox.showwarning("Seleção", "Selecione um pedido para ver detalhes!")
            return
        
        item = self.tree_pedidos.item(selection[0])
        pedido_id = int(item['values'][0])
        pedido = next((p for p in self.pedidos if p['id'] == pedido_id), None)
        
        if not pedido:
            messagebox.showerror("Erro", "Pedido não encontrado!")
            return
        
        # Criar janela de detalhes
        detalhes_window = tk.Toplevel(self.root)
        detalhes_window.title(f"Detalhes do Pedido #{pedido_id}")
        detalhes_window.geometry("500x600")
        detalhes_window.configure(bg='#16213e')
        detalhes_window.transient(self.root)
        detalhes_window.grab_set()
        
        # Centralizar janela
        detalhes_window.update_idletasks()
        x = (detalhes_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (detalhes_window.winfo_screenheight() // 2) - (600 // 2)
        detalhes_window.geometry(f"500x600+{x}+{y}")
        
        # Cabeçalho
        header_frame = tk.Frame(detalhes_window, bg='#0f3460')
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text=f"📋 Pedido #{pedido_id}", font=('Arial', 16, 'bold'),
                bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        status_color = {'pendente': '#f39c12', 'enviado': '#3498db', 'entregue': '#2ecc71', 'cancelado': '#e74c3c'}
        tk.Label(header_frame, text=pedido['status'].upper(), font=('Arial', 12, 'bold'),
                bg=status_color.get(pedido['status'], '#666666'), fg='white',
                padx=15, pady=8).pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Conteúdo
        content_frame = tk.Frame(detalhes_window, bg='#16213e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Informações do pedido
        info_frame = tk.Frame(content_frame, bg='#16213e')
        info_frame.pack(fill=tk.X, pady=10)
        
        usuario_nome = self.obter_nome_usuario(pedido['usuario_id'])
        
        infos = [
            ("Cliente:", usuario_nome),
            ("Data do Pedido:", pedido['data']),
            ("Status:", pedido['status'].title()),
            ("Total:", f"R$ {pedido['total']:.2f}")
        ]
        
        for label, valor in infos:
            linha = tk.Frame(info_frame, bg='#16213e')
            linha.pack(fill=tk.X, pady=8)
            
            tk.Label(linha, text=label, font=('Arial', 11, 'bold'),
                    bg='#16213e', fg='#e94560', width=15, anchor='w').pack(side=tk.LEFT)
            tk.Label(linha, text=valor, font=('Arial', 11),
                    bg='#16213e', fg='white', anchor='w').pack(side=tk.LEFT)
        
        # Separador
        tk.Frame(content_frame, bg='#0f3460', height=2).pack(fill=tk.X, pady=20)
        
        # Lista de itens
        tk.Label(content_frame, text="📦 Itens do Pedido:", font=('Arial', 12, 'bold'),
                bg='#16213e', fg='#e94560').pack(anchor='w', pady=10)
        
        itens_frame = tk.Frame(content_frame, bg='#16213e')
        itens_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para scroll dos itens
        canvas = tk.Canvas(itens_frame, bg='#16213e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(itens_frame, orient=tk.VERTICAL, command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg='#16213e')
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Adicionar itens
        for item in pedido['itens']:
            produto = next((p for p in self.produtos if p['id'] == item['produto_id']), None)
            nome_produto = produto['nome'] if produto else f"Produto #{item['produto_id']}"
            imagem_produto = produto['imagem'] if produto else '❓'
            
            item_frame = tk.Frame(scroll_frame, bg='#1a1a2e', relief=tk.RAISED, bd=1)
            item_frame.pack(fill=tk.X, pady=5, padx=5)
            
            tk.Label(item_frame, text=imagem_produto, font=('Arial', 16),
                    bg='#1a1a2e', fg='#e94560').pack(side=tk.LEFT, padx=10, pady=10)
            
            info_item = tk.Frame(item_frame, bg='#1a1a2e')
            info_item.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=10)
            
            tk.Label(info_item, text=nome_produto, font=('Arial', 11, 'bold'),
                    bg='#1a1a2e', fg='white', anchor='w').pack(fill=tk.X)
            tk.Label(info_item, text=f"Quantidade: {item['quantidade']}", font=('Arial', 10),
                    bg='#1a1a2e', fg='#aaaaaa', anchor='w').pack(fill=tk.X)
            tk.Label(info_item, text=f"Preço Unit.: R$ {item['preco']:.2f}", font=('Arial', 10),
                    bg='#1a1a2e', fg='#aaaaaa', anchor='w').pack(fill=tk.X)
            
            tk.Label(item_frame, text=f"R$ {item['preco'] * item['quantidade']:.2f}", 
                    font=('Arial', 11, 'bold'), bg='#1a1a2e', fg='#e94560').pack(side=tk.RIGHT, padx=15, pady=10)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botão fechar
        tk.Button(detalhes_window, text="✖️ Fechar", font=('Arial', 11),
                 bg='#e74c3c', fg='white', padx=20, pady=10,
                 command=detalhes_window.destroy).pack(pady=20)

    def alterar_status_pedido(self):
        """Altera status do pedido selecionado"""
        if not hasattr(self, 'tree_pedidos'):
            return
            
        selection = self.tree_pedidos.selection()
        if not selection:
            messagebox.showwarning("Seleção", "Selecione um pedido para alterar status!")
            return
        
        item = self.tree_pedidos.item(selection[0])
        pedido_id = int(item['values'][0])
        pedido = next((p for p in self.pedidos if p['id'] == pedido_id), None)
        
        if not pedido:
            messagebox.showerror("Erro", "Pedido não encontrado!")
            return
        
        # Criar janela para alterar status
        status_window = tk.Toplevel(self.root)
        status_window.title(f"Alterar Status - Pedido #{pedido_id}")
        status_window.geometry("350x250")
        status_window.configure(bg='#16213e')
        status_window.transient(self.root)
        status_window.grab_set()
        
        # Centralizar janela
        status_window.update_idletasks()
        x = (status_window.winfo_screenwidth() // 2) - (350 // 2)
        y = (status_window.winfo_screenheight() // 2) - (250 // 2)
        status_window.geometry(f"350x250+{x}+{y}")
        
        tk.Label(status_window, text=f"🔄 Pedido #{pedido_id}", font=('Arial', 14, 'bold'),
                bg='#16213e', fg='#e94560').pack(pady=20)
        
        tk.Label(status_window, text=f"Status atual: {pedido['status'].title()}", font=('Arial', 11),
                bg='#16213e', fg='white').pack(pady=5)
        
        tk.Label(status_window, text="Selecione o novo status:", font=('Arial', 11),
                bg='#16213e', fg='white').pack(pady=10)
        
        # ComboBox para status
        status_var = tk.StringVar(value=pedido['status'])
        status_combo = ttk.Combobox(status_window, textvariable=status_var,
                                   values=['pendente', 'enviado', 'entregue', 'cancelado'],
                                   font=('Arial', 11), width=20, state='readonly')
        status_combo.pack(pady=10)
        
        def salvar_status():
            novo_status = status_var.get()
            if novo_status == pedido['status']:
                messagebox.showinfo("Info", "Status não foi alterado!")
                status_window.destroy()
                return
            
            pedido['status'] = novo_status
            messagebox.showinfo("Sucesso", f"Status do pedido #{pedido_id} alterado para: {novo_status.title()}")
            status_window.destroy()
            self.atualizar_tabela_pedidos()
        
        # Botões
        botoes_frame = tk.Frame(status_window, bg='#16213e')
        botoes_frame.pack(pady=20)
        
        tk.Button(botoes_frame, text="💾 Salvar", font=('Arial', 11, 'bold'),
                 bg='#2ecc71', fg='white', padx=20, pady=8,
                 command=salvar_status).pack(side=tk.LEFT, padx=10)
        
        tk.Button(botoes_frame, text="❌ Cancelar", font=('Arial', 11),
                 bg='#e74c3c', fg='white', padx=20, pady=8,
                 command=status_window.destroy).pack(side=tk.LEFT, padx=10)

    def limpar_tela(self):
        """Remove todos os widgets da tela"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def executar(self):
        """Executa o sistema"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n🛑 Sistema encerrado pelo usuário")
        except Exception as e:
            print(f"❌ Erro inesperado: {str(e)}")
        finally:
            print("👋 Obrigado por usar o GameStore Manager!")


# ========== EXECUÇÃO DO SISTEMA ==========
if __name__ == "__main__":
    try:
        print("=" * 50)
        print("🎮 GAMESTORE MANAGER - SISTEMA DE GESTÃO")
        print("=" * 50)
        print("📊 Sistema Completo para Loja de Videogames")
        print("🔧 Versão: 2.0 - Totalmente Funcional")
        print("")
        print("👤 CONTAS DE TESTE:")
        print("📋 Administrador:")
        print("   📧 E-mail: admin@gamestore.com")
        print("   🔑 Senha: admin123")
        print("")
        print("👥 Clientes:")
        print("   📧 E-mail: joao@email.com")
        print("   🔑 Senha: cliente123")
        print("")
        print("   📧 E-mail: maria@email.com")
        print("   🔑 Senha: cliente123")
        print("")
        print("🚀 Iniciando aplicação...")
        print("=" * 50)
        
        app = SistemaGestaoVideogames()
        app.executar()
        
    except Exception as e:
        print(f"❌ Erro crítico ao iniciar o sistema: {str(e)}")
        print("💡 Verifique se todas as dependências estão instaladas:")
        print("   - tkinter (geralmente incluído no Python)")
        print("   - hashlib (biblioteca padrão)")
        print("   - datetime (biblioteca padrão)")
        input("Pressione Enter para sair...")