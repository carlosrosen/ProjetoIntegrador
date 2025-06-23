U-Balance - Sistema de Gestão Financeira

A U-Balance é uma plataforma web de gestão financeira pessoal desenvolvida para auxiliar os usuários no controle e organização de suas finanças. O sistema permite o cadastro e acompanhamento de receitas, despesas, metas financeiras e objetivos, oferecendo uma visão clara do saldo e das movimentações ao longo do tempo.

Este projeto foi desenvolvido como um trabalho acadêmico do terceiro semestre da graduação em Ciências da Computação, com o objetivo de proporcionar a compreensão das estruturas de dados e sua aplicação em projetos reais, utilizando tecnologias modernas para oferecer uma experiência intuitiva e eficiente.

Funcionalidades:

*Cadastro e autenticação de usuários
*Registro e categorização de receitas e despesas
*Controle e histórico detalhado do saldo financeiro
*Criação e acompanhamento de metas financeiras e objetivos
*Visualização de relatórios mensais e gráficos para análise financeira
*Interface responsiva e amigável com modais para operações rápidas

Tecnologias utilizadas:

Backend: Django (Python)
Frontend: HTML5, CSS3, JavaScript, Chart.js (para gráficos)
Banco de Dados: SQLite 

Como rodar o projeto:

1. Clone o repositório:
   git clone https://github.com/carlosrosen/U-Balance
   cd u-balance

2. Crie e ative um ambiente virtual:
   python -m venv venv
   source venv/bin/activate  (Linux/MacOS)
   venv\Scripts\activate     (Windows)

3. Instale as dependências necessárias:
   pip install django python-dateutil

4. Aplique as migrações do banco de dados:
   python manage.py migrate

5. Crie um superusuário para manusear a parte administrativa do Django (Opcional):
   python manage.py createsuperuser

6. Para iniciar o servidor local:
   python manage.py runserver

Equipe:

Carlos Eduardo (Backend)
Davi Roberto (Backend)
Gabriel Inácio (Frontend)
