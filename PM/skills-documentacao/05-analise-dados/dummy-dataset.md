# Dataset Dummy

## Propósito
Gerar datasets dummy realistas para teste com colunas customizáveis, restrições e formatos de saída (CSV, JSON, SQL, Python script). Usado ao criar dados de teste, construir datasets mock ou gerar dados amostrais para desenvolvimento e demos.

## Como Funciona
Gera datasets dummy realistas para teste com colunas customizáveis, restrições e formatos de saída. Cria scripts executáveis ou arquivos de dados diretos para uso imediato.

## Quando Usar
- Criação de dados de teste para desenvolvimento
- Geração de datasets amostrais para demos
- Construção de dados mock realistas
- População de ambientes de teste
- Validação de sistemas com dados variados

## Processo Passo a Passo

1. **Identificar tipo de dataset** — Entender o domínio de dados
2. **Definir especificações de colunas** — Nomes, tipos de dados e ranges de valores
3. **Determinar contagem de linhas** — Quantos registros amostrais necessários
4. **Selecionar formato de saída** — CSV, JSON, SQL INSERT, ou Python script
5. **Aplicar padrões realistas** — Garantir que dados pareçam autênticos e válidos
6. **Adicionar restrições de negócio** — Respeitar lógica de negócio e relacionamentos
7. **Gerar ou script de dados** — Criar saída executável
8. **Validar saída** — Garantir qualidade e completude dos dados

## Template: Saída Python Script

```python
import csv
import json
from datetime import datetime, timedelta
import random

# Configuração
ROWS = $ROWS
FILENAME = "$DATASET_TYPE.csv"

# Definições de colunas com geradores de valores realistas
columns = {
    "id": "auto-increment",
    "name": "first_last_name",
    "email": "email",
    "created_at": "timestamp",
    # Adicionar mais colunas...
}

def generate_dataset():
    """Gerar dataset dummy realista"""
    data = []
    for i in range(1, ROWS + 1):
        record = {
            "id": f"U{i:06d}",
            # Gerar valores baseados em definições de colunas
        }
        data.append(record)
    return data

def save_as_csv(data, filename):
    """Salvar dataset como CSV"""
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    dataset = generate_dataset()
    save_as_csv(dataset, FILENAME)
    print(f"Generated {len(dataset)} records in {FILENAME}")
```

## Exemplo de Especificação de Dataset

### Tipo de Dataset: Feedback de Cliente

**Colunas:**
- feedback_id (auto-increment, U001, U002...)
- customer_name (nomes realistas)
- email (formato de email válido)
- feedback_date (datas últimos 90 dias)
- rating (1-5 estrelas)
- category (Bug, Feature Request, Complaint, Praise)
- text (feedback realista)
- product (electronics, clothing, home)

**Restrições:**
- Ratings com skew: 40% 5 estrelas, 30% 4 estrelas, 20% 3 estrelas, 10% 1-2 estrelas
- Categoria Bug apenas com ratings 1-3
- Feature requests apenas com ratings 3-5
- Domínios de email realistas (gmail, yahoo, company.com)

## Exemplo Prático

### Dataset Dummy: FinanControl

### Tipo de Dataset: Transações Financeiras

**Colunas:**
- transaction_id (auto-increment, TXN001, TXN002...)
- user_id (referência a usuários existentes)
- company_id (referência a empresas)
- amount (valores monetários realistas)
- type (income, expense, transfer)
- category (salário, fornecedor, aluguel, material, etc.)
- description (descrições realistas de transações)
- date (datas últimos 6 meses)
- bank_id (referência a bancos integrados)
- status (pending, completed, failed)

**Restrições:**
- Amounts: Despesas R$50-R$10.000, Receitas R$1.000-R$50.000
- Categories específicas por tipo (salário só income, fornecedor só expense)
- Distribuição realista: 60% expenses, 40% income
- Status: 95% completed, 4% pending, 1% failed
- Datas: Mais transações fim de mês, menos fins de semana

### Script Python Gerado

