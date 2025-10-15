<body>
  <header>
    <h1>🕵️‍♂️ SCOD Scraping Challenge</h1>
    <p>Desafio de Estágio — SCOD Solutions</p>
  </header>

  <main>
    <section>
      <p>Bem-vindo(a) ao <strong>Desafio de Estágio - SCOD Solutions</strong>!<br>
      Este teste tem como objetivo avaliar sua capacidade de <strong>coletar dados (web scraping)</strong>, organizar informações e automatizar pequenas tarefas com boas práticas de código.</p>
    </section>

  <section>
    <h2>🚀 Desafio</h2>
    <p>Acesse a seguinte página de teste:</p>
    <p><a href="https://arth-inacio.github.io/scod_scraping_challenge/" target="_blank">🔗 https://arth-inacio.github.io/scod_scraping_challenge/</a></p>

  <h3>Sua missão:</h3>
  <ol>
    <li>Fazer o <strong>scraping</strong> da tabela de débitos exibida na página.</li>
    <li>Fazer o <strong>download dos boletos (PDFs)</strong> disponíveis em cada linha.</li>
    <li><strong>Extrair a linha digitável</strong> de dentro de cada PDF baixado.</li>
    <li><strong>Salvar os dados extraídos</strong> (descrição, exercício, parcela, vencimento, valor, status, link do boleto e linha digitável) em um arquivo JSON.</li>
    <li>Utilizar uma das seguintes abordagens:
      <ul>
        <li><code>requests</code> ou <code>httpx</code></li>
        <li><code>async-httpx</code></li>
        <li><code>selenium</code></li>
        <li><code>playwright</code> ou <code>async-playwright</code></li>
      </ul>
    </li>
  </ol>
  </section>

  <section>
    <h2>🧩 Requisitos</h2>
    <ul>
      <li>O código deve estar <strong>bem estruturado e legível</strong>.</li>
      <li>Desenvolvido em <strong>Python 3.9+</strong>.</li>
      <li>Utilizar <strong>orientação a objetos (OOP)</strong> é um diferencial.</li>
      <li>Organizar o projeto em pastas claras (ex: <code>src/</code>, <code>data/</code>, <code>boletos/</code>).</li>
      <li>Incluir um arquivo <code>requirements.txt</code> com as dependências.</li>
      <li>O script principal pode ser <code>main.py</code>.</li>
    </ul>
  </section>

  <section>
    <h2>📦 Saída esperada</h2>
    <p>Ao final da execução, o projeto deve gerar:</p>
    <ul>
      <li>Um arquivo <code>dados.json</code> contendo os registros da tabela.</li>
      <li>Uma pasta <code>boletos/</code> com os arquivos PDF baixados.</li>
    </ul>

  <p><strong>Exemplo do formato do <code>dados.json</code>:</strong></p>
  <pre><code>[
  {
    "descricao": "IPTU - Taxa Municipal",
    "exercicio": 2024,
    "parcela": "1/3",
    "vencimento": "2024-04-30",
    "valor": 1234.56,
    "status": "Vencido",
    "boleto_url": "boletos/18164829.pdf",
    "linha_digitavel": "34191.79001 01043.510047 91020.150008 6 00000045000"
  },
  {
    "descricao": "Taxa de Coleta de Lixo",
    "exercicio": 2025,
    "parcela": "2/2",
    "vencimento": "2025-06-15",
    "valor": 450.00,
    "status": "Pago",
    "boleto_url": "boletos/2139180.pdf",
    "linha_digitavel": "23793.38128 60005.104959 91020.150008 7 00000012345"
  }
]</code></pre>
    </section>

  <section>
    <h2>💡 Dicas</h2>
    <ul>
      <li>Utilize <code>async/await</code> para otimizar o download dos PDFs.</li>
      <li>Trate exceções e valide os links antes do download.</li>
      <li>Extraia a linha digitável com bibliotecas como <code>pdfplumber</code> ou <code>PyPDF2</code>.</li>
      <li>Adicione logs e comentários úteis no código.</li>
      <li>Faça commits organizados e descritivos.</li>
      <li>Use variáveis e funções com nomes significativos.</li>
      <li>Evite repetição — reutilize métodos e funções.</li>
    </ul>
  </section>

  <section>
    <h2>📂 Estrutura sugerida</h2>
    <pre><code>scod_scraping_challenge/
│
├── src/
│   ├── scraper.py          # Lógica principal do scraping
│   ├── downloader.py       # Download de boletos
│   ├── extractor.py        # Extração da linha digitável dos PDFs
│   └── utils.py            # Funções auxiliares
│
├── boletos/                # PDFs baixados
│   └── (arquivos gerados)
│
├── data/
│   └── dados.json          # Dados estruturados em JSON
│
├── requirements.txt        # Dependências do projeto
└── main.py                 # Script principal</code></pre>
    </section>

  <section>
    <h2>🔧 Tecnologias sugeridas</h2>
    <ul>
      <li><code>requests</code> / <code>httpx</code> — Requisições HTTP simples.</li>
      <li><code>BeautifulSoup4</code> / <code>lxml</code> — Parsing de HTML.</li>
      <li><code>selenium</code>, <code>playwright</code> ou <code>async-playwright</code> — Automação de navegador.</li>
      <li><code>pdfplumber</code> / <code>PyPDF2</code> — Extração de texto dos PDFs.</li>
      <li><code>json</code>, <code>os</code>, <code>asyncio</code>, <code>aiofiles</code> — Manipulação de arquivos e execução assíncrona.</li>
    </ul>
  </section>

  <section>
    <h2>🧠 Diferenciais</h2>
    <ul>
      <li>Uso de <strong>orientação a objetos (OOP)</strong>.</li>
      <li>Código modular e reutilizável.</li>
      <li>Tratamento de erros e logs organizados.</li>
      <li>Uso de <code>async/await</code> para desempenho.</li>
      <li>Documentação clara e organizada.</li>
    </ul>
  </section>

  <section>
    <h2>📫 Entrega</h2>
    <ol>
      <li>Crie um <strong>repositório público no GitHub</strong> (ex: <code>scod_scraping_<seu_nome></code>).</li>
      <li>Envie o <strong>link do repositório</strong> para:  
      <strong>arthur.inacio@scodbrasil.com.br e diretoria@scod.com.br </strong>
    </ol>
  </section>

  <section class="highlight">
    <h2>🏁 Boa sorte!</h2>
    <p>Mostre sua criatividade, atenção aos detalhes e domínio técnico.<br>
    Boa sorte e divirta-se no processo! 🚀</p>
  </section>

  <section>
    <h2>💼 Sobre a SCOD Solutions</h2>
    <p>A <strong>SCOD Solutions</strong> é uma empresa focada em <strong>inovação, tecnologia e soluções digitais</strong>.<br>
    Nosso objetivo é identificar talentos com vontade de aprender, crescer e contribuir com projetos reais.<br>
    Este desafio é uma oportunidade para mostrar o seu potencial e fazer parte do nosso time! 💚</p>
  </section>
  </main>

  <footer>
    <p>© 2025 SCOD Solutions - Desafio de Estágio</p>
  </footer>
</body>
