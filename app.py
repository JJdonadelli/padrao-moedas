import streamlit as st
import random
import time

# Configuração da página
st.set_page_config(
    page_title="🪙 Jogo da Moeda",
    page_icon="🪙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS customizado
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

/* Links com melhor contraste */
a {
    color: #ffd700 !important;
    text-decoration: none !important;
    font-weight: bold !important;
}

a:hover {
    color: #ffed4e !important;
    text-decoration: underline !important;
    transition: color 0.3s ease !important;
}

/* Links dentro de expanders */
.streamlit-expanderContent a {
    color: #00d4ff !important;
    font-weight: bold !important;
}

.streamlit-expanderContent a:hover {
    color: #33ddff !important;
    text-decoration: underline !important;
}                

.main-header {
    background: linear-gradient(135deg, #ff6b6b, #feca57);
    padding: 1rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
    color: black;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.pattern-card {
    background: yellow;
    padding: 1.5rem;
    border-radius: 10px;
    border: 3px solid #ddd;
    text-align: center;
    margin: 10px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    height: 185px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
}

.pattern-card h4 {
    margin: 0;
    font-size: 1.1em;
    color: #333;
}

.pattern-emojis {
    font-size: 2em;
    margin: 10px 0;
}

.pattern-text {
    font-size: 0.9em;
    color: #666;
    margin: 0;
}

.player-card {
    border-color: #28a745;
}

.computer-card {
    border-color: #dc3545;
}

.sequence-display {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 15px;
    text-align: center;
    font-size: 1.5em;
    margin: 1rem 0;
    border: 2px solid #dee2e6;
    min-height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.win-message {
    background: linear-gradient(135deg, #28a745, #20c997);
    color: white;
    padding: 1.5rem;
    border-radius: 15px;
    text-align: center;
    font-size: 1.5em;
    font-weight: bold;
    margin: 1rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.lose-message {
    background: linear-gradient(135deg, #dc3545, #e74c3c);
    color: white;
    padding: 1.5rem;
    border-radius: 15px;
    text-align: center;
    font-size: 1.5em;
    font-weight: bold;
    margin: 1rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.story-section {
    background: rgba(255,255,255,0.95);
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    border-left: 5px solid #667eea;
    font-style: italic;
    color:black;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.game-running {
    background: linear-gradient(135deg, #ffd700, #ffed4e);
    color: #333;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    margin: 1rem 0;
    font-weight: bold;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.7; }
    100% { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# Padrões e estratégia do computador
patterns = ["ccc", "cck", "ckc", "ckk", "kcc", "kck", "kkc", "kkk"]
second_pattern = {
    "ccc": "kcc", "cck": "kcc", "ckc": "cck", "ckk": "cck",
    "kcc": "kkc", "kck": "kkc", "kkc": "ckk", "kkk": "ckk"
}

# Função para converter padrão para emojis
def pattern_to_emojis(pattern):
    return pattern.replace('c', '🟡').replace('k', '🔴')

def pattern_to_text(pattern):
    return pattern.replace('c', 'Cara').replace('k', 'Coroa')

# Inicializar estado da sessão
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'sequence' not in st.session_state:
    st.session_state.sequence = ""
if 'player_pattern' not in st.session_state:
    st.session_state.player_pattern = ""
if 'computer_pattern' not in st.session_state:
    st.session_state.computer_pattern = ""
if 'game_finished' not in st.session_state:
    st.session_state.game_finished = False
if 'winner' not in st.session_state:
    st.session_state.winner = ""
if 'game_running' not in st.session_state:
    st.session_state.game_running = False

# História do jogo
st.markdown("""
<div class="story-section">
    <strong>📖 A primeira ocorrência de um padrão (ou, quem vai pagar o pastel?):</strong><br><br>
    Dois amigos foram passear na feira. Quando chegaram à barraca de pastel, 
    decidiram fazer uma aposta para ver quem iria pagar a conta. Cada um escolheu, 
    de antemão, uma sequência de três resultados possíveis nos lançamentos de uma 
    moeda — cara (c) e coroa (k). Em seguida, começaram a lançar a moeda repetidamente, 
    combinando que o vencedor seria aquele cuja sequência aparecesse primeiro.
</div>
""", unsafe_allow_html=True)

# Seleção do padrão
st.subheader("Escolha seu padrão")

# Criar grid de padrões
cols = st.columns(4)
selected_pattern = None

for i, pattern in enumerate(patterns):
    with cols[i % 4]:
        emoji_pattern = pattern_to_emojis(pattern)
        text_pattern = pattern_to_text(pattern)
        
        if st.button(f"{emoji_pattern}\n{text_pattern}", key=f"pattern_{pattern}", 
                    use_container_width=True, disabled=st.session_state.game_running):
            selected_pattern = pattern

# Atualizar padrão selecionado
if selected_pattern:
    st.session_state.player_pattern = selected_pattern
    st.session_state.computer_pattern = second_pattern[selected_pattern]

# Mostrar padrões selecionados
if st.session_state.player_pattern:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="pattern-card player-card">
            <h4>👤 Seu Padrão</h4>
            <div class="pattern-emojis">
                {pattern_to_emojis(st.session_state.player_pattern)}
            </div>
            <div class="pattern-text">{pattern_to_text(st.session_state.player_pattern)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="pattern-card computer-card">
            <h4>👽 Meu padrão 👀 </h4>
            <div class="pattern-emojis">
                {pattern_to_emojis(st.session_state.computer_pattern)}
            </div>
            <div class="pattern-text">{pattern_to_text(st.session_state.computer_pattern)}</div>
        </div>
        """, unsafe_allow_html=True)

# Controles do jogo
# st.subheader("Controles do Jogo")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🎲 Iniciar Jogo", type="primary", use_container_width=True,
                disabled=(not st.session_state.player_pattern) or st.session_state.game_running):
        if st.session_state.player_pattern:
            st.session_state.sequence = ""
            st.session_state.game_started = True
            st.session_state.game_finished = False
            st.session_state.winner = ""
            st.session_state.game_running = True
            st.rerun()

with col3:
    # CORREÇÃO: Simplificar a condição do disabled
    reset_disabled = st.session_state.game_running
    if st.button("🔄 Jogar Novamente", use_container_width=True, disabled=reset_disabled):
        # Resetar apenas os estados do jogo, mantendo os padrões escolhidos
        st.session_state.game_started = False
        st.session_state.sequence = ""
        st.session_state.game_finished = False
        st.session_state.winner = ""
        st.session_state.game_running = False
        # Os padrões (player_pattern e computer_pattern) são mantidos
        st.rerun()

# with col3:
#     if st.button("🔄 Reset Completo", use_container_width=True, disabled=st.session_state.game_running):
#         # Resetar TODOS os estados (incluindo padrões)
#         for key in ['game_started', 'sequence', 'player_pattern', 'computer_pattern', 
#                    'game_finished', 'winner', 'game_running']:
#             if key in st.session_state:
#                 if key in ['sequence', 'player_pattern', 'computer_pattern', 'winner']:
#                     st.session_state[key] = ""
#                 else:
#                     st.session_state[key] = False
#         st.rerun()

# Status do jogo
if st.session_state.game_running:
    st.markdown("""
    <div class="game-running">
        Lançando moedas... 
    </div>
    """, unsafe_allow_html=True)

# Container para o placeholder da sequência (ÚNICO DISPLAY)
sequence_placeholder = st.empty()

# Display inicial quando jogo começar
if st.session_state.game_started and not st.session_state.game_finished:
    if st.session_state.sequence:
        sequence_display = pattern_to_emojis(st.session_state.sequence)
        sequence_placeholder.markdown(f"""
        <div class="sequence-display">
            {sequence_display}
        </div>
        """, unsafe_allow_html=True)
    else:
        sequence_placeholder.markdown("""
        <div class="sequence-display">
            Preparando...
        </div>
        """, unsafe_allow_html=True)

# Lógica do jogo automático
if st.session_state.game_running and not st.session_state.game_finished:
    # Sortear resultado
    flip_result = random.choice(["c", "k"])
    st.session_state.sequence += flip_result
    
    # Atualizar display (ÚNICO LUGAR)
    sequence_display = pattern_to_emojis(st.session_state.sequence)
    sequence_placeholder.markdown(f"""
    <div class="sequence-display">
        {sequence_display}
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar vitória se temos pelo menos 3 lançamentos
    if len(st.session_state.sequence) >= 3:
        window = st.session_state.sequence[-3:]  # Últimos 3 sorteios
        
        if window == st.session_state.player_pattern:
            st.session_state.winner = "player"
            st.session_state.game_finished = True
            st.session_state.game_running = False
            st.rerun()  # Força atualização imediata
        elif window == st.session_state.computer_pattern:
            st.session_state.winner = "computer"
            st.session_state.game_finished = True
            st.session_state.game_running = False
            st.rerun()  # Força atualização imediata
    
    # Pausa entre lançamentos apenas se o jogo não terminou
    if st.session_state.game_running:
        time.sleep(1)
        st.rerun()

# Mostrar sequência final quando jogo terminar
if st.session_state.game_finished and st.session_state.sequence:
    sequence_display = pattern_to_emojis(st.session_state.sequence)
    sequence_placeholder.markdown(f"""
    <div class="sequence-display">
        {sequence_display}
    </div>
    """, unsafe_allow_html=True)

# Resultado final
if st.session_state.game_finished and st.session_state.winner:
    if st.session_state.winner == "player":
        st.markdown("""
        <div class="win-message">
            🎉 Parabéns!
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown("""
        <div class="lose-message">
            🤷‍♀️ Tente novamente!
        </div>
        """, unsafe_allow_html=True)

# Informações adicionais
with st.expander("Como jogar"):
    st.markdown("""
    **1. Escolha seu padrão:** Clique em uma das sequências de 3 resultados
    
    **2. O computador, seu adversário, escolhe automaticamente** outro padrão usando uma estratégia
    
    **3. Clique em "🎲 Iniciar Jogo"** e as moedas serão lançadas automaticamente
    
    **4. Use "🔄 Jogar Novamente"** para uma nova partida 
    
    **5. O jogo para automaticamente** quando um dos padrões aparecer primeiro nos últimos 3 lançamentos
    
    **5. Vence quem conseguir** que sua sequência apareça primeiro!
    
    **💡** O adversário usa uma estratégia que lhe dá vantagem estatística!
    """)

with st.expander("Estratégia do adversário"):
    st.markdown("""
    O adversário usa a seguinte estratégia baseada em probabilidades:
    
    | Seu Padrão | Escolha do Adversário |
    |------------|---------------------|
    | ccc | kcc |
    | cck | kcc |
    | ckc | cck |
    | ckk | cck |
    | kcc | kkc |
    | kck | kkc |
    | kkc | ckk |
    | kkk | ckk |
    
    Esta estratégia não é aleatória - ela maximiza as chances do adversário vencer baseada em análise probabilística!
  
    **Veja as demonstração aqui** [1](https://arxiv.org/pdf/1406.2212), [2](http://mat.puc-rio.br/~nicolau/publ/papers/otario.pdf)
    
    """)

# Legenda
st.markdown("---")
st.markdown("**Legenda:** 🟡 = Cara (c) | 🔴 = Coroa (k)")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    Desenvolvido usando Streamlit<br>
    Baseado no problema clássico dos padrões de Penney<br>
</div>
""", unsafe_allow_html=True)