```python
import csv
import json
from datetime import datetime, timedelta
import random

# Configuração
ROWS = 1000
FILENAME = "financial_transactions.csv"

# Definições de colunas com geradores de valores realistas
columns = {
    "transaction_id": "auto-increment",
    "user_id": "user_reference",
    "company_id": "company_reference", 
    "amount": "monetary_value",
    "type": "transaction_type",
    "category": "expense_category",
    "description": "realistic_description",
    "date": "date_last_6_months",
    "bank_id": "bank_reference",
    "status": "transaction_status"
}

# Dados de referência realistas
first_names = ["Ana", "Carlos", "Maria", "João", "Pedro", "Beatriz", "Lucas", "Julia"]
last_names = ["Silva", "Santos", "Costa", "Oliveira", "Pereira", "Lima", "Ferreira", "Alves"]
companies = ["Tech Solutions", "Digital Agency", "E-commerce Store", "Consulting Group", "Startup Brasil"]
banks = ["Banco do Brasil", "Itaú", "Bradesco", "Caixa", "Santander"]

expense_categories = ["Aluguel", "Fornecedores", "Material", "Serviços", "Marketing", "Transporte", "Software"]
income_categories = ["Salário", "Vendas", "Serviços", "Investimentos", "Consultoria"]
expense_descriptions = [
    "Pagamento aluguel escritório",
    "Compra material de escritório", 
    "Serviços de contabilidade",
    "Campanha marketing digital",
    "Manutenção equipamentos",
    "Software gestão empresarial"
]
income_descriptions = [
    "Salário mensal",
    "Recebimento cliente X",
    "Projeto consultoria Y",
    "Vendas produto Z",
    "Investimento retorno",
    "Serviços prestados"
]

def generate_dataset():
    """Gerar dataset dummy realista de transações financeiras"""
    data = []
    base_date = datetime.now() - timedelta(days=180)
    
    for i in range(1, ROWS + 1):
        # Gerar data aleatória nos últimos 6 meses
        random_days = random.randint(0, 180)
        transaction_date = base_date + timedelta(days=random_days)
        
        # 60% expenses, 40% income
        transaction_type = random.choices(['expense', 'income'], weights=[60, 40])[0]
        
        if transaction_type == 'expense':
            amount = round(random.uniform(50, 10000), 2)
            category = random.choice(expense_categories)
            description = random.choice(expense_descriptions)
        else:
            amount = round(random.uniform(1000, 50000), 2)
            category = random.choice(income_categories)
            description = random.choice(income_descriptions)
        
        # 95% completed, 4% pending, 1% failed
        status = random.choices(['completed', 'pending', 'failed'], weights=[95, 4, 1])[0]
        
        record = {
            "transaction_id": f"TXN{i:06d}",
            "user_id": f"U{random.randint(1, 500):03d}",
            "company_id": f"C{random.randint(1, 50):02d}",
            "amount": amount,
            "type": transaction_type,
            "category": category,
            "description": description,
            "date": transaction_date.strftime("%Y-%m-%d"),
            "bank_id": f"B{random.randint(1, 5):01d}",
            "status": status
        }
        data.append(record)
    
    # Ordenar por data
    data.sort(key=lambda x: x['date'])
    return data

def save_as_csv(data, filename):
    """Salvar dataset como CSV"""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def save_as_json(data, filename):
    """Salvar dataset como JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)

def generate_sql_inserts(data):
    """Gerar statements SQL INSERT"""
    sql_statements = []
    sql_statements.append("-- Financial Transactions Insert Statements")
    sql_statements.append("INSERT INTO financial_transactions (transaction_id, user_id, company_id, amount, type, category, description, date, bank_id, status) VALUES")
    
    for i, record in enumerate(data):
        values = f"('{record['transaction_id']}', '{record['user_id']}', '{record['company_id']}', {record['amount']}, '{record['type']}', '{record['category']}', '{record['description']}', '{record['date']}', '{record['bank_id']}', '{record['status']}')"
        
        if i < len(data) - 1:
            values += ","
        else:
            values += ";"
        
        sql_statements.append(values)
    
    return "\n".join(sql_statements)

if __name__ == "__main__":
    dataset = generate_dataset()
    
    # Salvar em múltiplos formatos
    save_as_csv(dataset, FILENAME)
    save_as_json(dataset, "financial_transactions.json")
    
    with open("financial_transactions.sql", "w") as f:
        f.write(generate_sql_inserts(dataset))
    
    print(f"Generated {len(dataset)} records:")
    print(f"- CSV: {FILENAME}")
    print(f"- JSON: financial_transactions.json")
    print(f"- SQL: financial_transactions.sql")
    
    # Estatísticas do dataset
    total_amount = sum(record['amount'] for record in dataset)
    expenses = sum(record['amount'] for record in dataset if record['type'] == 'expense')
    income = sum(record['amount'] for record in dataset if record['type'] == 'income')
    
    print(f"\nDataset Statistics:")
    print(f"- Total Amount: R${total_amount:,.2f}")
    print(f"- Total Expenses: R${expenses:,.2f}")
    print(f"- Total Income: R${income:,.2f}")
    print(f"- Net: R${income - expenses:,.2f}")
```

## Formatos de Saída

### CSV
Formato tabular plano, fácil de importar para spreadsheets e bancos de dados

### JSON
Estrutura aninhada, ideal para APIs e bancos de dados NoSQL

### SQL
Statements INSERT, diretamente executáveis em bancos de dados relacionais

### Python Script
Gerador executável para datasets customizados ou grandes volumes

## Entregáveis de Saída

- Script Python pronto para executar OU arquivo de dados direto
- Arquivo CSV com headers e formatação adequados
- Arquivo JSON com estrutura e tipos válidos
- Statements SQL INSERT para população de banco de dados
- Validação de dados e conformidade com restrições
- Valores realistas e apropriados para negócios
- Documentação da lógica de geração de dados
- Instruções de início rápido para usar o dataset

## Modelos Adicionais

### Dataset de Usuários
```python
# Colunas: user_id, name, email, created_at, plan, company_size, industry
# Restrições: Emails válidos, planos realistas, distribuição por tamanho
```

### Dataset de Produtos
```python
# Colunas: product_id, name, category, price, inventory, rating, reviews_count
# Restrições: Preços realistas por categoria, ratings distribuídos normal
```

### Dataset de Eventos
```python
# Colunas: event_id, user_id, event_type, timestamp, properties
# Restrições: Timestamps realistas, tipos de eventos válidos, propriedades consistentes
```

## Benefícios
- **Teste:** Dados realistas para testes de sistema e validação
- **Desenvolvimento:** Ambientes de desenvolvimento com dados representativos
- **Demo:** Apresentações com dados autênticos e relevantes
- **Privacidade:** Dados falsos mas realistas, sem informações reais de clientes

## Dicas de Uso
- Especifique claramente o tipo de dataset e restrições de negócio
- Forneça exemplos de valores esperados para maior realismo
- Considere relacionamentos entre diferentes datasets
- Use para testar edge cases e cenários limite
- Mantenha consistência entre datasets relacionados

## Recursos Adicionais
- [Data Generation Best Practices](https://www.productcompass.pm/p/data-generation-best-practices)
- [Test Data Management: Complete Guide](https://www.productcompass.pm/p/test-data-management)
- [Mock Data for Development](https://www.productcompass.pm/p/mock-data-development)
- [Database Testing Strategies](https://www.productcompass.pm/p/database-testing-strategies)
