import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import hashlib
import json
import os

class SistemaGestaoVideogames:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LogicFlow GameStore Manager")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        self.center_window()
        
        # Dados da sessão
        self.usuario_logado = None
        self.tipo_usuario = None
        self.usuario_id = None
        self.carrinho = []
        
        # Variáveis para filtros
        self.var_plataforma = None
        self.categoria_atual = None
        
        # Conectar ao banco de dados JSON
        self.conectar_db()
        self.mostrar_tela_boas_vindas()
    
    def conectar_db(self):
        """Conecta/Cria banco de dados JSON"""
        self.db_file = 'videogame_store.json'
        
        if not os.path.exists(self.db_file):
            # Criar banco inicial
            self.db = {
                'users': [
                    {
                        'id': 1,
                        'username': 'admin',
                        'password': self.hash_password('admin123'),
                        'full_name': 'Administrador',
                        'email': 'admin@logicflow.com',
                        'phone': '(11) 98765-4321',
                        'address': 'Rua Admin, 123',
                        'user_type': 'admin'
                    },
                    {
                        'id': 2,
                        'username': 'teste',
                        'password': self.hash_password('teste'),
                        'full_name': 'Cliente Teste',
                        'email': 'teste@email.com',
                        'phone': '(11) 91234-5678',
                        'address': 'Rua Cliente, 456',
                        'user_type': 'customer'
                    }
                ],
                'categories': [
                    {'id': 1, 'name': 'Jogos'},
                    {'id': 2, 'name': 'Consoles'},
                    {'id': 3, 'name': 'Acessórios'}
                ],
                'products': [
                    # Jogos
                    {'id': 1, 'name': 'The Last of Us Part II', 'description': 'Jogo de ação e aventura aclamado pela crítica', 'price': 199.90, 'category_id': 1, 'platform': 'PlayStation 4', 'stock_quantity': 15, 'min_stock_alert': 5, 'active': True},
                    {'id': 2, 'name': 'God of War Ragnarök', 'description': 'Continue a saga épica de Kratos e Atreus', 'price': 299.90, 'category_id': 1, 'platform': 'PlayStation 5', 'stock_quantity': 20, 'min_stock_alert': 5, 'active': True},
                    {'id': 3, 'name': 'Zelda: Tears of the Kingdom', 'description': 'Nova aventura em Hyrule', 'price': 349.90, 'category_id': 1, 'platform': 'Nintendo Switch', 'stock_quantity': 12, 'min_stock_alert': 5, 'active': True},
                    {'id': 4, 'name': 'FIFA 24', 'description': 'Simulador de futebol mais realista', 'price': 279.90, 'category_id': 1, 'platform': 'Xbox Series X', 'stock_quantity': 3, 'min_stock_alert': 5, 'active': True},
                    {'id': 5, 'name': 'Spider-Man 2', 'description': 'Seja Peter Parker e Miles Morales', 'price': 349.90, 'category_id': 1, 'platform': 'PlayStation 5', 'stock_quantity': 18, 'min_stock_alert': 5, 'active': True},
                    
                    # Consoles
                    {'id': 6, 'name': 'PlayStation 5', 'description': 'Console de última geração da Sony', 'price': 4199.00, 'category_id': 2, 'platform': None, 'stock_quantity': 8, 'min_stock_alert': 3, 'active': True},
                    {'id': 7, 'name': 'Xbox Series X', 'description': 'O console mais poderoso da Microsoft', 'price': 4499.00, 'category_id': 2, 'platform': None, 'stock_quantity': 5, 'min_stock_alert': 3, 'active': True},
                    {'id': 8, 'name': 'Nintendo Switch OLED', 'description': 'Versão com tela OLED melhorada', 'price': 2899.00, 'category_id': 2, 'platform': None, 'stock_quantity': 2, 'min_stock_alert': 3, 'active': True},
                    
                    # Acessórios
                    {'id': 9, 'name': 'Controle DualSense', 'description': 'Controle sem fio para PS5', 'price': 499.90, 'category_id': 3, 'platform': 'PlayStation 5', 'stock_quantity': 25, 'min_stock_alert': 10, 'active': True},
                    {'id': 10, 'name': 'Headset Gamer Pro', 'description': 'Fone com som surround 7.1', 'price': 399.90, 'category_id': 3, 'platform': None, 'stock_quantity': 15, 'min_stock_alert': 5, 'active': True},
                    {'id': 11, 'name': 'Cabo HDMI 2.1', 'description': 'Cabo HDMI para 4K 120Hz', 'price': 89.90, 'category_id': 3, 'platform': None, 'stock_quantity': 30, 'min_stock_alert': 10, 'active': True}
                ],
                'sales': [],
                'sale_items': []
            }
            self.salvar_db()
            print("✅ Banco de dados JSON criado!")
        else:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                self.db = json.load(f)
            print("✅ Conectado ao banco de dados JSON!")
    
    def salvar_db(self):
        """Salva dados no arquivo JSON"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, ensure_ascii=False, indent=2)
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def hash_password(self, password):
        """Cria hash SHA-256 da senha"""
        return hashlib.sha256(password.encode()).hexdigest()

    def mostrar_tela_boas_vindas(self):
        """Tela de Boas-Vindas com logo LogicFlow"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        logo_frame = tk.Frame(main_frame, bg='#1a1a2e')
        logo_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        logo_label = tk.Label(logo_frame, text="✚", font=('Arial', 80), bg='#1a1a2e', fg='#e94560')
        logo_label.pack(pady=20)
        
        titulo = tk.Label(logo_frame, text="LogicFlow", font=('Arial', 42, 'bold'), 
                         bg='#1a1a2e', fg='#ffffff')
        titulo.pack(pady=5)
        
        subtitulo = tk.Label(logo_frame, text="GameStore Manager", font=('Arial', 24), 
                           bg='#1a1a2e', fg='#e94560')
        subtitulo.pack(pady=5)
        
        descricao = tk.Label(logo_frame, text="Sistema de Gestão para Loja de Videogames", 
                           font=('Arial', 14), bg='#1a1a2e', fg='#aaaaaa')
        descricao.pack(pady=10)
        
        btn_entrar = tk.Button(logo_frame, text="ENTRAR NO SISTEMA", font=('Arial', 14, 'bold'),
                              bg='#e94560', fg='white', padx=30, pady=15,
                              command=self.mostrar_tela_login)
        btn_entrar.pack(pady=40)
        
        rodape = tk.Label(main_frame, text="© 2024 LogicFlow GameStore Manager - Powered by JSON",
                         font=('Arial', 10), bg='#1a1a2e', fg='#666666')
        rodape.pack(side=tk.BOTTOM, pady=20)

    def mostrar_tela_login(self):
        """Tela de Login"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#16213e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        login_container = tk.Frame(main_frame, bg='#16213e')
        login_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        notebook = ttk.Notebook(login_container)
        notebook.pack(padx=20, pady=20)
        
        login_frame = ttk.Frame(notebook, width=400, height=400)
        notebook.add(login_frame, text="Login")
        
        login_content = tk.Frame(login_frame, bg='#0f3460')
        login_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(login_content, text="✚", font=('Arial', 50), bg='#0f3460', fg='#e94560').pack(pady=20)
        tk.Label(login_content, text="Login", font=('Arial', 24, 'bold'), bg='#0f3460', fg='white').pack(pady=10)
        
        campos_frame = tk.Frame(login_content, bg='#0f3460')
        campos_frame.pack(pady=30, fill=tk.X)
        
        tk.Label(campos_frame, text="Usuário:", font=('Arial', 12), bg='#0f3460', fg='white').pack(anchor='w')
        self.login_usuario = tk.Entry(campos_frame, font=('Arial', 12), bg='#1a1a2e', fg='white', width=30)
        self.login_usuario.pack(fill=tk.X, pady=5, ipady=5)
        self.login_usuario.insert(0, "admin")
        
        tk.Label(campos_frame, text="Senha:", font=('Arial', 12), bg='#0f3460', fg='white').pack(anchor='w', pady=(10,0))
        self.login_senha = tk.Entry(campos_frame, font=('Arial', 12), show='*', bg='#1a1a2e', fg='white', width=30)
        self.login_senha.pack(fill=tk.X, pady=5, ipady=5)
        self.login_senha.insert(0, "admin123")
        
        botoes_frame = tk.Frame(login_content, bg='#0f3460')
        botoes_frame.pack(pady=20)
        
        btn_login = tk.Button(botoes_frame, text="Entrar", font=('Arial', 12, 'bold'),
                             bg='#e94560', fg='white', padx=30, pady=10,
                             command=self.fazer_login)
        btn_login.pack(fill=tk.X, pady=5)
        
        login_frame.pack_propagate(False)
        
        self.root.bind('<Return>', lambda event: self.fazer_login())

    def fazer_login(self):
        """Autentica o usuário"""
        usuario = self.login_usuario.get().strip()
        senha = self.login_senha.get().strip()
        
        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        senha_hash = self.hash_password(senha)
        
        user = next((u for u in self.db['users'] if u['username'] == usuario and u['password'] == senha_hash), None)
        
        if user:
            self.usuario_logado = user['full_name']
            self.tipo_usuario = user['user_type']
            self.usuario_id = user['id']
            
            if user['user_type'] == 'admin':
                self.mostrar_painel_administrador()
            else:
                self.mostrar_painel_cliente()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

    def mostrar_painel_cliente(self):
        """Painel do Cliente"""
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
            ("🎮 Jogos", "Ver catálogo de jogos", lambda: self.mostrar_catalogo_categoria('Jogos')),
            ("📺 Consoles", "Ver catálogo de consoles", lambda: self.mostrar_catalogo_categoria('Consoles')),
            ("🎧 Acessórios", "Ver acessórios disponíveis", lambda: self.mostrar_catalogo_categoria('Acessórios')),
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

    def mostrar_catalogo_categoria(self, categoria):
        """Mostra produtos de uma categoria específica"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"🛍️ {categoria}", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="← Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_cliente)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        produtos_frame = tk.Frame(main_frame, bg='#1a1a2e')
        produtos_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        canvas = tk.Canvas(produtos_frame, bg='#1a1a2e')
        scrollbar = ttk.Scrollbar(produtos_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a1a2e')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Buscar categoria
        cat = next((c for c in self.db['categories'] if c['name'] == categoria), None)
        if not cat:
            return
        
        produtos = [p for p in self.db['products'] if p['category_id'] == cat['id'] and p['active']]
        
        if not produtos:
            tk.Label(scrollable_frame, text="Nenhum produto encontrado", 
                    font=('Arial', 14), bg='#1a1a2e', fg='white').pack(pady=50)
        else:
            for produto in produtos:
                card = tk.Frame(scrollable_frame, bg='#16213e', relief=tk.RAISED, bd=1)
                card.pack(fill=tk.X, pady=5, padx=10)
                
                emoji = "🎮" if produto['platform'] else "📦"
                img_label = tk.Label(card, text=emoji, font=('Arial', 24), bg='#16213e', fg='#e94560')
                img_label.pack(side=tk.LEFT, padx=15, pady=15)
                
                info_frame = tk.Frame(card, bg='#16213e')
                info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
                
                tk.Label(info_frame, text=produto['name'], font=('Arial', 12, 'bold'),
                        bg='#16213e', fg='white', anchor='w').pack(fill=tk.X)
                tk.Label(info_frame, text=produto['description'][:100] + "...", font=('Arial', 9),
                        bg='#16213e', fg='#aaaaaa', anchor='w').pack(fill=tk.X)
                tk.Label(info_frame, text=f"R$ {produto['price']:.2f}", font=('Arial', 14, 'bold'),
                        bg='#16213e', fg='#e94560', anchor='w').pack(fill=tk.X)
                tk.Label(info_frame, text=f"Plataforma: {produto['platform'] or 'Universal'} | Estoque: {produto['stock_quantity']}", 
                        font=('Arial', 9), bg='#16213e', fg='#aaaaaa', anchor='w').pack(fill=tk.X)
                
                if produto['stock_quantity'] > 0:
                    btn_add = tk.Button(card, text="🛒 Adicionar", font=('Arial', 10),
                                      bg='#e94560', fg='white', padx=15,
                                      command=lambda p=produto: self.adicionar_carrinho(p))
                    btn_add.pack(side=tk.RIGHT, padx=10, pady=10)
                else:
                    tk.Label(card, text="SEM ESTOQUE", font=('Arial', 10, 'bold'),
                            bg='#e74c3c', fg='white', padx=15, pady=5).pack(side=tk.RIGHT, padx=10, pady=10)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def adicionar_carrinho(self, produto):
        """Adiciona produto ao carrinho"""
        if any(item['id'] == produto['id'] for item in self.carrinho):
            messagebox.showinfo("Carrinho", f"{produto['name']} já está no carrinho!")
            return
        
        self.carrinho.append(produto)
        messagebox.showinfo("Sucesso", f"✅ {produto['name']} adicionado ao carrinho!")

    def mostrar_carrinho(self):
        """Exibe o carrinho de compras"""
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
            return
        
        itens_frame = tk.Frame(content_frame, bg='#1a1a2e')
        itens_frame.pack(fill=tk.BOTH, expand=True)
        
        total = sum(item['price'] for item in self.carrinho)
        
        for i, item in enumerate(self.carrinho):
            item_frame = tk.Frame(itens_frame, bg='#16213e', relief=tk.RAISED, bd=1)
            item_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(item_frame, text="🎮", font=('Arial', 20), 
                    bg='#16213e', fg='#e94560').pack(side=tk.LEFT, padx=15, pady=10)
            
            info_frame = tk.Frame(item_frame, bg='#16213e')
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
            
            tk.Label(info_frame, text=item['name'], font=('Arial', 11, 'bold'),
                    bg='#16213e', fg='white').pack(anchor='w')
            tk.Label(info_frame, text=f"R$ {item['price']:.2f}", font=('Arial', 11),
                    bg='#16213e', fg='#e94560').pack(anchor='w')
            
            btn_remover = tk.Button(item_frame, text="❌ Remover", font=('Arial', 9),
                                  bg='#e94560', fg='white',
                                  command=lambda idx=i: self.remover_carrinho(idx))
            btn_remover.pack(side=tk.RIGHT, padx=10, pady=10)
        
        total_frame = tk.Frame(content_frame, bg='#16213e', relief=tk.RAISED, bd=2)
        total_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(total_frame, text=f"💰 Total: R$ {total:.2f}", 
                font=('Arial', 16, 'bold'), bg='#16213e', fg='#e94560').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_finalizar = tk.Button(total_frame, text="✅ Finalizar Compra", font=('Arial', 12, 'bold'),
                                 bg='#2ecc71', fg='white', padx=30, pady=10,
                                 command=self.finalizar_compra)
        btn_finalizar.pack(side=tk.RIGHT, padx=20, pady=10)

    def remover_carrinho(self, index):
        """Remove item do carrinho"""
        if 0 <= index < len(self.carrinho):
            self.carrinho.pop(index)
            self.mostrar_carrinho()

    def finalizar_compra(self):
        """Finaliza a compra"""
        if not self.carrinho:
            return
        
        total = sum(item['price'] for item in self.carrinho)
        
        # Criar venda
        sale_id = max([s['id'] for s in self.db['sales']], default=0) + 1
        venda = {
            'id': sale_id,
            'customer_id': self.usuario_id,
            'sale_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_amount': total,
            'payment_method': 'credit_card',
            'status': 'completed'
        }
        self.db['sales'].append(venda)
        
        # Criar itens da venda
        for item in self.carrinho:
            item_id = max([si['id'] for si in self.db['sale_items']], default=0) + 1
            sale_item = {
                'id': item_id,
                'sale_id': sale_id,
                'product_id': item['id'],
                'quantity': 1,
                'unit_price': item['price'],
                'subtotal': item['price']
            }
            self.db['sale_items'].append(sale_item)
            
            # Atualizar estoque
            for produto in self.db['products']:
                if produto['id'] == item['id']:
                    produto['stock_quantity'] -= 1
                    break
        
        self.salvar_db()
        messagebox.showinfo("Sucesso", f"Compra finalizada!\nTotal: R$ {total:.2f}")
        
        self.carrinho.clear()
        self.mostrar_painel_cliente()

    def mostrar_historico_pedidos(self):
        """Mostra histórico de pedidos do cliente"""
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
        
        pedidos = [s for s in self.db['sales'] if s['customer_id'] == self.usuario_id]
        pedidos.sort(key=lambda x: x['sale_date'], reverse=True)
        
        if not pedidos:
            empty_frame = tk.Frame(content_frame, bg='#1a1a2e')
            empty_frame.pack(expand=True)
            tk.Label(empty_frame, text="📦", font=('Arial', 80), bg='#1a1a2e', fg='#666666').pack(pady=20)
            tk.Label(empty_frame, text="Nenhum pedido realizado", font=('Arial', 16), 
                    bg='#1a1a2e', fg='white').pack()
            return
        
        for pedido in pedidos:
            item_count = len([si for si in self.db['sale_items'] if si['sale_id'] == pedido['id']])
            
            card = tk.Frame(content_frame, bg='#16213e', relief=tk.RAISED, bd=1)
            card.pack(fill=tk.X, pady=10)
            
            header_pedido = tk.Frame(card, bg='#0f3460')
            header_pedido.pack(fill=tk.X)
            
            tk.Label(header_pedido, text=f"Pedido #{pedido['id']}", font=('Arial', 12, 'bold'),
                    bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=15, pady=10)
            
            tk.Label(header_pedido, text=pedido['status'].upper(), font=('Arial', 10, 'bold'),
                    bg='#2ecc71', fg='white', padx=10, pady=5).pack(side=tk.RIGHT, padx=15, pady=10)
            
            info_frame = tk.Frame(card, bg='#16213e')
            info_frame.pack(fill=tk.X, padx=15, pady=10)
            
            tk.Label(info_frame, text=f"Data: {pedido['sale_date']}", font=('Arial', 10),
                    bg='#16213e', fg='#aaaaaa').pack(anchor='w')
            tk.Label(info_frame, text=f"Itens: {item_count}", font=('Arial', 10),
                    bg='#16213e', fg='white').pack(anchor='w', pady=5)
            tk.Label(info_frame, text=f"Total: R$ {pedido['total_amount']:.2f}", font=('Arial', 12, 'bold'),
                    bg='#16213e', fg='#e94560').pack(anchor='w')

    def mostrar_meus_dados(self):
        """Mostra dados do usuário"""
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
        
        usuario = next((u for u in self.db['users'] if u['id'] == self.usuario_id), None)
        
        if usuario:
            dados_frame = tk.Frame(content_frame, bg='#16213e', relief=tk.RAISED, bd=2)
            dados_frame.pack(fill=tk.X, padx=50, pady=20)
            
            tk.Label(dados_frame, text="👤", font=('Arial', 50), bg='#16213e', fg='#e94560').pack(pady=20)
            
            dados = [
                ("Nome:", usuario['full_name']),
                ("Usuário:", usuario['username']),
                ("E-mail:", usuario['email']),
                ("Telefone:", usuario['phone'] or "Não informado"),
                ("Endereço:", usuario['address'] or "Não informado")
            ]
            
            for campo, valor in dados:
                linha = tk.Frame(dados_frame, bg='#16213e')
                linha.pack(fill=tk.X, padx=30, pady=15)
                
                tk.Label(linha, text=campo, font=('Arial', 12, 'bold'), 
                        bg='#16213e', fg='#e94560', width=12, anchor='w').pack(side=tk.LEFT)
                tk.Label(linha, text=valor, font=('Arial', 12), 
                        bg='#16213e', fg='white', anchor='w').pack(side=tk.LEFT)

    def mostrar_painel_administrador(self):
        """Painel Administrativo"""
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
            ("📦 Produtos", "Gerenciar produtos", self.mostrar_produtos_admin),
            ("📊 Vendas", "Visualizar vendas", self.mostrar_vendas_admin),
            ("👥 Clientes", "Ver clientes", self.mostrar_clientes_admin),
            ("📈 Relatórios", "Dashboard e estatísticas", self.mostrar_dashboard),
            ("⚠️ Estoque Baixo", "Produtos críticos", self.mostrar_estoque_baixo),
            ("🏆 Top Vendas", "Produtos mais vendidos", self.mostrar_top_produtos)
        ]
        
        for i, (titulo, descricao, comando) in enumerate(funcionalidades):
            card = tk.Frame(content_frame, bg='#16213e', relief=tk.RAISED, bd=1)
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky='nsew')
            
            emoji = titulo.split()[0]
            texto = titulo[len(emoji):].strip()
            
            tk.Label(card, text=emoji, font=('Arial', 30), bg='#16213e', fg='#e94560').pack(pady=20)
            tk.Label(card, text=texto, font=('Arial', 12, 'bold'), bg='#16213e', fg='white').pack(pady=5)
            tk.Label(card, text=descricao, font=('Arial', 10), bg='#16213e', fg='#aaaaaa').pack(pady=10)
            
            btn = tk.Button(card, text="Acessar", font=('Arial', 10),
                          bg='#e94560', fg='white', command=comando)
            btn.pack(pady=10)
        
        for i in range(2):
            content_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            content_frame.grid_columnconfigure(i, weight=1)

    def mostrar_produtos_admin(self):
        """Lista produtos para admin"""
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
        
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        produtos = [p for p in self.db['products'] if p['active']]
        
        columns = ('ID', 'Nome', 'Categoria', 'Plataforma', 'Preço', 'Estoque')
        tree = ttk.Treeview(content_frame, columns=columns, show='headings', height=20)
        
        widths = {'ID': 50, 'Nome': 300, 'Categoria': 120, 'Plataforma': 100, 'Preço': 100, 'Estoque': 80}
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=widths.get(col, 100))
        
        for produto in produtos:
            cat = next((c['name'] for c in self.db['categories'] if c['id'] == produto['category_id']), 'N/A')
            tree.insert('', tk.END, values=(
                produto['id'],
                produto['name'],
                cat,
                produto['platform'] or 'Universal',
                f"R$ {produto['price']:.2f}",
                produto['stock_quantity']
            ))
        
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def mostrar_vendas_admin(self):
        """Lista vendas para admin"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📊 Vendas Realizadas", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="← Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_administrador)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        vendas = sorted(self.db['sales'], key=lambda x: x['sale_date'], reverse=True)
        
        columns = ('ID', 'Cliente', 'Data', 'Total', 'Pagamento', 'Status')
        tree = ttk.Treeview(content_frame, columns=columns, show='headings', height=20)
        
        widths = {'ID': 50, 'Cliente': 250, 'Data': 150, 'Total': 120, 'Pagamento': 120, 'Status': 100}
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=widths.get(col, 100))
        
        for venda in vendas:
            cliente = next((u['full_name'] for u in self.db['users'] if u['id'] == venda['customer_id']), 'N/A')
            tree.insert('', tk.END, values=(
                venda['id'],
                cliente,
                venda['sale_date'],
                f"R$ {venda['total_amount']:.2f}",
                venda['payment_method'],
                venda['status']
            ))
        
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def mostrar_clientes_admin(self):
        """Mostra clientes"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="👥 Clientes", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="← Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_administrador)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        clientes = [u for u in self.db['users'] if u['user_type'] == 'customer']
        
        # Calcular estatísticas
        clientes_stats = []
        for cliente in clientes:
            vendas_cliente = [v for v in self.db['sales'] if v['customer_id'] == cliente['id']]
            total_pedidos = len(vendas_cliente)
            total_gasto = sum(v['total_amount'] for v in vendas_cliente)
            ultima_compra = max([v['sale_date'] for v in vendas_cliente], default='Nunca')
            
            clientes_stats.append({
                'id': cliente['id'],
                'nome': cliente['full_name'],
                'email': cliente['email'],
                'pedidos': total_pedidos,
                'total': total_gasto,
                'ultima': ultima_compra
            })
        
        clientes_stats.sort(key=lambda x: x['total'], reverse=True)
        
        columns = ('ID', 'Nome', 'Email', 'Pedidos', 'Total Gasto', 'Última Compra')
        tree = ttk.Treeview(content_frame, columns=columns, show='headings', height=20)
        
        widths = {'ID': 50, 'Nome': 250, 'Email': 250, 'Pedidos': 80, 'Total Gasto': 120, 'Última Compra': 150}
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=widths.get(col, 100))
        
        for cliente in clientes_stats:
            tree.insert('', tk.END, values=(
                cliente['id'],
                cliente['nome'],
                cliente['email'],
                cliente['pedidos'],
                f"R$ {cliente['total']:.2f}",
                cliente['ultima']
            ))
        
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def mostrar_estoque_baixo(self):
        """Mostra produtos com estoque baixo"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="⚠️ Produtos com Estoque Baixo", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="← Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_administrador)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        produtos_baixo = [p for p in self.db['products'] if p['active'] and p['stock_quantity'] <= p['min_stock_alert']]
        
        if not produtos_baixo:
            tk.Label(content_frame, text="✅ Todos os produtos estão com estoque adequado!", 
                    font=('Arial', 16, 'bold'), bg='#1a1a2e', fg='#2ecc71').pack(expand=True)
            return
        
        columns = ('ID', 'Nome', 'Categoria', 'Estoque Atual', 'Mínimo', 'Diferença')
        tree = ttk.Treeview(content_frame, columns=columns, show='headings', height=20)
        
        widths = {'ID': 50, 'Nome': 300, 'Categoria': 120, 'Estoque Atual': 120, 'Mínimo': 100, 'Diferença': 100}
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=widths.get(col, 100))
        
        for produto in produtos_baixo:
            cat = next((c['name'] for c in self.db['categories'] if c['id'] == produto['category_id']), 'N/A')
            diferenca = produto['min_stock_alert'] - produto['stock_quantity']
            tree.insert('', tk.END, values=(
                produto['id'],
                produto['name'],
                cat,
                produto['stock_quantity'],
                produto['min_stock_alert'],
                diferenca
            ))
        
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def mostrar_top_produtos(self):
        """Mostra produtos mais vendidos"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🏆 Produtos Mais Vendidos", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="← Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_administrador)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Calcular vendas por produto
        vendas_por_produto = {}
        for item in self.db['sale_items']:
            pid = item['product_id']
            if pid not in vendas_por_produto:
                vendas_por_produto[pid] = {'quantidade': 0, 'receita': 0}
            vendas_por_produto[pid]['quantidade'] += item['quantity']
            vendas_por_produto[pid]['receita'] += item['subtotal']
        
        # Criar lista com detalhes
        top_produtos = []
        for pid, stats in vendas_por_produto.items():
            produto = next((p for p in self.db['products'] if p['id'] == pid), None)
            if produto:
                cat = next((c['name'] for c in self.db['categories'] if c['id'] == produto['category_id']), 'N/A')
                top_produtos.append({
                    'nome': produto['name'],
                    'categoria': cat,
                    'quantidade': stats['quantidade'],
                    'receita': stats['receita']
                })
        
        top_produtos.sort(key=lambda x: x['quantidade'], reverse=True)
        top_produtos = top_produtos[:20]
        
        columns = ('Posição', 'Nome', 'Categoria', 'Qtd. Vendida', 'Receita Total')
        tree = ttk.Treeview(content_frame, columns=columns, show='headings', height=20)
        
        widths = {'Posição': 80, 'Nome': 350, 'Categoria': 120, 'Qtd. Vendida': 120, 'Receita Total': 150}
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=widths.get(col, 100))
        
        for i, produto in enumerate(top_produtos, 1):
            tree.insert('', tk.END, values=(
                f"#{i}",
                produto['nome'],
                produto['categoria'],
                produto['quantidade'],
                f"R$ {produto['receita']:.2f}"
            ))
        
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def mostrar_dashboard(self):
        """Dashboard com estatísticas"""
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#0f3460', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📈 Dashboard", 
                font=('Arial', 16, 'bold'), bg='#0f3460', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_voltar = tk.Button(header_frame, text="← Voltar", font=('Arial', 10),
                              bg='#e94560', fg='white', command=self.mostrar_painel_administrador)
        btn_voltar.pack(side=tk.RIGHT, padx=20, pady=15)
        
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Estatísticas gerais
        total_clientes = len([u for u in self.db['users'] if u['user_type'] == 'customer'])
        total_produtos = len([p for p in self.db['products'] if p['active']])
        total_vendas = len(self.db['sales'])
        receita_total = sum(v['total_amount'] for v in self.db['sales'])
        estoque_baixo = len([p for p in self.db['products'] if p['active'] and p['stock_quantity'] <= p['min_stock_alert']])
        
        # Grid de KPIs
        kpis_frame = tk.Frame(content_frame, bg='#1a1a2e')
        kpis_frame.pack(fill=tk.X, pady=20)
        
        kpis = [
            ("👥", "Clientes", str(total_clientes), "#3498db"),
            ("📦", "Produtos", str(total_produtos), "#2ecc71"),
            ("💰", "Vendas", str(total_vendas), "#f39c12"),
            ("⚠️", "Estoque Baixo", str(estoque_baixo), "#e74c3c")
        ]
        
        for i, (emoji, titulo, valor, cor) in enumerate(kpis):
            kpi_card = tk.Frame(kpis_frame, bg=cor, relief=tk.RAISED, bd=2)
            kpi_card.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
            
            tk.Label(kpi_card, text=emoji, font=('Arial', 30), bg=cor, fg='white').pack(pady=15)
            tk.Label(kpi_card, text=valor, font=('Arial', 24, 'bold'), bg=cor, fg='white').pack()
            tk.Label(kpi_card, text=titulo, font=('Arial', 12), bg=cor, fg='white').pack(pady=10)
        
        for i in range(4):
            kpis_frame.grid_columnconfigure(i, weight=1)
        
        # Receita total
        receita_frame = tk.Frame(content_frame, bg='#16213e', relief=tk.RAISED, bd=2)
        receita_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(receita_frame, text=f"💵 Receita Total: R$ {receita_total:.2f}", 
                font=('Arial', 20, 'bold'), bg='#16213e', fg='#2ecc71').pack(pady=30)

    def logout(self):
        """Faz logout"""
        self.usuario_logado = None
        self.tipo_usuario = None
        self.usuario_id = None
        self.carrinho.clear()
        self.mostrar_tela_login()

    def limpar_tela(self):
        """Remove todos os widgets"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def executar(self):
        """Executa o sistema"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n🛑 Sistema encerrado")
        finally:
            self.salvar_db()
            print("✅ Dados salvos no arquivo JSON")


if __name__ == "__main__":
    print("=" * 60)
    print("✚ LOGICFLOW GAMESTORE MANAGER")
    print("=" * 60)
    print("📊 Sistema com Banco de Dados JSON")
    print("")
    print("🔐 CONTAS DE TESTE:")
    print("   Admin: admin / admin123")
    print("   Cliente: teste / teste")
    print("")
    print("💾 Dados serão salvos em: videogame_store.json")
    print("")
    print("🚀 Iniciando aplicação...")
    print("=" * 60)
    
    app = SistemaGestaoVideogames()
    app.executar()