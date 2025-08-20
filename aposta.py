from time import sleep
import random

M_T = [ #matriz das probabilidades, está aqui só para referencia
    [None,   1/2,   3/5,   3/5,   7/8,  7/12,  7/10,  1/2 ],  # ccc
    [1/2,   None,   1/3,   1/3,   3/4,  3/8,   1/2,   3/10],  # cck
    [2/5,   2/3,   None,   1/2,   1/2,  1/2,   5/8,   5/12],  # ckc
    [2/5,   2/3,   1/2,   None,   1/2,  1/2,   1/4,   1/8 ],  # ckk
    [1/8,   1/4,   1/2,   1/2,   None,  1/2,   2/3,   2/5 ],  # kcc
    [5/12,  5/8,   1/2,   1/2,   1/2,  None,   2/3,   2/5 ],  # kck
    [3/10,  1/2,   3/8,   3/4,   1/3,  1/3,   None,   1/2 ],  # kkc
    [1/2,   7/10,  7/12,  7/8 ,  3/5,  3/5,   1/2,   None ]   # kkk
]

patterns = ["ccc", "cck", "ckc", "ckk", "kcc", "kck", "kkc", "kkk"]
second_pattern = {
    "ccc": "kcc",
    "cck": "kcc",
    "ckc": "cck",
    "ckk": "cck",
    "kcc": "kkc",
    "kck": "kkc",
    "kkc": "ckk",
    "kkk": "ckk"
}

# ------------------- execução -------------------
if __name__ == "__main__":

    print("Dois amigos foram passear na feira. Quando chegaram à barraca de pastel, " \
    "decidiram fazer uma aposta para ver quem iria pagar a conta. Cada um escolheu, " \
    "de antemão, uma sequência de três resultados possíveis nos lançamentos de uma " \
    "moeda — cara (c) e coroa (k). Em seguida, começaram a lançar a moeda repetidamente, " \
    "combinando que o vencedor seria aquele cuja sequência aparecesse primeiro.")

    p1=""
    while p1 not in patterns:
        p1 = input("\nDigite o seu padrão (ex: ckc): ").strip().lower()
        if p1 not in patterns:  print("Padrão inválido! Use apenas combinações de 'c' e 'k' com 3 letras.")
    p2 = second_pattern[p1]
    print(f"O meu padrão é {p2}")

    seq = ""  # sequência sorteada
    while True:
        sorteio = random.choice(["c", "k"])
        seq += sorteio
        print(sorteio , end=' ', flush=True)
        sleep(1)
        if len(seq) >= 3:
            window = seq[-3:]  # últimos 3 sorteios
            if window == p1:
               vencedor = p1
               break 
            elif window == p2:
                vencedor = p2
                break 
                
    print(f"\n\nO padrão vencedor foi: {vencedor}")
    if vencedor == p1 : print("Parabéns")
    else : print("Tente novamente")