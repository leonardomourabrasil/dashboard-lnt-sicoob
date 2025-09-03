
# Dashboard Interativo Sicoob Secovicred

## Como executar o dashboard em qualquer navegador

### Requisitos
- Python 3.7 ou superior
- Navegador web moderno (Chrome, Firefox, Edge, Safari)

### Passos para rodar localmente:

1. **Instale o Python**:
   - Baixe e instale o Python em [python.org](https://www.python.org/downloads/)
   - Durante a instalação, marque a opção "Add Python to PATH"

2. **Clone ou baixe este repositório**:
   ```
   git clone https://github.com/leonardomourabrasil/dashboard-lnt-sicoob.git
   ```
   Ou baixe como ZIP e extraia os arquivos.

3. **Instale as dependências**:
   ```
   pip install -r requirements.txt
   ```
   
   Se o comando acima falhar, tente:
   ```
   python -m pip install -r requirements.txt
   ```
   ou
   ```
   python3 -m pip install -r requirements.txt
   ```

4. **Execute o dashboard**:
   ```
   streamlit run app.py
   ```
   
   Se o comando acima falhar, tente:
   ```
   python -m streamlit run app.py
   ```
   ou
   ```
   python3 -m streamlit run app.py
   ```

5. **Acesse o dashboard**:
   - O Streamlit abrirá automaticamente seu navegador padrão
   - Se não abrir, acesse manualmente: http://localhost:8501
   - O dashboard também estará disponível em sua rede local através do endereço mostrado no terminal

### Acesso em outros dispositivos na mesma rede:
- Anote o endereço "Network URL" exibido no terminal (exemplo: http://192.168.1.9:8501)
- Use este endereço para acessar o dashboard de outros dispositivos na mesma rede

### Publicação online (opcional):
- **Streamlit Cloud**: Gratuito para projetos públicos
- **Heroku**: Opção econômica para implantação
- **Azure Web Apps / AWS**: Para uso corporativo
- **Servidor interno**: Para manter os dados dentro da rede da empresa

### Compatibilidade com navegadores:
- Chrome/Edge (recomendado)
- Firefox
- Safari
- Opera

Observação de marca: respeite as políticas institucionais para uso do logotipo e identidade visual.
