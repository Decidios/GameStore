-- ============================================
-- SISTEMA DE GESTÃO PARA LOJA DE VIDEOGAMES
-- Banco de Dados MySQL Completo
-- ============================================

-- Criar banco de dados
DROP DATABASE IF EXISTS videogame_store;
CREATE DATABASE videogame_store CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE videogame_store;

-- ============================================
-- TABELA: CATEGORIAS
-- ============================================
CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: USUÁRIOS
-- ============================================
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    user_type ENUM('admin', 'customer') DEFAULT 'customer',
    phone VARCHAR(15),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_user_type (user_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: PRODUTOS
-- ============================================
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category_id INT,
    platform VARCHAR(50),
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    min_stock_alert INT DEFAULT 5,
    image_path VARCHAR(255),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    INDEX idx_category (category_id),
    INDEX idx_active (active),
    INDEX idx_price (price)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: VENDAS
-- ============================================
CREATE TABLE sales (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'completed',
    notes TEXT,
    FOREIGN KEY (customer_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_customer (customer_id),
    INDEX idx_sale_date (sale_date),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: ITENS DA VENDA
-- ============================================
CREATE TABLE sale_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sale_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT,
    INDEX idx_sale (sale_id),
    INDEX idx_product (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: CARRINHO DE COMPRAS
-- ============================================
CREATE TABLE cart_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_product (user_id, product_id),
    INDEX idx_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: MOVIMENTAÇÃO DE ESTOQUE
-- ============================================
CREATE TABLE inventory_movements (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    movement_type ENUM('in', 'out') NOT NULL,
    quantity INT NOT NULL,
    reference_id INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_product (product_id),
    INDEX idx_type (movement_type),
    INDEX idx_date (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- INSERIR DADOS: CATEGORIAS
-- ============================================
INSERT INTO categories (name, description) VALUES
('Consoles', 'Consoles de videogame de todas as gerações'),
('Jogos', 'Jogos para diversas plataformas'),
('Acessórios', 'Controles, fones de ouvido e outros acessórios'),
('Colecionáveis', 'Itens de coleção, action figures e memorabilia');

-- ============================================
-- INSERIR DADOS: USUÁRIOS
-- Senhas: admin123 (admin) e teste (teste)
-- Ambas criptografadas com SHA-256
-- ============================================
INSERT INTO users (username, password, email, full_name, user_type, phone, address) VALUES
('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin@gamestore.com', 'Administrador do Sistema', 'admin', '(11) 99999-9999', 'Rua da Administração, 100 - São Paulo, SP'),
('teste', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'teste@email.com', 'Usuário Teste', 'customer', '(11) 98888-8888', 'Rua do Teste, 200 - São Paulo, SP'),
('cliente1', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'joao@email.com', 'João Silva', 'customer', '(11) 97777-7777', 'Av. Paulista, 1000 - São Paulo, SP'),
('cliente2', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'maria@email.com', 'Maria Santos', 'customer', '(11) 96666-6666', 'Rua Augusta, 500 - São Paulo, SP'),
('cliente3', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'pedro@email.com', 'Pedro Costa', 'customer', '(11) 95555-5555', 'Rua Oscar Freire, 300 - São Paulo, SP'),
('cliente4', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'ana@email.com', 'Ana Oliveira', 'customer', '(11) 94444-4444', 'Av. Brigadeiro, 800 - São Paulo, SP');

-- ============================================
-- INSERIR DADOS: PRODUTOS
-- ============================================

-- CONSOLES
INSERT INTO products (name, description, category_id, platform, price, stock_quantity, min_stock_alert) VALUES
('PlayStation 5', 'Console de nova geração da Sony com SSD ultra-rápido de 825GB, gráficos em Ray Tracing e suporte a 4K/120fps', 1, 'PlayStation', 4999.00, 10, 3),
('PlayStation 5 Digital Edition', 'Versão totalmente digital do PS5, sem leitor de disco', 1, 'PlayStation', 4499.00, 8, 3),
('Xbox Series X', 'Console mais poderoso da Microsoft com 12 Teraflops, 1TB SSD e retrocompatibilidade', 1, 'Xbox', 4799.00, 12, 3),
('Xbox Series S', 'Console compacto e acessível da Microsoft, totalmente digital', 1, 'Xbox', 2799.00, 15, 5),
('Nintendo Switch OLED', 'Nova versão do Switch com tela OLED de 7 polegadas e melhor qualidade visual', 1, 'Nintendo', 2999.00, 20, 5),
('Nintendo Switch', 'Console híbrido que pode ser usado portátil ou conectado à TV', 1, 'Nintendo', 2499.00, 18, 5),
('PlayStation 4 Pro', 'Console PlayStation 4 com melhor desempenho e suporte a 4K', 1, 'PlayStation', 2199.00, 8, 3),
('Xbox One X', 'Console Xbox One mais potente com suporte a 4K nativo', 1, 'Xbox', 1999.00, 6, 2);

-- JOGOS PLAYSTATION
INSERT INTO products (name, description, category_id, platform, price, stock_quantity, min_stock_alert) VALUES
('The Last of Us Part II', 'Sequência aclamada pela crítica da saga de Ellie e Joel', 2, 'PlayStation', 199.90, 50, 10),
('God of War Ragnarök', 'Nova aventura épica de Kratos e Atreus na mitologia nórdica', 2, 'PlayStation', 279.90, 45, 12),
('Horizon Forbidden West', 'Continue a jornada de Aloy em um mundo pós-apocalíptico', 2, 'PlayStation', 249.90, 40, 10),
('Spider-Man Miles Morales', 'Assuma o papel de Miles Morales como o novo Homem-Aranha', 2, 'PlayStation', 219.90, 35, 10),
('Gran Turismo 7', 'O simulador de corrida definitivo para entusiastas', 2, 'PlayStation', 259.90, 30, 8),
('Demon''s Souls', 'Remake espetacular do clássico desafiador da FromSoftware', 2, 'PlayStation', 269.90, 25, 8),
('Ratchet & Clank: Rift Apart', 'Aventura intergaláctica com transições instantâneas entre dimensões', 2, 'PlayStation', 249.90, 28, 8);

-- JOGOS XBOX
INSERT INTO products (name, description, category_id, platform, price, stock_quantity, min_stock_alert) VALUES
('Halo Infinite', 'O retorno triunfal do Master Chief em uma nova aventura', 2, 'Xbox', 249.90, 35, 10),
('Forza Horizon 5', 'O melhor jogo de corrida arcade ambientado no México', 2, 'Xbox', 239.90, 40, 10),
('Gears 5', 'Continue a saga épica de guerra contra os Locusts', 2, 'Xbox', 189.90, 30, 8),
('Microsoft Flight Simulator', 'Simulador de voo ultra-realista que percorre o mundo todo', 2, 'Xbox', 279.90, 20, 6),
('Sea of Thieves', 'Aventura pirata multiplayer com seus amigos', 2, 'Xbox', 159.90, 25, 8);

-- JOGOS NINTENDO
INSERT INTO products (name, description, category_id, platform, price, stock_quantity, min_stock_alert) VALUES
('The Legend of Zelda: Tears of the Kingdom', 'Nova aventura épica de Link em Hyrule', 2, 'Nintendo', 329.90, 50, 15),
('Mario Kart 8 Deluxe', 'A melhor experiência de corrida com os personagens da Nintendo', 2, 'Nintendo', 299.90, 45, 12),
('Super Mario Odyssey', 'Aventura 3D do Mario em diversos reinos fantásticos', 2, 'Nintendo', 279.90, 40, 10),
('Animal Crossing: New Horizons', 'Crie sua ilha paradisíaca e relaxe com seus vizinhos animais', 2, 'Nintendo', 289.90, 38, 10),
('Super Smash Bros. Ultimate', 'O maior crossover de luta com personagens Nintendo e convidados', 2, 'Nintendo', 299.90, 35, 10),
('Splatoon 3', 'Batalhas de tinta frenéticas e coloridas', 2, 'Nintendo', 289.90, 30, 10),
('Pokémon Scarlet', 'Nova geração de Pokémon em mundo aberto', 2, 'Nintendo', 299.90, 42, 12);

-- JOGOS MULTIPLATAFORMA
INSERT INTO products (name, description, category_id, platform, price, stock_quantity, min_stock_alert) VALUES
('Elden Ring', 'RPG de ação desafiador dos criadores de Dark Souls', 2, 'Multi', 259.90, 48, 15),
('Hogwarts Legacy', 'Viva sua própria aventura no mundo de Harry Potter', 2, 'Multi', 279.90, 45, 12),
('FIFA 23', 'O simulador de futebol mais popular do mundo', 2, 'Multi', 249.90, 55, 15),
('Call of Duty: Modern Warfare II', 'FPS multiplayer intenso e campanha cinematográfica', 2, 'Multi', 299.90, 52, 15),
('Resident Evil 4 Remake', 'Remake do clássico jogo de survival horror', 2, 'Multi', 269.90, 38, 10);

-- ACESSÓRIOS PLAYSTATION
INSERT INTO products (name, description, category_id, platform, price, stock_quantity, min_stock_alert) VALUES
('Controle DualSense', 'Controle oficial do PlayStation 5 com feedback tátil', 3, 'PlayStation', 399.90, 30, 10),
('Controle DualSense Edge', 'Controle premium personalizável para jogadores competitivos', 3, 'PlayStation', 1299.90, 10, 3),
('Headset Pulse 3D', 'Fone de ouvido oficial com áudio 3D tempest', 3, 'PlayStation', 699.90, 20, 8),
('Câmera HD', 'Câmera para transmissões e reconhecimento facial', 3, 'PlayStation', 399.90, 15, 5),
('Controle Mídia Remoto', 'Controle remoto dedicado para streaming', 3, 'PlayStation', 199.90, 25, 8);

-- ACESSÓRIOS XBOX
INSERT INTO products (name, description, category_id, platform, price, stock_quantity, min_stock_alert) VALUES
('Controle Xbox Wireless', 'Controle oficial do Xbox Series X|S', 3, 'Xbox', 449.90, 35, 12),
('Controle Xbox Elite Series 2', 'Controle profissional com componentes intercambiáveis', 3, 'Xbox', 1499.90, 8, 3),
('Headset Xbox Wireless', 'Fone de ouvido oficial com áudio espacial', 3, 'Xbox', 799.90, 18, 6),
('Kit Play and Charge', 'Bateria recarregável e cabo USB-C', 3, 'Xbox', 249.90, 40, 15);

-- ACESSÓRIOS NINTENDO
INSERT INTO products (name, description, category_id, platform, price, stock_quantity, min_stock_alert) VALUES
('Joy-Con Pair', 'Par de controles Joy-Con em diversas cores', 3, 'Nintendo', 499.90, 25, 10),
('Pro Controller', 'Controle profissional para Nintendo Switch', 3, 'Nintendo', 449.90, 22, 8),
('Dock de Carregamento Joy-Con', 'Carregue até 4 Joy-Cons simultaneamente', 3, 'Nintendo', 179.90, 30, 10),
('Capa Protetora Switch', 'Case de proteção para transporte', 3, 'Nintendo', 89.90, 50, 20);

-- COLECIONÁVEIS
INSERT INTO products (name, description, category_id, platform, price, stock_quantity, min_stock_alert) VALUES
('Funko Pop! Master Chief', 'Boneco colecionável do protagonista de Halo', 4, 'Xbox', 89.90, 40, 15),
('Funko Pop! Kratos', 'Boneco colecionável do God of War', 4, 'PlayStation', 89.90, 38, 15),
('Funko Pop! Link', 'Boneco colecionável do herói de Zelda', 4, 'Nintendo', 89.90, 42, 15),
('Action Figure Ellie', 'Action figure articulado de The Last of Us', 4, 'PlayStation', 299.90, 15, 5),
('Réplica Master Sword', 'Réplica em metal da espada de Link', 4, 'Nintendo', 599.90, 8, 3),
('Camiseta PlayStation', 'Camiseta oficial com logo PlayStation', 4, 'PlayStation', 79.90, 60, 20),
('Camiseta Xbox', 'Camiseta oficial com logo Xbox', 4, 'Xbox', 79.90, 55, 20),
('Camiseta Nintendo', 'Camiseta oficial com logo Nintendo', 4, 'Nintendo', 79.90, 58, 20),
('Mousepad Gamer RGB', 'Mousepad grande com iluminação RGB', 4, 'Multi', 149.90, 45, 15),
('Cadeira Gamer Pro', 'Cadeira ergonômica para longas sessões de jogo', 4, 'Multi', 1299.90, 12, 4);

-- ============================================
-- INSERIR DADOS: VENDAS DE EXEMPLO
-- ============================================
INSERT INTO sales (customer_id, total_amount, payment_method, status, notes) VALUES
(3, 5498.80, 'credit_card', 'completed', 'Primeira compra do cliente - PlayStation 5 + jogo'),
(4, 2999.00, 'pix', 'completed', 'Nintendo Switch OLED'),
(5, 749.80, 'debit_card', 'completed', 'Jogos diversos'),
(6, 1899.70, 'credit_card', 'completed', 'Controle Elite + jogos');

-- ============================================
-- INSERIR DADOS: ITENS DAS VENDAS
-- ============================================
INSERT INTO sale_items (sale_id, product_id, quantity, unit_price) VALUES
-- Venda 1 (Cliente João)
(1, 1, 1, 4999.00),
(1, 10, 2, 249.90),
-- Venda 2 (Cliente Maria)
(2, 5, 1, 2999.00),
-- Venda 3 (Cliente Pedro)
(3, 20, 1, 249.90),
(3, 26, 2, 249.90),
-- Venda 4 (Cliente Ana)
(4, 38, 1, 1499.90),
(4, 17, 1, 199.90),
(4, 18, 1, 199.90);

-- ============================================
-- INSERIR DADOS: MOVIMENTAÇÕES DE ESTOQUE
-- ============================================
INSERT INTO inventory_movements (product_id, movement_type, quantity, reference_id, notes) VALUES
-- Entradas iniciais de estoque
(1, 'in', 15, NULL, 'Estoque inicial - PlayStation 5'),
(2, 'in', 12, NULL, 'Estoque inicial - PS5 Digital'),
(5, 'in', 25, NULL, 'Estoque inicial - Switch OLED'),
-- Saídas por vendas
(1, 'out', 1, 1, 'Venda #1 - PlayStation 5'),
(10, 'out', 2, 1, 'Venda #1 - God of War Ragnarök'),
(5, 'out', 1, 2, 'Venda #2 - Switch OLED'),
(20, 'out', 1, 3, 'Venda #3 - Mario Kart 8'),
(26, 'out', 2, 3, 'Venda #3 - Pokémon Scarlet'),
(38, 'out', 1, 4, 'Venda #4 - Controle Elite'),
(17, 'out', 1, 4, 'Venda #4 - Forza Horizon 5'),
(18, 'out', 1, 4, 'Venda #4 - Gears 5');

-- ============================================
-- CRIAR VIEWS ÚTEIS
-- ============================================

-- View: Produtos com estoque baixo
CREATE VIEW vw_low_stock_products AS
SELECT 
    p.id,
    p.name,
    c.name as category,
    p.stock_quantity,
    p.min_stock_alert,
    (p.min_stock_alert - p.stock_quantity) as difference
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
WHERE p.stock_quantity <= p.min_stock_alert AND p.active = TRUE
ORDER BY difference DESC;

-- View: Top produtos mais vendidos
CREATE VIEW vw_top_selling_products AS
SELECT 
    p.id,
    p.name,
    c.name as category,
    COALESCE(SUM(si.quantity), 0) as total_sold,
    COALESCE(SUM(si.quantity * si.unit_price), 0) as total_revenue
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN sale_items si ON p.id = si.product_id
GROUP BY p.id, p.name, c.name
ORDER BY total_sold DESC;

-- View: Resumo de vendas por cliente
CREATE VIEW vw_customer_sales_summary AS
SELECT 
    u.id,
    u.full_name,
    u.email,
    COUNT(s.id) as total_orders,
    COALESCE(SUM(s.total_amount), 0) as total_spent,
    MAX(s.sale_date) as last_purchase
FROM users u
LEFT JOIN sales s ON u.id = s.customer_id
WHERE u.user_type = 'customer'
GROUP BY u.id, u.full_name, u.email
ORDER BY total_spent DESC;

-- ============================================
-- CRIAR PROCEDURES ÚTEIS
-- ============================================

-- Procedure: Adicionar produto ao carrinho
DELIMITER $$
CREATE PROCEDURE sp_add_to_cart(
    IN p_user_id INT,
    IN p_product_id INT,
    IN p_quantity INT
)
BEGIN
    DECLARE v_existing_qty INT DEFAULT 0;
    
    -- Verificar se já existe no carrinho
    SELECT quantity INTO v_existing_qty
    FROM cart_items
    WHERE user_id = p_user_id AND product_id = p_product_id;
    
    IF v_existing_qty > 0 THEN
        -- Atualizar quantidade
        UPDATE cart_items
        SET quantity = quantity + p_quantity
        WHERE user_id = p_user_id AND product_id = p_product_id;
    ELSE
        -- Inserir novo item
        INSERT INTO cart_items (user_id, product_id, quantity)
        VALUES (p_user_id, p_product_id, p_quantity);
    END IF;
END$$
DELIMITER ;

-- Procedure: Processar venda
DELIMITER $$
CREATE PROCEDURE sp_process_sale(
    IN p_customer_id INT,
    IN p_payment_method VARCHAR(20),
    OUT p_sale_id INT
)
BEGIN
    DECLARE v_total DECIMAL(10,2) DEFAULT 0;
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_product_id INT;
    DECLARE v_quantity INT;
    DECLARE v_price DECIMAL(10,2);
    
    DECLARE cart_cursor CURSOR FOR
        SELECT ci.product_id, ci.quantity, p.price
        FROM cart_items ci
        JOIN products p ON ci.product_id = p.id
        WHERE ci.user_id = p_customer_id;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    -- Calcular total
    SELECT SUM(ci.quantity * p.price) INTO v_total
    FROM cart_items ci
    JOIN products p ON ci.product_id = p.id
    WHERE ci.user_id = p_customer_id;
    
    -- Criar venda
    INSERT INTO sales (customer_id, total_amount, payment_method, status)
    VALUES (p_customer_id, v_total, p_payment_method, 'completed');
    
    SET p_sale_id = LAST_INSERT_ID();
    
    -- Processar itens
    OPEN cart_cursor;
    
    read_loop: LOOP
        FETCH cart_cursor INTO v_product_id, v_quantity, v_price;
        
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Inserir item da venda
        INSERT INTO sale_items (sale_id, product_id, quantity, unit_price)
        VALUES (p_sale_id, v_product_id, v_quantity, v_price);
        
        -- Atualizar estoque
        UPDATE products
        SET stock_quantity = stock_quantity - v_quantity
        WHERE id = v_product_id;
        
        -- Registrar movimento
        INSERT INTO inventory_movements (product_id, movement_type, quantity, reference_id, notes)
        VALUES (v_product_id, 'out', v_quantity, p_sale_id, CONCAT('Venda #', p_sale_id));
    END LOOP;
    
    CLOSE cart_cursor;
    
    -- Limpar carrinho
    DELETE FROM cart_items WHERE user_id = p_customer_id;
END$$
DELIMITER ;

-- ============================================
-- TRIGGERS
-- ============================================

-- Trigger: Atualizar timestamp ao modificar produto
DELIMITER $$
CREATE TRIGGER trg_products_update
BEFORE UPDATE ON products
FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END$$
DELIMITER ;

-- Trigger: Validar quantidade mínima no estoque
DELIMITER $$
CREATE TRIGGER trg_validate_stock
BEFORE UPDATE ON products
FOR EACH ROW
BEGIN
    IF NEW.stock_quantity < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Quantidade em estoque não pode ser negativa';
    END IF;
END$$
DELIMITER ;

-- ============================================
-- ÍNDICES ADICIONAIS PARA PERFORMANCE
-- ============================================
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_sales_date_status ON sales(sale_date, status);

-- ============================================
-- ESTATÍSTICAS DO BANCO
-- ============================================
SELECT 'Banco de dados criado com sucesso!' as Status;
SELECT COUNT(*) as Total FROM users WHERE user_type = 'customer' UNION ALL
SELECT COUNT(*) FROM products WHERE active = TRUE UNION ALL
SELECT COUNT(*) FROM sales UNION ALL
SELECT COUNT(*) FROM categories;

-- ============================================
-- FIM DO SCRIPT
-- ============================================