# Geração de Datasets de Teste

## Propósito
Gerar datasets realistas para testes com colunas customizáveis, restrições e múltiplos formatos de saída (CSV, JSON, SQL, Python script). Cria scripts executáveis ou arquivos diretos para uso imediato em desenvolvimento e testes.

## Como Funciona
O processo identifica o tipo de dataset, define especificações de colunas, determina número de linhas, seleciona formato de saída, aplica padrões realistas, adiciona restrições de negócio, gera dados ou scripts, e valida a qualidade e completude dos dados.

## Quando Usar
- Desenvolvimento de novas funcionalidades
- Testes de performance e carga
- Criação de protótipos e demos
- População de ambientes de teste
- Validação de schemas e estruturas
- Treinamento de modelos de machine learning

## Passo a Passo

### 1. Identificação do Tipo de Dataset
**Domínios Comuns:**
- Customer feedback (feedback de clientes)
- Transactions (transações financeiras)
- User profiles (perfis de usuários)
- Product catalog (catálogo de produtos)
- Analytics events (eventos de analytics)
- Support tickets (tickets de suporte)

### 2. Definição de Colunas
**Especificações por Coluna:**
- Nome e tipo de dados
- Gerador de valores (email, nome, timestamp)
- Restrições e validações
- Relacionamentos com outras colunas

**Geradores Disponíveis:**
- `auto-increment`: IDs sequenciais
- `first_last_name`: Nomes realistas
- `email`: Emails válidos
- `timestamp`: Datas e horas
- `phone`: Telefones formatados
- `address`: Endereços completos
- `company`: Nomes de empresas
- `price`: Valores monetários
- `rating`: Avaliações numéricas

### 3. Determinação do Volume
**Considerações:**
- Necessidades do teste (unitário vs integração)
- Performance do sistema
- Requisitos de storage
- Tempo de geração

**Volumes Comuns:**
- Testes unitários: 10-100 linhas
- Testes de API: 100-1,000 linhas
- Performance: 10,000-100,000 linhas
- Carga/stress: 1M+ linhas

### 4. Seleção do Formato de Saída
**CSV:** Tabular, fácil importação
**JSON:** Estruturado, ideal para APIs
**SQL:** INSERT statements, para bancos
**Python Script:** Gerador customizável

### 5. Aplicação de Padrões Realistas
**Distribuições Realistas:**
- Ratings: 40% 5-star, 30% 4-star, 20% 3-star, 10% 1-2 star
- Preços: Distribuição normal com outliers
- Datas: Concentração em períodos recentes
- Categorias: Proporções de mercado realistas

### 6. Restrições de Negócio
**Exemplos:**
- Bug category apenas com ratings 1-3
- Feature requests apenas com ratings 3-5
- Emails com domínios realistas
- IDs únicos e consistentes

## Exemplos Práticos

### Exemplo 1: Customer Feedback Dataset
**Configuração:**
- Produto: SaaS de gestão de projetos
- Tipo: Customer feedback
- Linhas: 500
- Formato: CSV

**Especificação:**
```python
columns = {
    "feedback_id": "auto-increment",
    "customer_name": "first_last_name",
    "email": "email",
    "feedback_date": "timestamp_last_90_days",
    "rating": "rating_1_to_5_weighted",
    "category": "category_business_rules",
    "feedback_text": "realistic_feedback_text",
    "product_area": "product_modules"
}

constraints = {
    "rating_distribution": {"5": 40, "4": 30, "3": 20, "2": 7, "1": 3},
    "category_rating_rules": {
        "Bug": [1, 2, 3],
        "Feature Request": [3, 4, 5],
        "Complaint": [1, 2, 3],
        "Praise": [4, 5]
    },
    "email_domains": ["gmail.com", "yahoo.com", "outlook.com", "company.com"]
}
```

**Resultado CSV:**
```csv
feedback_id,customer_name,email,feedback_date,rating,category,feedback_text,product_area
F001,John Smith,john.smith@gmail.com,2025-02-15,4,Feature Request,"Would love to see Gantt chart integration",Timeline
F002,Maria Johnson,maria.j@company.com,2025-02-14,2,Bug,"Dashboard crashes when loading large projects",Dashboard
F003,David Wilson,david.w@yahoo.com,2025-02-13,5,Praise,"Best project management tool we've used!",General
```

### Exemplo 2: Python Script Generator
**Dataset:** E-commerce transactions
**Formato:** Python script executável

