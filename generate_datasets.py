def load_or_create_datasets():
    df = pd.read_csv("kc_house_data.csv")
    price = df["price"].astype(int).tolist()[:20000]

    A = price.copy()
    random.shuffle(A)

    B = sorted(price)

    C = B[::-1]

    D = B.copy()
    for _ in range(len(D)//20):
        i = random.randint(0, len(D)-1)
        j = random.randint(0, len(D)-1)
        D[i], D[j] = D[j], D[i]

    E = [x % 1000 for x in price]

    datasets = [A, B, C, D, E]
    names = ["A", "B", "C", "D", "E"]

    return datasets, names