```python
import csv
import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('pt_BR')

# Configuration
ROWS = 1000
FILENAME = "transactions.csv"

# Product catalog
products = [
    {"id": "P001", "name": "Notebook Pro", "price": 4500.00, "category": "Electronics"},
    {"id": "P002", "name": "Mouse Wireless", "price": 89.90, "category": "Accessories"},
    {"id": "P003", "name": "Keyboard Mechanical", "price": 299.90, "category": "Accessories"},
    {"id": "P004", "name": "Monitor 27\"", "price": 1200.00, "category": "Electronics"},
    {"id": "P005", "name": "Webcam HD", "price": 199.90, "category": "Electronics"}
]

def generate_transaction_id():
    """Generate unique transaction ID"""
    return f"TXN{random.randint(100000, 999999)}"

def generate_customer():
    """Generate realistic customer data"""
    return {
        "id": f"CUST{random.randint(1000, 9999)}",
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "address": fake.address().replace('\n', ', ')
    }

def generate_transaction():
    """Generate single transaction with business rules"""
    transaction = generate_transaction_id()
    customer = generate_customer()
    product = random.choice(products)
    quantity = random.randint(1, 5)
    
    # Apply business rules
    if product["category"] == "Electronics":
        # Electronics have 10% discount for quantities > 1
        unit_price = product["price"] * (0.9 if quantity > 1 else 1.0)
    else:
        unit_price = product["price"]
    
    total_amount = unit_price * quantity
    
    # Random date in last 90 days
    days_ago = random.randint(0, 90)
    transaction_date = datetime.now() - timedelta(days=days_ago)
    
    return {
        "transaction_id": transaction,
        "customer_id": customer["id"],
        "customer_name": customer["name"],
        "customer_email": customer["email"],
        "product_id": product["id"],
        "product_name": product["name"],
        "product_category": product["category"],
        "quantity": quantity,
        "unit_price": round(unit_price, 2),
        "total_amount": round(total_amount, 2),
        "transaction_date": transaction_date.strftime("%Y-%m-%d"),
        "payment_method": random.choice(["Credit Card", "PIX", "Boleto", "Debit Card"]),
        "status": random.choice(["Completed", "Processing", "Shipped"], 
                             weights=[0.85, 0.10, 0.05])
    }

def generate_dataset():
    """Generate complete dataset"""
    dataset = []
    for _ in range(ROWS):
        dataset.append(generate_transaction())
    return dataset

def save_as_csv(data, filename):
    """Save dataset as CSV"""
    if not data:
        print("No data to save")
        return
    
    fieldnames = data[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Generated {len(data)} transactions in {filename}")

def validate_dataset(data):
    """Validate dataset quality"""
    print(f"Validation Results:")
    print(f"- Total records: {len(data)}")
    print(f"- Unique customers: {len(set(t['customer_id'] for t in data))}")
    print(f"- Unique products: {len(set(t['product_id'] for t in data))}")
    print(f"- Date range: {min(t['transaction_date'] for t in data)} to {max(t['transaction_date'] for t in data))}")
    print(f"- Total revenue: R$ {sum(t['total_amount'] for t in data):,.2f}")

if __name__ == "__main__":
    print("Generating transaction dataset...")
    dataset = generate_dataset()
    save_as_csv(dataset, FILENAME)
    validate_dataset(dataset)
```

## Benefícios

- **Realismo:** Dados que parecem autênticos e válidos
- **Flexibilidade:** Múltiplos formatos e customizações
- **Velocidade:** Geração rápida de volumes grandes
- **Consistência:** Respeita regras de negócio
- **Reprodutibilidade:** Scripts executáveis repetidamente

## Dicas de Uso

### Para Melhores Resultados:
1. **Seja Específico:** Detalhe exatamente o que precisa
2. **Defina Restrições:** Inclua regras de negócio importantes
3. **Considere Volume:** Escolha tamanho adequado para seu uso
4. **Valide Formatos:** Verifique compatibilidade com seu sistema
5. **Teste Amostras:** Valide com pequenos volumes primeiro

### Boas Práticas:
- Usar nomes realistas para contexto local
- Incluir dados edge cases para testes robustos
- Manter consistência entre datasets relacionados
- Documentar regras de negócio aplicadas

## Formatos de Saída

### CSV
- Formato tabular padrão
- Facil importação para spreadsheets e bancos
- Ideal para análise de dados

### JSON
- Estrutura aninhada suportada
- Perfeito para APIs e NoSQL
- Preserva tipos de dados complexos

### SQL
- INSERT statements diretos
- Executável em bancos relacionais
- Inclui tipos de dados apropriados

### Python Script
- Código executável customizável
- Ideal para datasets grandes ou complexos
- Perter modificação pós-geração

## Recursos Adicionais

- **Faker Library:** [Python Faker](https://faker.readthedocs.io/)
- **Data Generation:** [Generating Realistic Test Data](https://www.testdata.com/)
- **CSV Tools:** [Python CSV Documentation](https://docs.python.org/3/library/csv.html)
- **JSON Tools:** [Python JSON Documentation](https://docs.python.org/3/library/json.html)

---

**Templates Rápidos:**

**User Profiles:**
```python
{
    "user_id": "auto-increment",
    "name": "first_last_name",
    "email": "email",
    "created_at": "timestamp_last_year",
    "last_login": "timestamp_last_30_days",
    "user_type": ["free", "premium", "enterprise"],
    "country": "country_codes_weighted"
}
```

**Analytics Events:**
```python
{
    "event_id": "uuid",
    "user_id": "existing_user_ids",
    "event_type": ["page_view", "click", "purchase", "signup"],
    "timestamp": "timestamp_last_7_days",
    "properties": "json_event_properties",
    "device": ["mobile", "desktop", "tablet"]
}
```

**Próximos Passos:**
- Executar script gerador
- Validar qualidade dos dados
- Importar para sistema de teste
- Documentar para equipe
- Manter versão controlada
